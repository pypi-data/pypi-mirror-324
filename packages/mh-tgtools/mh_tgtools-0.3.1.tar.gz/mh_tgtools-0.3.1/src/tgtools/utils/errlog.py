import datetime


class Err:
    """ Representation of an error resulting from an interaction with a radio.
    """

    def __init__(self, label: str = '', msg: str = '', timestamp: str = ''):
        """ Instantiating parameters:

            :param label: Arbitrary label identifying the device causing the error (typically its IP address and/or its name.
            :type label: str
            :param msg: A descriptive error message.
            :type msg: str
            :param timestamp: Timestamp (computer time) when the error occured. If not provided, then automatically set to instantiation time.
            :type timestamp: str
        """

        #: An arbitrary label, typically identifying the device.
        self.label = label
        #: Error message.
        self.msg = msg
        #: Timestamp for when error occurs.
        self.timestamp = timestamp if timestamp else datetime.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")

    def __repr__(self):
        string = f"Err(label={self.label}, "
        string += f"msg={self.msg}, "
        string += f"timestamp={self.timestamp})"
        return string

    def __str__(self):
        string = f"Err:\n"
        string += f"\tlabel: {self.label}\n"
        string += f"\tmsg: {self.msg}\n"
        string += f"\ttimestamp: {self.timestamp}\n"
        return string

    def as_dict(self) -> dict:
        """ Dictionary representation.

            :return: Dictionary representation of error.
            :rtype: dict
        """
        return dict(timestamp=self.timestamp,
                      label=self.label,
                      msg=self.msg,
                      )

