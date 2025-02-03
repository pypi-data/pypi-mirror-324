import datetime
from pathlib import Path

import requests
import urllib3

from tgtools import Credential, Err
from tgtools.consts import HTTP_CONNECT_TIMEOUT, HTTP_GET_CHUNK_SIZE, HTTP_READ_TIMEOUT
from tgtools.utils.ioutils.iogen import confirm_exists

urllib3.disable_warnings()


class TechLog:
    """ Fetch the tech log from a TG radio ('tech_file.zip') """

    def __init__(self, credential: Credential, remote_cn: str = ''):
        """
        :param credential: Radio log-in credential (IP address, username, password)
        :type credential: Credential
        :param remote_cn: (Optional): name of remote radio
        :type remote_cn: str
        """

        #: Credential to log into radio (IP address, username, password).
        self.credential: Credential = credential
        #: Name of remote Client Node (if tunneling into a remote radio).
        self.remote_cn: str = remote_cn

        #: List of errors.
        self.errors: list[Err] = []

    def fetch(self, output_path: Path | str) -> bool:
        """ Fetch tech_log (HTTP) and save to file.
            Returns True if successful and file is created, otherwise False.

            :param output_path: Path (or filename) of output file.
            :type output_path: pathlib.Path
            :return: Indication of success.
            :rtype: bool
        """
        output_path = Path(output_path)
        if self.remote_cn:
            r_id = f"{self.credential.ip_addr}_{self.remote_cn}"
            r_url = f"https://{self.credential.ip_addr}/remote/{self.remote_cn}/logs"
        else:
            r_id = f"{self.credential.ip_addr}"
            r_url = f"https://{self.credential.ip_addr}/logs"
        error: Err | None = None
        try:
            response = requests.get(r_url,
                                    auth=(self.credential.username, self.credential.password),
                                    stream=True,
                                    timeout=(HTTP_CONNECT_TIMEOUT, HTTP_READ_TIMEOUT),
                                    verify=False,
                                    )
        except requests.ConnectTimeout:
            error = Err(r_id, "HTTP timed out trying to connect to radio (to fetch tech_log)")
        except requests.ReadTimeout:
            error = Err(r_id, "HTTP timed out waiting for radio to send tech_log data")
        except requests.HTTPError:
            error = Err(r_id, "HTTP error trying to fetch tech_log")
        except requests.ConnectionError:
            error = Err(r_id, "HTTP connection error trying to fetch tech_log")
        except requests.RequestException as e:
            error = Err(r_id, f"Request exception trying to fetch tech_log: {e}")
        else:
            if response.ok:
                confirm_exists(output_path.parent, 'dir', create=True)
                with output_path.open('wb') as f:
                    for chunk in response.iter_content(chunk_size=HTTP_GET_CHUNK_SIZE):
                        f.write(chunk)
            else:
                error = Err(r_id, f"HTTP error fetching tech_log: {response.reason} ({response.status_code})")
            response.close()
        finally:
            if error:
                self.errors.append(error)
            return False


if __name__ == '__main__':
    credential = Credential('172.19.40.18', 'admin', 'Air-band12?')
    t = TechLog(credential)
    t.fetch('tech_log.zip')
