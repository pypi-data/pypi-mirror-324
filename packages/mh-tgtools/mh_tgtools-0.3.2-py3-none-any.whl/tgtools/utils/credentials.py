from collections import abc
import ipaddress
from pathlib import Path
import re
from typing import Generator

from tgtools.utils.ioutils.iogen import confirm_exists

DEFAULT_USERNAME = 'admin'
DEFAULT_PASSWORD = 'admin'
_RE_USERNAME = re.compile(r'[Uu]sername\s*=\s*(\S+)')
_RE_PASSWORD = re.compile(r'[Pp]assword\s*=\s*(\S+)')


def str_validate_ip_address(ip_addr: str | ipaddress.IPv4Address | ipaddress.IPv6Address) -> str:
    """ Validates argument as a valid IP address, and return as str.

        :param ip_addr: candidate IP address
        :type ip_addr: str | ipaddress.IPv4Address | ipaddress.IPv6Address
        :rtype: str
    """

    if isinstance(ip_addr, str):
        try:
            ipaddress.ip_address(ip_addr)
        except ValueError as e:
            raise e
        else:
            return ip_addr
    elif isinstance(ip_addr, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        return str(ip_addr)
    else:
        raise ValueError(f"{ip_addr} is not a valid IP address")


class Credential:
    """ Radio's login credentials: IP address, username, and password.
    """

    def __init__(self, ip_addr: str | ipaddress.IPv4Address | ipaddress.IPv6Address,
                 username: str = DEFAULT_USERNAME,
                 password: str = DEFAULT_PASSWORD):
        """
        :param ip_addr: IP address
        :type ip_addr: str | ipaddress.IPv4Address | ipaddress.IPv6Address
        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        """

        #: IP Address of radio
        self.ip_addr: str = str_validate_ip_address(ip_addr)
        #: Username to log into radio
        self.username: str = username
        #: Password to log into radio
        self.password: str = password

    def __hash__(self):
        return hash(self.ip_addr)

    def __lt__(self, other):
        return self.ip_addr < other.ip_addr

    def __repr__(self):
        return f"Credential({self.ip_addr}, '{self.username}', '{self.password}')"

    def padded_ip_addr(self):
        """ Zero-pad each decimal number, e.g.: '192.168.0.1' -> '192.168.000.001'. Useful for sorting.
        """
        output = ""
        for number in str(self.ip_addr).split('.'):
            output += f"{int(number):03}."
        return output[:-1]


class Credentials(abc.Sequence):
    """ A sequence of :class:`Credential`, sorted by IP address, and without any duplicates
    """

    def __init__(self, items=None, *, text_to_parse=None):
        """ Initialises an instance of the class.

            :param items: an optional single :class:`Credential` or a sequence of :class:`Credential`
            :type items: Credential | list[Credential]
            :param text_to_parse: an optional text to parse
            :type text_to_parse: str

            There are 2 ways to initialise :class:`Credentials`:

            1. If `text_to_parse` is provided (usually by reading the contents of a config file)
               then parse the text to obtain:

               * Login credentials: username and password (example below)
                 If omitted, the defaults are 'admin'/'admin'.

               * A range of IP addresses. Can be *any number* of the following, each on a new line:
                  * A single IP address
                  * A range of IP addresses: start and end addresses separated by a hyphen
                  * A subnet, with a forward slash denoting the number of subnet bits

               Here is an example content for the input file::

                    username = my_user_name
                    password = my_password
                    192.168.0.100
                    192.168.0.101
                    10.11.12.1 - 10.11.12.200
                    10.10.10.0/24
                    192.168.100.0/23

               This would result in a total of  1+1+200+254+510 IP addresses.

            2. Alternatively, If `text_to_parse` is `None`, then `items` can be either a single :class:`Credential`
               or a sequence of :class:`Credential`. This option is added in order to implement __getitem__(),
               and hence the
               `abc.Sequence <https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence>`_
               protocol.
        """

        self.text_to_parse = text_to_parse
        if text_to_parse:
            self._credentials = self._parse_credentials()
        elif items:
            if isinstance(items, abc.Sequence):
                self._credentials = items
            else:
                self._credentials = [items]
        else:
            self._credentials = []
        # Remove duplicates and sort
        self._uniquify()

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._credentials[item]
        else:
            return Credentials(self._credentials[item])

    def __len__(self):
        return len(self._credentials)

    def __repr__(self):
        if self.text_to_parse:
            return f"Credentials('{self.text_to_parse}')"
        else:
            return f"Credentials(list_of_items)"

    def __str__(self):
        if self._credentials:
            first = self._credentials[0]
            last = self._credentials[-1]
            return f"{len(self._credentials)} Credentials: from {first.ip_addr} to {last.ip_addr}"
        else:
            return f"No Credentials"

    def _parse_credentials(self):
        """ Read a list of IP addresses and login credentials
        """
        username = DEFAULT_USERNAME
        password = DEFAULT_PASSWORD
        credentials = []
        for row_num, row in enumerate(self.text_to_parse.split('\n')):
            line = row.strip()
            # Line is a comment or a blank line
            if line == '' or line[0] == '#':
                pass
            # Line updates the username
            elif new_username := _RE_USERNAME.search(line):
                username = new_username[1]
            # Line updates the password
            elif new_password := _RE_PASSWORD.search(line):
                password = new_password[1]
            # Line designates a network, e.g.: 192.168.3.0/24
            elif r'/' in line:
                try:
                    network = ipaddress.IPv4Network(line)
                except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
                    print(f"\tSkipping line #{row_num + 1}: found '/' but line syntax unknown: '{line}'")
                except ValueError:
                    print(f"\tSkipping line #{row_num + 1}: host bits set: '{line}'")
                else:
                    for host in network.hosts():
                        credentials.append(Credential(host, username, password))
            # Line designates a range of addresses, e.g.: 192.168.3.10-192.168.3.14
            elif r'-' in line:
                try:
                    first, last = line.split('-')
                    first_ip = ipaddress.IPv4Address(first.strip())
                    last_ip = ipaddress.IPv4Address(last.strip())
                except ValueError:
                    print(f"\tSkipping line #{row_num + 1}: found '-' but line syntax unknown: '{line}")
                else:
                    for host in range(int(first_ip), int(last_ip) + 1):
                        credentials.append(Credential(ipaddress.IPv4Address(host), username, password))
            # Single IP address, e.g.: 192.168.3.5
            else:
                try:
                    host = ipaddress.IPv4Address(line)
                except ipaddress.AddressValueError:
                    print(f"\tSkipping line #{row_num + 1}: invalid IP address: '{line}")
                else:
                    credentials.append(Credential(host, username, password))
        return credentials

    def _uniquify(self):
        """ Remove any duplicate IP addresses, and sort the remaining ones
        """

        credentials_set = set(self._credentials)
        self._credentials = list(credentials_set)
        self._credentials.sort(key = lambda x: x.padded_ip_addr())

    def get_batches(self, batch_size=1000) -> Generator[list[Credential]]:
        """ A generator method which yields batches at a time, where each batch is a list of :class:`Credential`.
            In each batch, the length of the returned list is `batch_size`, except possibly for the last batch
            which may be shorter (remainder).

            :param batch_size: Number of :class:`Credential` in each batch (defaults to 1000)
            :type batch_size: int
            :return: A list of :class:`Credential`
            :rtype: Generator[List[Credential]]
        """
        batches = len(self) // batch_size + 1
        for batch in range(batches):
            start_index = batch * batch_size
            end_index = min(start_index + batch_size, len(self))
            yield self[start_index: end_index]

    @staticmethod
    def from_file(filepath: Path):
        """ Read credentials from text file.

        :param filepath: input filename
        :type filepath: pathlib.Path
        :rtype: Credentials

        """
        if confirm_exists(filepath):
            text_from_filenm = filepath.read_text()
            return Credentials(text_to_parse=text_from_filenm)
        else:
            raise FileNotFoundError(f"File '{filepath}' not found")


if __name__ == '__main__':
    cred = Credential('192.168.0.1')
    print(cred)
    print(cred.padded_ip_addr())
    print()
    text = "username = admin \n password = adminpassw \n 192.168.0.0/28"
    creds = Credentials(text_to_parse=text)
    print(f"Total of {len(creds)} credentials")
    for batch in creds.get_batches(5):
        print(batch)
