from pathlib import Path
from helpers.assertion_helper import assert_status_code
from helpers.json_helper import read_json


class RequestsHelper:

    def __init__(self, session):
        self.session = session

    def send_post_request(self, url, request_name, filename):
        source_file = Path("data") / filename
        data = read_json(source_file)
        with self.session.post(url, name=request_name, data=data, verify=False,
                               catch_response=True) as response:
            assert_status_code(response)

    def send_get_request(self, url, request_name, filename=None):
        if filename:
            source_file = Path("data") / filename
            params = read_json(source_file)
        else:
            params = None
        with self.session.get(url, name=request_name, params=params, verify=False,
                              catch_response=True) as response:
            assert_status_code(response)
