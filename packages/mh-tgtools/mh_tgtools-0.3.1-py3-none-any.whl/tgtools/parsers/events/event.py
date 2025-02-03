import enum
from pathlib import Path
import re
import threading
import typing

from tgtools.utils.errlog import Err
import tgtools.utils.ioutils.iocsv as iocsv
from tgtools.utils.timefunc import seconds_to_uptime


class Token(enum.StrEnum):
    index = 'index'
    timestamp = 'timestamp'
    id = 'id'
    cat = 'category'
    dev = 'device'
    type = 'type'
    msg = 'msg'
    power = 'power_event'
    lname = 'link_name'
    levent = 'link_event'
    up_for = 'up_for'
    cause = 'cause'


class Event(dict):
    """ Representation  for a single event fetched from a TG radio, including parsing. This class is an extension
        of `dict <https://docs.python.org/3/library/stdtypes.html#dict>`_.

        An instance can be initialised:
         * from a string (refer to :meth:`from_xml`), or
         * from a dictionary (refer to :meth:`from_dict`).

    """

    _RE_EVENT = re.compile(
        r"^(?P<timestamp>.+?),\s*(?P<id>\d+),\s*(?P<category>\w+),\s*(?P<device>\w+),\s*(?P<type>\w+),\s*(?P<msg>.+)")
    _RE_LINK_UP = re.compile(r"^(?P<linkname>[-a-zA-Z0-9]{1,8}) link up")
    _RE_LINK_DOWN = re.compile(r"^(?P<linkname>[-a-zA-Z0-9]{1,8}) link down")
    _RE_WAS_UP_1 = re.compile(r"\(was up for (?P<uptime>\d+:\d+:\d+:\d+)\)")
    _RE_WAS_UP_2 = re.compile(r"\(was up for (?P<uptime>\d+) seconds")  # Older SW versions
    _RE_CAUSE = re.compile(r"Cause: (?P<cause>\w+);")
    _RE_POWER = re.compile(r"^Power")

    #: The principal parsing tokens.
    core_tokens = tuple(str(token) for token in Token)
    _core_dict = {token: '' for token in core_tokens}

    def __init__(self):
        """
            :meta private:
        """
        super().__init__()
        self._prefix_dict: dict[str, str] = {}
        #: List of parsing errors
        self.errors: list[Err] = []

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()


    def __eq__(self, other):
        """ Defines equality between two class instances, based on unique, fixed fields.
        """
        value1 = ''.join(self[token] for token in (Token.id, Token.cat, Token.dev, Token.type, Token.msg))
        value2 = ''.join(other[token] for token in (Token.id, Token.cat, Token.dev, Token.type, Token.msg))
        return value1 == value2


    @property
    def prefix_dict(self):
        """ An optional arbitrtary dictionary whose key/value pairs are prepend do the parsed event.
        """
        return self._prefix_dict

    @prefix_dict.setter
    def prefix_dict(self, prefix_dict: dict[str, str] | None = None):
        if prefix_dict:
            if any(key in prefix_dict for key in self.core_tokens):
                raise Exception(f"One or more of the keys in prefix_tokens duplicates the core Event tokens")
            else:
                self._prefix_dict = prefix_dict
        else:
            self._prefix_dict = {}

    @classmethod
    def from_dict(cls, source_dict: dict) -> typing.Self:
        """ Create a class instance from a dictionary.

            :param source_dict: Source dictionary
            :type source_dict: dict
            :return: A class instance
            """
        event = cls()
        event.update(source_dict)
        return event

    @classmethod
    def from_xml(cls, event_string: str, event_index: int | None = None,
                 prefix_dict: dict[str, str] | None = None) -> typing.Self:
        """ Return a class instance from an event string, for example::

            "2024-10-13 23:31:03.784, 1388,SYSTEM, LOCAL,  RADIO,   cn1 link up; Local/Remote Sector: 3/1; Tx/Rx Beam: 32/32; Tx/Rx Az: 20/20 deg; Tx/Rx El: -10/-10 deg"

            The event string is parsed, and prepended by additional optional tokens:

             * ``prefix_dict``: an arbitrary dictionary, typically identifying the source radio and computer's timestamp. Note: the keys of this dictionary must not replicate any tokens in :attr:`core_tokens`.
             * ``event_index``: an integer designating the event number as returned by the **get-events** RPC.

            :param event_string: an event string - example shown above.
            :type event_string: str
            :param event_index: an optional integer designating the event number as returned by the **get-events** RPC (default: None).
            :type event_index: int | None
            :param prefix_dict: an optional arbitrary dictionary, prepending the parsed event (default None).
            :type prefix_dict: dict | None
            :return: a class instance.
        """
        event = cls()
        if prefix_dict:
            event.prefix_dict = prefix_dict
        event.parse_xml(event_string, event_index)
        return event

    def parse_xml(self, event_string: str, event_index: int | None = None):
        """ Tokenise a string representing a TG event.
            The parsing tokens used are listed in :attr:`core_tokens`.
            This method is not typically  called directly, but rather implicitly by calling :meth:`from_xml`.

            Parsing errors appended to :attr:`errors`.

            :param event_string: an event string.
            :type event_string: str
            :param event_index: an optional integer designating the event number as returned by the **get-events** RPC (default: None).
            :type event_index: int | None
        """
        self.errors = []
        if m := re.match(self._RE_EVENT, event_string):
            self.update(self._prefix_dict)
            self.update(self._core_dict)
            if event_index is not None:
                self[Token.index] = event_index
            self[Token.timestamp] = ' ' + m['timestamp']
            self[Token.id] = m['id']
            self[Token.cat] = m['category']
            self[Token.dev] = m['device']
            self[Token.type] = m['type']
            self[Token.msg] = m['msg']
            if m := re.match(self._RE_LINK_UP, self[Token.msg]):
                self[Token.lname] = m['linkname']
                self[Token.levent] = 'link up'
            elif m := re.match(self._RE_LINK_DOWN, self[Token.msg]):
                self[Token.lname] = m['linkname']
                self[Token.levent] = 'link down'
                if m := re.search(self._RE_CAUSE, self[Token.msg]):
                    self[Token.cause] = m['cause']
                if m := re.search(self._RE_WAS_UP_1, self[Token.msg]):
                    self[Token.up_for] = m['uptime']
                elif m := re.search(self._RE_WAS_UP_2, self[Token.msg]):
                    self[Token.up_for] = seconds_to_uptime(int(m['uptime']))
            elif _ := re.match(self._RE_POWER, self[Token.msg]):
                self[Token.power] = 'Y'
            else:
                pass  # future parsing
        else:
            self.errors.append(Err(f"{type(self).__name__}()", f"unable to parse event: '{event_string}'"))
        return None
    """
    def append_csv(self, path_file: Path, threading_lock: threading.Lock | None = None) -> bool:
        # Append parsed event to a csv file.

            :param path_file: Path of csv file.
            :type path_file: Path
            :param threading_lock: Threading lock, if desired to ensure method is thread-safe (Defaults to None).
            :type threading_lock:  threading.Lock | None
            :return: Indication if successful.
            :rtype: bool
        #
        if len(self):
            return iocsv.write_csv(self, path_file, threading_lock=threading_lock)
        else:
            return False
    """

if __name__ == "__main__":
    test_str1 = r'2024-10-13 23:31:03.784, 1388,SYSTEM, LOCAL,  RADIO,   498381 link up; Local/Remote Sector: 3/1; Tx/Rx Beam: 32/32; Tx/Rx Az: 20/20 deg; Tx/Rx El: -10/-10 deg'
    test_str2 = r'2024-10-13 23:31:03.784, 1388,SYSTEM, LOCAL,  RADIO,   498381 link up; Local/Remote Sector: 3/1; Tx/Rx Beam: 32/32; Tx/Rx Az: 20/20 deg; Tx/Rx El: -10/-11 deg'
    event_string = "2024-10-13 23:31:03.784, 1388,SYSTEM, LOCAL,  RADIO,   cn1 link up; Local/Remote Sector: 3/1; Tx/Rx Beam: 32/32; Tx/Rx Az: 20/20 deg; Tx/Rx El: -10/-10 deg"
    prefix_fields = {'route': '192.168.0.1', 'sampled': '2024-10-23 17:09:00'}
    event = Event.from_xml(event_string, event_index=1, prefix_dict=prefix_fields)
    print(event)
