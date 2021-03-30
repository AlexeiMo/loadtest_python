import os

from locust import HttpUser, between, task, TaskSet
import urllib3
from helpers.authorize_helper import AuthorizationHelper
from helpers.json_helper import read_json
from helpers.requests_helper import RequestsHelper

urllib3.disable_warnings()

filepath = os.path.abspath("target.json")
target = read_json(filepath)


class UserBehavior(TaskSet):

    @task(1)
    class AdminModule(TaskSet):

        def on_start(self):
            AuthorizationHelper().log_in(
                session=self.client,
                name=target["login"]["name"],
                password=target["login"]["password"],
                role="admin"
            )

        @task(1)
        class TransferRequestsModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(3)
            def create_tba_request(self):
                url = target["tba_request"]["endpoint"]
                filename_1 = target["tba_request"]["fill_data_filename"]
                filename_2 = target["tba_request"]["finish_filename"]
                self.requests_helper.send_post_request(url, "/TBA FILL IN DATA", filename_1)
                self.requests_helper.send_post_request(url, "/TBA ACCEPT DATA", filename_2)

            @task(3)
            def create_tbu_request(self):
                url = target["tbu_request"]["endpoint"]
                filename_1 = target["tbu_request"]["fill_data_filename"]
                filename_2 = target["tbu_request"]["finish_filename"]
                self.requests_helper.send_post_request(url, "/TBU FILL IN DATA", filename_1)
                self.requests_helper.send_post_request(url, "/TBU ACCEPT DATA", filename_2)

            @task(1)
            def create_owt_request(self):
                url = target["owt_request"]["endpoint"]
                filename_1 = target["owt_request"]["fill_data_filename"]
                filename_2 = target["owt_request"]["finish_filename"]
                self.requests_helper.send_post_request(url, "/OWT FILL IN DATA", filename_1)
                self.requests_helper.send_post_request(url, "/OWT ACCEPT DATA", filename_2)

            @task(4)
            def stop(self):
                self.interrupt()

        @task(1)
        class RequestsModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(5)
            def view_all_requests(self):
                url = target["all_requests"]["endpoint"] + "/export"
                filename = target["all_requests"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL REQUESTS EXPORT", filename)  # 500 error
                url = target["all_requests"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL REQUESTS PRINT", filename)

            @task(4)
            def view_filtered_requests(self):
                url = target["filtered_requests"]["endpoint"] + "/export"
                filename = target["filtered_requests"]["filename"]
                self.requests_helper.send_get_request(url, "/FILTERED REQUESTS EXPORT", filename)
                url = target["filtered_requests"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/FILTERED REQUESTS PRINT", filename)

            @task(4)
            def view_request_by_id(self):
                url = target["request_by_id"]["endpoint"] + "/export"
                filename = target["request_by_id"]["filename"]
                self.requests_helper.send_get_request(url, "/REQUEST BY ID EXPORT", filename)  # 500 error
                url = target["request_by_id"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/REQUEST BY ID PRINT", filename)

            @task(6)
            def stop(self):
                self.interrupt()

        @task(1)
        class UserReportModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(3)
            def view_transactions_by_user_id(self):
                url = target["user_tr_report"]["endpoint"] + "/export"
                filename = target["user_tr_report"]["filename"]
                self.requests_helper.send_get_request(url, "/TRANSACTIONS BY USER ID EXPORT", filename)
                url = target["user_tr_report"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/TRANSACTIONS BY USER ID PRINT", filename)

            @task(3)
            def view_balance_by_user_id(self):
                url = target["user_balance_report"]["endpoint"] + "/export"
                filename = target["user_balance_report"]["filename"]
                self.requests_helper.send_get_request(url, "/BALANCE BY USER ID EXPORT", filename)
                url = target["user_balance_report"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/BALANCE BY USER ID PRINT", filename)

            @task(4)
            def stop(self):
                self.interrupt()

        @task(1)
        class GlobalSystemReportModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(3)
            def view_all_system_transactions(self):
                url = target["gsr_transactions"]["endpoint"] + "/export"
                filename = target["gsr_transactions"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL SYSTEM TRANSACTIONS EXPORT", filename)
                url = target["gsr_transactions"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL SYSTEM TRANSACTIONS PRINT", filename)

            @task(3)
            def view_all_system_balances(self):
                url = target["gsr_balances"]["endpoint"] + "/export"
                filename = target["gsr_balances"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL SYSTEM BALANCES EXPORT", filename)
                url = target["gsr_balances"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL SYSTEM BALANCES PRINT", filename)

            @task(3)
            def view_all_system_owt_requests(self):
                url = target["gsr_owt_requests"]["endpoint"] + "/export"
                filename = target["gsr_balances"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL SYSTEM OWT REQUESTS EXPORT", filename)
                url = target["gsr_owt_requests"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL SYSTEM OWT REQUESTS PRINT", filename)

            @task(3)
            def view_system_overview(self):
                url = target["gsr_system_overview"]["endpoint"] + "/export"
                filename = target["gsr_system_overview"]["filename"]
                self.requests_helper.send_get_request(url, "/SYSTEM OVERVIEW EXPORT", filename)
                url = target["gsr_system_overview"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/SYSTEM OVERVIEW PRINT", filename)

            @task(3)
            def view_all_system_interests(self):
                url = target["gsr_interests"]["endpoint"] + "/export"
                filename = target["gsr_interests"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL SYSTEM INTERESTS EXPORT", filename)
                url = target["gsr_interests"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL SYSTEM INTERESTS PRINT", filename)

            @task(3)
            def view_system_revenue(self):
                url = target["gsr_revenue"]["endpoint"] + "/export"
                filename = target["gsr_revenue"]["filename"]
                self.requests_helper.send_get_request(url, "/SYSTEM REVENUE EXPORT", filename)
                url = target["gsr_revenue"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/SYSTEM REVENUE PRINT", filename)

            @task(3)
            def view_system_access_log(self):
                url = target["gsr_access_log"]["endpoint"] + "/export"
                self.requests_helper.send_get_request(url, "/SYSTEM ACCESS LOG EXPORT")  # 500 error
                url = target["gsr_access_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/SYSTEM ACCESS LOG PRINT")  # 500 error

            @task(4)
            def stop(self):
                self.interrupt()

        @task(1)
        class SystemLogModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(3)
            def view_all_transactions_log(self):
                url = target["all_transactions_log"]["endpoint"] + "/export"
                filename = target["gsr_revenue"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL TRANSACTIONS LOG EXPORT", filename)
                url = target["all_transactions_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL TRANSACTIONS LOG PRINT", filename)

            @task(3)
            def view_filtered_transactions_log(self):
                url = target["filtered_transactions_log"]["endpoint"] + "/export"
                filename = target["filtered_transactions_log"]["filename"]
                self.requests_helper.send_get_request(url, "/FILTERED TRANSACTIONS LOG EXPORT", filename)
                url = target["all_transactions_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/FILTERED TRANSACTIONS LOG PRINT", filename)

            @task(3)
            def view_all_information_log(self):
                url = target["all_information_log"]["endpoint"] + "/export"
                filename = target["all_information_log"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL INFORMATION LOG EXPORT", filename)
                url = target["all_information_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL INFORMATION LOG PRINT", filename)

            @task(3)
            def view_filtered_information_log(self):
                url = target["filtered_information_log"]["endpoint"] + "/export"
                filename = target["all_information_log"]["filename"]
                self.requests_helper.send_get_request(url, "/FILTERED INFORMATION LOG EXPORT", filename)
                url = target["all_information_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/FILTERED INFORMATION LOG PRINT", filename)

            @task(4)
            def stop(self):
                self.interrupt()

        @task(1)
        class RegistrationRequestsModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(3)
            def view_all_registration_requests(self):
                url = target["all_registration_requests"]["endpoint"]
                filename = target["all_registration_requests"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL REGISTRATION REQUESTS", filename)

            @task(3)
            def view_filtered_registration_requests(self):
                url = target["filtered_registration_requests"]["endpoint"]
                filename = target["filtered_registration_requests"]["filename"]
                self.requests_helper.send_get_request(url, "/FILTERED REGISTRATION REQUESTS", filename)

            @task(3)
            def view_registration_request_by_id(self):
                url = target["registration_request_by_id"]["endpoint"]
                filename = target["registration_request_by_id"]["filename"]
                self.requests_helper.send_get_request(url, "/REGISTRATION REQUESTS BY ID", filename)

            @task(4)
            def stop(self):
                self.interrupt()

        @task(1)
        class UserProfileModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(3)
            def create_user_profile(self):
                url = target["create_user_profile"]["endpoint"]
                filename = target["create_user_profile"]["filename"]
                self.requests_helper.send_post_request(url, "/CREATE USER PROFILE", filename)

            @task(3)
            def view_account_types(self):
                url = target["account_types"]["endpoint"]
                self.requests_helper.send_get_request(url, "/ACCOUNT TYPES")

            @task(3)
            def create_new_account(self):
                url = target["new_account"]["endpoint"]
                filename = target["create_user_profile"]["filename"]
                self.requests_helper.send_post_request(url, "/NEW ACCOUNT", filename)

            @task(3)
            def unblock_user_profile(self):
                url = target["unblock_user_profile"]["endpoint"]
                filename = target["reply_to_message"]["filename"]
                self.requests_helper.send_post_request(url, "/USER UNBLOCK", filename)

            @task(4)
            def stop(self):
                self.interrupt()

        @task(1)
        class MessagesModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(3)
            def navigate_to_messages(self):
                url = target["messages"]["endpoint"]
                self.requests_helper.send_get_request(url, "/MESSAGES")

            @task(3)
            def read_message(self):
                url = target["read_message"]["endpoint"] + "/" + target["read_message"]["id"]
                self.requests_helper.send_get_request(url, "/MESSAGE READ")

            @task(3)
            def send_message(self):
                url = target["send_message"]["endpoint"]
                filename = target["send_message"]["filename"]
                self.requests_helper.send_post_request(url, "NEW MESSAGE", filename)

            @task(3)
            def reply_to_message(self):
                url = target["reply_to_message"]["endpoint"] + "/" + target["reply_to_message"]["id"]
                filename = target["reply_to_message"]["filename"]
                self.requests_helper.send_post_request(url, "/REPLY TO MESSAGE", filename)

            @task(4)
            def stop(self):
                self.interrupt()

        # @task(1)
        # def stop(self):
        #     self.interrupt()


class LoadTestUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://34.91.47.190"

    tasks = [UserBehavior]
