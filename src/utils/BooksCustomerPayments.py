import requests
from requests.structures import CaseInsensitiveDict
from ADNBooksAPI.settings import ZBOOKS_ORGANITATION_ID
import json
from czohobooks.utils.BooksConnection import BooksConnection

class BooksCustomerPayments(BooksConnection):
    def __init__(self):
        super().__init__()
        self.headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}


    def create_record(self,json_payment):
        """
            Query Params
            customer_id string (Required)
            Customer ID of the customer involved in the payment.
            payment_mode string (Required) Mode through which payment is made. This can be check, cash, creditcard, banktransfer, bankremittance, autotransaction or others. Max-length [100]
            amount double (Required) Amount paid in the respective payment.
            date string (Required) Date on which payment is made. Format [yyyy-mm-dd]
            reference_number string Reference number generated for the payment. A string of your choice can also be used as the reference number. Max-length [100]
            description string Description about the payment.
            invoices array (Required) List of invoices associated with the payment. Each invoice object contains invoice_id, invoice_number, date, invoice_amount, amount_applied and balance_amount.
            Show Sub-Attributes arrow
            exchange_rate double , default is 1 Exchange rate for the currency used in the invoices and customer's currency. The payment amount would be the multiplicative product of the original amount and the exchange rate.
            bank_charges double Denotes any additional bank charges.
            custom_fields array Additional fields for the payments.
            Show Sub-Attributes arrow
            invoice_id string (Required)
            Invoice ID of the required invoice.
            amount_applied double (Required) Amount paid for the invoice.
            tax_amount_withheld double Amount withheld for tax.
            account_id string ID of the cash/bank account the payment has to be deposited.
            contact_persons array IDs of the contact personsthe thank you mail has to be triggered.
        """
        json_data = json_payment

        headers = {
            "Content-Type": "application/json;charset=UTF-8", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_create = requests.post(
            f'https://books.zoho.com/api/v3/customerpayments?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json.dumps(json_data))
        return json_create.json()


    def get_records(self, queryparams,page = 1):
        """
        Query Params
            customer_name Search payments by customer name. Variants: customer_name_startswith and customer_name_contains. Max-len [100]
            reference_number Search payments by reference number. Variants: reference_number_startswith and reference_number_contains. Max-len [100]
            date
            amount Search payments by payment amount. Variants: amount_less_than, amount_less_equals, amount_greater_than and amount_greater_equals
            notes Search payments by customer notes. Variants: notes_startswith and notes_contains
            payment_mode Search payments by payment mode. Variants: payment_mode_startswith and payment_mode_contains
            filter_by Filter payments by mode.Allowed Values: PaymentMode.All, PaymentMode.Check, PaymentMode.Cash, PaymentMode.BankTransfer, PaymentMode.Paypal, PaymentMode.CreditCard, PaymentMode.GoogleCheckout, PaymentMode.Credit, PaymentMode.Authorizenet, PaymentMode.BankRemittance, PaymentMode.Payflowpro, PaymentMode.Stripe, PaymentMode.TwoCheckout, PaymentMode.Braintree and PaymentMode.Others
            sort_column search_text Search payments by reference number or customer name or payment description. Max-length [100]
            customer_id Customer ID of the customer involved in the payment.
            Example argummenst
                params= amunt=2000&filter=PaymentMode.All
         """

        request_query = {
            "url": f'https://books.zoho.com/api/v3/customerpayments?page={str(page)}&organization_id={ZBOOKS_ORGANITATION_ID}',
            "headers": self.headers,
        }
        if queryparams:
            for key, value in queryparams.items():
                request_query['url'] = f"{request_query['url']}&{key}={value}"

        get_customer_payment = requests.get(**request_query)
        bankt_collected = []

        if get_customer_payment.status_code == 200:
            bankt_collected = bankt_collected + get_customer_payment.json().get("customerpayments")
            has_more_pages = get_customer_payment.json().get("page_context").get("has_more_page")
            actual_page = get_customer_payment.json().get("page_context").get("page")

            response_json = {
                "customerpayments": bankt_collected,
                "has_more_pages": has_more_pages,
                "page": actual_page,
                "status_code": get_customer_payment.status_code,
                "code": get_customer_payment.json().get("code"),
                "message": get_customer_payment.json().get("message")
            }

        else:
            response_json = {"customerpayments": [],
                             "has_more_pages": False,
                             "page": 0,
                             "status_code": get_customer_payment.status_code,
                             "code": get_customer_payment.json().get("code"),
                             "message": get_customer_payment.json().get("message")}

        return response_json

    #Return payment of client
    def get_record(self,payment_id):
        """
            Query Params
                Payment id

        """
        headers = {
                 "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_create = requests.get(
            f'https://books.zoho.com/api/v3/customerpayments/{payment_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)

        return json_create.json()


    def update_record(self,payment_id,json_update):
        json_data=json_update
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_res = requests.put(
            f'https://books.zoho.com/api/v3/customerpayments/{payment_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)
        return json_res

    def delete_record(self,payment_id):
        """
            Query Params
                id of payment to delete
            reponse
            {
                "code": 0,
                "message": "The payment has been deleted."
            }
        """
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

        del_contact = requests.delete(
            f'https://books.zoho.com/api/v3/customerpayments/{payment_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)

        return del_contact.json()

    def refund_record_excess(self,payment_id ,json_payment):
        """
        Query Params
            date string (Required)
            Date on which payment is made. Format [yyyy-mm-dd]
            refund_mode string The method of refund. Max-length [50]
            reference_number string Reference number generated for the payment. A string of your choice can also be used as the reference number. Max-length [100]
            amount double (Required) Amount paid in the respective payment.
            exchange_rate double , default is 1 Exchange rate for the currency used in the invoices and customer's currency. The payment amount would be the multiplicative product of the original amount and the exchange rate.
            from_account_id string (Required) The account from which payment is refunded.
            description string Description about the payment.
        """
        json_data = json_payment

        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_create = requests.post(
            f'ttps://books.zoho.com/api/v3/customerpayments/{payment_id}/refunds?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)
        return json_create

    def get_refunds(self, customer_payment_id, page=1):
        """
        Query Params
            customer_name Search payments by customer name. Variants: customer_name_startswith and customer_name_contains. Max-len [100]
            reference_number Search payments by reference number. Variants: reference_number_startswith and reference_number_contains. Max-len [100]
            date
            amount Search payments by payment amount. Variants: amount_less_than, amount_less_equals, amount_greater_than and amount_greater_equals
            notes Search payments by customer notes. Variants: notes_startswith and notes_contains
            payment_mode Search payments by payment mode. Variants: payment_mode_startswith and payment_mode_contains
            filter_by Filter payments by mode.Allowed Values: PaymentMode.All, PaymentMode.Check, PaymentMode.Cash, PaymentMode.BankTransfer, PaymentMode.Paypal, PaymentMode.CreditCard, PaymentMode.GoogleCheckout, PaymentMode.Credit, PaymentMode.Authorizenet, PaymentMode.BankRemittance, PaymentMode.Payflowpro, PaymentMode.Stripe, PaymentMode.TwoCheckout, PaymentMode.Braintree and PaymentMode.Others
            sort_column search_text Search payments by reference number or customer name or payment description. Max-length [100]
            customer_id Customer ID of the customer involved in the payment.
            Example argummenst
                params= amunt=2000&filter=PaymentMode.All
         """


        request_query = {
            "url": f'$ curl https://books.zoho.com/api/v3/customerpayments/{customer_payment_id}/refunds?pages{str(page)}&organization_id={ZBOOKS_ORGANITATION_ID}',
            "headers": self.headers,
        }

        get_invoices_list_refunds = requests.get(**request_query)
        refunds_collected = []

        if get_invoices_list_refunds.status_code == 200:
            refunds_collected = refunds_collected + get_invoices_list_refunds .json().get("payment_refunds")
            has_more_pages = get_invoices_list_refunds.json().get("page_context").get("has_more_page")
            actual_page = get_invoices_list_refunds.json().get("page_context").get("page")

            result = {"payment_refunds": refunds_collected, "has_more_pages": has_more_pages, "page": actual_page,
                      "status_code": 200}
        else:
            result = {"payment_refunds": refunds_collected, "has_more_pages": False, "page": 0, "status_code": 404}

        return result


    def update_refunds(self,customer_payment_id,refund_id, json_update):
        """
            Query params:
            date string (Required) Date on which payment is made. Format [yyyy-mm-dd]
            refund_mode string The method of refund. Max-length [50]
            reference_number string Reference number generated for the payment. A string of your choice can also be used as the reference number. Max-length [100]
            amount double (Required) Amount paid in the respective payment.
            exchange_rate double , default is 1
            Exchange rate for the currency used in the invoices and customer's currency. The payment amount would be the multiplicative product of the original amount and the exchange rate.
            description string Description about the payment.
            from_account_id string (Required)
            The account from which payment is refunded.
        """
        json_data = json_update
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_res = requests.put(
            f'https://books.zoho.com/api/v3/customerpayments/{customer_payment_id}/refunds/{refund_id}?organization_id{ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)
        return json_res


    def get_details_refunds(self,customer_payment_id):
        """

        """
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        get_records = requests.get(
            f'ttps://books.zoho.com/api/v3/customerpayments/{customer_payment_id}/refunds?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)
        return get_records.json()
