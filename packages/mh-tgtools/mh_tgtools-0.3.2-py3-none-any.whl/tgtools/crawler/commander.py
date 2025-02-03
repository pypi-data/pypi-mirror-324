import datetime

from tgtools import Cmd, Credential, Err, Events, SSHNetconf, TgParser
from tgtools.consts import MAX_NUM_GET_EVENTS_RPC, RADIO_NAME_MAX_LEN
from tgtools.utils.miscfuncs import prettyprint_xml


class TgCommander:
    def __init__(self, credential: Credential, remote_cn: str = ''):
        """

        :param credential: Credential to log into radio (IP address, username, password).
        :type credential: Credential
        :param remote_cn: Name of remote Client Node (if tunneling into a remote radio).
        :type remote_cn: str
        """

        #: Radio's login credential (IP address, username, password).
        self.credential: Credential = credential
        #: Name of remote radio (if tunneling into a remote Client Node, rather than a local one specified in ``credential``).
        self.remote_cn: str = remote_cn
        #: Name of local radio (updated after calling :meth:`get_and_parse`).
        self.local_name: str = ''
        #: List of all remote Client Nodes (updated after calling :meth:`get_and_parse`).
        self.remote_cns_names: list[str] = []

        # RPC: Get
        #: Response to the **get** RPC (the raw XML).
        self.get_xml: str = ''
        #: Response to the **get** RPC, parsed.
        self.get_parsed: dict[str, list] = {}
        # Parsing tokens for the response of **get** RPC (per section).
        # self.get_tokens: dict[str, list] = {}
        #: Parsing sections for the response of the **get** RPC.
        self.get_sections: list[str] = []

        #: Response to the **get-config** RPC (raw XML).
        self.config_xml: dict[str, str] = {}

        # RPC: Get Events
        #: Response to the **get-events** RPC (raw XML).
        self.events_xml: str = ''
        #: Response to the **get-events** RPC, parsed.
        self.events_parsed: Events
        # Parsing tokens for the response to the **get-events** RPC.
        # self.events_tokens: list[str] = []

        #: List of (configuration-changing) commands sent to radio.
        self.commands: list[Cmd] = []
        # self.commands_tokens: list[str] = []

        #: List of errors encountered while interacting with radio.
        self.errors: list[Err] = []

        self._route: str = credential.padded_ip_addr()
        if remote_cn:
            self._route += f"_{remote_cn}"

        #: Underlying SSHNetconf session.
        self.ssh = SSHNetconf(credential.ip_addr, credential.username, credential.password, remote_cn)
        return

    def connect(self) -> bool:
        """ Connect to radio.

            :return: Indication of whether connection was successful.
            :rtype: bool
        """
        success: bool = self.ssh.connect()
        err: Err = self.ssh.last_err
        if err:
            self.errors.append(err)
        return success

    @property
    def is_connected(self) -> bool:
        """ Indication if radio is connected.

            rtype: bool
        """
        if self.ssh:
            return self.ssh.is_connected()
        else:
            return False

    def disconnect(self):
        """ Disconnect from radio.
        """
        self.ssh.disconnect()
        return None

    def get_rpc(self) -> str:
        """ Execute the **get** RPC. Avoid calling directly, and use instead :meth:`get_and_parse`.

            :return: response from radio, as raw XML
            :rtype: str
        """
        cmd = '<get xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>'
        xml = self.ssh.rpc(cmd)
        err: Err = self.ssh.last_err
        if err:
            self.errors.append(err)
            return ''
        else:
            return xml

    def get_parse(self, get_xml: str, prefix_fields: dict[str, str]) -> TgParser:
        """ Parse the XML response of the **get** RPC. Avoid calling directly, and use instead :meth:`get_and_parse`.

            :param get_xml: The raw XML response from the radio to the **get** RPC.
            :type get_xml: str
            :param prefix_fields: Optional labels to prepend to the parsed output (typically indicating the radio and timestamp).
            :type prefix_fields: dict[str,str]
            :rtype: TgParser
        """

        tgparser = TgParser(get_xml, prefix_fields)
        if tgparser.errors:
            self.errors.extend(tgparser.errors)
        return tgparser

    def get_and_parse(self):
        """ The main API for running the **get** RPC, fetching result and parsing it. The parsed output is
            updated in :attr:`get_parsed`. Also updated are
            the :attr:`local_name` and :attr:`remote_cns_names` attributes.
        """
        timestamp = datetime.datetime.now()
        self.get_xml = self.get_rpc()
        prefix_fields = dict(
            route=self._route,
            sampled=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            local='',
        )
        tgparser: TgParser = self.get_parse(self.get_xml, prefix_fields)
        self.get_parsed = tgparser.parsed
        # self.get_tokens = tgparser.tokens
        self.get_sections = tgparser.sections
        self.local_name = tgparser.local
        for section in self.get_sections:
            for record in self.get_parsed[section]:
                record['local'] = self.local_name
        self.remote_cns_names = tgparser.remote_cns

    def get_events_rpc(self, num_events: int = 200) -> str | None:
        """ Execute the **get-events** RPC. Avoid calling directly, and use instead :meth:`get_events_and_parse`.

            :param num_events: Number of events to fetch (default: 200).
            :type num_events: int
            :return: response from radio as XML
            :rtype: str | None
        """
        if not isinstance(num_events, int) or num_events > MAX_NUM_GET_EVENTS_RPC:
            raise TypeError(
                "TgCommander.get_events_rpc: num_events () must be integer not larger than {MAX_NUM_GET_EVENTS_RPC}")
        cmd = f'<get-events xmlns="http://siklu.com/yang/tg/events"><number>{num_events}</number></get-events>'
        xml = self.ssh.rpc(cmd)
        err: Err = self.ssh.last_err
        if err:
            self.errors.append(err)
            return ''
        else:
            return xml

    def get_events_and_parse(self, num_events: int = 200):
        """ The main API for running the **get-events** RPC, fetching result and parsing it.

            :param num_events: Number of events to fetch (default: 200).
            :type num_events: int
        """
        timestamp = datetime.datetime.now()
        self.events_xml = self.get_events_rpc(num_events)
        prefix_fields = dict(
            route=self._route,
            sampled=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            local=self.local_name,
        )
        self.events_parsed = Events.from_xml(self.events_xml, prefix_fields)
        if self.events_parsed.errors:
            self.errors += self.events_parsed.errors

    def get_config(self, config_db: str):
        """ Run the **get-config** RPC and pretty-format the received XML.

            :param config_db: The configuration database requested: 'candidate', 'running, or 'startup'.
            :type config_db: sr
        """
        if config_db not in ('candidate', 'running', 'startup'):
            raise ValueError(f"TgCommander.get_config: Unknown config_db: '{config_db}'")
        cmd = f'<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><source><{config_db}/></source></get-config>'
        xml = self.ssh.rpc(cmd)
        err: Err = self.ssh.last_err
        if err:
            self.errors.append(err)
            self.config_xml[config_db] = ''
        else:
            self.config_xml[config_db] = prettyprint_xml(xml)

    def cli_send(self, commands: list[str]):
        """ Run the **run-cli-commands** RPC, sending to the radio a list of CLI commands.

            :param commands: List of CLI commands.
            :type commands: list[str]
        """
        cmd: str = ""
        for index, command in enumerate(commands):
            cmd += "<commands>"
            cmd += f"<id>{str(index + 1)}</id>"
            cmd += f"<command>{command}</command>"
            cmd += "</commands>"
        cmd = f'<run-cli-commands xmlns="http://siklu.com/yang/tg/system">{cmd}</run-cli-commands>'
        response = self.ssh.rpc(cmd)
        cmd_str = f"RPC request: cli_send = {','.join(commands)}"
        self._update_commands_errors(cmd_str, response, self.ssh.last_err)
        return None

    def set_tod(self, hours_shift: float = 0):
        """ Configure the date and time using the **set-system-time** and **set-system*date** RPCs.
            The date and time are copied from the computer (running this program),
            with the addition of `hours_shift` (to compensate for possible different time zones).

            :param hours_shift: delta hours added to the computer's time before sending to radio. For example,
                                if computer time is 08:00 and `hours_shift` equals 2.5, the time configured to radio
                                will be 10:30. The default for `hours_shift` is zero.
            :type hours_shift: float
        """
        if isinstance(hours_shift, int):
            hours_shift = float(hours_shift)
        else:
            assert isinstance(hours_shift, float)
        # Set time
        tod = datetime.datetime.now()
        adjusted_tod = tod + datetime.timedelta(hours=hours_shift)
        time = adjusted_tod.strftime('%H:%M:%S')
        cmd = f'<set-system-time xmlns="http://siklu.com/yang/tg/system"><time>{time}</time></set-system-time>'
        cmd_str = f"RPC request: set-system-time = {time}"
        response = self.ssh.rpc(cmd)
        self._update_commands_errors(cmd_str, response, self.ssh.last_err)
        # Set date
        tod = datetime.datetime.now()
        adjusted_tod = tod + datetime.timedelta(hours=hours_shift)
        date = adjusted_tod.strftime('%Y-%m-%d')
        cmd = f'<set-system-date xmlns="http://siklu.com/yang/tg/system"><date>{date}</date></set-system-date>'
        cmd_str = f"RPC request: set-system-date = {date}"
        response = self.ssh.rpc(cmd)
        self._update_commands_errors(cmd_str, response, self.ssh.last_err)

    def _update_commands_errors(self, cmd_str: str, response: str, err: Err):
        timestamp = datetime.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")
        if err:
            self.errors.append(err)
            self.commands.append(
                Cmd(cmd_str, target_id=self._route, response=response, success=False, timestamp=timestamp))
        else:
            self.commands.append(
                Cmd(cmd_str, target_id=self._route, response=response, success=True, timestamp=timestamp))


if __name__ == '__main__':
    credential = Credential('172.19.40.10', 'admin', 'Air-band12?')
    cmd = TgCommander(credential)
    cmd.connect()
    if cmd.is_connected:
        cmd.get_and_parse()
        print(f"Local radio name: {cmd.local_name}")
        print(f"List of remote Client Nodes: {cmd.remote_cns_names}")
        cmd.get_events_and_parse(10)
        print(cmd.events_parsed)
        cmd.disconnect()
