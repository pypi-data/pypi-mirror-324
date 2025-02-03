import logging
from pathlib import Path


def logger_by_label(label: str, *,
                    log_enable: bool = True,
                    log_dir: Path | str = 'internal_logs',
                    log_level_console: int = logging.ERROR,
                    log_level_file: int = logging.INFO,
                    ) -> logging.Logger:
    """ Create a logger with name ``label``, add two handlers (console and file), and set level each.

        :param label: Name of logger (and of output log file) - typically IP address
        :type label: str
        :param log_enable: Enable logger if ``True`` (default),
                           else disable the logger
        :type log_enable: bool
        :param log_dir: Path (or name) of directory for log file (default: 'internal_logs')
        :type log_dir: pathlib.Path | str
        :param log_level_console: logging level for console (default: logging.ERROR)
        :type log_level_console: int
        :param log_level_file: logging level for file (default: logging.INFO)
        :type log_level_file: int
        :return: Created logger
        :rtype: logging.Logger

    """

    # Create logger
    logger = logging.getLogger(label)

    # If logging disabled, return a disabled logger
    if not log_enable:
        logger.setLevel(logging.CRITICAL + 1)
        return logger
    # If the logger already exists, return it
    elif logger.hasHandlers():
        return logger
    else:  # configure the newly created logger
        # Set level to the minimum of the console handler and file handler
        logger.setLevel(min(log_level_console, log_level_file))
        # Create log_dir if it doesn't exist
        path_log_dir = Path(log_dir)
        path_log_dir.mkdir(parents=True, exist_ok=True)
        # Create logger file handler
        path_filename = path_log_dir / f"{label}.log"
        fh = logging.FileHandler(path_filename)
        # Create logger console handler
        ch = logging.StreamHandler()
        # Set levels for each handler
        fh.setLevel(log_level_file)
        ch.setLevel(log_level_console)
        # Set Formatter:
        formatter = logging.Formatter("%(asctime)s %(module)s:%(funcName)10s - %(levelname)7s - %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # Add handlers to logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger
