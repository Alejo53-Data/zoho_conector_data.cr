import requests
from settings import ZBOOKS_ORGANITATION_ID
from src.utils.BooksConnection import BooksConnection


class BooksBankAccounts(BooksConnection):
    def __init__(self):
        super().__init__()
        self.headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

    #Create a bank account or a credit card account for your organization.
    def create_record(self, json_client):
        """

        Params Query

            account_name string (Required)  Name of the account
            account_type string(Required)  Type of the account
            account_number  string Number associated with the Bank Account
            account_code string  Code of the Account
            currency_id string ID of the Currency associated with the Account
            currency_code string Code of the currency associated with the Bank Account
            description string Description of the Account
            bank_name string Name of the Bank
            routing_number string Routing Number of the Account
            is_primary_account boolean Check if the Account is Primary Account in Zoho Books
            is_paypal_account boolean Check if the Account is Paypal Account
            paypal_type string The type of Payment for the Paypal Account. Allowed Values : standard and adaptive
            paypal_email_address string Email Address of the Paypal account.

        """
        json_data = json_client
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_create = requests.post(
            f'https://books.zoho.com/api/v3/bankaccounts?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)
        return json_create.json()

    #List all bank and credit card accounts for your organization.
    def get_records(self,queryparams,page=1):
        """
         Filter the account by their status. Allowed Values: Status.All, Status.Active and Status.Inactive.
         Sort the values based on the allowed values. Allowed Values: account_name,account_type and account_code.

        """

        request_query = {
            "url": f'https://books.zoho.com/api/v3/bankaccounts?page={str(page)}&organization_id={ZBOOKS_ORGANITATION_ID}',
            "headers": self.headers,
        }
        if queryparams:
            for key, value in queryparams.items():
                request_query['url'] = f"{request_query['url']}&{key}={value}"

        get_customer_payment = requests.get(**request_query)
        bankt_collected = []
        res = (get_customer_payment.json())

        if get_customer_payment.status_code == 200:
            res = (get_customer_payment.json())
            bankt_collected = bankt_collected + get_customer_payment.json().get("bankaccounts")
            has_more_pages = get_customer_payment.json().get("page_context").get("has_more_page")
            actual_page = get_customer_payment.json().get("page_context").get("page")

            response_json = {
                "bankaccounts": bankt_collected,
                "has_more_pages": has_more_pages,
                "page": actual_page,
                "status_code": get_customer_payment.status_code,
                "code": get_customer_payment.json().get("code"),
                "message": get_customer_payment.json().get("message")
            }

        else:
            response_json = {"bankaccounts": [],
                             "has_more_pages": False,
                             "page": 0,
                             "status_code": get_customer_payment.status_code,
                             "code": get_customer_payment.json().get("code"),
                             "message": get_customer_payment.json().get("message")}

        return response_json



    #Modify the account that was created.
    def update_record(self, account_id,json_client):
        """
            account_name string (Required) Name of the account
            account_type string (Required) Type of the account
            account_number string Number associated with the Bank Account
            account_code string Code of the Account
            currency_id string ID of the Currency associated with the Account
            currency_code string Code of the currency associated with the Bank Account
            description string Description of the Account
            bank_name string Name of the Bank
            routing_number string Routing Number of the Account
            is_primary_account boolean Check if the Account is Primary Account in Zoho Books
            is_paypal_account boolean Check if the Account is Paypal Account
            paypal_type string The type of Payment for the Paypal Account. Allowed Values : standard and adaptive
            paypal_email_address string Email Address of the Paypal account.
        """
        json_data = json_client
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_create = requests.put(
            f'https://books.zoho.com/api/v3/bankaccounts/{account_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)
        return json_create.json()

    def get_record(self, account_id):
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        get_details = requests.get(
            f'https://books.zoho.com/api/v3/bankaccounts/{account_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)
        return get_details.json()
    # Delete a bank account from your organization.
    def del_record(self,account_id):
        """
         Params Query
            account id

        response:
        {
            "code": 0,
            "message": "The account has been deleted."
        }
        error
            {"code": 1043, "message": "The account you are trying to delete does not exist."}
        """
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        del_bank = requests.delete(
            f'https://books.zoho.com/api/v3/bankaccounts/{account_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)
        return del_bank.json()

    #Make an account active or inactivate
    def mark_record(self,account_id,status):
        """
        Arguments
            account id | Required | valid id of bank account
            option | Required | "activate" to activate mark  "inactivate" to inactivate  mark


        Response:
            for optn 1:
                {"code": 0, "message": "The account has been marked as active.", "data": []}
            for optn 0:
                {"code": 0, "message": "The account has been marked as inactivate.", "data": []}
        err:
            {"code": 5, "message": "Invalid URL Passed"}

        """
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        mark_acc = requests.post(
            f'https://books.zoho.com/api/v3/bankaccounts/{account_id}/{status}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)
        return mark_acc.json()

    def import_record(self,json_bank):
        """
        Arguments:
            account_id string (Required) ID of the Bank/Credit Card account
            start_date string Least date in the transaction set
            end_date string Greatest date in the transaction set
            transactions array (Required)

        example:
            {
                "account_id": "460000000050127",
                "start_date": "2019-01-01",
                "end_date": "2019-01-02",
                "transactions": [
                    {
                        "transaction_id": "XXXXSCD01",
                        "date": "2012-01-14",
                        "debit_or_credit": "credit",
                        "amount": 7500,
                        "payee": "Bowman and Co",
                        "description": "Electronics purchase",
                        "reference_number": "Ref-2134"
                    }
                ]
            }
        response:
            {"code": 0, "message": "Your bank statement has been imported."}
        """
        data=json_bank
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        import_record = requests.post(
            f'https://books.zoho.com/api/v3/bankstatements?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=data)
        return import_record.json()

    def get_last_import(self,account_id):
        """
        arguments:

            account id | Required | valid id of bank account
        response:
            {
            "code": 0,
            "message": "success",
            "statement": [
                {
                    "statement_id": "460000000049013",
                    "from_date": "2012-01-12",
                    "to_date": "2012-01-19",
                    "source": "csv",
                    "transactions": [
                        {
                            "transaction_id": "460000000049023",
                            "debit_or_credit": "credit",
                            "date": "2012-01-14",
                            "customer_id": "460000000026049",
                            "payee": "Bowman and Co",
                            "reference_number": "Ref-2134",
                            "transaction_type": "expense",
                            "amount": 7500,
                            "status": "categorized"
                        }
                    ]
                }

        """
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        lastimp = requests.get(
            f'https://books.zoho.com/api/v3/bankaccounts/{account_id}/statement/lastimported?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)
        return lastimp.json()


    def delete_last_import(self,account_id,transaction_id):
        """
            Arguments
                account id | Required | valid id of bank account
                transacttion id | Required | id transacttion to delete
            response
                {"code": 0, "message": "The last imported statement has been deleted."}
        """
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        del_lastimp = requests.delete(
            f'https://books.zoho.com/api/v3/bankaccounts/{account_id}/statement/{transaction_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)
        return del_lastimp.json()





