import ipaddress
import logging
import re

from lxml import etree
import ncclient.manager
from ncclient.operations.rpc import NCClientError
from ncclient.transport.errors import AuthenticationError, SSHError, SSHUnknownHostError

from tgtools import Err
from tgtools.consts import NETCONF_SSH_TIMEOUT, RE_RADIO_NAME
from tgtools.utils import mylogger


# Uncomment for ncclient logging
# logging.basicConfig(level=logging.INFO,)

class SSHNetconf:
    """ A NETCONF driver for Siklu by Ceragon TG radios. Essentially a wrapper for
        `ncclient <https://pypi.org/project/ncclient>`_.

        Radio can be connected to directly (to ``ip_addr``); or indirectly, by tunneling into
        a remote Client Node (with name ``remote``) via ``ip_addr``.
    """

    def __init__(self,
                 ip_addr: str | ipaddress.IPv4Address | ipaddress.IPv6Address,
                 username: str = 'admin',
                 password: str = 'admin',
                 remote: str = '',
                 socket_timeout: float = NETCONF_SSH_TIMEOUT,
                 ssh_logger: bool = False,
                 log_level_file: int = logging.INFO,
                 log_level_console: int = logging.CRITICAL):
        """ Initialise with arguments:

        :param ip_addr: IP address of radio.
        :type ip_addr: str | ipaddress.IPv4Address | ipaddress.IPv6Address
        :param username: Username to log in to radio (default: `admin`).
        :type username: str
        :param password: Password to log in to radio (default `admin`).
        :type password: str
        :param remote: Name of remote radio to tunnel into (default: '', for no-tunneling).
        :type remote: str
        :param socket_timeout: Timeout for socket connection (default in ``consts.py``).
        :type socket_timeout: float
        :param ssh_logger: If ``True``, enable logger (default: ``False``).
        :type ssh_logger: bool
        :param log_level_file: Logging level to file (default: logging.INFO).
        :type log_level_file: int
        :param log_level_console: Logging level to console (default: logging.CRITICAL).
        :type log_level_console: int
        """

        #: IP address for radio, or (if ``remote`` provided: gateway to remote radio).
        self.ip_addr: str
        if isinstance(ip_addr, ipaddress.IPv4Address) or isinstance(ip_addr, ipaddress.IPv6Address):
            self.ip_addr = str(ip_addr)
        else:
            ipaddress.ip_address(ip_addr)
            self.ip_addr = ip_addr
        #: Username to log in to radio.
        self.username: str = username
        #: Password to log in to radio.
        self.password: str = password
        #: Name of remote device (if tunneling through).
        self.remote: str = remote
        if remote and not re.fullmatch(RE_RADIO_NAME, remote):
            raise ValueError("SSHNetConf: illegal value for argument 'remote': {remote}")

        #: Socket timeout
        self.socket_timeout: float = socket_timeout

        if ssh_logger:
            self._logger = mylogger.logger_by_label(label=self.ip_addr, log_enable=True, log_dir='ssh_logs',
                                                    log_level_console=log_level_console,
                                                    log_level_file=log_level_file)
        else:
            self._logger = mylogger.logger_by_label(label=self.ip_addr, log_enable=False)

        #: Underlying ncclient instance.
        self.netconf: ncclient.manager.Manager | None = None

        self._last_err = ''
        self._rpc_response = ''
        self._label_id = f"{self.ip_addr}->{self.remote}" if remote else f"{self.ip_addr}"

    @property
    def last_err(self):
        """ Last error (clears after it's accessed). """
        last_err = self._last_err
        self._last_err = ''
        return last_err

    @property
    def rpc_response(self):
        """ RPC response to :meth:`rpc` (clears after it's accessed). """
        response = self._rpc_response
        self._rpc_response = ''
        return response

    def __repr__(self):
        info = f"{self.__class__.__name__}("
        info += f"ip_addr={self.ip_addr}, "
        info += f"username={self.username}, "
        info += f"password={self.password}, "
        if self.remote:
            info += f"remote={self.remote}, "
        info += f"socket_timeout={self.socket_timeout}"
        info += ')'
        return info

    def __str__(self):
        info = f"{self.__class__.__name__}"
        info += f"\tip_addr: {self.ip_addr}\n"
        info += f"\tusername: {self.username}\n"
        info += f"\tpassword: {self.password}\n"
        info += f"\tremote: {self.remote}\n"
        info += f"\tconnected: {self.is_connected()}\n"
        info += f"\tlast_err: {self._last_err}"
        return info

    def connect(self) -> bool:
        """ Open NETCONF connection to radio (either directly to :attr:`ip_addr`, or else
            to remote :attr:`remote` (if provided), by tunneling via :attr:`ip_addr`.

            :return: ``True`` if radio is connected, ``False`` otherwise.
            :rtype: bool
        """
        # Check if already connected?
        if self.is_connected():
            self._logger.debug(f"{self._label_id}  Netconf session: already connected")
            return True
        # Tunnel into remote CN?
        if self.remote:
            environment = {"AN": self.remote}
        else:
            environment = None
        # Attempt connection
        try:
            self.netconf = ncclient.manager.connect(host=self.ip_addr,
                                                    port=22,
                                                    username=self.username,
                                                    password=self.password,
                                                    hostkey_verify=False,
                                                    timeout=self.socket_timeout,
                                                    environment=environment)
        except (AuthenticationError, SSHError, SSHUnknownHostError) as e:
            err_msg = ','.join([str(arg) for arg in e.args])
            self._logger.error(f"{self._label_id} {err_msg}")
            self._last_err = Err(self._label_id, err_msg)
        else:
            self._logger.debug(f"{self._label_id} Netconf session: Successfully connected")
        finally:
            return self.is_connected()

    def disconnect(self):
        """ Disconnect Netconf session.
        """
        if self.netconf and self.netconf.is_connected:
            try:
                self.netconf.close_session()
            except NCClientError as e:
                self._last_err = Err(self._label_id, str(e))
                self._logger.error(f"{self._label_id} {e}")
            else:
                self._logger.debug(f"{self._label_id} Netconf session: connection closed")
        else:
            self._logger.debug(f"{self._label_id} Netconf session: attempt to close, but found already closed")
        self.netconf = None
        return None

    def is_connected(self) -> bool:
        """ Check connection status.

            :return: ``True`` if radio is connected, ``False`` otherwise.
            :rtype: bool
        """
        if self.netconf:
            return self.netconf.connected
        else:
            return False

    def rpc(self, cmd_xml: str) -> str:
        """ Send an RPC request (represented as XML) and return the XML response.

            :param cmd_xml: RPC request, as XML.
            :type cmd_xml: str
            :return: Response to RPC reponse, as XML.
            :rtype: str
        """
        if not self.is_connected():
            err_msg = f"Cannot request RPC: Netconf session is closed ({cmd_xml})"
            self._last_err = Err(self._label_id, err_msg)
            self._logger.error(f"{self._label_id} {err_msg}")
            return ''
        self._logger.debug(f"{self._label_id} Requesting RPC: {cmd_xml}")
        # Check validity of XML
        try:
            cmd = etree.fromstring(cmd_xml)
        except etree.XMLSyntaxError as e:
            err_msg = ','.join([str(arg) for arg in e.args]) + f' in RPC request {cmd_xml}'
            self._last_err = Err(self._label_id, err_msg)
            self._logger.error(f"{self._label_id} {err_msg}")
            return ''
        else:  # Validity confirmed. Now send RPC command
            try:
                response = self.netconf.dispatch(cmd)
            except NCClientError as e:
                err_msg = ','.join([str(arg) for arg in e.args]) + f' in RPC request {cmd_xml}'
                self._last_err = Err(self._label_id, err_msg)
                self._logger.error(f"{self._label_id} {err_msg}")
                return ''
            else:
                self._logger.debug(f"{self._label_id} RPC Response received")
                self._rpc_response = response.xml
                return response.xml


if __name__ == '__main__':
    netconf = SSHNetconf('192.168.0.1')
    netconf.connect()
    if err := netconf.last_err:
        print(err)
    else:
        cmd = f'<get-events xmlns="http://siklu.com/yang/tg/events"><number>1</number></get-events>'
        response = netconf.rpc(cmd)
        if err := netconf.last_err:
            print(err)
        else:
            print(response)
    netconf.disconnect()
