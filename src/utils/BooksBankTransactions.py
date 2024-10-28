import requests
from ADNBooksAPI.settings import ZBOOKS_ORGANITATION_ID
from czohobooks.utils.BooksConnection import BooksConnection

class BooksBankTransactions(BooksConnection):
    def __init__(self):
        super().__init__()
        self.headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

        # Create a bank account or a credit card account for your organization.

    def create_record(self, json_transaction):
        """
        Arguments
                from_account_id string The account ID from which money will be transferred(Mandatory for specific type of transactions). These accounts differ with respect to transaction_type. Ex: To a bank account, from-account can be: bank , card, income, refund. To a card account, from account can be: bank, card, refund.
                to_account_id string ID of the account to which the money gets transferred(Mandatory for specific type of transactions). Ex: From a bank account, to-account can be: bank, card, drawings, expense,credit notes. From a card account, to-account can be: card, bank, expense.
                transaction_type string (Required) Type of the transaction.
                Allowed transaction types : deposit, refund(*Supported only in Credit Card accounts), transfer_fund, card_payment, sales_without_invoices, expense_refund, owner_contribution, interest_income, other_income, owner_drawings, sales_return
                Note: You will not be able to create the following module-specific transaction types under Bank Transaction endpoints :
                Expense, Vendor Advance/Vendor Payment/Bill Payment, Vendor Credit Refund, Vendor Payment Refund, Customer Advance/Customer Payment, Credit Note Refund, Payment Refund. Hence, refer them in their repective modules.
                amount double Amount of the transaction
                payment_mode string Mode of payment for the transaction. (not applicable for transfer_fund, card_payment, owner_drawings). Ex:cash, cheque, etc.,
                exchange_rate integer The foreign currency exchange rate value.
                date string Transaction date.
                customer_id string ID of the customer or vendor.
                reference_number string
                Reference Number of the transaction
                description string A brief description about the transaction.
                currency_id string The currency ID involved in the transaction.
                ID of the tax or tax group applied
                is_inclusive_tax boolean Check if transaction is tax Inclusive
                tags array Show Sub-Attributes arrow
                from_account_tags array Show Sub-Attributes arrow
                to_account_tags  array Show Sub-Attributes arrow
                documents  array List of files to be attached to a particular transaction.
                bank_charges double Bank Charges applied to the transaction
                user_id  long ID of the User involved in the Transaction
                custom_fields array

            Example:
                {
                "from_account_id": "460000000070003",
                "to_account_id": "460000000048001",
                "transaction_type": "deposit",
                "amount": 2000,
                "payment_mode": "Cash",
                "exchange_rate": 1,
                "date": "2013-10-01",
                "customer_id": "460000000000111",
                "reference_number": "Ref-121",
                "description": "string",
                "currency_id": "460000000000097",
                "tax_id": "string",
                "is_inclusive_tax": false,
                "tags": [
                    {
                        "tag_id": 0,
                        "tag_option_id": 0
                    }
                ],
                "from_account_tags": [
                    {
                        "tag_id": 0,
                        "tag_option_id": 0
                    }
                ],
                "to_account_tags": [
                    {
                        "tag_id": 0,
                        "tag_option_id": 0
                    }
                ],
                "documents": [
                    {
                        "file_name": null,
                        "document_id": null
                    }
                ],
                "bank_charges": 0,
                "user_id": 0,
                "tax_authority_id": "string",
                "tax_exemption_id": "string",
                "custom_fields": [
                    {
                        "custom_field_id": 0,
                        "index": 0,
                        "label": "string",
                        "value": "string"
                    }
                ]
            }
        """
        json_data = json_transaction
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_create = requests.post(
            f'https://books.zoho.com/api/v3/banktransactions?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)
        return json_create.json()

    # List all transactions bank and credit card accounts for your organization.
    def get_records(self,queryparams,page=1):
        """
            Query Parameters account_id transaction_type
            date Start and end date, to provide a range within which the transaction date exist. Variants: date_start and date_end
            amount Start and end amount, to provide a range within which the transaction amount exist. Variants: amount_start and amount_end
            status Transaction status wise list view - All, uncategorized, manually_added, matched, excluded, categorized
            reference_number Search using Reference Number of the transaction
            filter_by Filters the transactions based on the allowed types. Allowed Values: Status.All, Status.Uncategorized, Status.Categorized, Status.ManuallyAdded, Status.Excluded and Status.Matched.
            sort_column Sorts the transactions based on the allowed sort types. Allowed Values: date.
            transaction_status Transaction status wise list view - All, uncategorized, manually_added, matched, excluded, categorized
            search_text Search Transactions by contact name or description
        """
        request_query = {
            "url": f'https://books.zoho.com/api/v3/banktransactions?page={str(page)}&organization_id={ZBOOKS_ORGANITATION_ID}',
            "headers": self.headers,
        }
        if queryparams:
            for key, value in queryparams.items():
                request_query['url'] = f"{request_query['url']}&{key}={value}"

        get_bankt_list_response = requests.get(**request_query)
        bankt_collected = []

        if get_bankt_list_response.status_code == 200:
            res= ( get_bankt_list_response.json())
            bankt_collected = bankt_collected + get_bankt_list_response.json().get("banktransactions")
            has_more_pages = get_bankt_list_response.json().get("page_context").get("has_more_page")
            actual_page = get_bankt_list_response.json().get("page_context").get("page")

            response_json = {
                "banktransactions": bankt_collected,
                "has_more_pages": has_more_pages,
                "page": actual_page,
                "status_code": get_bankt_list_response.status_code,
                "code": get_bankt_list_response.json().get("code"),
                "message": get_bankt_list_response.json().get("message")
            }

        else:
            response_json = {"banktransactions": [],
                             "has_more_pages": False,
                             "page": 0,
                             "status_code": get_bankt_list_response.status_code,
                             "code": get_bankt_list_response.json().get("code"),
                             "message": get_bankt_list_response.json().get("message")}

        return response_json



    def get_record(self,transaction_id):
        """
            Params Query
                Transaction id
            Response:
            {"code": 0, "message": "success", "banktransaction": {"transaction_id": "2826459000000212455", "from_account_id": "2826459000000000370", "from_account_name": "Advance Tax", "to_account_id": "2826459000000212179", "to_account_name": "Colones Prueba", "transaction_type": "deposit", "currency_id": "2826459000000074082", "currency_code": "CRC", "payment_mode": "Cash", "exchange_rate": 1.0, "date": "2022-02-01", "customer_id": "2826459000000211189", "customer_name": "Test customer", "vendor_id": "", "vendor_name": "", "vendor_country_code": "", "reference_number": "REF - 2661984", "description": "Crd.Dir.SINPE NELLY SOTO SEGURA", "bank_charges": 0.0, "tax_id": "", "documents": [], "is_inclusive_tax": false, "tax_name": "", "tax_percentage": 0, "tax_amount": 0.0, "sub_total": 215000.0, "total": 215000.0, "bcy_total": 215000.0, "amount": 215000.0, "imported_transactions": [{"imported_transaction_id": "2826459000000212343", "date": "2022-02-01", "amount": 215000.0, "payee": "", "description": "Crd.Dir.SINPE NELLY SOTO SEGURA", "reference_number": "REF - 2661984", "status": "categorized", "account_id": "2826459000000212179"}], "tags": [], "line_items": [{"from_account_id": "2826459000000000370", "from_account_name": "Advance Tax", "payment_mode": "Cash", "customer_id": "2826459000000211189", "customer_name": "2826459000000211189", "vendor_id": "", "vendor_name": "", "sub_total": 215000.0, "total": 215000.0, "bcy_total": 215000.0, "tags": []}], "custom_fields": [], "custom_field_hash": {}}}

        """
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        get_record = requests.get(
            f'https://books.zoho.com/api/v3/banktransactions/{transaction_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)
        return get_record.json()

    def delete_record(self,transaction_id):
        """
        Params Query
                Transaction id

        """
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        del_record = requests.delete(
            f'https://books.zoho.com/api/v3/banktransactions/{transaction_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)
        return del_record.json()

    def match_record(self,transaction_id,transaction_json):
        """
             Params Query
                     Transaction id

         """
        data=transaction_json
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        match_record = requests.post(
            f'https://books.zoho.com/api/v3/banktransactions/uncategorized/{transaction_id}/match?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers,data=data)
        return match_record.json()

    def get_macth_record(self,queryparams,transaction_id):
        """
            Params Query
             Transaction id

             transaction_type Type of the transaction.  Allowed transaction types : deposit, refund(*Supported only in Credit Card accounts), transfer_fund, card_payment, sales_without_invoices, expense_refund, owner_contribution, interest_income, other_income, owner_drawings, sales_return
            Note: You will not be able to create the following module-specific transaction types under Bank Transaction endpoints :
            Expense, Vendor Advance/Vendor Payment/Bill Payment, Vendor Credit Refund, Vendor Payment Refund, Customer Advance/Customer Payment, Credit Note Refund, Payment Refund. Hence, refer them in their repective modules.
             date_before Date before which Transactions are to be filtered
            amount_start Starting amout with which transactions are to be filtered
            amount_end Starting amout with which transactions are to be filtered
            contact Contact person name, involved in the transaction.
            reference_number Reference Number of the transaction
            show_all_transactions Check if all transactions must be shown



         """
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        match_record = requests.get(
            f'https://books.zoho.com/api/v3/banktransactions/uncategorized/{transaction_id}/match?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)
        return match_record




