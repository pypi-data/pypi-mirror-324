import asyncio
import io
import logging
import pprint
import threading
from pathlib import Path
from threading import Lock, Thread
from typing import Any, Optional, Union

import skpy
from requests.exceptions import ConnectionError
from slidge import (
    BaseGateway,
    BaseSession,
    FormField,
    LegacyContact,
    LegacyMUC,
    LegacyRoster,
    entrypoint,
    global_config,
)
from slidge.util.util import get_version  # noqa: F401
from slixmpp import JID
from slixmpp.exceptions import XMPPError


class Gateway(BaseGateway):
    REGISTRATION_INSTRUCTIONS = "Enter skype credentials"
    REGISTRATION_FIELDS = [
        FormField(var="username", label="Username", required=True),
        FormField(var="password", label="Password", required=True, private=True),
    ]

    ROSTER_GROUP = "Skype"

    COMPONENT_NAME = "Skype (slidge)"
    COMPONENT_TYPE = "skype"

    COMPONENT_AVATAR = "https://logodownload.org/wp-content/uploads/2017/05/skype-logo-1-1-2048x2048.png"

    async def validate(
        self, user_jid: JID, registration_form: dict[str, Optional[str]]
    ):
        try:
            await asyncio.to_thread(
                skpy.Skype,
                registration_form["username"],
                registration_form["password"],
                str(global_config.HOME_DIR / user_jid.bare),
            )
        except skpy.SkypeApiException:
            raise XMPPError("bad-request")
        except skpy.SkypeAuthException:
            raise XMPPError("forbidden")


class Contact(LegacyContact[str]):
    session: "Session"

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._mood: str | None = None

    def serialize_extra_attributes(self) -> Optional[dict]:
        return {"mood": self._mood}

    def deserialize_extra_attributes(self, data: dict) -> None:
        self._mood = data.get("mood")

    def update_presence(self, status: skpy.SkypeUtils.Status):
        if status == skpy.SkypeUtils.Status.Offline:
            self.offline(self._mood)
        elif status == skpy.SkypeUtils.Status.Busy:
            self.busy(self._mood)
        elif status == skpy.SkypeUtils.Status.Idle:
            self.away(self._mood)
        elif status == skpy.SkypeUtils.Status.Away:
            self.extended_away(self._mood)
        elif status == skpy.SkypeUtils.Status.Online:
            self.online(self._mood)
        else:
            log.warning("Unknown contact status: %s", status)

    async def update_info(self, contact: Optional[skpy.SkypeContact] = None):
        if contact is None:
            contact = self.session.sk.contacts.contact(self.legacy_id)
            if contact is None:
                raise XMPPError("item-not-found")

        self._mood = str(contact.mood)
        first = contact.name.first
        last = contact.name.last

        if first is not None and last is not None:
            self.name = f"{first} {last}"
        elif first is not None:
            self.name = first
        elif last is not None:
            self.name = last

        if contact.avatar is not None:
            await self.set_avatar(contact.avatar)

        self.set_vcard(
            given=first,
            surname=last,
            full_name=self.name,
            locality=str(contact.location),
            phones=[p for p in contact.phones if p.number],
            birthday=contact.birthday,
        )

        self.is_friend = True


class ListenThread(Thread):
    def __init__(self, session: "Session", *a, **kw):
        super().__init__(*a, **kw, daemon=True)
        self.name = f"listen-{session.user_jid}"
        self.session = session
        self._target = self.skype_blocking
        self.stop_event = threading.Event()

    def skype_blocking(self):
        session = self.session
        sk = session.sk
        loop = session.xmpp.loop
        while True:
            if self.stop_event.is_set():
                break
            for event in sk.getEvents():
                # no need to sleep since getEvents blocks for 30 seconds already
                asyncio.run_coroutine_threadsafe(session.on_skype_event(event), loop)

    def stop(self):
        self.stop_event.set()


class Roster(LegacyRoster):
    session: "Session"

    async def fill(self):
        for contact in self.session.sk.contacts:
            c = await self.by_legacy_id(contact.id)
            yield c


Recipient = Union[Contact, LegacyMUC]


class Session(BaseSession[int, Recipient]):
    skype_token_path: Path
    sk: skpy.Skype

    def __init__(self, user):
        super().__init__(user)
        self.skype_token_path = global_config.HOME_DIR / self.user_jid.bare
        self.thread: Optional[ListenThread] = None
        self.sent_by_user_to_ack = dict[int, asyncio.Future]()
        self.unread_by_user = dict[int, skpy.SkypeMsg]()
        self.send_lock = Lock()

    async def login(self):
        f = self.user.legacy_module_data
        self.sk = await asyncio.to_thread(
            skpy.Skype,
            f["username"],
            f["password"],
            str(self.skype_token_path),
        )

        try:
            self.sk.subscribePresence()
        except skpy.core.SkypeApiException:
            self.log.warning("Could not subscribe to presences")
            extra = " (presences not working) "
        else:
            extra = ""

        # TODO: Creating 1 thread per user is probably very not optimal.
        #       We should contribute to skpy to make it aiohttp compatible…
        self.thread = thread = ListenThread(self)
        thread.start()
        return f"Connected{extra} as '{self.sk.userId}'"

    async def on_skype_event(self, event: skpy.SkypeEvent):
        log.debug("Skype event: %s", event)
        if isinstance(event, skpy.SkypeNewMessageEvent):
            while self.send_lock.locked():
                await asyncio.sleep(0.1)
            msg = event.msg
            chat = event.msg.chat
            if isinstance(chat, skpy.SkypeSingleChat):
                log.debug("this is a single chat with user: %s", chat.userIds[0])
                contact = await self.contacts.by_legacy_id(chat.userIds[0])
                if msg.userId == self.sk.userId:
                    try:
                        fut = self.sent_by_user_to_ack.pop(msg.clientId)
                    except KeyError:
                        if log.isEnabledFor(logging.DEBUG):
                            log.debug(
                                "Slidge did not send this message: %s",
                                pprint.pformat(vars(event)),
                            )
                        contact.send_text(msg.plain, carbon=True)
                    else:
                        fut.set_result(msg)
                else:
                    if isinstance(msg, skpy.SkypeTextMsg):
                        contact.send_text(msg.plain, legacy_msg_id=msg.clientId)
                        self.unread_by_user[msg.clientId] = msg
                    elif isinstance(msg, skpy.SkypeFileMsg):
                        # non-blocking download / lambda because fileContent = property
                        data = await asyncio.to_thread(lambda: msg.fileContent)
                        await contact.send_file(file_name=msg.file.name, data=data)
        elif isinstance(event, skpy.SkypeTypingEvent):
            contact = await self.contacts.by_legacy_id(event.userId)
            if event.active:
                contact.composing()
            else:
                contact.paused()
        elif isinstance(event, skpy.SkypeEditMessageEvent):
            msg = event.msg
            chat = event.msg.chat
            if isinstance(chat, skpy.SkypeSingleChat):
                if (user_id := msg.userId) != self.sk.userId:
                    if log.isEnabledFor(logging.DEBUG):
                        log.debug("edit msg event: %s", pprint.pformat(vars(event)))
                    contact = await self.contacts.by_legacy_id(user_id)
                    msg_id = msg.clientId
                    log.debug("edited msg id: %s", msg_id)
                    if text := msg.plain:
                        contact.correct(msg_id, text)
                    else:
                        if msg_id:
                            contact.retract(msg_id)
                        else:
                            contact.send_text(
                                "/me tried to remove a message, but slidge got in"
                                " trouble"
                            )
        elif isinstance(event, skpy.SkypeChatUpdateEvent):
            if log.isEnabledFor(logging.DEBUG):
                log.debug("chat update: %s", pprint.pformat(vars(event)))
        elif isinstance(event, skpy.SkypePresenceEvent):
            if event.userId != self.sk.userId:
                (await self.contacts.by_legacy_id(event.userId)).update_presence(
                    event.status
                )

        # No 'contact has read' event :( https://github.com/Terrance/SkPy/issues/206
        await asyncio.to_thread(event.ack)

    async def on_text(self, chat: Recipient, text: str, **k):
        skype_chat = self.sk.contacts[chat.legacy_id].chat
        self.send_lock.acquire()
        msg = await asyncio.to_thread(skype_chat.sendMsg, text)
        if log.isEnabledFor(logging.DEBUG):
            log.debug("Sent msg: %s", pprint.pformat(vars(msg)))
        future = asyncio.Future[skpy.SkypeMsg]()
        self.sent_by_user_to_ack[msg.clientId] = future
        self.send_lock.release()
        skype_msg = await future
        return skype_msg.clientId

    async def logout(self):
        if self.thread is not None:
            self.thread.stop()

    async def on_file(self, chat: Recipient, url: str, http_response, **kwargs):
        fname = url.split("/")[-1]
        await asyncio.to_thread(
            self.sk.contacts[chat.legacy_id].chat.sendFile,
            io.BytesIO(await http_response.read()),
            fname,
            http_response.content_type.startswith("image"),
        )

    async def on_composing(self, c: Recipient, thread=None):
        await asyncio.to_thread(self.sk.contacts[c.legacy_id].chat.setTyping, True)

    async def on_paused(self, c: Recipient, thread=None):
        await asyncio.to_thread(self.sk.contacts[c.legacy_id].chat.setTyping, False)

    async def on_displayed(self, c: Recipient, legacy_msg_id: int, thread=None):
        try:
            skype_msg = self.unread_by_user.pop(legacy_msg_id)
        except KeyError:
            log.debug(
                "We did not transmit: %s (%s)", legacy_msg_id, self.unread_by_user
            )
        else:
            log.debug("Calling read on %s", skype_msg)
            try:
                await asyncio.to_thread(skype_msg.read)
            except skpy.SkypeApiException as e:
                # FIXME: this raises HTTP 400 and does not mark the message as read
                # https://github.com/Terrance/SkPy/issues/207
                self.log.debug("Skype read marker failed: %r", e)

    async def on_correct(
        self,
        c: Recipient,
        text: str,
        legacy_msg_id: Any,
        thread=None,
        link_previews=(),
        mentions=None,
    ):
        m = self.get_msg(legacy_msg_id, c)
        await asyncio.to_thread(m.edit, text)

    async def on_retract(self, c: Recipient, legacy_msg_id: Any, thread=None):
        m = self.get_msg(legacy_msg_id, c)
        log.debug("Deleting %s", m)
        await asyncio.to_thread(m.delete)

    async def on_search(self, form_values: dict[str, str]):
        pass

    def get_msg(self, legacy_msg_id: int, contact: Recipient) -> skpy.SkypeTextMsg:
        for m in self.sk.contacts[contact.legacy_id].chat.getMsgs():
            log.debug("Message %r vs %r : %s", legacy_msg_id, m.clientId, m)
            if m.clientId == legacy_msg_id:
                return m
        else:
            raise XMPPError(
                "item-not-found", text=f"Could not find message '{legacy_msg_id}'"
            )


def main():
    entrypoint("skidge")


def handle_thread_exception(args: threading.ExceptHookArgs):
    if (
        (thread := getattr(args, "thread"))
        and isinstance(thread, ListenThread)
        and args.exc_type is ConnectionError
    ):
        session = thread.session
        log.info("Connection error, attempting re-login for %s", session.user)
        session.logged = False
        thread.stop()
        session.re_login()
    else:
        log.error("Exception in thread: %s", args)


threading.excepthook = handle_thread_exception

log = logging.getLogger(__name__)

__version__ = "v0.2.0"
