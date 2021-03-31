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
    class UserModule(TaskSet):

        def on_start(self):
            AuthorizationHelper().log_in(
                session=self.client,
                name=target["user"]["login"]["name"],
                password=target["user"]["login"]["password"],
                role="user"
            )

        @task(1)
        class AccountModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def navigate_to_account(self):
                url = target["user"]["navigate_to_account"]["endpoint"]
                self.requests_helper.send_get_request(url, "/ACCOUNTS")

            @task(1)
            def view_account(self):
                url = target["user"]["view_account"]["endpoint"]
                filename = target["user"]["view_account"]["filename"]
                self.requests_helper.send_get_request(url, "/ACCOUNT", filename)

            @task(1)
            def view_transaction(self):
                url = target["user"]["view_transaction"]["endpoint"]
                filename = target["user"]["view_transaction"]["filename"]
                self.requests_helper.send_get_request(url, "/TRANSACTION", filename)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class RequestsModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def create_tba_request(self):
                url = target["user"]["tba_request"]["endpoint"]
                filename_1 = target["user"]["tba_request"]["fill_in_filename"]
                filename_2 = target["user"]["tba_request"]["finish_filename"]
                self.requests_helper.send_post_request(url, "/TBA FILL IN DATA", filename_1)
                self.requests_helper.send_post_request(url, "/TBA ACCEPT DATA", filename_2)

            @task(1)
            def create_tbu_request(self):
                url = target["user"]["tbu_request"]["endpoint"]
                filename_1 = target["user"]["tbu_request"]["fill_in_filename"]
                filename_2 = target["user"]["tbu_request"]["finish_filename"]
                self.requests_helper.send_post_request(url, "/TBU FILL IN DATA", filename_1)
                self.requests_helper.send_post_request(url, "/TBU ACCEPT DATA", filename_2)

            @task(1)
            def create_owt_request(self):
                url = target["user"]["owt_request"]["endpoint"]
                filename_1 = target["user"]["owt_request"]["fill_in_filename"]
                filename_2 = target["user"]["owt_request"]["finish_filename"]
                self.requests_helper.send_post_request(url, "/OWT FILL IN DATA", filename_1)
                self.requests_helper.send_post_request(url, "/OWT ACCEPT DATA", filename_2)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class ReportModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def view_sas_report(self):
                url = target["user"]["sas_report"]["endpoint"]
                filename = target["user"]["sas_report"]["filename"]
                self.requests_helper.send_get_request(url, "/SAS REPORT", filename)
                url += "/export"
                self.requests_helper.send_get_request(url, "/SAS REPORT EXPORT", filename)

            @task(1)
            def view_all_balances_report(self):
                url = target["user"]["all_balances"]["endpoint"]
                self.requests_helper.send_get_request(url, "/ALL BALANCES REPORT")
                url += "/export"
                self.requests_helper.send_get_request(url, "/ALL BALANCES REPORT EXPORT")

            @task(1)
            def view_all_transactions_report(self):
                url = target["user"]["all_transactions"]["endpoint"]
                self.requests_helper.send_get_request(url, "/ALL TRANSACTIONS REPORT")
                url += "/export"
                self.requests_helper.send_get_request(url, "/ALL TRANSACTIONS REPORT EXPORT")

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class MessagesModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def navigate_to_messages(self):
                url = target["user"]["navigate_to_messages"]["endpoint"]
                self.requests_helper.send_get_request(url, "/MESSAGES")

            @task(1)
            def read_message(self):
                url = target["user"]["read_message"]["endpoint"] + "/" + target["user"]["read_message"]["id"]
                self.requests_helper.send_get_request(url, "/MESSAGE READ")

            @task(1)
            def send_new_message(self):
                url = target["user"]["send_new_message"]["endpoint"]
                filename = target["user"]["send_new_message"]["filename"]
                self.requests_helper.send_post_request(url, "/SEND NEW MESSAGE", filename)

            @task(1)
            def reply_to_message(self):
                url = target["user"]["reply_to_message"]["endpoint"] + "/" + target["user"]["reply_to_message"]["id"]
                filename = target["user"]["reply_to_message"]["filename"]
                self.requests_helper.send_post_request(url, "/REPLY TO MESSAGE", filename)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(2)
        def stop(self):
            self.interrupt()

    @task(1)
    class AdminModule(TaskSet):

        def on_start(self):
            AuthorizationHelper().log_in(
                session=self.client,
                name=target["admin"]["login"]["name"],
                password=target["admin"]["login"]["password"],
                role="admin"
            )

        @task(1)
        class TransferRequestsModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def create_tba_request(self):
                url = target["admin"]["tba_request"]["endpoint"]
                filename_1 = target["admin"]["tba_request"]["fill_data_filename"]
                filename_2 = target["admin"]["tba_request"]["finish_filename"]
                self.requests_helper.send_post_request(url, "/TBA FILL IN DATA", filename_1)
                self.requests_helper.send_post_request(url, "/TBA ACCEPT DATA", filename_2)

            @task(1)
            def create_tbu_request(self):
                url = target["admin"]["tbu_request"]["endpoint"]
                filename_1 = target["admin"]["tbu_request"]["fill_data_filename"]
                filename_2 = target["admin"]["tbu_request"]["finish_filename"]
                self.requests_helper.send_post_request(url, "/TBU FILL IN DATA", filename_1)
                self.requests_helper.send_post_request(url, "/TBU ACCEPT DATA", filename_2)

            @task(1)
            def create_owt_request(self):
                url = target["admin"]["owt_request"]["endpoint"]
                filename_1 = target["admin"]["owt_request"]["fill_data_filename"]
                filename_2 = target["admin"]["owt_request"]["finish_filename"]
                self.requests_helper.send_post_request(url, "/OWT FILL IN DATA", filename_1)
                self.requests_helper.send_post_request(url, "/OWT ACCEPT DATA", filename_2)

            @task(1)
            def perform_debit(self):
                url = target["admin"]["debit"]["endpoint"]
                filename = target["admin"]["debit"]["filename"]
                self.requests_helper.send_post_request(url, "/DEBIT", filename)

            @task(1)
            def perform_credit(self):
                url = target["admin"]["credit"]["endpoint"]
                filename = target["admin"]["credit"]["filename"]
                self.requests_helper.send_post_request(url, "/CREDIT", filename)

            @task(1)
            def approve_transfer_request(self):
                url = target["admin"]["approve_request"]["endpoint"]
                filename = target["admin"]["approve_request"]["filename"]
                self.requests_helper.send_post_request(url, "/EXECUTE TRANSFER REQUEST", filename)

            @task(1)
            def cancel_transfer_request(self):
                url = target["admin"]["cancel_request"]["endpoint"]
                filename = target["admin"]["cancel_request"]["filename"]
                self.requests_helper.send_post_request(url, "/CANCEL TRANSFER REQUEST", filename)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class RequestsModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def view_all_requests(self):
                url = target["admin"]["all_requests"]["endpoint"] + "/export"
                filename = target["admin"]["all_requests"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL REQUESTS EXPORT", filename)  # 500 error
                url = target["admin"]["all_requests"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL REQUESTS PRINT", filename)

            @task(1)
            def view_filtered_requests(self):
                url = target["admin"]["filtered_requests"]["endpoint"] + "/export"
                filename = target["admin"]["filtered_requests"]["filename"]
                self.requests_helper.send_get_request(url, "/FILTERED REQUESTS EXPORT", filename)
                url = target["admin"]["filtered_requests"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/FILTERED REQUESTS PRINT", filename)

            @task(1)
            def view_request_by_id(self):
                url = target["admin"]["request_by_id"]["endpoint"] + "/export"
                filename = target["admin"]["request_by_id"]["filename"]
                self.requests_helper.send_get_request(url, "/REQUEST BY ID EXPORT", filename)  # 500 error
                url = target["admin"]["request_by_id"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/REQUEST BY ID PRINT", filename)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class UserReportModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def view_transactions_by_user_id(self):
                url = target["admin"]["user_tr_report"]["endpoint"] + "/export"
                filename = target["admin"]["user_tr_report"]["filename"]
                self.requests_helper.send_get_request(url, "/TRANSACTIONS BY USER ID EXPORT", filename)
                url = target["admin"]["user_tr_report"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/TRANSACTIONS BY USER ID PRINT", filename)

            @task(1)
            def view_balance_by_user_id(self):
                url = target["admin"]["user_balance_report"]["endpoint"] + "/export"
                filename = target["admin"]["user_balance_report"]["filename"]
                self.requests_helper.send_get_request(url, "/BALANCE BY USER ID EXPORT", filename)
                url = target["admin"]["user_balance_report"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/BALANCE BY USER ID PRINT", filename)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class GlobalSystemReportModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def view_all_system_transactions(self):
                url = target["admin"]["gsr_transactions"]["endpoint"] + "/export"
                filename = target["admin"]["gsr_transactions"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL SYSTEM TRANSACTIONS EXPORT", filename)
                url = target["admin"]["gsr_transactions"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL SYSTEM TRANSACTIONS PRINT", filename)

            @task(1)
            def view_all_system_balances(self):
                url = target["admin"]["gsr_balances"]["endpoint"] + "/export"
                filename = target["admin"]["gsr_balances"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL SYSTEM BALANCES EXPORT", filename)
                url = target["admin"]["gsr_balances"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL SYSTEM BALANCES PRINT", filename)

            @task(1)
            def view_all_system_owt_requests(self):
                url = target["admin"]["gsr_owt_requests"]["endpoint"] + "/export"
                filename = target["admin"]["gsr_balances"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL SYSTEM OWT REQUESTS EXPORT", filename)
                url = target["admin"]["gsr_owt_requests"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL SYSTEM OWT REQUESTS PRINT", filename)

            @task(1)
            def view_system_overview(self):
                url = target["admin"]["gsr_system_overview"]["endpoint"] + "/export"
                filename = target["admin"]["gsr_system_overview"]["filename"]
                self.requests_helper.send_get_request(url, "/SYSTEM OVERVIEW EXPORT", filename)
                url = target["admin"]["gsr_system_overview"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/SYSTEM OVERVIEW PRINT", filename)

            @task(1)
            def view_all_system_interests(self):
                url = target["admin"]["gsr_interests"]["endpoint"] + "/export"
                filename = target["admin"]["gsr_interests"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL SYSTEM INTERESTS EXPORT", filename)
                url = target["admin"]["gsr_interests"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL SYSTEM INTERESTS PRINT", filename)

            @task(1)
            def view_system_revenue(self):
                url = target["admin"]["gsr_revenue"]["endpoint"] + "/export"
                filename = target["admin"]["gsr_revenue"]["filename"]
                self.requests_helper.send_get_request(url, "/SYSTEM REVENUE EXPORT", filename)
                url = target["admin"]["gsr_revenue"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/SYSTEM REVENUE PRINT", filename)

            @task(1)
            def view_system_access_log(self):
                url = target["admin"]["gsr_access_log"]["endpoint"] + "/export"
                self.requests_helper.send_get_request(url, "/SYSTEM ACCESS LOG EXPORT")  # 500 error
                url = target["admin"]["gsr_access_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/SYSTEM ACCESS LOG PRINT")  # 500 error

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class SystemLogModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def view_all_transactions_log(self):
                url = target["admin"]["all_transactions_log"]["endpoint"] + "/export"
                filename = target["admin"]["gsr_revenue"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL TRANSACTIONS LOG EXPORT", filename)
                url = target["admin"]["all_transactions_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL TRANSACTIONS LOG PRINT", filename)

            @task(1)
            def view_filtered_transactions_log(self):
                url = target["admin"]["filtered_transactions_log"]["endpoint"] + "/export"
                filename = target["admin"]["filtered_transactions_log"]["filename"]
                self.requests_helper.send_get_request(url, "/FILTERED TRANSACTIONS LOG EXPORT", filename)
                url = target["admin"]["all_transactions_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/FILTERED TRANSACTIONS LOG PRINT", filename)

            @task(1)
            def view_all_information_log(self):
                url = target["admin"]["all_information_log"]["endpoint"] + "/export"
                filename = target["admin"]["all_information_log"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL INFORMATION LOG EXPORT", filename)
                url = target["admin"]["all_information_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/ALL INFORMATION LOG PRINT", filename)

            @task(1)
            def view_filtered_information_log(self):
                url = target["admin"]["filtered_information_log"]["endpoint"] + "/export"
                filename = target["admin"]["all_information_log"]["filename"]
                self.requests_helper.send_get_request(url, "/FILTERED INFORMATION LOG EXPORT", filename)
                url = target["admin"]["all_information_log"]["endpoint"] + "/print"
                self.requests_helper.send_get_request(url, "/FILTERED INFORMATION LOG PRINT", filename)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class RegistrationRequestsModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def view_all_registration_requests(self):
                url = target["admin"]["all_registration_requests"]["endpoint"]
                filename = target["admin"]["all_registration_requests"]["filename"]
                self.requests_helper.send_get_request(url, "/ALL REGISTRATION REQUESTS", filename)

            @task(1)
            def view_filtered_registration_requests(self):
                url = target["admin"]["filtered_registration_requests"]["endpoint"]
                filename = target["admin"]["filtered_registration_requests"]["filename"]
                self.requests_helper.send_get_request(url, "/FILTERED REGISTRATION REQUESTS", filename)

            @task(1)
            def view_registration_request_by_id(self):
                url = target["admin"]["registration_request_by_id"]["endpoint"]
                filename = target["admin"]["registration_request_by_id"]["filename"]
                self.requests_helper.send_get_request(url, "/REGISTRATION REQUESTS BY ID", filename)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class UserProfileModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def approve_registration_request(self):
                url = target["admin"]["approve_reg_request"]["endpoint"]
                filename = target["admin"]["approve_reg_request"]["filename"]
                self.requests_helper.send_post_request(url, "/APPROVE REGISTRATION REQUEST", filename)

            @task(1)
            def create_user_profile(self):
                url = target["admin"]["create_user_profile"]["endpoint"]
                filename = target["admin"]["create_user_profile"]["filename"]
                self.requests_helper.send_post_request(url, "/CREATE USER PROFILE", filename)

            @task(1)
            def view_account_types(self):
                url = target["admin"]["account_types"]["endpoint"]
                self.requests_helper.send_get_request(url, "/ACCOUNT TYPES")

            @task(1)
            def create_new_account(self):
                url = target["admin"]["new_account"]["endpoint"]
                filename = target["admin"]["create_user_profile"]["filename"]
                self.requests_helper.send_post_request(url, "/NEW ACCOUNT", filename)

            @task(1)
            def unblock_user_profile(self):
                url = target["admin"]["unblock_user_profile"]["endpoint"]
                filename = target["admin"]["reply_to_message"]["filename"]
                self.requests_helper.send_post_request(url, "/USER UNBLOCK", filename)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(1)
        class MessagesModule(TaskSet):

            def __init__(self, parent):
                super().__init__(parent)
                self.requests_helper = RequestsHelper(self.client)

            @task(1)
            def navigate_to_messages(self):
                url = target["admin"]["messages"]["endpoint"]
                self.requests_helper.send_get_request(url, "/MESSAGES")

            @task(1)
            def read_message(self):
                url = target["admin"]["read_message"]["endpoint"] + "/" + target["admin"]["read_message"]["id"]
                self.requests_helper.send_get_request(url, "/MESSAGE READ")

            @task(1)
            def send_message(self):
                url = target["admin"]["send_message"]["endpoint"]
                filename = target["admin"]["send_message"]["filename"]
                self.requests_helper.send_post_request(url, "NEW MESSAGE", filename)

            @task(1)
            def reply_to_message(self):
                url = target["admin"]["reply_to_message"]["endpoint"] + "/" + target["admin"]["reply_to_message"]["id"]
                filename = target["admin"]["reply_to_message"]["filename"]
                self.requests_helper.send_post_request(url, "/REPLY TO MESSAGE", filename)

            @task(2)
            def stop(self):
                self.interrupt()

        @task(2)
        def stop(self):
            self.interrupt()


class LoadTestUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://34.91.47.190"

    tasks = [UserBehavior]
