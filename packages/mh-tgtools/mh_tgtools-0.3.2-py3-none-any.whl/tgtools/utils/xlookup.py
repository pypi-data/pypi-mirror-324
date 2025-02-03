from dataclasses import dataclass
from typing import Callable


@dataclass
class XLookup:
    """ A class to store parameters for the xlookup function
    """
    #: Target key: list of dictionary keys
    target_data: list[dict]
    target_keys: list[str]
    target_lookup: str
    ref_data: list[dict]
    ref_keys: list[str]
    ref_lookup: str
    func: Callable[[str, str], str]


def process_xlookups(xlookups: tuple[XLookup, ...]):
    """ In-place xlookup
    """
    for xlookup in xlookups:
        for record in xlookup.target_data:
            target_values = [record[key] for key in xlookup.target_keys]
            for item in xlookup.ref_data:
                if [item[key] for key in xlookup.ref_keys] == target_values:
                    record[xlookup.target_lookup] = xlookup.func(record[xlookup.target_lookup], item[xlookup.ref_lookup])
                    break
    return None
