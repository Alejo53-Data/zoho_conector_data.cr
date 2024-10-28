import requests
from requests.structures import CaseInsensitiveDict
from settings import ZBOOKS_ORGANITATION_ID

from src.utils.BooksConnection import BooksConnection


class BooksContacts(BooksConnection):

    def __init__(self):
        super().__init__()
        self.headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

    #Create record in BooksContacts
    def create_record(self, json_client):
        """
        Required *  optional -
        contact_name: -Display Name of the contact. Max-length [200] *
        company_name: Company Name of the contact. Max-length [200] -
        website: -
        language_code: language of a contact. allowed values de,en,es,fr,it,ja,nl,pt,pt_br,sv,zh,en_gb -
        contact_type: Contact type of the contact -
        customer_sub_type : Type of the customer -
        credit_limit: Credit limit for a customer -
        tags: Filter all your reports based on the tag -
        is_portal_enabled: To enable client portal for the contact. Allowed value is true and false. -
        currency_id: Currency ID of the customer's currency. -
        payment_terms: Net payment term for the customer. -
        payment_terms_label: Label for the paymet due details. -
        notes: Commennts about the payment made by the contact. -
        billing_address:-
            attention
            address
            street2
            city
            state
            Optional
            zip
            country
            fax
            phone
        shipping_address
        attention: -
            address
            street2
            city
            state
            Optional
            zip
            country
            fax
            phone
        contact_persons:-
            salutation:
            first_name:    Max-length [100]
            last_name :   Max-length [100]
            email:
            phone:  Search contacts by phone number of the contact person. Variants: phone_startswith and phone_contains
            mobile:
            designation:
            department:
            skype:-
            is_primary_contact To mark contact person as primary for contact. Allowed value is true only.
            enable_portal To enable client portal for the primary contact. Allowed value is true and false.
            default_templates:
        custom_fields:-
            index:Index of the custom field. It can hold any value from 1 to 10.
            value
        opening_balance_amount: Opening balance amount for a contact.
        exchange_rate: Exchange rate for the opening balance.
        vat_reg_no:-
        owner_id:-
        tax_reg_no:-
        country_code:-
        vat_treatment:-
        tax_treatment: VAT treatment of the contact.Allowed Values: vat_registered,vat_not_registered,gcc_vat_not_registered,gcc_vat_registered,non_gcc,dz_vat_registered and dz_vat_not_registered.
        place_of_contact:-
        gst_no 15 digit GST identification number of the customer/vendor.
        gst_treatment Choose whether the contact is GST registered/unregistered/consumer/overseas. Allowed values are business_gst , business_none , overseas , consume
        tax_authority_name Enter tax authority name.
        avatax_exempt_no Exemption certificate number of the customer.
        avatax_use_code:-
        tax_exemption_id:-
        tax_exemption_code:-
        tax_authority_id:-
        tax_id:-
        is_taxab6le:  Boolean to track the taxability of the customer.-
        facebook:-
        twitter:-
        track_1099: Boolean to track a contact for 1099 reporting.-
        tax_id_type: Tax ID type of the contact, it can be SSN, ATIN, ITIN or EIN.-
        tax_id_value:-

        POST
        -H "Content-Type: application/json;charset=UTF-8"
        -H "Authorization: Zoho-oauthtoken 1000.41d9f2cfbd1b7a8f9e314b7aff7bc2d1.8fcc9810810a216793f385b9dd6e125f"
        -d '{
            "contact_name": "Bowman and Co",
            "company_name": "Bowman and Co",
            "website": "www.bowmanfurniture.com",
            "language_code": "string",
            "contact_type": "customer",
            "customer_sub_type": "business",
            "credit_limit": 1000,
            "tags": [
                {
                    "tag_id": 462000000009070,
                    "tag_option_id": 462000000002670
                }
            ],
            "is_portal_enabled": true,
            "currency_id": 460000000000097,
            "payment_terms": 15,
            "payment_terms_label": "Net 15",
            "notes": "Payment option : Through check",
            "billing_address": {
                "attention": "Mr.John",
                "address": "4900 Hopyard Rd",
                "street2": "Suite 310",
                "state_code": "CA",
                "city": "Pleasanton",
                "state": "CA",
                "zip": 94588,
                "country": "U.S.A",
                "fax": "+1-925-924-9600",
                "phone": "+1-925-921-9201"
            },
            "shipping_address": {
                "attention": "Mr.John",
                "address": "4900 Hopyard Rd",
                "street2": "Suite 310",
                "state_code": "CA",
                "city": "Pleasanton",
                "state": "CA",
                "zip": 94588,
                "country": "U.S.A",
                "fax": "+1-925-924-9600",
                "phone": "+1-925-921-9201"
            },
            "contact_persons": "Contact persons of a contact.",
            "default_templates": {
                "invoice_template_id": 460000000052069,
                "estimate_template_id": 460000000000179,
                "creditnote_template_id": 460000000000211,
                "purchaseorder_template_id": 460000000000213,
                "salesorder_template_id": 460000000000214,
                "retainerinvoice_template_id": 460000000000215,
                "paymentthankyou_template_id": 460000000000216,
                "retainerinvoice_paymentthankyou_template_id": 460000000000217,
                "invoice_email_template_id": 460000000052071,
                "estimate_email_template_id": 460000000052073,
                "creditnote_email_template_id": 460000000052075,
                "purchaseorder_email_template_id": 460000000000218,
                "salesorder_email_template_id": 460000000000219,
                "retainerinvoice_email_template_id": 460000000000220,
                "paymentthankyou_email_template_id": 460000000000221,
                "retainerinvoice_paymentthankyou_email_template_id": 460000000000222
            },
            "custom_fields": [
                {
                    "index": 1,
                    "value": "GBGD078"
                }
            ],
            "opening_balance_amount": 1200,
            "exchange_rate": 1,
            "vat_reg_no": "string",
            "owner_id": 460000000016051,
            "tax_reg_no": 12345678912345,
            "country_code": "string",
            "vat_treatment": "string",
            "tax_treatment": "string",
            "place_of_contact": "TN",
            "gst_no": "22AAAAA0000A1Z5",
            "gst_treatment": "business_gst",
            "tax_authority_name": "string",
            "avatax_exempt_no": "string",
            "avatax_use_code": "string",
            "tax_exemption_id": 11149000000061054,
            "tax_exemption_code": "string",
            "tax_authority_id": 11149000000061052,
            "tax_id": 11149000000061058,
            "is_taxable": true,
            "facebook": "zoho",
            "twitter": "zoho",
            "track_1099": true,
            "tax_id_type": "string",
            "tax_id_value": "string"
        }'
        """

        json_data=json_client
        #headers = CaseInsensitiveDict()
        #headers["Content-Type"] = "application/json"
        #headers["Content-Type"]
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_create = requests.post(
            f'https://books.zoho.com/api/v3/contacts/?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)


        return json_create.json()


        # new_customer_custom_fields_list = {{"index":1,"value":"Cédula Jurídica"},{"index":2,"value":cedula_customer},{"index":3,"value":numeroCircuito},{"index":15,"value":segmento_customer},{"label":"Creado por ZM","value":"true"},{"label":"Exonerado","value":is_exonerado_customer}};
        # vendor = zoho.books.createRecord("Contacts",booksID,{"contact_name":razon_social_customer,"customer_name":razon_social_customer,"company_name":razon_social_customer,"contact_type":"customer","contact_persons":{{"email":contact_email,"phone":contact_phone,"first_name":contact_first_name,"last_name":contact_last_name}},"currency_id":customer_currency_id,"custom_fields":new_customer_custom_fields_list},"booksitems");

        return json_create.json()

    #Ruturn all records of zohobooks
    def get_records(self, queryparams = {}, page = 1):
        """
        Return all contacts

        Query Parameter as DICT
            contact_name| Optional | Search contacts by contact name. Max-length [100] Variants: contact_name_startswith and contact_name_contains. Max-length [100]
            company_name | Optional | Search contacts by company name. Max-length [100] Variants: company_name_startswith and company_name_contains
            first_name | Optional | Search contacts by first name of the contact person. Max-length [100] Variants: first_name_startswith and first_name_contains
            last_name | Optional |  Search contacts by last name of the contact person. Max-length [100] Variants: last_name_startswith and last_name_contains
            address | Optional | Search contacts by any of the address fields. Max-length [100] Variants: address_startswith and address_contains
            email | Optional | Search contacts by email of the contact person. Max-length [100] Variants: email_startswith and email_contains
            phone | Optional | Search contacts by phone number of the contact person. Max-length [100] Variants: phone_startswith and phone_contains
            filter_by | Optional | Filter contacts by status. Allowed Values: Status.All, Status.Active, Status.Inactive, Status.Duplicate and Status.Crm
            search_text | Optional | Search contacts by contact name or notes. Max-length [100]
            sort_column | Optional | Sort contacts. Allowed Values: contact_name, first_name, last_name, email, outstanding_receivable_amount, created_time and last_modified_time
            organization_id | Required | ID of the organization

        Test Response
        {
          'contact_id': '1990571000002165003',
          'contact_name': '2CO.COM',
          'customer_name': '2CO.COM',
          'vendor_name': '2CO.COM',
          'company_name': '2CO.COM',
          'website': '',
          'language_code': '',
          'language_code_formatted': '',
          'contact_type': 'vendor',
          'contact_type_formatted': 'Proveedores',
          'status': 'active',
          'customer_sub_type': 'business',
          'source': 'csv',
          'is_linked_with_zohocrm': False,
          'payment_terms': 0,
          'payment_terms_label': 'Pagadero a la recepción',
          'currency_id': '1990571000000000097',
          'twitter': '',
          'facebook': '',
          'currency_code': 'USD',
          'outstanding_receivable_amount': 0.0,
          'outstanding_receivable_amount_bcy': 0.0,
          'outstanding_payable_amount': 0.0,
          'outstanding_payable_amount_bcy': 0.0,
          'unused_credits_receivable_amount': 0.0,
          'unused_credits_payable_amount': 0.0,
          'first_name': '',
          'last_name': '',
          'email': '',
          'phone': '',
          'mobile': '',
          'portal_status': 'disabled',
          'created_time': '2021-11-07T09:19:52-0600',
          'created_time_formatted': '07 nov 2021',
          'last_modified_time': '2022-03-02T04:34:17-0600',
          'last_modified_time_formatted': '02 mar 2022',
          'custom_fields': [

          ],
          'custom_field_hash': {

          },
          'ach_supported': False,
          'has_attachment': False
        },

        """
        request_query = {
            "url": f'https://books.zoho.com/api/v3/contacts?page={str(page)}&organization_id={ZBOOKS_ORGANITATION_ID}',
            "headers": self.headers,
        }
        if queryparams:
            for key, value in queryparams.items():
                request_query['url'] = f"{request_query['url']}&{key}={value}"

        get_contacts_list_response = requests.get(**request_query)
        contacts_collected = []


        if get_contacts_list_response.status_code == 200:
            contacts_collected = contacts_collected + get_contacts_list_response.json().get("contacts")
            has_more_pages = get_contacts_list_response.json().get("page_context").get("has_more_page")
            actual_page = get_contacts_list_response.json().get("page_context").get("page")

            response_json={
                "contacts": contacts_collected,
                "has_more_pages": has_more_pages,
                "page": actual_page,
                "status_code":get_contacts_list_response.status_code,
                "code":get_contacts_list_response.json().get("code"),
                "message":get_contacts_list_response.json().get("message")
            }

        else:
            response_json = {"contacts": [],
                             "has_more_pages": False,
                             "page": 0,
                             "status_code": get_contacts_list_response.status_code,
                             "code": get_contacts_list_response.json().get("code"),
                             "message": get_contacts_list_response.json().get("message")}

        return response_json

    #Return a single contact of zohobooks, need a client id
    def get_record(self,idclient):
        """
        Get a single record, register contact on organization\

        Arguments
            contact_persons | Required | ID of the contact person

        Query Params as DICT
            organization_id |Required| ID of the organization
        """
        get_single_contatcs = requests.get(
            f'https://books.zoho.com/api/v3/contacts/{idclient}?organization_id={ZBOOKS_ORGANITATION_ID}', headers=self.headers)

        if get_single_contatcs.status_code == 200:

            response_json = {"contact": get_single_contatcs.json().get("contact"),
                             "status_code": get_single_contatcs.status_code,
                             "code": get_single_contatcs.json().get("code"),
                             "message": get_single_contatcs.json().get("message")}
        else:
            response_json={"contact":{},"status_code":get_single_contatcs.status_code,"code":get_single_contatcs.json().get("code"),"message":get_single_contatcs.json().get("message")}

        return response_json

    #update Single record of  books contatcs Need to finish 2
    def update_record(self,idclient,json_client):
        """
        PUT /contacts/{contact_id}
       {
            "contact_name": "Bowman and Co",
            "company_name": "Bowman and Co",
            "payment_terms": 15,
            "payment_terms_label": "Net 15",
            "contact_type": "customer",
            "customer_sub_type": "business",
            "currency_id": 460000000000097,
            "opening_balance_amount": 1200,
            "exchange_rate": 1,
            "credit_limit": 1000,
            "tags": [
                {
                    "tag_id": 462000000009070,
                    "tag_option_id": 462000000002670
                }
            ],
            "website": "www.bowmanfurniture.com",
            "owner_id": 460000000016051,
            "custom_fields": [
                {
                    "index": 1,
                    "value": "GBGD078",
                    "label": "VAT ID"
                }
            ],
            "billing_address": {
                "attention": "Mr.John",
                "address": "4900 Hopyard Rd",
                "street2": "Suite 310",
                "state_code": "CA",
                "city": "Pleasanton",
                "state": "CA",
                "zip": 94588,
                "country": "U.S.A",
                "fax": "+1-925-924-9600",
                "phone": "+1-925-921-9201"
            },
            "shipping_address": {
                "attention": "Mr.John",
                "address": "4900 Hopyard Rd",
                "street2": "Suite 310",
                "state_code": "CA",
                "city": "Pleasanton",
                "state": "CA",
                "zip": 94588,
                "country": "U.S.A",
                "fax": "+1-925-924-9600",
                "phone": "+1-925-921-9201"
            },
            "contact_persons": [
                {
                    "contact_person_id": 460000000026051,
                    "salutation": "Mr",
                    "first_name": "Will",
                    "last_name": "Smith",
                    "email": "willsmith@bowmanfurniture.com",
                    "phone": "+1-925-921-9201",
                    "mobile": "+1-4054439562",
                    "designation": "Sales Executive",
                    "department": "Sales and Marketing",
                    "skype": "Zoho",
                    "is_primary_contact": true,
                    "enable_portal": true
                }
            ],
            "default_templates": {
                "invoice_template_id": 460000000052069,
                "estimate_template_id": 460000000000179,
                "creditnote_template_id": 460000000000211,
                "purchaseorder_template_id": 460000000000213,
                "salesorder_template_id": 460000000000214,
                "retainerinvoice_template_id": 460000000000215,
                "paymentthankyou_template_id": 460000000000216,
                "retainerinvoice_paymentthankyou_template_id": 460000000000217,
                "invoice_email_template_id": 460000000052071,
                "estimate_email_template_id": 460000000052073,
                "creditnote_email_template_id": 460000000052075,
                "purchaseorder_email_template_id": 460000000000218,
                "salesorder_email_template_id": 460000000000219,
                "retainerinvoice_email_template_id": 460000000000220,
                "paymentthankyou_email_template_id": 460000000000221,
                "retainerinvoice_paymentthankyou_email_template_id": 460000000000222
            },
            "notes": "Payment option : Through check",
            "vat_reg_no": "string",
            "tax_reg_no": 12345678912345,
            "country_code": "string",
            "tax_treatment": "string",
            "vat_treatment": "string",
            "place_of_contact": "TN",
            "gst_no": "22AAAAA0000A1Z5",
            "gst_treatment": "business_gst",
            "tax_authority_name": "string",
            "avatax_exempt_no": "string",
            "avatax_use_code": "string",
            "tax_exemption_id": 11149000000061054,
            "tax_exemption_code": "string",
            "tax_authority_id": 11149000000061052,
            "tax_id": 11149000000061058,
            "is_taxable": true,
            "facebook": "zoho",
            "twitter": "zoho",
            "track_1099": true,
            "tax_id_type": "string",
            "tax_id_value": "string"
        }'
        """

        json_data= json_client
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_update = requests.put(
            f'https://books.zoho.com/api/v3/contacts/{idclient}?organization_id=696634191',
            headers=headers, data=json_data)

        return json_update.json()

    #Delete contact
    def delete_record(self,idclient):
        """
        {
                "code": 0,
                "message": "The contact has been deleted."
        }

        """
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        del_contact = requests.delete(
            f'https://books.zoho.com/api/v3/contacts/{idclient}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers)


        response_json = del_contact.json()

        return response_json


    #Mark a contact active or unactive
    def mark_record(self,idclient,optn):
        """

        Arguments
            idclient | Required | valid id of client
            option | Required | 1 to activate mark  0 to inactivate  mark

        Response
            optn=1
            {
            "code": 0,
            "message": "The contact has been marked as active."
            }
            optn=0
            {
            "code": 0,
            "message": "The contact has been marked as inactive."
             }
             err:
             {"code": 1002, "message": "El recurso no existe."}

        """
        urlp=['active','inactive']
        mark_contact = requests.post(
            f'https://books.zoho.com/api/v3/contacts/{idclient}/{urlp[optn]}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=self.headers)
        response_json = mark_contact.json()
        return response_json

    def enable_portal_access(self,idclient,json_client):
        """
        Arguments
        contact_persons | Required | ID of the contact person

        Query Parameter as DICT
            organization_id | Required | ID of the organization

        Response:

            {
                "code": 0,
                "message": "Client Portal preferences have been updated"
            }
        """
        json_data=json_client
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        requestZBK = requests.post(
            f'https://books.zoho.com/api/v3/contacts/{idclient}/portal/enable?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)

        return requestZBK.json()



    #method to set payment reminder in books contacts
    def payment_reminder(self,idclient,optn):
        """
        Arguments
            contact_persons | Required | ID of the contact person
            optn | Required | 1 to activate reminder / 0 to inactivate reminder

        Response
            Enable
            {
            "code": 0,
            "message": "All reminders associated with this contact have been enabled."
            }
            Disable
            {
            "code": 0,
            "message": "All reminders associated with this contact have been stopped."
            }
        """
        edo=['enable','disable']
        requestZBK= requests.post(f'https://books.zoho.com/api/v3/contacts/{idclient}/paymentreminder/{edo[optn]}?organization_id={ZBOOKS_ORGANITATION_ID}',
                    headers=self.headers)
        response_json = requestZBK.json()

        return response_json

    # need to finish 3
    def email_statment(self,jsonmail):
        """
            POST /contacts/{:contact_id}/statements/email

            send_from_org_email_id:    Boolean to trigger the email from the organization's email address -
            to_mail_ids:  Array of email address of the recipients. *
            cc_mail_ids:  Array of email address of the recipients to be cced. -
            subject:     Subject of an email has to be sent. Max-length [1000] *
            body:  Body of an email has to be sent. Max-length [5000] *

            {
            "send_from_org_email_id": true,
            "to_mail_ids": [
                "willsmith@bowmanfurniture.com"
            ],
            "cc_mail_ids": [
                "peterparker@bowmanfurniture.com"
                ],
                "subject": "Statement of transactions with Zillium Inc",
                "body": "Dear Customer,
                }'
                response
                {
                "code": 0,
                "message": "Statement has been sent to the Customer."
                }
            """
        pass
    #Need to finish 1
    def get_statment_mail(self,idclient):
        """
        GET /contacts/{:contact_id}/statements/email

        start_date  If start_date and end_date are not given, current month's statement will be sent to contact. Date format [yyyy-mm-dd]
        end_date   End date for the statement. Date format [yyyy-mm-dd]
        organization_id

        Response example:
        {
        "code": 0,
        "message": "success",
        "data": {
            "body": "Dear Customer,     <br/>We have attached with this email a list of all your transactions",
            "subject": "Statement of transactions with Zillium Inc",
            "to_contacts": [
         {
            "first_name": "Will",
            "selected": true,
            "phone": "+1-925-921-9201",
            "email": "willsmith@bowmanfurniture.com",
            "contact_person_id": 460000000026051,
            "last_name": "Smith",
            "salutation": "Mr",
            "mobile": "+1-4054439562"
            }
        ],
        "file_name": "statement_BowmanandCo.pdf",
        "from_emails": [
            {
                "user_name": "John Smith",
                "selected": true,
                "email": "willsmith@bowmanfurniture.com"
            }
                    ],
                    "contact_id": 460000000026049
                }
            }
            """
        pass
    #Need to finish 2
    def send_mail_contact(self):
        """
        to_mail_ids: Array of email address of the recipients.*
        subject: subject of an email has to be sent. Max-length [1000]*
        body: Body of an email has to be sent. Max-length [5000]*
        attachments: Files to be attached to the email. It has to be sent in multipart/formdata


        '{
            "to_mail_ids": [
                "willsmith@bowmanfurniture.com"
            ],
            "subject": "Welcome to Zillium Inc .",
            "body": "Dear Customer,     <br/>We have attached f to us or call us if you need any assistance or clarifications.     <br/>Thanks for your business.<br/>Regards<br/>Zillium Inc",
            "attachments": "string"
        }'
        """
        pass


    def list_comments_contacts(self,idclient,queryparams = {}, page = 1):
        """
        Arguments
            contact_persons | Required | ID of the contact person
            page | Optional |  index of page response if have a more page

        Response
            {
                "code": 0,
                "message": "success",
                "contact_comments": [
                    {
                        "comment_id": 460000000053131,
                        "contact_id": 460000000026049,
                        "contact_name": "Bowman and Co",
                        "description": "",
                        "commented_by_id": 460000000024003,
                        "commented_by": "John David",
                        "date": "2013-11-19",
                        "date_description": "4 days ago",
                        "time": "6:03 PM",
                        "transaction_id": 460000000053123,
                        "transaction_type": "customer_payment",
                        "is_entity_deleted": false,
                        "operation_type": "added"
                    },
                    {...},
                    {...}
                ],
                "page_context": {
                    "page": 1,
                    "per_page": 200,
                    "has_more_page": false,
                    "applied_filter": "Status.All",
                    "sort_column": "contact_name",
                    "sort_order": "D"
                }
            }


        Return all comments of the contacts
        """
        requestZKB = requests.get(
            f'https://books.zoho.com/api/v3/contacts/{idclient}/comments?organization_id={ZBOOKS_ORGANITATION_ID}', headers=self.headers)

        return requestZKB.json()


    def get_contact_address(self,idclient):
        """
        Arguments
            contact_persons | Required | ID of the contact person

        Response
            {
            "code": 0,
            "message": "success",
            "addresses": [
                {
                    "address_id": 1053791000000186000,
                    "attention": "Mr.John",
                    "address": "4900 Hopyard Rd",
                    "street2": "Suite 310",
                    "city": "Pleasanton",
                    "state": "CA",
                    "zip": 94588,
                    "country": "U.S.A",
                    "fax": "+1-925-924-9600",
                    "phone": "+1-925-921-9201"
                },
                {...},
                {...}
            ]
        }
        """
        requestZKB= requests.get(f'https://books.zoho.com/api/v3/contacts/{idclient}/address?organization_id={ZBOOKS_ORGANITATION_ID}',headers=self.headers)
        return requestZKB.json()

    #Return all credit note of contacts
    def list_refunds(self,idclient):
        """
        Arguments
             contact_persons | Required | ID of the contact person

        Response
            {
                "code": 0,
                "message": "success",
                "creditnote_refunds": [
                    {
                        "creditnote_refund_id": 982000000567158,
                        "creditnote_id": 982000000567134,
                        "date": "2013-11-19",
                        "refund_mode": "cash",
                        "reference_number": 782364,
                        "creditnote_number": "CN-00001",
                        "customer_name": "Bowman & Co",
                        "description": "gf",
                        "amount_bcy": 57.15,
                        "amount_fcy": 57.15
                    },
                    {...},
                    {...}
                ],
                "page_context": {
                    "page": 1,
                    "per_page": 200,
                    "has_more_page": false,
                    "report_name": "Credit Notes Refund",
                    "sort_column": "date",
                    "sort_order": "D"
                }
            }
        """
        requestZKB = requests.get(f'https://books.zoho.com/api/v3/contacts/{idclient}/refunds?organization_id={ZBOOKS_ORGANITATION_ID}',headers=self.headers)

        refunds =requestZKB.json()

        return refunds























