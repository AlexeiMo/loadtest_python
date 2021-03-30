import os

from helpers.assertion_helper import assert_status_code
from helpers.json_helper import read_json

filepath = os.path.abspath("target.json")
target = read_json(filepath)


class AuthorizationHelper:
    cookies = {"user": None, "admin": None}

    def log_in(self, session, name, password, role):
        if self.cookies[role]:
            session.headers.update(
                {"Cookie": self.cookies[role]}
            )
        else:
            session.headers.update(
                {"Content-Type": "application/x-www-form-urlencoded"}
            )

            data = {
                "name": name,
                "pass": password,
                "form_id": target["user"]["login"]["form_id"]
            }

            with session.post("/", name="/LOGIN", data=data, catch_response=True, verify=False) as response:
                assert_status_code(response)
                if not session.cookies:
                    response.failure("No cookie retrieve from authorization response")
                else:
                    cookie_parts = session.cookies.items()[0]
                    cookie = cookie_parts[0] + '=' + cookie_parts[1]
                    self.cookies[role] = cookie
                    session.headers.update({
                        "Cookie": f"{cookie}"
                    })
                response.success()
                return None
