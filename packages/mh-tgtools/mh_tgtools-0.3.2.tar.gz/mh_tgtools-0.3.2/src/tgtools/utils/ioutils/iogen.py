import enum
from pathlib import Path
import threading

from tgtools.consts import DEFAULT_FILE_TIMESTAMP_LEN
from tgtools.utils.timefunc import timestamp_for_files_to_time


class FileType(enum.StrEnum):
    """ String enumeration for 'file' and 'dir'.
    """
    file = 'file'
    dir = 'dir'


def confirm_exists(path_file: Path, filetype: FileType | str = FileType.file, create: bool = False) -> bool:
    """ Check if ``path_file`` exists. If it does, and it is of type ``filetype``, return ``True``.
        If file exists, but is of the wrong filetype, return ``False``.

        If the file doesn't exist, then:
          * If ``create`` is ``True``, then create the file and return ``True``;
          * Otherwise, return ``False``.

        :param path_file: Path to file.
        :type path_file: pathlib.Path
        :param filetype: Type of file.
        :type filetype: FileType
        :param create: Indicates whether to create a file that doesn't already exist.
        :type create: bool
        :rtype: bool
    """
    assert filetype in FileType

    if path_file.exists():
        if path_file.is_file() and filetype == FileType.file:
            return True
        elif path_file.is_dir() and filetype == FileType.dir:
            return True
        else:
            return False
    elif create:  # File does not exist and need to create it
        if filetype == FileType.file:
            path_file.parent.mkdir(parents=True, exist_ok=True)
            path_file.touch(exist_ok=True)
            return True
        elif filetype == FileType.dir:
            path_file.mkdir(parents=True)
            return True
        else:
            return False
    else:
        return False


def enforce_max_files(path_dir: Path, max_number_files: int, glob_pattern: str) -> int:
    """ If the number of files matching ``glob_pattern`` in ``path_dir`` exceed ``max_number_files``,
        then delete the oldest surplus files. It is assumed that the last characters of the files stem is a timestamp.

        :param path_dir: directory path
        :type path_dir: pathlib.Path
        :param max_number_files: maximum number of files permitted in directory
        :type max_number_files: int
        :param glob_pattern: Glob pattern for files
        :type glob_pattern: str
        :return: The number of files deleted
        :rtype: int
    """
    counter = 0
    files = [file for file in path_dir.glob(glob_pattern)]
    if len(files) > max_number_files:
        files.sort(reverse=True, key=lambda x: timestamp_for_files_to_time(x.stem[-DEFAULT_FILE_TIMESTAMP_LEN:]))
        while len(files) > max_number_files:
            delete_candidate = files.pop()
            delete_candidate.unlink()
            counter += 1
    return counter


def file_write(content: str,
               path_file: Path,
               threading_lock: threading.Lock | None = None) -> bool:
    """  Write ``content`` to text file (overwrite file if it exists).
         This function can be made is thread-safe by providing a threading lock.

         :param content: Text to write to output text file.
         :type content: str
         :param path_file: Path to output filename.
         :type path_file: pathlib.Path
         :param threading_lock: Optional threading lock for thread-safe operation.
         :type threading_lock: threading.Lock
         :return: Indication if writing is successful.
         :rtype: bool
     """
    success: bool = False
    if content:
        # Lock file access (make thread-safe)
        if threading_lock:
            threading_lock.acquire()
        # If file doesn't exist, create it
        if confirm_exists(path_file, create=True):
            try:
                path_file.write_text(content, newline='\n')
            except OSError as e:
                print(f"file_write - aborting due to error: '{e}'")
            else:
                success = True
            finally:
                if threading_lock:
                    threading_lock.release()
    return success
