# skidge

A
[feature-rich](https://slidge.im/skidge/features.html)
[Skype](https://skype.com/) to
[XMPP](https://xmpp.org/) puppeteering
[gateway](https://xmpp.org/extensions/xep-0100.html), based on
[slidge](https://slidge.im) and
[skpy](https://skpy.t.allofti.me/).

[![PyPI package version](https://badge.fury.io/py/skidge.svg)](https://pypi.org/project/skidge/)
[![CI pipeline status](https://ci.codeberg.org/api/badges/14073/status.svg)](https://ci.codeberg.org/repos/14073)
[![Chat](https://conference.nicoco.fr:5281/muc_badge/slidge@conference.nicoco.fr)](https://conference.nicoco.fr:5281/muc_log/slidge/)

## Installation

Refer to the [slidge admin documentation](https://slidge.im/core/admin/)
for general info on how to set up an XMPP server component.

### Containers

From [the codeberg package registry](https://codeberg.org/slidge/-/packages?q=&type=container)

```sh
docker run codeberg.org/slidge/skidge
```

### Python package

With [pipx](https://pypa.github.io/pipx/):

```sh

# for the latest stable release (if any)
pipx install skidge

# for the bleeding edge
pipx install skidge==0.0.0.dev0 \
    --pip-args='--extra-index-url https://codeberg.org/api/packages/slidge/pypi/simple/'

# to update bleeding edge installs
pipx install skidge==0.0.0.dev0 \
    --pip-args='--extra-index-url https://codeberg.org/api/packages/slidge/pypi/simple/' --force

skidge --help
```

## Dev

```sh
git clone https://codeberg.org/slidge/skidge
cd skidge
docker-compose up
```
