""" A Command line launcher for TgCrawl.
"""

import argparse
import datetime
import logging
from pathlib import Path
import sys
import tomllib

import tgtools
from tgtools import TgCrawler, Credentials

# Terminal text highlight colours
CBOLD, CEND, CRED = "\033[1m", "\033[0m", "\033[91m"

MODE_ONCE = 'once'
MODE_POLL = 'poll'


def parse_args():
    """ Auxiliary function for parsing command-line arguments (using the standard
        `argpass <https://docs.python.org/3/library/argparse.html>`_ library).
    """

    parser = argparse.ArgumentParser(prog='tgcrawl',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-m",
                        dest='mode',
                        help='''Mode of operation (default: %(default)s). One of:
     - once: perform actions one time; 
     - poll: perform actions repeatedly;''',
                        default='once')
    parser.add_argument("-n",
                        dest='network_filename',
                        help="Mandatory filename specifying the Network. "
                             "Default: '%(default)s'",
                        default='network.txt')
    parser.add_argument("-c",
                        dest='config_filename',
                        help="Optional configuration file for overriding default program parameters. "
                             "Default: '%(default)s'",
                        default='configs.toml')
    parser.add_argument("-s",
                        dest='silent',
                        help="Run in silent (rather than verbose) mode",
                        action='store_true')
    return parser.parse_args()


class CrawlLauncher:
    """ The main API for launching the TgCrawl from the command line.
    """

    def __init__(self, **kwargs):
        """ Collect all program attributes, including command line arguments, and parameters
            specified in some ancilliary configuration text files.
        """

        # Parse kwargs
        #: Mode of operation. Default: 'once'.
        self.mode: str = kwargs.get('mode', MODE_ONCE)
        #: Name of file describing the network over which TgCrawl will 'crawl'. Default: 'network.txt'.
        self.network_filename: str = kwargs.get('network_filename', 'network.txt')
        #: Name of TOML file overriding default running parameters. Default: 'configs.toml'.
        self.config_filename: str = kwargs.get('config_filename', 'configs.toml')
        #: Run in silent mode. Default: False.
        self.silent: bool = kwargs.get('silent', False)
        #: Run in interactive mode. Default: True.
        self.interactive: bool = kwargs.get('interactve', True)

        # Default values for configs
        #: Action IP-accessible radios (whose IP addresses are denoted in :attr:`network_filename`).
        #: Default: True (but may be overridden by :attr:`config_filename`).
        self.action_local: bool = True
        #: Action IP-less radios (remote Client Nodes without a network-accessible IP address).
        #: Default: True (but may be overridden by :attr:`config_filename`).
        self.action_remote_cns: bool = True
        #: Applicable if :attr:`action_remote_cns` is ``True``: List of remote radio names for actions.
        #: If None: remote radios are automatically discovered and actions are applied to them all.
        #: Default: None (but may be overridden by :attr:`config_filename`).
        self.action_remote_cns_list: list | None = None
        #: If ``True``: access radios concurrently (multiple threads); else: sequentially.
        #: Default: True (but may be overridden by :attr:`config_filename`).
        self.concurrency: bool = True
        #: Applicable if :attr:`concurrency` is ``True``: maximum number of concurrent threads.
        #: Default: 10 (but may be overridden by :attr:`config_filename`).
        self.concurrency_threads: int = 10
        #: Applicable if :attr:`mode` is 'poll': Number of iterations (value of zero means: forever).
        #: Default: 0 (but may be overridden by :attr:`config_filename`).
        self.num_iterations: int = 0
        #: Applicable if :attr:`mode` is 'poll': Period of iterations.
        #: Default: 5 minutes (but may be overridden by :attr:`config_filename`).
        self.iteration_period = datetime.timedelta(minutes=5)
        #: Actions to include fetching configuration from radio.
        #: Default: False (but may be overridden by :attr:`config_filename`).
        self.get_configs: bool = False
        #: Applicable if :attr:`get_configs` is ``True``: type of configuration to fetch.
        #: Default: 'startup' (but may be overridden by :attr:`config_filename`).
        self.get_configs_db: str = 'startup'
        #: Applicable if :attr:`get_configs` is ``True``: maximum number of files to save before rolling over.
        #: Default: 3 (but may be overridden by :attr:`config_filename`).
        self.get_configs_max_files: int = 3
        #: Actions to include fetching events from radio.
        #: Default: True (but may be overridden by :attr:`config_filename`).
        self.get_events: bool = True
        #: Actions to include fetching comprehensive telemetry from radio, parsing and saving.
        #: Default: True (but may be overridden by :attr:`config_filename`).
        self.get_status: bool = True
        #: Applicable if :attr:`get_status` is ``True``: Save the raw XML response from radio.
        #: Default: False (but may be overridden by :attr:`config_filename`).
        self.get_status_xml: bool = False
        #: Applicable if :attr:`get_status` is ``True``: maximum number of files to save before rolling over.
        #: Default: 3 (but may be overridden by :attr:`config_filename`).
        self.get_status_xml_max_files: int = 3
        #: Actions to include fetching the tech_log from radio.
        #: Default: False (but may be overridden by :attr:`config_filename`).
        self.get_tech_logs: bool = False
        #: Applicable if :attr:`get_tech_logs` is ``True``: maximum number of files to save before rolling over.
        #: Default: 10 (but may be overridden by :attr:`config_filename`).
        self.get_tech_log_max_files: int = 10
        #: Actions to include sending a command script to radio.
        #: Default: False (but may be overridden by :attr:`config_filename`).
        self.send_cmds: bool = False
        #: Applicable if :attr:`send_cmds` is ``True``: name of file containing the script.
        #: Default: 'script.txt' (but may be overridden by :attr:`config_filename`).
        self.send_cmds_script_filename: str = 'script.txt'
        #: Actions to include setting the radio's date and time based on the computer's clock.
        #: Default: False (but may be overridden by :attr:`config_filename`).
        self.set_tod: bool = False
        #: Applicable if :attr:`set_tod` is ``True``: a time shift (in hours) for cases where the computer
        #: is in a different timezone relative to the radios.
        #: Default: 0 (but may be overridden by :attr:`config_filename`).
        self.set_tod_shift: float = 0
        #: Path to output root directory.
        #: Default: 'output' (but may be overridden by :attr:`config_filename`).
        self.dir_output_root: str = 'output'
        #: Directory to save config files fetched from radios.
        #: Default: 'configs' (but may be overridden by :attr:`config_filename`).
        self.dir_get_configs: str = 'configs'
        #: Directory to save events files fetched from radios.
        #: Default: 'events' (but may be overridden by :attr:`config_filename`).
        self.dir_get_events: str = 'events'
        #: Directory to save parsed status (telemetry) files fetched from radios.
        #: Default: 'get_status' (but may be overridden by :attr:`config_filename`).
        self.dir_get_status: str = 'get_status'
        #: Directory to save raw XML telemetry files fetched from radios.
        #: Default: 'get_status_xml' (but may be overridden by :attr:`config_filename`).
        self.dir_get_status_xml: str = 'get_status_xml'
        #: Directory to save tech_log files fetched from radios.
        #: Default: 'configs' (but may be overridden by :attr:`config_filename`).
        self.dir_get_tech_logs: str = 'tech_logs'
        self.filename_cmdlog: str = 'cmds_log.csv'
        self.filename_errlog: str = 'errs_log.csv'
        #: Run with additional output to console
        #: Default: True (but may be overridden by :attr:`config_filename`).
        self.debug_print: bool = True
        #: Script commands as read from :attr:`send_cmds_script_filename`. Defaults to an empty list.
        self.send_script_cmds: list[str] = []

        #: Console logger for this class.
        self.logger = logging.getLogger('tgtools.tgcrawl')
        if not self.silent:
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.WARNING)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

        # Read parameters from TOML configuration file
        self.read_toml_config()

        # Get credentials
        #: Network credentials, as read from :meth:`get_credentials`.
        self.credentials: Credentials = self.get_credentials()

    def read_toml_config(self):
        """ Get program configurations from TOML file :attr:`configs_filename`,
            and attempt to override the default running parameters. Automatically called by :meth:`__init__`.
        """
        filename = Path(self.config_filename)
        try:
            with filename.open('rb') as fp:
                t = tomllib.load(fp)
        except FileNotFoundError:
            self.logger.warning(f"Using default program parameters: file '{filename.absolute()}' not found")
            input('Press a key to continue... ')
            return None
        except tomllib.TOMLDecodeError as e:
            self.logger.warning(
                f"Using default program parameters: invalid TOML syntax in '{filename.absolute()}':\n\t{e}")
            input('Press a key to continue... ')
            return None

        self.action_local = t.get('action_scope', {}).get('action_local', self.action_local)
        self.action_remote_cns = t.get('action_scope', {}).get('action_remote_cns', self.action_remote_cns)
        self.action_remote_cns_list = t.get('action_scope', {}).get('action_remote_cns_list',
                                                                    self.action_remote_cns_list)
        self.concurrency = t.get('concurrency', {}).get('concurrency', self.concurrency)
        self.concurrency_threads = t.get('concurrency', {}).get('concurrency_threads', self.concurrency_threads)
        self.num_iterations = t.get('poller', {}).get('iterations', self.num_iterations)
        try:
            period = t['poller']['iteration_period']
        except KeyError:
            pass
        else:
            try:
                hours, mins, secs = str(period).split(':')
                self.iteration_period = datetime.timedelta(hours=int(hours), minutes=int(mins),
                                                           seconds=int(secs))
            except ValueError:
                self.logger.warning(f"Unable to parse '{period}' in {filename} for 'iteration_period'")
        self.get_configs = t.get('get_configs', {}).get('get_configs', self.get_configs)
        self.get_configs_db = t.get('get_configs', {}).get('get_configs_db', self.get_configs_db)
        self.get_configs_max_files = t.get('get_configs', {}).get('get_configs_max_files',
                                                                  self.get_configs_max_files)
        self.get_events = t.get('get_events', {}).get('get_events', self.get_events)
        self.get_status = t.get('get_status', {}).get('get_status', self.get_status)
        self.get_status_xml = t.get('get_status', {}).get('get_status_xml', self.get_status_xml)
        self.get_status_xml_max_files = t.get('get_status', {}).get('get_status_xml_max_files',
                                                                    self.get_status_xml_max_files)
        self.get_tech_logs = t.get('get_tech_logs', {}).get('get_tech_logs', self.get_tech_logs)
        self.get_tech_log_max_files = t.get('get_tech_logs', {}).get('get_tech_log_max_files',
                                                                     self.get_tech_log_max_files)
        self.send_cmds = t.get('send_script', {}).get('send_cmds', self.send_cmds)
        self.send_cmds_script_filename = t.get('send_script', {}).get('send_cmds_script_filename',
                                                                      self.send_cmds_script_filename)
        self.set_tod = t.get('set_tod', {}).get('set_tod', self.set_tod)
        self.set_tod_shift = t.get('set_tod', {}).get('set_tod_shift', self.set_tod_shift)
        self.dir_output_root = t.get('output_files', {}).get('dir_output_root', self.dir_output_root)
        self.dir_get_configs = t.get('output_files', {}).get('dir_get_configs', self.dir_get_configs)
        self.dir_get_events = t.get('output_files', {}).get('dir_get_events', self.dir_get_events)
        self.dir_get_status = t.get('output_files', {}).get('dir_get_status', self.dir_get_status)
        self.dir_get_status_xml = t.get('output_files', {}).get('dir_get_status_xml', self.dir_get_status_xml)
        self.dir_get_tech_logs = t.get('output_files', {}).get('dir_get_tech_logs', self.dir_get_tech_logs)
        self.filename_cmdlog = t.get('output_files', {}).get('filename_cmdlog', self.filename_cmdlog)
        self.filename_errlog = t.get('output_files', {}).get('filename_errlog', self.filename_errlog)
        self.debug_print = t.get('debug', {}).get('debug_print', self.debug_print)

        self.logger.info(f"Updated program parameters from file '{filename.absolute()}'")
        return

    def get_credentials(self) -> Credentials:
        """ Read the network description (IP addresses, log-in credentials) from file :attr:`network_filename`.
            Automatically called by :meth:`__init__`.
        """
        filename = Path(self.network_filename)
        try:
            credentials = Credentials.from_file(filename.absolute())
        except FileNotFoundError as e:
            self.logger.error(f"{CRED}No network credentials: {e}{CEND}")
            return []
        if len(credentials) == 0:
            self.logger.error(
                f"{CRED}Unable to parse any network credentials from '{filename.absolute()}'{CEND}")
            return []
        # Success
        msg = f"Network:\tParsed credentials from file: '{filename.absolute()}'\n"
        msg += f"\t\t\t\t{len(credentials)} IP addresses (in range: {credentials[0].ip_addr} - {credentials[-1].ip_addr})"
        self.logger.info(msg)
        return credentials

    def read_script_file(self) -> list[str]:
        """ Read script file :attr:`send_cmds_script_filename`.
            Automatically called by :meth:`validate`.

            :rtype: list[str]
        """
        path_script = Path(self.send_cmds_script_filename)
        try:
            text_from_filenm = path_script.read_text()
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"{CRED}Error reading script file {path_script}:{CEND} {e}")
            return []
        script_commands = [line.strip() for line in text_from_filenm.split('\n') if line]
        if not script_commands:
            self.logger.error(f"{CRED}No script content in '{path_script}'{CEND}")
            return []
        else:
            return script_commands

    def validate(self) -> bool:
        """ Validate coherency of all attributes:

             * Action includes at least some radios (local and/or remote).
             * The network descriptor file is read and parsed
             * If required, read :attr:`send_cmds_script_filename` into :attr:`send_script_cmds`.

            Automatically run by :meth:`run`.

            :rtype: bool
        """
        success = True
        # Validate scope of action
        if not self.action_local and not self.action_remote_cns:
            self.logger.error(
                f"{CRED}Action scope does not include any radios{CEND} (set 'action_local' and/or 'action_remote_cns' to True)")
            success = False
        if not self.credentials:
            success = False
        # Validate script file
        if self.send_cmds:
            self.send_script_cmds = self.read_script_file()
            if not self.send_script_cmds:
                success = False
        return success

    def print_summary(self):
        """ Print summary of pending action. Automatically called by :meth:`run`.
        """
        if self.mode == MODE_POLL:
            num_iterations = self.num_iterations if self.num_iterations else 'forever'
            self.logger.info(f"\t\tNumber of iterations: {num_iterations}")
            self.logger.info(f"\t\tIteration period: {self.iteration_period}\n")
        self.logger.info(f"Summary Actions:")
        if self.get_configs:
            msg = f"\t\t- {CBOLD}get_configs{CEND}: Fetch {CBOLD}{self.get_configs_db}{CEND} config"
            msg += f" (keep only {self.get_configs_max_files} most recent files)"
            self.logger.info(msg)
        if self.get_events:
            self.logger.info(f"\t\t- {CBOLD}get_events{CEND}: Fetch events")
        if self.get_status:
            self.logger.info(f"\t\t- {CBOLD}get_status{CEND}: Fetch status and save parsed")
        if self.get_status_xml:
            self.logger.info(f"\t\t- {CBOLD}get_status_xml{CEND}: Fetch status and save raw XML")
        if self.get_tech_logs:
            msg = f"\t\t- {CBOLD}get_tech_logs{CEND}: Fetch tech_files "
            msg += f"(keep only {self.get_tech_log_max_files} most recent files)"
            self.logger.info(msg)
        if self.send_cmds:
            self.logger.info(f"\t\t- {CBOLD}send_cmds{CEND}:")
            for command in self.send_script_cmds:
                self.logger.info(f"\t\t\t> {command}")
        if self.set_tod:
            self.logger.info(
                f"\t\t- {CBOLD}set_tod{CEND}: Set radios' date/time, based on OS clock (+{self.set_tod_shift} hours)")
        self.logger.info(f"Actions Scope:")
        if self.action_local:
            self.logger.info(f"\t\t{CBOLD}Including{CEND}: Local radios (indicated IP addresses)")
        else:
            self.logger.info(f"\t\tExcluding: Local radios (indicated IP addresses)")
        if self.action_remote_cns:
            self.logger.info(f"\t\t{CBOLD}Including{CEND}: Remote radios (by tunneling):")
            if self.action_remote_cns_list:
                for item in self.action_remote_cns_list:
                    self.logger.info(f"\t\t\t> {item}")
            else:
                self.logger.info(f"\t\t\t\t> {CBOLD}All{CEND} remote radios")
        else:
            self.logger.info(f"\t\texcluding: Remote radios")
        self.logger.info(f"Output Dir:\t{self.dir_output_root}")
        return None

    def run(self):
        """ Validate parameters, print a summary of pending actions, and run the TgCrawl batch engine
            (as determined by :attr:`mode`: either once, or repeatedly (polling).
        """

        if not self.validate():
            self.logger.error(f"Unable to run - terminating program")
            return

        if self.mode == MODE_ONCE:
            print(f"\n{CBOLD}Running {MODE_ONCE.capitalize()}{CEND}\n")
        elif self.mode == MODE_POLL:
            print(f"\n{CBOLD}Running in {MODE_POLL.capitalize()} mode{CEND}")
        else:
            self.logger.error(f"Unknown mode '{self.mode}' - Quitting")
            return

        # Print summary
        self.print_summary()

        if self.interactive:
            input('Press any key to start...')

        crawler = TgCrawler(self.credentials,
                            action_local=self.action_local,
                            action_remote_cns=self.action_remote_cns,
                            action_remote_cns_list=self.action_remote_cns_list,
                            get_status=self.get_status,
                            get_status_xml=self.get_status_xml,
                            get_status_xml_max_files=self.get_status_xml_max_files,
                            get_configs=self.get_configs,
                            get_configs_db=self.get_configs_db,
                            get_configs_max_files=self.get_configs_max_files,
                            get_events=self.get_events,
                            get_tech_logs=self.get_tech_logs,
                            get_tech_log_max_files=self.get_tech_log_max_files,
                            send_cmds=self.send_cmds,
                            send_cmds_script=self.send_script_cmds,
                            set_tod=self.set_tod,
                            set_tod_shift=self.set_tod_shift,
                            concurrency=self.concurrency,
                            concurrency_threads=self.concurrency_threads,
                            dir_output_root=self.dir_output_root,
                            dir_get_configs=self.dir_get_configs,
                            dir_get_events=self.dir_get_events,
                            dir_get_status=self.dir_get_status,
                            dir_get_status_xml=self.dir_get_status_xml,
                            dir_get_tech_logs=self.dir_get_tech_logs,
                            filename_cmdlog=self.filename_cmdlog,
                            filename_errlog=self.filename_errlog,
                            debug_print=self.debug_print,
                            )

        start_time = datetime.datetime.now()
        if self.mode == MODE_ONCE:
            crawler.batch_run()
        elif self.mode == MODE_POLL:
            crawler.poll_run(self.iteration_period, self.num_iterations)
        else:
            pass
        elapsed_time = datetime.datetime.now() - start_time
        self.logger.info(f"Elapsed time: {elapsed_time}")


def main():
    """ Interpret command line and launch appropriate program
     """
    args = parse_args()
    # Welcome message
    print(f"\n\n{CBOLD}TgCrawl{CEND} (of TgTools ver {tgtools.__version__})", end='')
    if not args.silent:
        print(f": Crawl the network to mine telemetry from Siklu by Ceragon TG radios.")
        print(f"{tgtools.__author__}, 2024. Documentation: https://tg.readthedocs.io.\n")
    else:
        print('\n')

    # Invoke appropriate mode
    launcher = CrawlLauncher(**vars(args))
    launcher.run()
    print(f"\nProgram terminated")



if __name__ == '__main__':
    main()
