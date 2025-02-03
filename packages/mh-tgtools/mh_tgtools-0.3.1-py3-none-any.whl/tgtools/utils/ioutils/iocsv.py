from collections.abc import Sequence
import csv
from pathlib import Path
import threading

from tgtools.utils.ioutils.iogen import confirm_exists


def read_csv(file_path: Path) -> list[dict]:
    """ Read csv file into list of dicts.

        :param file_path: Path to input csv file.
        :type file_path: pathlib.Path
        :rtype: list[dict]
    """

    data = []
    if confirm_exists(file_path):
        with open(file_path, 'rt', newline='') as csvfile:
            try:
                reader = csv.DictReader(csvfile)
            except csv.Error as e:
                print(f"Unable to csv-parse: {file_path} - {e}")
            else:
                data = list(reader)
    else:
        print(f"Unable to find file: {file_path}")
    return data


def write_csv(records: dict | Sequence[dict],
              path_file: Path,
              append: bool = True,
              fieldnames: Sequence[str] | None = None,
              threading_lock: threading.Lock | None = None):
    """ Append a dict (or sequence of dicts) to csv file. It is assumed all dict keys are identical.
        If the output csv file does not exist, it is created, and the dict keys (fieldnames) written as the first line.
        Each subsequent line corresponds to the values of each dict.
        This method can be made thread-safe by providing a threading lock.

        :param records: A dict (or sequence of dicts).
        :type records: dict | collections.abc.Sequence[dict]
        :param path_file: Path to output csv file.
        :type path_file: pathlib.Path
        :param append: Indicates whether to append to file if it exists (default), or overwrite file.
        :type append: bool
        :param fieldnames: Optional: csv fieldnames (if None, automatically derived from first record in ``records``)
        :type fieldnames: collection.abc.Sequence[str]
        :param threading_lock: Optional threading lock for thread-safe operation
        :type threading_lock: threading.Lock
    """

    if records:
        # if a single record (dict), convert to sequence of dicts (with single element)
        if not isinstance(records, Sequence):
            records = (records,)
        # Lock file access (make thread-safe)
        if threading_lock:
            threading_lock.acquire()
        # If file doesn't exist, create it (and optionally derive field names)
        if append and confirm_exists(path_file):
            write_header = False
        else:
            confirm_exists(path_file, create=True)
            write_header = True
        # Derive filed names if unknown
        if not fieldnames:
            fieldnames = records[0].keys()
        # File write mode
        mode = 'at' if append else 'wt'
        # Write file
        try:
            with open(path_file, mode, newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerows(records)
        except (OSError, csv.Error) as e:
            print(f"file_append_csv - aborting due to error: '{e}'")
        # Release thread lock
        if threading_lock:
            threading_lock.release()
    return None
