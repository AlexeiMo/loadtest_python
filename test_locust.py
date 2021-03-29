import os
from pathlib import Path

from locust import HttpUser, between, task, TaskSet
import urllib3
from helpers.authorize_helper import AuthorizationHelper
from helpers.assertion_helper import assert_status_code
from helpers.json_helper import read_json

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

        # @task(3)
        def create_tba_request(self):
            url = target["tba_request"]["endpoint"]
            data = {
                "user_id": target["tba_request"]["user_id"],
                "debit_from": target["tba_request"]["debit_from"],
                "credit_to": target["tba_request"]["credit_to"],
                "amount_to_transfer": target["tba_request"]["amount_to_transfer"],
                "transfer_fee": None,
                "next": "Continue",
                "form_token": target["tba_request"]["form_token"],
                "form_id": target["tba_request"]["form_id"]
            }
            with self.client.post(url, name="/TBA FILL IN DATA", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

            data = {
                "finish": "Continue",
                "form_token": target["tba_request"]["form_token"],
                "form_id": target["tba_request"]["form_id"]
            }
            with self.client.post(url, name="/TBA ACCEPT DATA", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def create_tbu_request(self):
            url = target["tbu_request"]["endpoint"]
            data = {
                "user_id": target["tbu_request"]["user_id"],
                "debit_from": target["tbu_request"]["debit_from"],
                "username": target["tbu_request"]["username"],
                "account": target["tbu_request"]["account"],
                "amount_to_transfer": target["tbu_request"]["amount_to_transfer"],
                "next": "Continue",
                "form_token": target["tbu_request"]["form_token"],
                "form_id": target["tbu_request"]["form_id"]
            }
            with self.client.post(url, name="/TBU FILL IN DATA", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

            data = {
                "transfer_fee": None,
                "finish": "Continue",
                "form_token": target["tba_request"]["form_token"],
                "form_id": target["tba_request"]["form_id"]
            }
            with self.client.post(url, name="/TBU ACCEPT DATA", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(1)
        def create_owt_request(self):
            url = target["owt_request"]["endpoint"]
            data = {
                "user_id": target["owt_request"]["user_id"],
                "debit_from": target["owt_request"]["debit_from"],
                "beneficiary_bank_swift": target["owt_request"]["beneficiary_bank_swift"],
                "beneficiary_bank_name": target["owt_request"]["beneficiary_bank_name"],
                "beneficiary_bank_address": target["owt_request"]["beneficiary_bank_address"],
                "beneficiary_bank_location": target["owt_request"]["beneficiary_bank_location"],
                "beneficiary_bank_country": target["owt_request"]["beneficiary_bank_country"],
                "beneficiary_customer_name": target["owt_request"]["beneficiary_customer_name"],
                "beneficiary_customer_address": target["owt_request"]["beneficiary_customer_address"],
                "beneficiary_customer_iban": target["owt_request"]["beneficiary_customer_iban"],
                "information_ref": target["owt_request"]["information_ref"],
                "amount_to_transfer": target["owt_request"]["amount_to_transfer"],
                "currency": target["owt_request"]["currency"],
                "transfer_fee": None,
                "next": "Continue",
                "form_token": target["owt_request"]["form_token"],
                "form_id": target["owt_request"]["form_id"]
            }
            with self.client.post(url, name="/OWT FILL IN DATA", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

            data = {
                "finish": "Continue",
                "form_token": target["owt_request"]["form_token"],
                "form_id": target["owt_request"]["form_id"]
            }
            with self.client.post(url, name="/OWT ACCEPT DATA", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(5)
        def view_all_requests(self):
            url = target["all_requests"]["endpoint"] + "/export"
            params = {
                "op": target["all_requests"]["op"],
                "form_build_id": target["all_requests"]["form_build_id"],
                "form_token": target["all_requests"]["form_token"],
                "form_id": target["all_requests"]["form_id"]
            }
            with self.client.get(url, name="/ALL REQUESTS EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["all_requests"]["endpoint"] + "/print"
            with self.client.get(url, name="/ALL REQUESTS PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(4)
        def view_filtered_requests(self):
            url = target["all_requests"]["endpoint"] + "/export"
            params = {
                "date_from%5Bdate%5D": target["filtered_requests"]["date_from"],
                "date_to%5Bdate%5D": target["filtered_requests"]["date_to"],
                "currency": target["filtered_requests"]["currency"],
                "request_types": target["filtered_requests"]["request_types"],
                "request_status": target["filtered_requests"]["request_status"],
                "op": target["all_requests"]["op"],
                "form_build_id": target["all_requests"]["form_build_id"],
                "form_token": target["all_requests"]["form_token"],
                "form_id": target["all_requests"]["form_id"]
            }
            with self.client.get(url, name="/FILTERED REQUESTS EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["all_requests"]["endpoint"] + "/print"
            with self.client.get(url, name="/FILTERED REQUESTS PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(4)
        def view_request_by_id(self):
            url = target["all_requests"]["endpoint"] + "/export"
            params = {
                "request_id": target["request_by_id"]["id"],
                "op": target["all_requests"]["op"],
                "form_build_id": target["all_requests"]["form_build_id"],
                "form_token": target["all_requests"]["form_token"],
                "form_id": target["all_requests"]["form_id"]
            }
            with self.client.get(url, name="/REQUEST BY ID EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["all_requests"]["endpoint"] + "/print"
            with self.client.get(url, name="/REQUEST BY ID PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_transactions_by_user_id(self):
            url = target["user_tr_report"]["endpoint"] + "/export"
            params = {
                "user_id": target["user_tr_report"]["user_id"],
                "generate": "Generate",
                "form_build_id": target["user_tr_report"]["form_build_id"],
                "form_token": target["user_tr_report"]["form_token"],
                "form_id": target["user_tr_report"]["form_id"]
            }
            with self.client.get(url, name="/TRANSACTIONS BY USER ID EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["user_tr_report"]["endpoint"] + "/print"
            with self.client.get(url, name="/TRANSACTIONS BY USER ID PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_balance_by_user_id(self):
            url = target["user_balance_report"]["endpoint"] + "/export"
            params = {
                "user_id": target["user_balance_report"]["user_id"],
                "generate": "Generate",
                "form_build_id": target["user_balance_report"]["form_build_id"],
                "form_token": target["user_balance_report"]["form_token"],
                "form_id": target["user_balance_report"]["form_id"]
            }
            with self.client.get(url, name="/BALANCE BY USER ID EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["user_balance_report"]["endpoint"] + "/print"
            with self.client.get(url, name="/BALANCE BY USER ID PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_all_system_transactions(self):
            url = target["gsr_transactions"]["endpoint"] + "/export"
            params = {
                "generate": "Generate",
                "form_build_id": target["gsr_transactions"]["form_build_id"],
                "form_token": target["gsr_transactions"]["form_token"],
                "form_id": target["gsr_transactions"]["form_id"]
            }
            with self.client.get(url, name="/ALL SYSTEM TRANSACTIONS EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["gsr_transactions"]["endpoint"] + "/print"
            with self.client.get(url, name="/ALL SYSTEM TRANSACTIONS PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_all_system_balances(self):
            url = target["gsr_balances"]["endpoint"] + "/export"
            params = {
                "generate": "Generate",
                "form_build_id": target["gsr_balances"]["form_build_id"],
                "form_token": target["gsr_balances"]["form_token"],
                "form_id": target["gsr_balances"]["form_id"]
            }
            with self.client.get(url, name="/ALL SYSTEM BALANCES EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["gsr_balances"]["endpoint"] + "/print"
            with self.client.get(url, name="/ALL SYSTEM BALANCES PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_all_system_owt_requests(self):
            url = target["gsr_owt_requests"]["endpoint"] + "/export"
            params = {
                "generate": "Generate",
                "form_build_id": target["gsr_owt_requests"]["form_build_id"],
                "form_token": target["gsr_owt_requests"]["form_token"],
                "form_id": target["gsr_owt_requests"]["form_id"]
            }
            with self.client.get(url, name="/ALL SYSTEM OWT REQUESTS EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["gsr_owt_requests"]["endpoint"] + "/print"
            with self.client.get(url, name="/ALL SYSTEM OWT REQUESTS PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_system_overview(self):
            url = target["gsr_system_overview"]["endpoint"] + "/export"
            params = {
                "generate": "Generate",
                "form_build_id": target["gsr_system_overview"]["form_build_id"],
                "form_token": target["gsr_system_overview"]["form_token"],
                "form_id": target["gsr_system_overview"]["form_id"]
            }
            with self.client.get(url, name="/SYSTEM OVERVIEW EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["gsr_system_overview"]["endpoint"] + "/print"
            with self.client.get(url, name="/SYSTEM OVERVIEW PRINT", params=params,
                                 verify=False, catch_respone=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_all_system_interests(self):
            url = target["gsr_interests"]["endpoint"] + "/export"
            params = {
                "generate": "Generate",
                "form_build_id": target["gsr_interests"]["form_build_id"],
                "form_token": target["gsr_interests"]["form_token"],
                "form_id": target["gsr_interests"]["form_id"]
            }
            with self.client.get(url, name="/ALL SYSTEM INTERESTS EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["gsr_interests"]["endpoint"] + "/print"
            with self.client.get(url, name="/ALL SYSTEM INTERESTS PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_system_revenue(self):
            url = target["gsr_revenue"]["endpoint"] + "/export"
            params = {
                "source": target["gsr_revenue"]["source"],
                "currency": target["gsr_revenue"]["currency"],
                "generate": "Generate",
                "form_build_id": target["gsr_revenue"]["form_build_id"],
                "form_token": target["gsr_revenue"]["form_token"],
                "form_id": target["gsr_revenue"]["form_id"]
            }
            with self.client.get(url, name="/SYSTEM REVENUE EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["gsr_revenue"]["endpoint"] + "/print"
            with self.client.get(url, name="/SYSTEM REVENUE PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_system_access_log(self):
            url = target["gsr_access_log"]["endpoint"] + "/export"
            with self.client.get(url, name="/SYSTEM ACCESS LOG EXPORT", verify=False,
                                 catch_response=True) as response:
                assert_status_code(response)
            url = target["gsr_access_log"]["endpoint"] + "/print"
            with self.client.get(url, name="/SYSTEM ACCESS LOG PRINT", verify=False,
                                 catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_all_transactions_log(self):
            url = target["all_transactions_log"]["endpoint"] + "/export"
            params = {
                "type_1": target["all_transactions_log"]["type_1"],
                "items_per_page": target["all_transactions_log"]["items_per_page"]
            }
            with self.client.get(url, name="/ALL TRANSACTIONS LOG EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["all_transactions_log"]["endpoint"] + "/print"
            with self.client.get(url, name="/ALL TRANSACTIONS LOG PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_filtered_transactions_log(self):
            url = target["all_transactions_log"]["endpoint"] + "/export"
            params = {
                "type_1": target["filtered_transactions_log"]["type_1"],
                "date_filter%5Bvalue%5D%5Bdate%5D": target["filtered_transactions_log"]["date_from"],
                "date_filter_1%5Bvalue%5D%5Bdate%5D": target["filtered_transactions_log"]["date_to"],
                "items_per_page": target["all_transactions_log"]["items_per_page"]
            }
            with self.client.get(url, name="/FILTERED TRANSACTIONS LOG EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["all_transactions_log"]["endpoint"] + "/print"
            with self.client.get(url, name="/FILTERED TRANSACTIONS LOG PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_all_information_log(self):
            url = target["all_information_log"]["endpoint"] + "/export"
            params = {
                "type_1": target["all_information_log"]["type_1"],
                "items_per_page": target["all_information_log"]["items_per_page"]
            }
            with self.client.get(url, name="/ALL INFORMATION LOG EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["all_information_log"]["endpoint"] + "/print"
            with self.client.get(url, name="/ALL INFORMATION LOG PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_filtered_information_log(self):
            url = target["all_information_log"]["endpoint"] + "/export"
            params = {
                "type_1": target["filtered_information_log"]["type_1"],
                "items_per_page": target["all_information_log"]["items_per_page"]
            }
            with self.client.get(url, name="/FILTERED INFORMATION LOG EXPORT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)
            url = target["all_information_log"]["endpoint"] + "/print"
            with self.client.get(url, name="/FILTERED INFORMATION LOG PRINT", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_all_registration_requests(self):
            url = target["all_registration_requests"]["endpoint"]
            params = {
                "field_registr_request_status_value": target["all_registration_requests"]["status_value"],
                "items_per_page": target["all_registration_requests"]["items_per_page"]
            }
            with self.client.get(url, name="/ALL REGISTRATION REQUESTS", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_filtered_registration_requests(self):
            url = target["all_registration_requests"]["endpoint"]
            params = {
                "field_registration_request_from_value": target["filtered_registration_requests"]["from_value"],
                "field_registr_request_status_value": target["filtered_registration_requests"]["status_value"],
                "date_filter%5Bvalue%5D%5Bdate%5D": target["filtered_registration_requests"]["date_from"],
                "date_filter_1%5Bvalue%5D%5Bdate%5D": target["filtered_registration_requests"]["date_to"],
                "items_per_page": target["all_registration_requests"]["items_per_page"]
            }
            with self.client.get(url, name="/FILTERED REGISTRATION REQUESTS", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_registration_request_by_id(self):
            url = target["all_registration_requests"]["endpoint"]
            params = {
                "request_id": target["registration_request_by_id"]["request_id"],
                "field_registr_request_status_value": target["all_registration_requests"]["status_value"],
                "items_per_page": target["all_registration_requests"]["items_per_page"]
            }
            with self.client.get(url, name="/REGISTRATION REQUESTS BY ID", params=params,
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def create_user_profile(self):
            url = target["create_user_profile"]["endpoint"]
            data = {
                "field_profile_type[und]": target["create_user_profile"]["profile_type"],
                "field_user_first_name[und][0][value]": target["create_user_profile"]["first_name"],
                "field_user_last_name[und][0][value]": target["create_user_profile"]["last_name"],
                "name": target["create_user_profile"]["name"],
                "mail": target["create_user_profile"]["mail"],
                "field_user_confirm_email_address[und][0][value]": target["create_user_profile"]["mail"],
                "pass[pass1]": target["create_user_profile"]["password"],
                "pass[pass2]": target["create_user_profile"]["password"],
                "roles[5]": target["create_user_profile"]["role"],
                "field_user_status[und]": target["create_user_profile"]["status"],
                "field_user_document_type[und]": target["create_user_profile"]["doc_type"],
                "form_build_id": target["create_user_profile"]["form_build_id"],
                "form_token": target["create_user_profile"]["form_token"],
                "form_id": target["create_user_profile"]["form_id"],
                "notify": target["create_user_profile"]["notify"],
                "create": target["create_user_profile"]["create"]
            }
            with self.client.post(url, name="/CREATE USER PROFILE", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def view_account_types(self):
            url = target["account_types"]["endpoint"]
            with self.client.get(url, name="/ACCOUNT TYPES",
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def create_new_account(self):
            url = target["new_account"]["endpoint"]
            data = {
                "field_account_type[und]": target["new_account"]["field_account_type[und]"],
                "form_build_id": target["new_account"]["form_build_id"],
                "form_token": target["new_account"]["form_token"],
                "form_id": target["new_account"]["form_id"],
                "unique_field_override": target["new_account"]["unique_field_override"],
                "title": target["new_account"]["title"],
                "field_account_username[und][0][uid]": target["new_account"]["field_account_username[und][0][uid]"],
                "field_account_status[und]": target["new_account"]["field_account_status[und]"],
                "field_account_initial_balance[und][0][value]": target["new_account"]["field_account_initial_balance[und][0][value]"],
                "field_account_payment_options[und]": target["new_account"]["field_account_payment_options[und]"],
                "menu[parent]": target["new_account"]["menu[parent]"],
                "menu[weight]": target["new_account"]["menu[weight]"],
                "name": target["new_account"]["name"],
                "status": target["new_account"]["status"],
                "additional_settings__active_tab": target["new_account"]["additional_settings__active_tab"],
                "op": target["new_account"]["op"]
            }
            with self.client.post(url, name="/NEW ACCOUNT", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def navigate_to_messages(self):
            url = target["messages"]["endpoint"]
            with self.client.get(url, name="/MESSAGES",
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def read_message(self):
            url = target["read_message"]["endpoint"] + "/" + target["read_message"]["id"]
            with self.client.get(url, name="/MESSAGE READ",
                                 verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def send_message(self):
            url = target["send_message"]["endpoint"]
            data = {
                "recipient_types": target["send_message"]["recipient_types"],
                "group": target["send_message"]["group"],
                "recipient": target["send_message"]["recipient"],
                "subject": target["send_message"]["subject"],
                "body[value]": target["send_message"]["body[value]"],
                "body[format]": target["send_message"]["body[format]"],
                "form_build_id": target["send_message"]["form_build_id"],
                "form_token": target["send_message"]["form_token"],
                "form_id": target["send_message"]["form_id"],
                "op": target["send_message"]["op"]
            }
            with self.client.post(url, name="NEW MESSAGE", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

        # @task(3)
        def reply_to_message(self):
            url = target["reply_to_message"]["endpoint"] + "/" + target["reply_to_message"]["id"]
            data = {
                "body[value]": target["reply_to_message"]["body[value]"],
                "body[format]": target["reply_to_message"]["body[format]"],
                "form_build_id": target["reply_to_message"]["form_build_id"],
                "form_token": target["reply_to_message"]["form_token"],
                "form_id": target["reply_to_message"]["form_id"],
                "op": target["reply_to_message"]["op"]
            }
            with self.client.post(url, name="/REPLY TO MESSAGE", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)

        @task(3)
        def unblock_user_profile(self):
            url = target["unblock_user_profile"]["endpoint"]
            data = {
                "operation": target["unblock_user_profile"]["operation"],
                "op": target["unblock_user_profile"]["op"],
                "accounts[1269]": target["unblock_user_profile"]["accounts[1269]"],
                "form_build_id": target["unblock_user_profile"]["form_build_id"],
                "form_token": target["unblock_user_profile"]["form_token"],
                "form_id": target["unblock_user_profile"]["form_id"]
            }
            with self.client.post(url, name="/USER UNBLOCK", data=data,
                                  verify=False, catch_response=True) as response:
                assert_status_code(response)


class LoadTestUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://34.91.47.190"

    tasks = [UserBehavior]
