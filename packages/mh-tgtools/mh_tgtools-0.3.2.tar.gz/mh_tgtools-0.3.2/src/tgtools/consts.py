import datetime
import re

NS = {
    "snmp": "urn:ietf:params:xml:ns:yang:ietf-snmp",
    "events": "http://siklu.com/yang/tg/events",
    "interfaces": "http://siklu.com/yang/tg/interfaces",
    "inventory": "http://siklu.com/yang/tg/inventory",
    "ip": "http://siklu.com/yang/tg/ip",
    "radioc": "http://siklu.com/yang/tg/radio",
    "radiod": "http://siklu.com/yang/tg/radio/dn",
    "system": "http://siklu.com/yang/tg/system",
    "bridges": "http://siklu.com/yang/tg/user-bridge",
    "users": "http://siklu.com/yang/tg/user-management",
}


NETCONF_SSH_TIMEOUT = 2.5                           #: Socket timeout for NETCONF session.


DEFAULT_DATETIME = datetime.datetime(1970, 1, 1)

MAX_NUM_GET_EVENTS_RPC = 200                        #: Maximum number of events retrievable via the get-events RPC.
LEN_RESP_DISPL_TRUNC = 100                          #: Maximum number of chars for displaying a response to a command

DEFAULT_FILE_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"     #: Default format for timestamp in filename.
DEFAULT_FILE_TIMESTAMP_LEN = 15                     #: Length of `DEFAULT_FILE_TIMESTAMP_FORMAT`.

HTTP_CONNECT_TIMEOUT = 5
HTTP_READ_TIMEOUT = 60
HTTP_GET_CHUNK_SIZE = 10000

# Regular expressions

RE_EVENT = re.compile(
    r"^(?P<timestamp>.+?),\s*(?P<label>\d+),\s*(?P<category>\w+),\s*(?P<device>\w+),\s*(?P<type>\w+),\s*(?P<msg>.+)")


RE_RADIO_NAME = re.compile(r'[-a-zA-Z0-9]{1,8}')    #: Regex for radio name

RADIO_NAME_MAX_LEN = 8                              #: Max number of characters in radio name

RE_SW_VER = re.compile(r'(\d+\.\d+\.\d+-\d+)')