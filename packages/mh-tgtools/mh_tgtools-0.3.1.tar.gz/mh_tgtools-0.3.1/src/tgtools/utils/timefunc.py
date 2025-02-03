import datetime

from tgtools.consts import DEFAULT_FILE_TIMESTAMP_FORMAT

def get_timestamp_for_files():
    return datetime.datetime.now().strftime(DEFAULT_FILE_TIMESTAMP_FORMAT)

def timestamp_for_files_to_time(timestamp: str):
    return datetime.datetime.strptime(timestamp, DEFAULT_FILE_TIMESTAMP_FORMAT)


def uptime_to_timedelta(uptime: str) -> datetime.timedelta | None:
    if uptime:
        time_rep = [int(item) for item in uptime.split(':')]
        return datetime.timedelta(days=time_rep[0], hours=time_rep[1], minutes=time_rep[2], seconds=time_rep[3])
    else:
        return None


def timedelta_to_uptime(duration: datetime.timedelta) -> str:
    if duration:
        days = duration.days
        remainder = duration.seconds
        hours = remainder // 3600
        remainder %= 3600
        minutes = remainder // 60
        seconds = remainder % 60
        return f"{days:04}:{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return ""


def seconds_to_uptime(x: int) -> str:
    duration = datetime.timedelta(seconds=x)
    return timedelta_to_uptime(duration)


TIMESTAMP_FORMAT1 = '%Y%m%d_%H%M%S'


def datetime_to_string1(x: datetime.datetime) -> str:
    """ String of format %Y%m%d_%H%M%S """
    assert isinstance(x, datetime.datetime)
    return x.strftime(TIMESTAMP_FORMAT1)


TIMESTAMP_FORMAT2 = '%Y-%m-%d %H:%M:%S'


def datetime_to_string2(x: datetime.datetime) -> str:
    assert isinstance(x, datetime.datetime)
    return x.strftime(TIMESTAMP_FORMAT2)


TIMESTAMP_FORMAT3 = '%Y-%m-%d %H:%M:%S.%f'


def datetime_to_string3(x: datetime.datetime) -> str:
    assert isinstance(x, datetime.datetime)
    timestamp = x.strftime(TIMESTAMP_FORMAT3)
    return ' ' + timestamp[:-3]


def string_to_datetime(x: str) -> datetime.datetime:
    assert isinstance(x, str)
    xx = x.strip()
    if '_' in xx:
        return datetime.datetime.strptime(xx, TIMESTAMP_FORMAT1)
    elif '.' in xx:
        return datetime.datetime.strptime(xx, TIMESTAMP_FORMAT3)
    else:
        return datetime.datetime.strptime(xx, TIMESTAMP_FORMAT2)

