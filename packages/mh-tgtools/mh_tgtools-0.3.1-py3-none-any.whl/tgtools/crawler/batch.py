import concurrent.futures
import datetime
from pathlib import Path
import threading
import time
import typing

from tgtools import Credential, Credentials, TechLog, TgCommander
from tgtools.consts import RADIO_NAME_MAX_LEN
from tgtools.utils.ioutils import iocsv, iogen
from tgtools.utils.ioutils.iogen import enforce_max_files
from tgtools.utils.miscfuncs import prettyprint_xml
from tgtools.utils.timefunc import get_timestamp_for_files

ActionType = typing.Literal['get_configs', 'get_events', 'get_status', 'get_status_xml', 'get_tech_logs',
                            'send_commands', 'set_tod']


class _RadioID:
    """ Representation of radio IP address, local name and name of remote radio (if applicable)
    """

    def __init__(self, ip_addr, local, remote_cn=''):
        #: IP address
        self.ip_addr = str(ip_addr)
        #: Name of local radio (dialed to via ``ip_addr``)
        self.local = local
        #: Name of remote radio (if applicable)
        self.remote = remote_cn

    def __str__(self):
        msg = self.ip_addr.ljust(15, ' ')
        if self.local:
            msg += f" ({self.local.ljust(RADIO_NAME_MAX_LEN, ' ')})"
        else:
            msg += ' ' * (RADIO_NAME_MAX_LEN + 3)
        if self.remote:
            msg += f" -> {self.remote.ljust(RADIO_NAME_MAX_LEN, ' ')}"
        else:
            msg += ' ' * (RADIO_NAME_MAX_LEN + 4)
        return msg

    def file_label(self):
        """ Label for filename prefix
        """
        if self.remote:
            return self.remote
        elif self.local:
            return self.local
        else:
            return f"{self.ip_addr}"


class TgCrawler:
    """ A batch manager for 'crawling' over a TG network and performing one or more *actions*:
         - get_status (**get** RPC)
         - get_configs (**get-configs** RPC)
         - get_events (**get-events** RPC)
         - get_tech_logs (via HTTP)
         - send_cmds (**run-cli-commands** RPC)
         - set_tod (**set-system-time** and **set-system-date** RPCs)

        Actions are executed on local radios (with network IP addresses) and/or remote Client Nodes (via tunneling).

        Results are saved to text files. Errors and commands sent to radios are logged to text files.

        Functionality is controlled via instantiation arguments.
    """

    def __init__(self, credentials: Credentials, /,
                 action_local: bool = True,
                 action_remote_cns: bool = False,
                 action_remote_cns_list: list[str] | None = None,
                 get_status: bool = True,
                 get_status_xml: bool = False,
                 get_status_xml_max_files: int = 3,
                 get_configs: bool = False,
                 get_configs_db: str = 'startup',
                 get_configs_max_files: int = 3,
                 get_events: bool = True,
                 get_tech_logs: bool = False,
                 get_tech_log_max_files: int = 20,
                 send_cmds: bool = False,
                 send_cmds_script: list[str] | None = None,
                 set_tod: bool = False,
                 set_tod_shift: float = 0,
                 concurrency: bool = True,
                 concurrency_threads: int = 10,
                 dir_output_root: str = 'output',
                 dir_get_configs: str = 'configs',
                 dir_get_events: str = 'events',
                 dir_get_status: str = 'status',
                 dir_get_status_xml: str = 'status_xml',
                 dir_get_tech_logs: str = 'tech_logs',
                 filename_cmdlog: str = 'cmdlog.txt',
                 filename_errlog: str = 'errlog.txt',
                 debug_print: bool = True, ):
        """

        :param credentials: Description of network and login credentials over which actions are taken.
        :type credentials: Credentials
        :param action_local: Execute actions on the local radio (directly connected to via its IP address). Default: True.
        :type action_local: bool
        :param action_remote_cns: Execute actions on some/all remote radios (via tunnelling from local radio(s)). Default: True.
        :type action_remote_cns: bool
        :param action_remote_cns_list: Applicable only if ``action_remote_cns`` is ``True``: List of remote radio names for actions. If None or empty, remote radios are automatically discovered and actions are applied to them all. Default: None
        :type action_remote_cns_list: list[str]|None
        :param get_status: Actions to include fetching comprehensive telemetry (**get** RPC), parsing, and saving the parsed results. Default: True.
        :type get_status: bool
        :param get_status_xml: Applicable only if ``get_status`` is ``True``: Save the raw XML response from radio. Default: False.
        :type get_status_xml: bool
        :param get_status_xml_max_files: Applicable only if ``get_status_xml`` is ``True``: The maximum number of files to save before rolling over. Default: 3.
        :type get_status_xml_max_files: int
        :param get_configs: actions to include fetching configuration file of type ``get_configs_db``. Default: False.
        :type get_configs: bool
        :param get_configs_db: Applicable only if ``get_configs`` is ``True``: indicates type of configuration file to fetch: 'candidate', 'running, or 'startup'. Default: 'candidate'.
        :type get_configs_db: str
        :param get_configs_max_files: Applicable only if ``get_configs`` is ``True``: The maximum number of files to save before rolling over. Default: 3.
        :type get_configs_max_files: int
        :param get_events: actions to include fetching and parsing events. *Default*: True
        :type get_events: bool
        :param get_tech_logs: actions to include fetching the tech_files. *Default*: False
        :type get_tech_logs: bool
        :param get_tech_log_max_files: Applicable only if ``get_tech_logs`` is ``True``: The maximum number of files to save before rolling over. Default: 20.
        :type get_tech_log_max_files: int
        :param send_cmds: actions to include sending commands (script). Default: False.
        :type send_cmds: bool
        :param send_cmds_script: Applicable only if ``send_cmds`` is ``True``: script contents. Default: None.
        :type send_cmds_script: list[str]
        :param set_tod: actions to include setting the time of day based on the computer's clock. Default: False.
        :type set_tod: bool
        :param set_tod_shift: Applicable only if ``set_tod`` is ``True``: a time shift (in hours) for cases where the computer is in a different timezone relative to the radios. Default: 0.
        :type set_tod_shift: float
        :param concurrency: if ``True``: access radios concurrently (multiple threads); else: sequentially (much slower, handy for debugging). Default: True.
        :type concurrency: bool
        :param concurrency_threads: Applicable if ``concurrency`` is ``True``: maximum number of concurrent threads (exceeding 10 may lead to trouble due to TG embedded CPU limitations). Default: 10.
        :type concurrency_threads: int
        :param dir_output_root: Root directory for all output files. Default: 'output'.
        :type dir_output_root: str
        :param dir_get_configs: Applicable if ``get_configs`` is ``True``: Directory for saving config files. Default: 'configs'.
        :type dir_get_configs: str
        :param dir_get_events: Applicable if ``get_events`` is ``True``: Directory for saving files containing events. Default: 'events'.
        :type dir_get_events: str
        :param dir_get_status: Applicable if ``get_status`` is ``True``: Directory for saving files containing parsed *get* telemetry. Default: 'status'.
        :type dir_get_status: str
        :param dir_get_status_xml: Applicable if ``get_status_xml`` is ``True``: Directory for saving files containing the raw XML response to **get** RPC. Default: 'status_xml'.
        :type dir_get_status_xml: str
        :param dir_get_tech_logs: Applicable if ``get_tech_logs`` is ``True``: Directory for saving tech_files. Default: 'tech_logs'.
        :type dir_get_tech_logs: str
        :param filename_cmdlog: Filename for logging commands sent to radios. Default: 'cmdlog.txt'.
        :type filename_cmdlog: str
        :param filename_errlog: Filename for logging errors. Default: 'errlog.txt'.
        :type filename_errlog: str
        :param debug_print: Run with additional output to console.
        :type debug_print: bool
        """

        #: Description of network and login credentials over which actions are taken.
        self.credentials: Credentials = credentials

        # Scope of action
        #: Execute actions on the local radio (whose IP addresses are provided in :attr:`credentials`).
        self.action_local: bool = action_local
        #: Execute actions on some/all remote radios (via tunnelling from local radio(s)).
        self.action_remote_cns: bool = action_remote_cns
        #: Applicable if :attr:`action_remote_cns`==``True``: List of remote radio names  for actions.
        #: If None or empty, remote radios are automatically discovered and actions are applied to them all.
        self.action_remote_cns_list: list[str] = action_remote_cns_list

        # Get status
        #: Actions to include fetching comprehensive telemetry (**get** RPC), parsing, and saving the parsed results.
        self.get_status: bool = get_status
        #: Applicable if :attr:`get_status`==``True``: Save the raw XML response from radio.
        self.get_status_xml: bool = get_status_xml
        #: Applicable  if :attr:`get_status_xml`==``True``: The maximum number of files to save before rolling over.
        self.get_status_xml_max_files: int = get_status_xml_max_files

        # Get configs
        #: Actions to include fetching configuration file of type :attr:`get_configs_db`.
        self.get_configs: bool = get_configs
        #: Applicable only if :attr:`get_configs`==``True``: indicates type of configuration file to fetch.
        self.get_configs_db: str = get_configs_db
        #: Applicable only if :attr:`get_configs`==``True``: The maximum number of files to save before rolling over.
        self.get_configs_max_files: int = get_configs_max_files

        #: Actions to include fetching and parsing events.
        self.get_events: bool = get_events

        #: Actions to include fetching the tech_files
        self.get_tech_logs: bool = get_tech_logs
        #: Applicable if :attr:`get_tech_logs`==``True``: The maximum number of files to save before rolling over.
        self.get_tech_log_max_files: int = get_tech_log_max_files

        #: Actions to include sending commands (script)
        self.send_cmds: bool = send_cmds
        #: Applicable if :attr:`send_cmds`==``True``: script contents.
        self.send_cmds_script: list[str] = send_cmds_script

        #: Actions to include setting the time of day based on the computer's clock.
        self.set_tod: bool = set_tod
        #: Applicable if :attr:`set_tod`==``True``: a time shift (in hours) for cases where the computer is in a different timezone relative to the radios.
        self.set_tod_shift: float = set_tod_shift

        # Path to output root directory.
        path_output_root = Path(dir_output_root)
        #: Path to directory for saving fetched configs.
        self.path_get_configs = path_output_root / dir_get_configs
        #: Path to directory where files containing events are saved.
        self.path_get_events = path_output_root / dir_get_events
        #: Path to directory for saving files containing parsed outputs of the **get** RPC.
        self.path_get_status = path_output_root / dir_get_status
        #: Path to directory for saving files containing raw XML outputs of the **get** RPC.
        self.path_get_status_xml = path_output_root / dir_get_status_xml
        #: Path to directory for saving tech_files.
        self.path_get_tech_logs = path_output_root / dir_get_tech_logs
        #: Path to file for logging commands sent to radios.
        self.path_cmdlog = path_output_root / filename_cmdlog
        #: Path to file for logging errors.
        self.path_errlog = path_output_root / filename_errlog

        # Concurrency
        #: If ``True``: access radios concurrently (multiple threads); else: sequentially.
        self.concurrency: bool = concurrency
        #: Applicable if :attr:`concurrency`==``True``: maximum number of concurrent threads.
        self.concurrency_threads: int = concurrency_threads

        # Internal & debug parameters
        #: Run with additional output to console
        self.debug_print: bool = debug_print
        self.lock_cmd_file: threading.Lock | None = None
        self.lock_err_file: threading.Lock | None = None
        self.lock_status_file: threading.Lock | None = None
        if self.concurrency:
            self.lock_cmd_file = threading.Lock()
            self.lock_err_file = threading.Lock()
            self.lock_status_file = threading.Lock()
        self.local_names: dict[Credential, str] = {}

    def _debug_print(self, print_str: str):
        """ Print debug message if :attr:`debug_print` is true.
        """
        if self.debug_print:
            msg: str = datetime.datetime.now().strftime('%H:%M:%S')
            msg += f" - {print_str}"
            print(msg)
        return None

    def do_actions(self, credential: Credential, remote_cn: str = '') -> TgCommander:
        """ Executed actions on a single radio, pointed to by ``credential`` (or one of its remote CNs named
            ``remote_cn``). Results, configuration-altering commands, and errors are written to files.

            :param credential: radio's IP addresses, username, password
            :type credential: Credential
            :param remote_cn: name of remote radio (optional)
            :type remote_cn: str
            :rtype: TgCommander
        """

        radio_id = _RadioID(credential.ip_addr, self.local_names.get(credential, ''), remote_cn)
        timestamp = get_timestamp_for_files()
        cmd = TgCommander(credential, remote_cn)
        if cmd.connect():
            self._debug_print(f"{radio_id} - identifying (fetching status)")
            cmd.get_and_parse()
            if cmd.local_name and not remote_cn:
                self.local_names[credential] = cmd.local_name
                radio_id.local = cmd.local_name
            if self.action_local or remote_cn:
                if self.get_status:
                    self._debug_print(f"{radio_id} - parsing/saving get status")
                    for section in cmd.get_sections:
                        if section[0] != '_':
                            path_file = self.path_get_status / f"{section}.csv"
                            iocsv.write_csv(cmd.get_parsed[section], path_file, threading_lock=self.lock_status_file)
                    if self.get_status_xml:
                        content = prettyprint_xml(cmd.get_xml)
                        path_file = self.path_get_status_xml / f"{radio_id.file_label()}_{timestamp}.xml"
                        iogen.file_write(content, path_file)
                        if self.get_status_xml_max_files:
                            enforce_max_files(path_file, self.get_configs_max_files, "*.xml")
                if self.get_events:
                    self._debug_print(f"{radio_id} - fetching events")
                    cmd.get_events_and_parse()
                    path_file = self.path_get_events / f"{radio_id.file_label()}.csv"
                    cmd.events_parsed.append_csv(path_file)
                if self.get_configs:
                    self._debug_print(f"{radio_id} - fetching configuration: {self.get_configs_db}")
                    cmd.get_config(self.get_configs_db)
                    glob_id = f"{self.get_configs_db}-{radio_id.file_label()}"
                    path_file = (self.path_get_configs / f"{glob_id}_{timestamp}.txt")
                    iogen.file_write(cmd.config_xml[self.get_configs_db], path_file)
                    # If required, delete older files
                    if self.get_configs_max_files:
                        enforce_max_files(self.path_get_configs, self.get_configs_max_files, f"{glob_id}*.txt")
                if self.send_cmds:
                    self._debug_print(f"{radio_id} - sending commands script")
                    cmd.cli_send(self.send_cmds_script)
                if self.set_tod:
                    self._debug_print(f"{radio_id} - setting time of day")
                    cmd.set_tod(self.set_tod_shift)
            cmd.disconnect()
        # Placing tech_log outside cmd loop as more robust (in case cmd fails)
        if self.get_tech_logs:
            self._debug_print(f"{radio_id} - getting tech_log")
            glob_id = f"tech_file_{radio_id.file_label()}"
            file_path = self.path_get_tech_logs / f"{glob_id}_{timestamp}.zip"
            tech_log = TechLog(credential, remote_cn)
            _ = tech_log.fetch(file_path)
            # If required, delete older files
            if self.get_tech_log_max_files:
                enforce_max_files(self.path_get_tech_logs, self.get_tech_log_max_files, f"{glob_id}*.zip")
        iocsv.write_csv([c.as_dict() for c in cmd.commands], self.path_cmdlog, threading_lock=self.lock_cmd_file)
        iocsv.write_csv([e.as_dict() for e in cmd.errors], self.path_errlog, threading_lock=self.lock_err_file)
        return cmd

    def batch_run(self):
        """ Batch-run :meth:`do_action` for multiple radios, either concurrently
            (if :attr:`concurrency`==`True``), or else sequentially.

            If :attr:`action_remote_cns` is ``True``, then :meth:`do_action` is automatically called for remote CNs:
            those listed in :attr:`action_remote_cns_list` (if populated), or otherwise all remote CNs (automatically
            discovered).
        """

        if self.concurrency:  # Batch run `do_action` concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency_threads) as executor:
                futures = [executor.submit(self.do_actions, credential, '') for credential in self.credentials]
                if self.action_remote_cns:
                    for future in concurrent.futures.as_completed(futures):
                        cmd: TgCommander = future.result()
                        if self.action_remote_cns_list:
                            cns = [cn for cn in cmd.remote_cns_names if cn in self.action_remote_cns_list]
                        else:
                            cns = cmd.remote_cns_names
                        futures.extend([executor.submit(self.do_actions, cmd.credential, cn) for cn in cns])
        else:  # Batch run `do_action` sequentially
            for credential in self.credentials:
                cmd: TgCommander = self.do_actions(credential)
                if self.action_remote_cns:
                    if self.action_remote_cns_list:
                        cns = [cn for cn in cmd.remote_cns_names if cn in self.action_remote_cns_list]
                    else:
                        cns = cmd.remote_cns_names
                    for cn in cns:
                        self.do_actions(credential, cn)
        return None

    def poll_run(self, iteration_period: datetime.timedelta = 0, num_iterations: int = 1):
        """ Run :meth:`batch_run` every ``iteration_period``, for a maximum of ``num_iterations``.

            :param iteration_period: Time in between iterations. If iteration executes for longer, then start next iteration immediately.
            :type iteration_period: datetime.timedelta
            :param num_iterations: The maximum number of iterations. Default: 1. A value of zero means 'forever'.
            :type num_iterations: int
        """
        iteration = 0
        while True:
            start_time = datetime.datetime.now()
            iteration += 1
            self._debug_print(f"*** Iteration {iteration} ***")
            self.batch_run()
            if num_iterations and iteration >= num_iterations:
                break
            elapsed_time = datetime.datetime.now() - start_time
            remaining_time = iteration_period - elapsed_time
            if remaining_time.seconds > 0:
                self._debug_print(f"Sleeping till next iteration, scheduled for {datetime.datetime.now()+remaining_time}")
                time.sleep(remaining_time.seconds)
