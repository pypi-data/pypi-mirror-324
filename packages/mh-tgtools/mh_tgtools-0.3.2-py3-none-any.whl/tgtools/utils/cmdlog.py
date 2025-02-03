import datetime
import typing

from tgtools.consts import LEN_RESP_DISPL_TRUNC


class Cmd:
    """ Representation of a command interaction with a radio:
        the command itself, target radio, response, success indication, timestamp.
    """

    def __init__(self, command: str, target_id: str = '', response: str = '', success: bool = False,
                 timestamp: str = ''):
        """
            :param command: The command string.
            :type command: str
            :param target_id: Designation of the target radio.
            :type target_id: str
            :param response: Copy of the response.
            :type response: str
            :param success: Indication if response is successful.
            :type success: bool
            :param timestamp: Timestamp sending command.
            :type timestamp: str

        """

        #: The command string.
        self.command: str = command
        #: An arbitrary label identifying the target device (typically IP address and/or radio param_name).
        self.target_id: str = target_id
        #: The radio's response to the command.
        self.response: str = response
        #: Indication if command executed successfully.
        self.success: bool = success
        #: Timestamp for when command executed (if not provided, set to instantiation time)
        self.timestamp: str = timestamp if timestamp else datetime.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")

        if len(self.response) > LEN_RESP_DISPL_TRUNC:
            self._truc_response = f"{self.response[:LEN_RESP_DISPL_TRUNC]!r}...,"
        else:
            self._truc_response = f"response={self.response!r}, "

    def __add__(self, other: typing.Self):
        """ Amalgamate two class instances by combining information from both:

             * :attr:`command` is a concatenation of the corresponding attribute of both instances
             * :attr:`target_id` is that of the first instance (assumed identical for both instances)
             * :attr:`response` is a concatenation of the corresponding attribute of both instances
             * :attr:`success` is the logical *and* of the corresponding attribute of both instances
             * :attr:`timestamp` is that of the second instance.
        """
        combined = Cmd(command=f"{self.command} + {other.command}",
                       target_id=self.target_id,
                       response=f"{self.response}\n{other.response}",
                       success=self.success and other.success,
                       timestamp=other.timestamp)
        return combined

    def __repr__(self):
        string = f"Cmd(command={self.command}, "
        string += f"target_id={self.target_id}, "
        string += f"success={self.success}, "
        string += f"response={self._truc_response},"
        string += f"timestamp={self.timestamp})"
        return string

    def __str__(self):
        string = f"Cmd:\n"
        string += f"\tcommand: {self.command}\n"
        string += f"\ttarget_id: {self.target_id}\n"
        string += f"\tsuccess: {self.success}\n"
        string += f"\tresponse: {self._truc_response!r}\n"
        string += f"\ttimestamp: {self.timestamp}\n"
        return string

    def as_dict(self) -> dict:
        """ Convert to dict (response may be truncated).

            :rtype: dict
        """

        return dict(timestamp=self.timestamp,
                    target_id=self.target_id,
                    command=self.command,
                    success=self.success,
                    response=self._truc_response,
                    )
