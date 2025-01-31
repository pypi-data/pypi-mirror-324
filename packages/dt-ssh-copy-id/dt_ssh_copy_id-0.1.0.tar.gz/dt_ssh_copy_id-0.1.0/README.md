# dt-ssh-copy-id

Command-line windows tool that loosely mimics the *nix ssh-copy-id command.


## Purpose

ssh-copy-id installs (one or more) SSH keys on a target server as an authorized key. Its purpose is to provide access without requiring a password for each login. 

This provides the ability to enable automated (passwordless) logins using the SSH protocol.

## Features:

- Command line driven (loosely mimics the *nix syntax)
- Multiple target hosts can be setup via single run
- Identifies if keys are already present on target host(s).

## Pre-requisites

- Python 3.10+ (may work with earlier version, not tested)
- [fabric](https://www.fabfile.org/) - layer over paramiko
- [paramiko](https://www.paramiko.org/) - facilitates SSH interactions with target servers
- [loguru](https://github.com/Delgan/loguru) - manages logging

## Setup
To install as a CLI (no source)
- [pipx](https://github.com/pypa/pipx) install dt-ssh-copy-id   (creates a virtual environment)

or

- pip install dt-ssh-copy-id [--user]


To install source code
- git clone https://github.com/JavaWiz1/dt-ssh-copy-id.git

If you use [Poetry](https://python-poetry.org/), a virtual environment will be created with the required dependencies.
- poetry install

else, you may install manually with - 
- pip install fabric loguru


## Syntax
```
usage: ssh-copy-id [-h] [-f] [-i FILE] [-p PORT] hostname [hostname ...]

ssh-copy-id - copy ssh public keys to target host

positional arguments:
  hostname              [user@]hostname

options:
  -h, --help            show this help message and exit
  -f, --force           Force copy, no existence check.
  -i FILE, --identity_file FILE
                        the identity file to be copied. If not specified, adds all keys.
  -p PORT, --port PORT  SSH port (default 22)
```

## Examples

- Install all public keys for user tom onto server1

    ```> ssh-copy-id tom@server1```

- Install ONLY the rsa public key for user tom onto server1,2,3 and 4

    ```> ssh-copy-id -i ~/.ssh/id_rsa.pub tom@server1 tom@server2 tom@server3 tom@server4```

- Install all public keys for configured (.ssh/config) user onto server 'rasberrypi'
  
  ```> ssh-copy-id raspberypi```
---

NOTE:
  - If you have a .ssh/config setup with defaults, those will be used (i.e. pre-defined usernames).
  - You will be prompted for a password upon first login.  
      - That password will be re-used for each server
      - If login fails for a server, you will be re-prompted to supply a valid password.
