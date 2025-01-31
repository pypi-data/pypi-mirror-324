"""
Windows version of ssh-copy-id.

Copy ssh keys to target host authorized_keys file.

"""
import argparse
import pathlib
import sys
from getpass import getpass
from typing import Union

try:
    from loguru import logger as LOGGER
except ImportError:
    print('ERROR: loguru package not installed.')

try:
    from fabric import Connection
    from invoke.runners import Result
    from paramiko.ssh_exception import AuthenticationException
except ImportError:
    print ("ERROR: fabric package not installed.")
    sys.exit(1)


DEFAULT_CONSOLE_LOGFMT = "<level>{message}</level>"
DEFAULT_DEBUG_LOGFMT =  "<green>{time:HH:mm:ss}</green> |<level>{level: <8}</level>|<cyan>{module:20}</cyan>|<cyan>{line:4}</cyan>| <level>{message}</level>"

class SshCopyTarget():
    def __init__(self, hostname, port=22, username=None, password=None, local_sshkeys_path=None):        
        self.connection: Connection = None

        LOGGER.debug('SshCopyTarget.__init__()')
        LOGGER.trace(f'-  host: {hostname}:{port}  credentials: {username}/{password}  local ssh path: {local_sshkeys_path}')
        self.hostname = hostname
        self.port = port
        self.username = username
        self._password = password
        self.local_sshkeys_path = self._get_local_sshkeys_path() if local_sshkeys_path is None else pathlib.Path(local_sshkeys_path).absolute()
        self.remote_auth_keys_path = '~/.ssh/authorized_keys'

    def _get_local_sshkeys_path(self) -> pathlib.Path:
        LOGGER.debug('- _get_local_sshkeys_path()')
        pubkey_filename: pathlib.Path = None
        home_ssh = pathlib.Path('~/.ssh').expanduser()
        if not home_ssh.exists() or not home_ssh.is_dir():
            raise RuntimeError(f'SSH config directory [{home_ssh.expanduser()}] does not exist.')

        # Check to make sure that at least 1 public key file exists.
        for key_type in ['rsa', 'dsa', 'ecdsa', 'ecdsa-sk', 'ed25519', 'ed25519-sk']:
            token_file = pathlib.Path("~") / ".ssh" / f'id_{key_type}.pub'
            if token_file.expanduser().exists():
                LOGGER.trace(f'  - found {token_file}')
                pubkey_filename = token_file.expanduser().absolute()
                break

        if pubkey_filename is None:
            raise RuntimeError('Unable to locate andy public ssh keyfiles. Abort.')

        # Return the path
        return pubkey_filename.expanduser().absolute().parent

    def _get_local_key(self, key_file: pathlib.Path):
        LOGGER.debug(f'- _get_local_key(key_file={key_file})')
        try:
            LOGGER.trace(f'  - read {key_file} and retrieve key')
            key = key_file.read_text().strip()
            LOGGER.info(f'Source of key to be installed: {key_file}')
        except:
            raise RuntimeError(f"ERROR: key file '{key_file}' could not be opened.")

        return key

    def _validate_connection(self) -> Union[Connection, None]:
        LOGGER.debug('- _validate_connection()')
        password = self._password
        if password is None:
            password = getpass()
        connect_kwargs = {'password': password, 'look_for_keys': False}
        LOGGER.trace('  - create connection.')
        connection = Connection(host=self.hostname, port=self.port, user=self.username, connect_kwargs=connect_kwargs)
        try:
            _ = connection.run('ls', hide=True)
            self._password = password
            LOGGER.trace(f'  - successful login to {connection.user}@{connection.host}')
        except AuthenticationException as ae:
            LOGGER.debug(f'  - {ae} | user: {connection.user}   pass: {password}')
            connection = None
            self._password = None
    
        return connection
    
    def _copy_key(self, key_file: pathlib.Path, force_copy: bool = False) -> bool:
        LOGGER.debug(f'- _copy_key(key_file={key_file}, force_copy={force_copy})')
        copied = False
        key = self._get_local_key(key_file)
        LOGGER.trace('  - retrieve authorized keys...')
        authorized_keys = self.connection.run(f'cat {self.remote_auth_keys_path}', hide=True)
        if key not in authorized_keys.stdout or force_copy:
            LOGGER.trace('  - add key to authorized_keys.')
            # Add the key to authorized keys
            self.connection.run(f'echo {key} >> {self.remote_auth_keys_path}')
            copied = True
        else:
            LOGGER.warning(f'- public key already exists in {self.hostname}:{self.remote_auth_keys_path}')

        return copied
    
    def copy_keys(self, force_copy: bool = False):
        LOGGER.debug(f'copy_keys(force_copy={force_copy})')
        login_cnt = 1 if self._password is None else 0
        self.connection = self._validate_connection()
        while login_cnt < 2 and self.connection is None:
            # if login_cnt == 0:
            #     LOGGER.warning('  Unable to authenticate, try again...')
            self.connection = self._validate_connection()
            login_cnt += 1

        if self.connection is None:
            LOGGER.error('  Invalid credentials (unknown username and/or password).  Abort.')
            sys.exit(1)

        copied = 0
        not_copied = 0
        result: Result = None

        LOGGER.debug('- determine if authorized_keys exists on target.')
        result = self.connection.run(f'[ -f {self.remote_auth_keys_path} ] && echo 1 || echo 0', hide=True)
        if '0' in result.stdout:
            # file or directory does not exist.
            LOGGER.debug(f'  - creating {self.hostname}:{self.remote_auth_keys_path}')
            self.connection.run(f'mkdir -p {self.remote_auth_keys_path.replace("authorized_keys","")}', hide=True)
            self.connection.run(f'touch {self.remote_auth_keys_path}', hide=True)
            self.connection.run(f'chmod 600 {self.remote_auth_keys_path}', hide=True)
        else:
            LOGGER.debug(f'  - {self.remote_auth_keys_path} exists on {self.hostname}')

        if self.local_sshkeys_path.is_file():
            if self._copy_key(self.local_sshkeys_path, force_copy):
                copied += 1
            else:
                not_copied += 1
        else:
            for key_type in ['rsa', 'dsa', 'ecdsa', 'ecdsa-sk', 'ed25519', 'ed25519-sk']:
                key_file = pathlib.Path(f'~/.ssh/id_{key_type}.pub').expanduser().absolute()
                if key_file.exists():
                    if self._copy_key(key_file, force_copy):
                        copied += 1
                    else:
                        not_copied += 1
        LOGGER.info('')
        if not_copied > 0:
            LOGGER.info(f'Number of keys copied: {copied}  skipped: {not_copied}')
        else:
            LOGGER.success(f'Number of keys copied: {copied}')
        if copied > 0:
            LOGGER.info(f"Now try logging into the machine with: 'ssh {self.connection.user}@{self.hostname}'")
        self.connection.close()

def setup_logging(args: argparse.Namespace):
    l_level = "INFO"
    l_format = DEFAULT_CONSOLE_LOGFMT
    if args.verbose > 0:
        # 1=debug format, 2 enable=debug, 3=trace
        l_format = DEFAULT_DEBUG_LOGFMT
        if args.verbose == 2:
            l_level = "DEBUG"
        elif args.verbose > 2:
            l_level = "TRACE"
    
    LOGGER.remove()
    _ = LOGGER.add(sink=sys.stderr, level=l_level, format=l_format)

def valid_host(hostname: str) -> bool:
    LOGGER.debug(f'valid_host({hostname})')
    is_up = False
    try:
        import os
        is_up = True if os.system(f'ping -n 1 {hostname.split()[0]} > NUL') == 0 else False
    except Exception as ex:
        LOGGER.debug(f'ERROR: {ex}')
    return is_up

def main():
    parser = argparse.ArgumentParser(description='ssh-copy-id - copy ssh public keys to target host')
    parser.add_argument('hostname', nargs='+', help='[user@]hostname')
    parser.add_argument('-f', '--force', action='store_true', default=False, help='Force copy, no existence check.')
    parser.add_argument('-i', '--identity_file', type=str, default=None, metavar='FILE',
                        help='the identity file to be copied.  If not specified, adds all keys.')
    parser.add_argument('-p', '--port', type=int, default=22,
                        help='SSH port (default 22)')
    parser.add_argument('-v', '--verbose', action='count', default=0, help=argparse.SUPPRESS)
    args = parser.parse_args()
    setup_logging(args)

    if args.identity_file is not None:
        id_file = pathlib.Path(args.identity_file)
        print(id_file)
        id_file = id_file.expanduser()
        print(id_file)
        if not id_file.exists():
            parser.print_usage()
            LOGGER.error(f'Identity file {id_file} does not exist.')
            sys.exit(1)

    cached_pwd: str = None
    for hostname in args.hostname:
        LOGGER.info('')
        # hostname = args.hostname
        username = None
        if '@' in hostname:
            if args.hostname.count('@') > 1:
                LOGGER.error(f'ERROR: unrecognized [user@]hostname - {hostname}')
                continue
            username, hostname = hostname.split('@')

        if not valid_host(hostname):
            LOGGER.error(f'ERROR: Unknown, invalid or off-line host [{hostname}]')
            continue

        ssh_copy_id: SshCopyTarget = None        
        try:
            header_line = f'Setup keys for {hostname}'
            LOGGER.info(header_line)
            LOGGER.info('-'*len(header_line))
            ssh_copy_id = SshCopyTarget(hostname=hostname, port=args.port, 
                                        username=username, password=cached_pwd, 
                                        local_sshkeys_path=args.identity_file)
            ssh_copy_id.copy_keys(force_copy=args.force)
            cached_pwd = ssh_copy_id._password
        except KeyboardInterrupt:
            LOGGER.error('Ctrl-C - Abort.')
            sys.exit(1)
        except RuntimeError as rte:
            LOGGER.error(f'Runtime: {rte}')
            sys.exit(1)
        except Exception as e:
            LOGGER.exception(f'ERROR: {e}')
            sys.exit(1)
        finally:
            if ssh_copy_id is not None and ssh_copy_id.connection is not None:
                ssh_copy_id.connection.close()

if __name__ == "__main__":
    sys.exit(main())