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

        @task(3)
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

        @task(3)
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

        @task(1)
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


class LoadTestUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://34.91.47.190"

    tasks = [UserBehavior]
