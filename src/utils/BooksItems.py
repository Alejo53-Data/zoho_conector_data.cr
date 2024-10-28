import requests
from settings import ZBOOKS_ORGANITATION_ID

from utils.BooksConnection import BooksConnection


class BooksItems(BooksConnection):

    def __init__(self):
        super().__init__()
        self.headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

    #Returns all invoices of zohobooks filtering by queryparams
    def get_records(self, queryparams, page = 1):

        request_query = {
            "url": f'https://books.zoho.com/api/v3/items?page={str(page)}&organization_id={ZBOOKS_ORGANITATION_ID}',
            "headers": self.headers,
        }
        if queryparams:
            for key, value in queryparams.items():
                request_query['url'] = f"{request_query['url']}&{key}={value}"
            # request_query['data'] = queryparams
        get_items_list_response = requests.get(**request_query)
        items_collected = []

        if get_items_list_response.status_code == 200:
            items_collected = items_collected + get_items_list_response.json().get("items")
            has_more_pages = get_items_list_response.json().get("page_context").get("has_more_page")
            actual_page = get_items_list_response.json().get("page_context").get("page")

            result = {"items":items_collected, "has_more_pages":has_more_pages,"page":actual_page,"status_code":200}
        else:
            result = {"items":items_collected, "has_more_pages":False,"page":0,"status_code":404}

        return result

    #Returns a single contact of Zoho Books, invoice_id required
    def get_record(self, invoice_id):
        """
                Query Parameters as DICT:
                    invoice_id | Optional | Search a specific invoice by invoice id.

                :return: {
                            "status_code": 200, #extra
                            "code": 0,
                            "message": "success",
                            "invoice": {
                                "invoice_id": 982000000567114,
                                "ach_payment_initiated": false,
                                "invoice_number": "INV-00003",
                                "is_pre_gst": true,
                                "place_of_supply": "TN",
                                "gst_no": "22AAAAA0000A1Z5",
                                "gst_treatment": "business_gst",
                                "vat_treatment": "string",
                                "tax_treatment": "vat_registered",
                                "vat_reg_no": "string",
                                "date": "2013-11-17",
                                "status": "draft",
                                "payment_terms": 15,
                                "payment_terms_label": "Net 15",
                                "due_date": "2013-12-03",
                                "payment_expected_date": " ",
                                "last_payment_date": " ",
                                "reference_number": " ",
                                "customer_id": 982000000567001,
                                "customer_name": "Bowman & Co",
                                "contact_persons": [
                                    "982000000870911",
                                    "982000000870915"
                                ],
                                "currency_id": 982000000000190,
                                "currency_code": "USD",
                                "exchange_rate": 1,
                                "discount": 0,
                                "is_discount_before_tax": true,
                                "discount_type": "item_level",
                                "is_inclusive_tax": false,
                                "recurring_invoice_id": " ",
                                "is_viewed_by_client": false,
                                "has_attachment": false,
                                "client_viewed_time": "",
                                "line_items": [
                                    {
                                        "line_item_id": 982000000567021,
                                        "item_id": 982000000030049,
                                        "project_id": 90300000087378,
                                        "project_name": "Sample Project",
                                        "time_entry_ids": [],
                                        "warehouses": [
                                            {
                                                "warehouse_id": "",
                                                "warehouse_name": "",
                                                "warehouse_stock_on_hand": ""
                                            }
                                        ],
                                        "item_type": "goods",
                                        "product_type": "goods",
                                        "expense_id": " ",
                                        "expense_receipt_name": "string",
                                        "name": "Hard Drive",
                                        "description": "500GB, USB 2.0 interface 1400 rpm, protective hard case.",
                                        "item_order": 1,
                                        "bcy_rate": 120,
                                        "rate": 120,
                                        "quantity": 1,
                                        "unit": " ",
                                        "discount_amount": 0,
                                        "discount": 0,
                                        "tags": [
                                            {
                                                "is_tag_mandatory": false,
                                                "tag_id": 982000000009070,
                                                "tag_name": "Location",
                                                "tag_option_id": 982000000002670,
                                                "tag_option_name": "USA"
                                            }
                                        ],
                                        "tax_id": 982000000557028,
                                        "tax_name": "VAT",
                                        "tax_type": "tax",
                                        "tax_percentage": 12.5,
                                        "tax_treatment_code": "uae_others",
                                        "item_total": 120,
                                        "header_name": "Electronic devices",
                                        "header_id": 982000000000670
                                    }
                                ],
                                "shipping_charge": 0,
                                "adjustment": 0,
                                "adjustment_description": " ",
                                "sub_total": 153,
                                "tax_total": 22.6,
                                "total": 40.6,
                                "taxes": [
                                    {
                                        "tax_name": "VAT",
                                        "tax_amount": 19.13
                                    }
                                ],
                                "payment_reminder_enabled": true,
                                "payment_made": 26.91,
                                "credits_applied": 22.43,
                                "tax_amount_withheld": 0,
                                "balance": 40.6,
                                "write_off_amount": 0,
                                "allow_partial_payments": true,
                                "price_precision": 2,
                                "payment_options": {
                                    "payment_gateways": [
                                        {
                                            "configured": true,
                                            "additional_field1": "standard",
                                            "gateway_name": "paypal"
                                        }
                                    ]
                                },
                                "is_emailed": false,
                                "reminders_sent": 1,
                                "last_reminder_sent_date": " ",
                                "billing_address": {
                                    "address": "4900 Hopyard Rd, Suite 310",
                                    "street2": "McMillan Avenue",
                                    "city": "Pleasanton",
                                    "state": "CA",
                                    "zip": 94588,
                                    "country": "U.S.A",
                                    "fax": "+1-925-924-9600"
                                },
                                "shipping_address": {
                                    "address": "4900 Hopyard Rd, Suite 310",
                                    "street2": "McMillan Avenue",
                                    "city": "Pleasanton",
                                    "state": "CA",
                                    "zip": 94588,
                                    "country": "U.S.A",
                                    "fax": "+1-925-924-9600"
                                },
                                "notes": "Looking forward for your business.",
                                "terms": "Terms & Conditions apply",
                                "custom_fields": [
                                    {
                                        "customfield_id": "46000000012845",
                                        "value": "Normal"
                                    }
                                ],
                                "template_id": 982000000000143,
                                "template_name": "Service - Classic",
                                "created_time": "2013-11-18T02:17:40-0800",
                                "last_modified_time": "2013-11-18T02:02:51-0800",
                                "attachment_name": " ",
                                "can_send_in_mail": true,
                                "salesperson_id": " ",
                                "salesperson_name": " ",
                                "invoice_url": "https://books.zoho.com/SecurePayment?CInvoiceID=23d84d0cf64f9a72ea0c66fded25a08c8bafd0ab508aff05323a9f80e2cd03fdc5dd568d3d6407bbda969d3e870d740b6fce549a9438c4ea"
                            }
                        }
                """
        get_single_invoice = requests.get(
            f'https://books.zoho.com/api/v3/invoices/{invoice_id}?organization_id={ZBOOKS_ORGANITATION_ID}', headers=self.headers)

        if get_single_invoice.status_code == 200:
            response_json={"invoice":get_single_invoice.json().get("invoice"),"status_code":get_single_invoice.status_code,"code":get_single_invoice.json().get("code"),"message":get_single_invoice.json().get("message")}
        else:
            response_json={"invoice":{},"status_code":get_single_invoice.status_code,"code":get_single_invoice.json().get("code"),"message":get_single_invoice.json().get("message")}

        return response_json

        # def update_record(self,idclient,arrayc):
        #
        #     headers = {"Content-Type: application/json;charset=UTF-8 Authorization": f"Zoho-oauthtoken {self.access_token}"}
        #     update_contact=arrayc
        #     set_update_contatcs = requests.put(
        #         f'https://books.zoho.com/api/v3/contacts/{idclient}?organization_id={ZBOOKS_ORGANITATION_ID}',
        #         headers=headers)
        #
        #     """"
        #     https://books.zoho.com/api/v3/contacts/{contact_id}?organization_id=10234695
        #     -X PUT
        #     -H "Content-Type: application/json;charset=UTF-8"
        #     -H "Authorization: Zoho-oauthtoken 1000.41d9f2cfbd1b7a8f9e314b7aff7bc2d1.8fcc9810810a216793f385b9dd6e125f"
        #     -d '{
        #     "contact_name": "Bowman and Co",
        #     "company_name": "Bowman and Co",
        #     "payment_terms": 15,
        #     "payment_terms_label": "Net 15",
        #     "contact_type": "customer",
        #     "customer_sub_type": "business",
        #     "currency_id": 460000000000097,
        #     "opening_balance_amount": 1200,
        #     "exchange_rate": 1,
        #     "credit_limit": 1000,
        #     "tags": [
        #         {
        #             "tag_id": 462000000009070,
        #             "tag_option_id": 462000000002670
        #         }
        #     ]
        #     }
        #     """
        #     pass
        #
        # def create_record(self,arrayc):
        #     headers = {
        #         "Content-Type: application/json;charset=UTF-8 Authorization": f"Zoho-oauthtoken {self.access_token}"}
        #     set_update_contatcs = requests.put(
        #         f'https://books.zoho.com/api/v3/contacts/{idclient}?organization_id={ZBOOKS_ORGANITATION_ID}',
        #         headers=headers)
        #
        #
        #     # new_customer_custom_fields_list = {{"index":1,"value":"Cédula Jurídica"},{"index":2,"value":cedula_customer},{"index":3,"value":numeroCircuito},{"index":15,"value":segmento_customer},{"label":"Creado por ZM","value":"true"},{"label":"Exonerado","value":is_exonerado_customer}};
        #     # vendor = zoho.books.createRecord("Contacts",booksID,{"contact_name":razon_social_customer,"customer_name":razon_social_customer,"company_name":razon_social_customer,"contact_type":"customer","contact_persons":{{"email":contact_email,"phone":contact_phone,"first_name":contact_first_name,"last_name":contact_last_name}},"currency_id":customer_currency_id,"custom_fields":new_customer_custom_fields_list},"booksitems");
        #
        #     pass

    #Update an invoice into Zoho Books, using invoice_id *
    def update_record(self, invoice_id,queryparams):
        """
        Arguments
            customer_id | Required | ID of the customer the invoice has to be created.
            contact_persons | Optional | Array of contact person(s) for whom invoice has to be sent.
            invoice_number | Optional | Search invoices by invoice number.Variants: invoice_number_startswith and invoice_number_contains. Max-length [100]
            place_of_supply | Optional | Place where the goods/services are supplied to. (If not given, place of contact given for the contact will be taken)
                            Supported codes for UAE emirates are :
                            Abu Dhabi - AB,
                            Ajman - AJ,
                            Dubai - DU,
                            Fujairah - FU,
                            Ras al-Khaimah - RA,
                            Sharjah - SH,
                            Umm al-Quwain - UM
                            Supported codes for the GCC countries are :
                            United Arab Emirates - AE,
                            Saudi Arabia - SA,
                            Bahrain - BH,
                            Kuwait - KW,
                            Oman - OM,
                            Qatar - QA.
            vat_treatment | Optional | (Optional) VAT treatment for the invoices. VAT treatment denotes the location of the customer, if the customer resides in UK then the VAT treatment is uk. If the customer is in an EU country & VAT registered, you are resides in Northen Ireland and selling Goods then his VAT treatment is eu_vat_registered, if he resides outside of the UK then his VAT treatment is overseas (For Pre Brexit, this can be split as eu_vat_registered, eu_vat_not_registered and non_eu).
            tax_treatment | Optional | VAT treatment for the invoice .Choose whether the contact falls under: vat_registered,vat_not_registered,gcc_vat_not_registered,gcc_vat_registered,non_gcc.
                                        dz_vat_registered and dz_vat_not_registered supported only for UAE.
            gst_treatment | Optional | Choose whether the contact is GST registered/unregistered/consumer/overseas. Allowed values are business_gst , business_none , overseas , consumer .
            gst_no | Optional | 15 digit GST identification number of the customer.
            reference_number | Optional | The reference number of the invoice
            template_id | Optional | ID of the pdf template associated with the invoice.
            date | Optional | Search invoices by invoice date. Default date format is yyyy-mm-dd. Variants: due_date_start, due_date_end, due_date_before and due_date_after.
            payment_terms | Optional | Payment terms in days e.g. 15, 30, 60. Invoice due date will be calculated based on this. Max-length [100]
            payment_terms_label | Optional | Used to override the default payment terms label. Default value for 15 days is "Net 15 Days". Max-length [100]
            due_date | Optional | Search invoices by due date. Default date format is yyyy-mm-dd. Variants: due_date_start, due_date_end, due_date_before and due_date_after
            discount | Optional | Discount applied to the invoice. It can be either in % or in amount. e.g. 12.5% or 190. Max-length [100]
            is_discount_before_tax | Optional | Used to specify how the discount has to applied. Either before or after the calculation of tax.
            discount_type | Optional | How the discount is specified. Allowed values: entity_level and item_level.
            is_inclusive_tax | Optional | Used to specify whether the line item rates are inclusive or exclusivr of tax.
            exchange_rate | Optional | Exchange rate of the currency.
            recurring_invoice_id | Optional | ID of the recurring invoice from which the invoice is created.
            invoiced_estimate_id | Optional | ID of the invoice from which the invoice is created.
            salesperson_name | Optional | Name of the salesperson. Max-length [200]

            custom_fields | Optional | Custom fields for an invoice.
                customfield_id | Optional
                value | Optional | Value of the Custom Field

            line_items | Required
                item_id | Required | Search invoices by item id.
                project_id | Optional | ID of the Project.
                time_entry_ids | Optional | IDs of the time entries associated with the project.
                product_type | Optional | Enter goods/services
                hsn_or_sac | Optional | Add HSN/SAC code for your goods/services
                warehouse_id | Optional | Enter warehouse ID
                expense_id | Optional
                expense_receipt_name | Optional
                name | Optional | The name of the line item. Max-length [100]
                description | Optional | The description of the line items. Max-length [2000]
                item_order | Optional | The order of the line item_order
                bcy_rate | Optional | base currency rate
                rate | Optional | Rate of the line item.
                quantity | Optional | The quantity of line item
                unit | Optional | Unit of the line item e.g. kgs, Nos. Max-length [100]
                discount_amount | Optional | The discount amount on the line item
                tags | Optional | Filter all your reports based on the tag
                    tag_id | Optional | ID of the reporting tag
                    tag_option_id | Optional | ID of the reporting tag's option
                discount | Optional | Discount applied to the invoice. It can be either in % or in amount. e.g. 12.5% or 190. Max-length [100]
                tax_id | Optional | ID of the tax.
                tax_name | Optional | The name of the tax
                tax_type | Optional | The type of the tax
                tax_percentage | Optional | The percentage of tax levied
                tax_treatment_code | Optional | Specify reason for using out of scope.
                    Supported values for UAE are uae_same_tax_group, uae_reimbursed_expense and uae_others.
                    Supported values for Bahrain are bahrain_same_tax_group, bahrain_transfer_of_concern, bahrain_disbursement, bahrain_head_to_branch_transaction, bahrain_warranty_repair_services and bahrain_others.
                    Supported values for Saudi Arabia are ksa_pvt_health, ksa_pvt_edu, ksa_reimbursed_expense and ksa_house_sales.
                header_name | Optional | Name of the item header
                header_id | Optional | ID of the item header

            payment_options | Optional | Payment options for the invoice, online payment gateways and bank accounts. Will be displayed in the pdf.
                payment_gateways | Optional | Online payment gateways through which payment can be made.
                configured | Optional | Boolean check to see if a payment gateway ahs been configured
                additional_field1 | Optional | Paypal payment method. Allowed Values: standard and adaptive
                gateway_name | Optional | Name of the payment gateway associated with the invoice. E.g. paypal, stripe.Allowed Values: paypal, authorize_net, payflow_pro, stripe, 2checkout and braintree

            allow_partial_payments | Optional | Boolean to check if partial payments are allowed for the contact
            custom_body | Optional
            custom_subject | Optional
            notes | Optional | The notes added below expressing gratitude or for conveying some information.
            terms | Optional | The terms added below expressing gratitude or for conveying some information.
            shipping_charge | Optional | Shipping charges applied to the invoice. Max-length [100]
            adjustment | Optional | Adjustments made to the invoice.
            adjustment_description | Optional | Customize the adjustment description. E.g. Rounding off.
            reason | Optional
            tax_authority_id | Optional | ID of the tax authority. Tax authority depends on the location of the customer. For example, if the customer is located in NY, then the tax authority is NY tax authority.
            tax_exemption_id | Optional | ID of the tax exemption.
            avatax_use_code | Optional | Used to group like customers for exemption purposes. It is a custom value that links customers to a tax rule. Select from Avalara [standard codes][1] or enter a custom code. Max-length [25]
            avatax_exempt_no | Optional | Exemption certificate number of the customer. Max-length [25]
            tax_id | Optional | ID of the tax.
            expense_id | Optional
            salesorder_item_id | Optional | ID of the sales order line item which is invoices.
            avatax_tax_code | Optional | A tax code is a unique label used to group Items (products, services, or charges) together. Refer the [link][2] for more deails. Max-length [25]
            line_item_id | Optional | The line item id |  Query Parameters
            ignore_auto_number_generation | Optional | Ignore auto invoice number generation for this invoice. This mandates the invoice number. Allowed values true and false
            organization_id | Required | ID of the organization
    Query Parameters
        ignore_auto_number_generation | Optional | Ignore auto invoice number generation for this invoice. This mandates the invoice number. Allowed values true and false
        organization_id | Required | ID of the organization


    :param invoice_id:
    :return:
    {
    "code": 0,
    "message": "Invoice information has been updated.",
    "invoice": {
        "invoice_id": 982000000567114,
        "ach_payment_initiated": false,
        "invoice_number": "INV-00003",
        "is_pre_gst": true,
        "place_of_supply": "TN",
        "gst_no": "22AAAAA0000A1Z5",
        "gst_treatment": "business_gst",
        "vat_treatment": "string",
        "tax_treatment": "vat_registered",
        "vat_reg_no": "string",
        "date": "2013-11-17",
        "status": "draft",
        "payment_terms": 15,
        "payment_terms_label": "Net 15",
        "due_date": "2013-12-03",
        "payment_expected_date": " ",
        "last_payment_date": " ",
        "reference_number": " ",
        "customer_id": 982000000567001,
        "customer_name": "Bowman & Co",
        "contact_persons": [
            "982000000870911",
            "982000000870915"
        ],
        "currency_id": 982000000000190,
        "currency_code": "USD",
        "exchange_rate": 1,
        "discount": 0,
        "is_discount_before_tax": true,
        "discount_type": "item_level",
        "is_inclusive_tax": false,
        "recurring_invoice_id": " ",
        "is_viewed_by_client": false,
        "has_attachment": false,
        "client_viewed_time": "",
        "line_items": [
            {
                "line_item_id": 982000000567021,
                "item_id": 982000000030049,
                "project_id": 90300000087378,
                "project_name": "Sample Project",
                "time_entry_ids": [],
                "warehouses": [
                    {
                        "warehouse_id": "",
                        "warehouse_name": "",
                        "warehouse_stock_on_hand": ""
                    }
                ],
                "item_type": "goods",
                "product_type": "goods",
                "expense_id": " ",
                "expense_receipt_name": "string",
                "name": "Hard Drive",
                "description": "500GB, USB 2.0 interface 1400 rpm, protective hard case.",
                "item_order": 1,
                "bcy_rate": 120,
                "rate": 120,
                "quantity": 1,
                "unit": " ",
                "discount_amount": 0,
                "discount": 0,
                "tags": [
                    {
                        "is_tag_mandatory": false,
                        "tag_id": 982000000009070,
                        "tag_name": "Location",
                        "tag_option_id": 982000000002670,
                        "tag_option_name": "USA"
                    }
                ],
                "tax_id": 982000000557028,
                "tax_name": "VAT",
                "tax_type": "tax",
                "tax_percentage": 12.5,
                "tax_treatment_code": "uae_others",
                "item_total": 120,
                "header_name": "Electronic devices",
                "header_id": 982000000000670
            }
        ],
        "shipping_charge": 0,
        "adjustment": 0,
        "adjustment_description": " ",
        "sub_total": 153,
        "tax_total": 22.6,
        "total": 40.6,
        "taxes": [
            {
                "tax_name": "VAT",
                "tax_amount": 19.13
            }
        ],
        "payment_reminder_enabled": true,
        "payment_made": 26.91,
        "credits_applied": 22.43,
        "tax_amount_withheld": 0,
        "balance": 40.6,
        "write_off_amount": 0,
        "allow_partial_payments": true,
        "price_precision": 2,
        "payment_options": {
            "payment_gateways": [
                {
                    "configured": true,
                    "additional_field1": "standard",
                    "gateway_name": "paypal"
                }
            ]
        },
        "is_emailed": false,
        "reminders_sent": 1,
        "last_reminder_sent_date": " ",
        "billing_address": {
            "address": "4900 Hopyard Rd, Suite 310",
            "street2": "McMillan Avenue",
            "city": "Pleasanton",
            "state": "CA",
            "zip": 94588,
            "country": "U.S.A",
            "fax": "+1-925-924-9600"
        },
        "shipping_address": {
            "address": "4900 Hopyard Rd, Suite 310",
            "street2": "McMillan Avenue",
            "city": "Pleasanton",
            "state": "CA",
            "zip": 94588,
            "country": "U.S.A",
            "fax": "+1-925-924-9600"
        },
        "notes": "Looking forward for your business.",
        "terms": "Terms & Conditions apply",
        "custom_fields": [
            {
                "customfield_id": "46000000012845",
                "value": "Normal"
            }
        ],
        "template_id": 982000000000143,
        "template_name": "Service - Classic",
        "created_time": "2013-11-18T02:17:40-0800",
        "last_modified_time": "2013-11-18T02:02:51-0800",
        "attachment_name": " ",
        "can_send_in_mail": true,
        "salesperson_id": " ",
        "salesperson_name": " ",
        "invoice_url": "https://books.zoho.com/SecurePayment?CInvoiceID=23d84d0cf64f9a72ea0c66fded25a08c8bafd0ab508aff05323a9f80e2cd03fdc5dd568d3d6407bbda969d3e870d740b6fce549a9438c4ea"
    }
}
    """
        if queryparams:
            self.headers["Content-Type"] = "application/json;charset=UTF-8"
            get_single_invoice = requests.put(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers,data=queryparams)

            if get_single_invoice.status_code == 200:
                response_json = {"invoice": get_single_invoice.json().get("invoice"),
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"invoice": {}, "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {"invoice": {}, "status_code": 404,
                                 "code": 404,
                                 "message": "You must specify some valid params." }
        return response_json

    def create_record(self,queryparams):
        """
        ### Arguments ###
            - customer_id | Required | ID of the customer the invoice has to be created.
            - contact_persons | Optional | Array of contact person(s) for whom invoice has to be sent.
            - invoice_number | Optional | Search invoices by invoice number.Variants: invoice_number_startswith and invoice_number_contains. Max-length [100]
            - place_of_supply | Optional | Place where the goods/services are supplied to. (If not given, place of contact given for the contact will be taken)
            - Supported codes for UAE emirates are :
                    - - Abu Dhabi - AB,
                    - Ajman - AJ,
                    - Dubai - DU,
                    - Fujairah - FU,
                    - Ras al-Khaimah - RA,
                    - Sharjah - SH,
                    - Umm al-Quwain - UM
                    - Supported codes for the GCC countries are :
                    - United Arab Emirates - AE,
                    - Saudi Arabia - SA,
                    - Bahrain - BH,
                    - Kuwait - KW,
                    - Oman - OM,
                    - Qatar - QA.
            - vat_treatment | Optional | (Optional) VAT treatment for the invoices. VAT treatment denotes the location of the customer, if the customer resides in UK then the VAT treatment is uk. If the customer is in an EU country & VAT registered, you are resides in Northen Ireland and selling Goods then his VAT treatment is eu_vat_registered, if he resides outside of the UK then his VAT treatment is overseas (For Pre Brexit, this can be split as eu_vat_registered, eu_vat_not_registered and non_eu).
            - tax_treatment | Optional | VAT treatment for the invoice .Choose whether the contact falls under: vat_registered,vat_not_registered,gcc_vat_not_registered,gcc_vat_registered,non_gcc. dz_vat_registered and dz_vat_not_registered supported only for UAE.
            - gst_treatment | Optional | Choose whether the contact is GST registered/unregistered/consumer/overseas. Allowed values are business_gst , business_none , overseas , consumer .
            - gst_no | Optional | 15 digit GST identification number of the customer.
            - reference_number | Optional | The reference number of the invoice
            - template_id | Optional | ID of the pdf template associated with the invoice.
            - date | Optional | Search invoices by invoice date. Default date format is yyyy-mm-dd. Variants: due_date_start, due_date_end, due_date_before and due_date_after.
            - payment_terms | Optional | Payment terms in days e.g. 15, 30, 60. Invoice due date will be calculated based on this. Max-length [100]
            - payment_terms_label | Optional | Used to override the default payment terms label. Default value for 15 days is "Net 15 Days". Max-length [100]
            - due_date | Optional | Search invoices by due date. Default date format is yyyy-mm-dd. Variants: due_date_start, due_date_end, due_date_before and due_date_after
            - discount | Optional | Discount applied to the invoice. It can be either in % or in amount. e.g. 12.5% or 190. Max-length [100]
            - - is_discount_before_tax | Optional | Used to specify how the discount has to applied. Either before or after the calculation of tax.
            - discount_type | Optional | How the discount is specified. Allowed values: entity_level and item_level.
            - is_inclusive_tax | Optional | Used to specify whether the line item rates are inclusive or exclusivr of tax.
            - exchange_rate | Optional | Exchange rate of the currency.
            - recurring_invoice_id | Optional | ID of the recurring invoice from which the invoice is created.
            - invoiced_estimate_id | Optional | ID of the invoice from which the invoice is created.
            - salesperson_name | Optional | Name of the salesperson. Max-length [200]

            - custom_field | Optional | Custom fields for an invoice.
                - customfield_id | Optional
                - value | Optional | Value of the Custom Field

            - line_items | Required
                - item_id | Required | Search invoices by item id.
                - project_id | Optional | ID of the Project.
                - time_entry_ids | Optional | IDs of the time entries associated with the project.
                - product_type | Optional | Enter goods/services
                - hsn_or_sac | Optional | Add HSN/SAC code for your goods/services
                - warehouse_id | Optional | Enter warehouse ID
                - expense_id | Optional
                - expense_receipt_name | Optional
                - name | Optional | The name of the line item. Max-length [100]
                - description | Optional | The description of the line items. Max-length [2000]
                - item_order | Optional | The order of the line item_order
                - bcy_rate | Optional | base currency rate
                - rate | Optional | Rate of the line item.
                - quantity | Optional | The quantity of line item
                - unit | Optional | Unit of the line item e.g. kgs, Nos. Max-length [100]
                - discount_amount | Optional | The discount amount on the line item
                - discount | Optional | Discount applied to the invoice. It can be either in % or in amount. e.g. 12.5% or 190. Max-length [100]
                - tag_id | Optional | ID of the reporting tag
                - tag_option_id | Optional |  ID of the reporting tag's option

            - payment_options | Optional | Payment options for the invoice, online payment gateways and bank accounts. Will be displayed in the pdf.
                - payment_gateways | Optional | Online payment gateways through which payment can be made.
                    - configured | Optional | Boolean check to see if a payment gateway ahs been configured
                    - additional_field1 | Optional | Paypal payment method. Allowed Values: standard and adaptive
                    - gateway_name | Optional | Name of the payment gateway associated with the invoice. E.g. paypal, stripe.Allowed Values: paypal, authorize_net, payflow_pro, stripe, 2checkout and braintree

            - allow_partial_payments | Optional | Boolean to check if partial payments are allowed for the contact
            - custom_body | Optional
            - custom_subject | Optional
            - notes | Optional | The notes added below expressing gratitude or for conveying some information.
            - terms | Optional | The terms added below expressing gratitude or for conveying some information.
            - shipping_charge | Optional | Shipping charges applied to the invoice. Max-length [100]
            - adjustment | Optional | Adjustments made to the invoice.
            - adjustment_description | Optional | Customize the adjustment description. E.g. Rounding off.
            - reason | Optional
            - tax_authority_id | Optional | ID of the tax authority. Tax authority depends on the location of the customer. For example, if the customer is located in NY, then the tax authority is NY tax authority.
            - tax_exemption_id | Optional | ID of the tax exemption.
            - avatax_use_code | Optional | Used to group like customers for exemption purposes. It is a custom value that links customers to a tax rule. Select from Avalara [standard codes][1] or enter a custom code. Max-length [25]
            - avatax_exempt_no | Optional | Exemption certificate number of the customer. Max-length [25]
            - tax_id | Optional | ID of the tax.
            - expense_id | Optional
            - salesorder_item_id | Optional | ID of the sales order line item which is invoices.
            - avatax_tax_code | Optional | A tax code is a unique label used to group Items (products, services, or charges) together. Refer the [link][2] for more deails. Max-length [25]
            - time_entry_ids | Optional | IDs of the time entries associated with the project.

        ### Query Parameters ###
        - send | Optional | Send the invoice to the contact person(s) associated with the invoice. Allowed values true and false.
        - ignore_auto_number_generation | Optional | Ignore auto invoice number generation for this invoice. This mandates the invoice number. Allowed values true and false
        - organization_id | Required | ID of the organization

        :param USE JSON|DICT with the arguments as a key:value :
        :return:{
                    "code": 0,
                    "message": "The invoice has been created.",
                    "invoice": {
                        "invoice_id": 982000000567114,
                        "ach_payment_initiated": false,
                        "invoice_number": "INV-00003",
                        "is_pre_gst": true,
                        "place_of_supply": "TN",
                        "gst_no": "22AAAAA0000A1Z5",
                        "gst_treatment": "business_gst",
                        "vat_treatment": "string",
                        "tax_treatment": "vat_registered",
                        "vat_reg_no": "string",
                        "date": "2013-11-17",
                        "status": "draft",
                        "payment_terms": 15,
                        "payment_terms_label": "Net 15",
                        "due_date": "2013-12-03",
                        "payment_expected_date": " ",
                        "last_payment_date": " ",
                        "reference_number": " ",
                        "customer_id": 982000000567001,
                        "customer_name": "Bowman & Co",
                        "contact_persons": [
                            "982000000870911",
                            "982000000870915"
                        ],
                        "currency_id": 982000000000190,
                        "currency_code": "USD",
                        "exchange_rate": 1,
                        "discount": 0,
                        "is_discount_before_tax": true,
                        "discount_type": "item_level",
                        "is_inclusive_tax": false,
                        "recurring_invoice_id": " ",
                        "is_viewed_by_client": false,
                        "has_attachment": false,
                        "client_viewed_time": "",
                        "line_items": [
                            {
                                "line_item_id": 982000000567021,
                                "item_id": 982000000030049,
                                "project_id": 90300000087378,
                                "project_name": "Sample Project",
                                "time_entry_ids": [],
                                "warehouses": [
                                    {
                                        "warehouse_id": "",
                                        "warehouse_name": "",
                                        "warehouse_stock_on_hand": ""
                                    }
                                ],
                                "item_type": "goods",
                                "product_type": "goods",
                                "expense_id": " ",
                                "expense_receipt_name": "string",
                                "name": "Hard Drive",
                                "description": "500GB, USB 2.0 interface 1400 rpm, protective hard case.",
                                "item_order": 1,
                                "bcy_rate": 120,
                                "rate": 120,
                                "quantity": 1,
                                "unit": " ",
                                "discount_amount": 0,
                                "discount": 0,
                                "tags": [
                                    {
                                        "is_tag_mandatory": false,
                                        "tag_id": 982000000009070,
                                        "tag_name": "Location",
                                        "tag_option_id": 982000000002670,
                                        "tag_option_name": "USA"
                                    }
                                ],
                                "tax_id": 982000000557028,
                                "tax_name": "VAT",
                                "tax_type": "tax",
                                "tax_percentage": 12.5,
                                "tax_treatment_code": "uae_others",
                                "item_total": 120,
                                "header_name": "Electronic devices",
                                "header_id": 982000000000670
                            }
                        ],
                        "shipping_charge": 0,
                        "adjustment": 0,
                        "adjustment_description": " ",
                        "sub_total": 153,
                        "tax_total": 22.6,
                        "total": 40.6,
                        "taxes": [
                            {
                                "tax_name": "VAT",
                                "tax_amount": 19.13
                            }
                        ],
                        "payment_reminder_enabled": true,
                        "payment_made": 26.91,
                        "credits_applied": 22.43,
                        "tax_amount_withheld": 0,
                        "balance": 40.6,
                        "write_off_amount": 0,
                        "allow_partial_payments": true,
                        "price_precision": 2,
                        "payment_options": {
                            "payment_gateways": [
                                {
                                    "configured": true,
                                    "additional_field1": "standard",
                                    "gateway_name": "paypal"
                                }
                            ]
                        },
                        "is_emailed": false,
                        "reminders_sent": 1,
                        "last_reminder_sent_date": " ",
                        "billing_address": {
                            "address": "4900 Hopyard Rd, Suite 310",
                            "street2": "McMillan Avenue",
                            "city": "Pleasanton",
                            "state": "CA",
                            "zip": 94588,
                            "country": "U.S.A",
                            "fax": "+1-925-924-9600"
                        },
                        "shipping_address": {
                            "address": "4900 Hopyard Rd, Suite 310",
                            "street2": "McMillan Avenue",
                            "city": "Pleasanton",
                            "state": "CA",
                            "zip": 94588,
                            "country": "U.S.A",
                            "fax": "+1-925-924-9600"
                        },
                        "notes": "Looking forward for your business.",
                        "terms": "Terms & Conditions apply",
                        "custom_fields": [
                            {
                                "customfield_id": "46000000012845",
                                "value": "Normal"
                            }
                        ],
                        "template_id": 982000000000143,
                        "template_name": "Service - Classic",
                        "created_time": "2013-11-18T02:17:40-0800",
                        "last_modified_time": "2013-11-18T02:02:51-0800",
                        "attachment_name": " ",
                        "can_send_in_mail": true,
                        "salesperson_id": " ",
                        "salesperson_name": " ",
                        "invoice_url": "https://books.zoho.com/SecurePayment?CInvoiceID=23d84d0cf64f9a72ea0c66fded25a08c8bafd0ab508aff05323a9f80e2cd03fdc5dd568d3d6407bbda969d3e870d740b6fce549a9438c4ea"
                    }
                }
        """
        if queryparams:
            self.headers["Content-Type"] = "application/json;charset=UTF-8"
            get_single_invoice = requests.post(
                f'https://books.zoho.com/api/v3/invoices?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers,data=queryparams)

            if get_single_invoice.status_code == 200:
                response_json = {"invoice": get_single_invoice.json().get("invoice"),
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"invoice": {}, "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {"invoice": {}, "status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}
        return response_json

    def delete_record(self,invoice_id):
        """
        ### Query Parameters ###
            - invoice_id | Required | ID of the invoice

        :param JSON|DICT use query parameters as key:value :
        :return:{
                    "code": 0,
                    "message": "The invoice has been deleted."
                }
        """
        if invoice_id:
            get_single_invoice = requests.delete(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers)

            if get_single_invoice.status_code == 200:
                response_json = {
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = { "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = { "status_code": 404,
                             "code": 404,
                             "message": "You must specify a valid id."}
        return response_json

    def mark_record(self, invoice_id, mark_as_value):
        """
         ### Query Parameters ###
            - invoice_id | Required | ID of the invoice
            - mark_as_value | Required | Values: "draft", "void" ,"sent"

        :param USE JSON|DICT with the arguments as a key:value :
        :return:{
                    "code": 0,
                    "message": "Invoice status has been changed to sent|draft|void."
                }
        """
        if invoice_id and mark_as_value:
            self.headers["Content-Type"] = "application/json;charset=UTF-8"
            get_single_invoice = requests.post(
                f'https://books.zoho.com/api/v3/invoices/:invoice_id/status/{mark_as_value}?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers)

            if get_single_invoice.status_code == 200:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {"status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def email_record(self, invoice_id, queryparams):
        """
           ### Description ###
               - Email an invoice to the customer. Input json string is not mandatory. If input json string is empty, mail will be send with default mail content

           ### Arguments ###
               - send_from_org_email_id | Optional | Boolean to trigger the email from the organization's email address
               - to_mail_ids | Required | Array of email address of the recipients.
               - cc_mail_ids | Optional | Array of email address of the recipients to be cced.
               - subject | Optional | The subject of the mail
               - body | Optional | The body of the mail

           ### Query Parameters ###
               - send_customer_statement | Optional | Send customer statement pdf a with email.
               - send_attachment | Optional | Send the invoice attachment a with the email.
               - attachments | Optional | Files to be attached to the email

        :param USE JSON|DICT with the arguments as a key:value
                Example:
                {
                    "send_from_org_email_id": false,
                    "to_mail_ids": [
                        "willsmith@bowmanfurniture.com"
                    ],
                    "cc_mail_ids": [
                        "peterparker@bowmanfurniture.com"
                    ],
                    "subject": "Invoice from Zillium Inc (Invoice#: INV-00001)",
                    "body": "Dear Customer,         <br><br><br><br>Thanks for your business.         <br><br><br><br>The invoice INV-00001 is attached with this email. You can choose the easy way out and <a href= https://invoice.zoho.com/SecurePayment?CInvoiceID=b9800228e011ae86abe71227bdacb3c68e1af685f647dcaed747812e0b9314635e55ac6223925675b371fcbd2d5ae3dc  >pay online for this invoice.</a>         <br><br>Here's an overview of the invoice for your reference.         <br><br><br><br>Invoice Overview:         <br><br>Invoice  : INV-00001         <br><br>Date : 05 Aug 2013         <br><br>Amount : $541.82         <br><br><br><br>It was great working with you. Looking forward to working with you again.<br><br><br>\\nRegards<br>\\nZillium Inc<br>\\n\","
                }

        :return:
                {
                    "code": 0,
                    "message": "Your invoice has been sent."
                }
        """
        if invoice_id:
            get_single_invoice = requests.post(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}/email?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers,data=queryparams)

            if get_single_invoice.status_code == 200:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {"status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def email_records(self, invoice_ids, queryparams):
        """
            ### Description ###
                - Send invoices to your customers by email. Maximum of 10 invoices can be sent at once.

            ### Arguments ###
                - contacts | Optional | Contacts for whom email or snail mail has to be sent.
                - contact_id | Required | ID of the contact. Can specify if email or snail mail has to be sent for each contact.
            ### Query Parameters ###
                - invoice_ids | Required | Comma separated invoice ids which are to be emailed.

        :param USE JSON|DICT with the arguments as a key:value
                Example:
                {
                    "contacts": [
                        "example@mail.com"
                    ],
                    "contact_id": 460000000026049
                }

        :return:
                {
                    "code": 0,
                    "message": "Mission accomplished! We've sent all the invoices."
                }
        """
        if invoice_ids:
            self.headers["Content-Type"] = "application/json;charset=UTF-8"
            get_single_invoice = requests.post(
                f'https://books.zoho.com/api/v3/invoices/email?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers, data=queryparams)

            if get_single_invoice.status_code == 200:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {"status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def submit_record(self, invoice_id):
        """
            ### Description ###
                - Submit an invoice for approval.

            ### Query Parameters ###
                - invoice_id | Required | Invoice id.

        :param invoice_id ( string )
        :return:
                {
                    "code": 0,
                    "message": "The invoice has been submitted for approval successfully."
                }
        """
        if invoice_id:
            get_single_invoice = requests.post(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}/submit?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers)

            if get_single_invoice.status_code == 200:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {"status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def approve_record(self, invoice_id):
        """
            ### Description ###
                - Approve an invoice.

            ### Query Parameters ###
                - invoice_id | Required | Invoice id.

        :param invoice_id ( string )
        :return:
                {
                    "code": 0,
                    "message": "You have approved the invoice."
                }
        """
        if invoice_id:
            get_single_invoice = requests.post(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}/submit?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers)

            if get_single_invoice.status_code == 200:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {"status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def get_email_content(self, invoice_id,queryparams = None):
        """
            ### Description ###
                - Get the email content of an invoice

            ### Query Parameters ###
                - invoice_id | Required | Invoice id.

        :param invoice_id ( string )
        :return:
                {
                    "code": 0,
                    "message": "success",
                    "data": {
                        "bcc_mails": [
                            "string"
                        ],
                        "gateways_configured": true,
                        "gateways_associated": true,
                        "bcc_mails_str": "",
                        "body": "Dear Customer,         <br><br><br><br>Thanks for your business.         <br><br><br><br>The invoice INV-00001 is attached with this email. You can choose the easy way out and <a href= https://invoice.zoho.com/SecurePayment?CInvoiceID=b9800228e011ae86abe71227bdacb3c68e1af685f647dcaed747812e0b9314635e55ac6223925675b371fcbd2d5ae3dc  >pay online for this invoice.</a>         <br><br>Here's an overview of the invoice for your reference.         <br><br><br><br>Invoice Overview:         <br><br>Invoice  : INV-00001         <br><br>Date : 05 Aug 2013         <br><br>Amount : $541.82         <br><br><br><br>It was great working with you. Looking forward to working with you again.<br><br><br>\\nRegards<br>\\nZillium Inc<br>\\n\",",
                        "documents": "",
                        "customer_name": "Bowman & Co",
                        "attach_pdf": true,
                        "entity_id": "2000000007037",
                        "cc_mails_list": [
                            {
                                "user_name": "Sujin Kumar",
                                "email": null
                            }
                        ],
                        "file_name_without_extension": "INV-000004",
                        "to_mails_str": "",
                        "cc_mails_str": "",
                        "from_email": "",
                        "from_address": "",
                        "deprecated_placeholders_used": [],
                        "error_list": [],
                        "subject": "Invoice from Zillium Inc (Invoice#: INV-00001)",
                        "emailtemplates": [
                            {
                                "selected": true,
                                "name": "Default",
                                "email_template_id": "982000000000067"
                            }
                        ],
                        "emailtemplate_documents": [
                            "string"
                        ],
                        "to_contacts": [
                            {
                                "first_name": "Sujin",
                                "selected": true,
                                "phone": "+1-925-921-9201",
                                "email": null,
                                "last_name": "Kumar",
                                "salutation": "Mr",
                                "contact_person_id": 982000000567003,
                                "mobile": "+1-4054439562"
                            }
                        ],
                        "attachment_name": " ",
                        "file_name": "INV-00001.pdf",
                        "from_emails": [
                            {
                                "user_name": "Sujin Kumar",
                                "selected": true,
                                "email": null,
                                "organization_contact_id": "2000000002266",
                                "is_org_email_id": true
                            }
                        ],
                        "customer_id": 982000000567001
                    }
                }
        """
        if invoice_id:
            if queryparams:
                get_single_invoice = requests.get(
                    f'https://books.zoho.com/api/v3/invoices/{invoice_id}/email?organization_id={ZBOOKS_ORGANITATION_ID}',
                    headers=self.headers,data=queryparams)
            else:
                get_single_invoice = requests.get(
                    f'https://books.zoho.com/api/v3/invoices/{invoice_id}/email?organization_id={ZBOOKS_ORGANITATION_ID}',
                    headers=self.headers)

            if get_single_invoice.status_code == 200:
                response_json = {
                                 "data": get_single_invoice.json().get("data"),
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"data": {},
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {
                             "data": {},
                             "status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def remind_customer(self, invoice_id,queryparams):
        """
            ### Description ###
                - Remind your customer about an unpaid invoice by email. Reminder will be sent, only for the invoices which are in open or overdue status..

            ### Arguments ###
                - to_mail_ids | Optional | Array of email address of the recipients.
                - cc_mail_ids | Required | Array of email address of the recipients to be cced.
                - subject | Optional | The subject of the mail
                - body | Optional | The body of the mail
                - send_from_org_email_id | Optional | Boolean to trigger the email from the organization's email address

            ### Query Parameters ###
                - send_customer_statement | Optional | Send customer statement pdf a with email.
                - attachments | Optional | Files to be attached to the email

        :param invoice_id ( string )
                - Example: {
                                "to_mail_ids": [
                                    "willsmith@bowmanfurniture.com"
                                ],
                                "cc_mail_ids": [
                                    "peterparker@bowmanfurniture.com"
                                ],
                                "subject": "Invoice from Zillium Inc (Invoice#: INV-00001)",
                                "body": "<br>Dear Mr. Sujin,&nbsp;<br><br>You might have missed the payment date and the invoice is now overdue by&nbsp;1&nbsp;days.<br><br>----------------------------------------------------------------------------------------<br><h2>Invoice# : INV-000004 </h2>Dated : 23 Dec 2016<br>----------------------------------------------------------------------------------------<br><b>&nbsp;Due Date &nbsp; &nbsp; &nbsp; &nbsp; : &nbsp;&nbsp;23 Dec 2016</b><br><b>&nbsp;Amount &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; : &nbsp;&nbsp;$139.65</b><br>----------------------------------------------------------------------------------------<br><br><span>Not to worry at all !&nbsp;</span>View your invoice and take the easy way out by making an&nbsp;<a href=\"https://books.zoho.com/portal/zilliuminc/index#/invoices/invoice/2000000007037 \">online payment</a>.<br><br>If you have already paid, please accept our apologies and kindly ignore this payment reminder.<br><br><br>Regards,<br><br>David Sujin<br>Zillium Inc<br><br><br>",
                                "send_from_org_email_id": false
                            }

        :return:
                {
                    "code": 0,
                    "message": "Your payment reminder has been sent."
                }

        """
        if invoice_id and queryparams:
            self.headers["Content-Type"] = "application/json;charset=UTF-8"
            get_single_invoice = requests.post(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}/paymentreminder?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers,data=queryparams)

            if get_single_invoice.status_code == 200:
                response_json = {
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {
                             "status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def get_payment_reminder_mail_content(self, invoice_id):
        """
            ### Description ###
                - Get the mail content of the payment reminder.

            ### Query Parameters ###
                - invoice_id | Optional | Invoice ID.

        :param invoice_id ( string )
                - Example: {
                                "to_mail_ids": [
                                    "willsmith@bowmanfurniture.com"
                                ],
                                "cc_mail_ids": [
                                    "peterparker@bowmanfurniture.com"
                                ],
                                "subject": "Invoice from Zillium Inc (Invoice#: INV-00001)",
                                "body": "<br>Dear Mr. Sujin,&nbsp;<br><br>You might have missed the payment date and the invoice is now overdue by&nbsp;1&nbsp;days.<br><br>----------------------------------------------------------------------------------------<br><h2>Invoice# : INV-000004 </h2>Dated : 23 Dec 2016<br>----------------------------------------------------------------------------------------<br><b>&nbsp;Due Date &nbsp; &nbsp; &nbsp; &nbsp; : &nbsp;&nbsp;23 Dec 2016</b><br><b>&nbsp;Amount &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; : &nbsp;&nbsp;$139.65</b><br>----------------------------------------------------------------------------------------<br><br><span>Not to worry at all !&nbsp;</span>View your invoice and take the easy way out by making an&nbsp;<a href=\"https://books.zoho.com/portal/zilliuminc/index#/invoices/invoice/2000000007037 \">online payment</a>.<br><br>If you have already paid, please accept our apologies and kindly ignore this payment reminder.<br><br><br>Regards,<br><br>David Sujin<br>Zillium Inc<br><br><br>",
                                "send_from_org_email_id": false
                            }

        :return:
                {
                    "code": 0,
                    "message": "success",
                    "data": {
                        "bcc_mails": [
                            "string"
                        ],
                        "gateways_configured": true,
                        "gateways_associated": true,
                        "bcc_mails_str": "",
                        "body": "<br>Dear Mr. Sujin,&nbsp;<br><br>You might have missed the payment date and the invoice is now overdue by&nbsp;1&nbsp;days.<br><br>----------------------------------------------------------------------------------------<br><h2>Invoice# : INV-000004 </h2>Dated : 23 Dec 2016<br>----------------------------------------------------------------------------------------<br><b>&nbsp;Due Date &nbsp; &nbsp; &nbsp; &nbsp; : &nbsp;&nbsp;23 Dec 2016</b><br><b>&nbsp;Amount &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; : &nbsp;&nbsp;$139.65</b><br>----------------------------------------------------------------------------------------<br><br><span>Not to worry at all !&nbsp;</span>View your invoice and take the easy way out by making an&nbsp;<a href=\"https://books.zoho.com/portal/zilliuminc/index#/invoices/invoice/2000000007037 \">online payment</a>.<br><br>If you have already paid, please accept our apologies and kindly ignore this payment reminder.<br><br><br>Regards,<br><br>David Sujin<br>Zillium Inc<br><br><br>",
                        "documents": "",
                        "customer_name": "Bowman & Co",
                        "attach_pdf": true,
                        "entity_id": "2000000007037",
                        "cc_mails_list": [
                            {
                                "user_name": "Sujin Kumar",
                                "email": null
                            }
                        ],
                        "file_name_without_extension": "INV-000004",
                        "to_mails_str": "",
                        "cc_mails_str": "",
                        "from_email": "",
                        "from_address": "",
                        "deprecated_placeholders_used": [],
                        "error_list": [],
                        "subject": "Invoice from Zillium Inc (Invoice#: INV-00001)",
                        "emailtemplates": [
                            {
                                "selected": true,
                                "name": "Default",
                                "email_template_id": "982000000000067"
                            }
                        ],
                        "emailtemplate_documents": [
                            "string"
                        ],
                        "to_contacts": [
                            {
                                "first_name": "Sujin",
                                "selected": true,
                                "phone": "+1-925-921-9201",
                                "email": null,
                                "last_name": "Kumar",
                                "salutation": "Mr",
                                "contact_person_id": 982000000567003,
                                "mobile": "+1-4054439562"
                            }
                        ],
                        "attachment_name": " ",
                        "file_name": "INV-00001.pdf",
                        "from_emails": [
                            {
                                "user_name": "Sujin Kumar",
                                "selected": true,
                                "email": null,
                                "organization_contact_id": "2000000002266",
                                "is_org_email_id": true
                            }
                        ],
                        "customer_id": 982000000567001
                    }
                }

        """
        if invoice_id:
            self.headers["Content-Type"] = "application/json;charset=UTF-8"
            get_single_invoice = requests.get(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}/paymentreminder?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers)

            if get_single_invoice.status_code == 200:
                response_json = {
                                 "data": get_single_invoice.json().get("data"),
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {
                                "data":{},
                                "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {
                             "data": {},
                             "status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def bulk_invoice_reminder(self, queryparams):
        """
            ### Description ###
                - Remind your customer about an unpaid invoices by email. Reminder mail will be send, only for the invoices is in open or overdue status. Maximum 10 invoices can be reminded at once.

            ### Query Parameters ###
                - invoice_ids | Required | Array of invoice ids for which the reminder has to be sent.

        :param invoice_id ( string )
                - Example: {
                                "to_mail_ids": [
                                    "willsmith@bowmanfurniture.com"
                                ],
                                "cc_mail_ids": [
                                    "peterparker@bowmanfurniture.com"
                                ],
                                "subject": "Invoice from Zillium Inc (Invoice#: INV-00001)",
                                "body": "<br>Dear Mr. Sujin,&nbsp;<br><br>You might have missed the payment date and the invoice is now overdue by&nbsp;1&nbsp;days.<br><br>----------------------------------------------------------------------------------------<br><h2>Invoice# : INV-000004 </h2>Dated : 23 Dec 2016<br>----------------------------------------------------------------------------------------<br><b>&nbsp;Due Date &nbsp; &nbsp; &nbsp; &nbsp; : &nbsp;&nbsp;23 Dec 2016</b><br><b>&nbsp;Amount &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; : &nbsp;&nbsp;$139.65</b><br>----------------------------------------------------------------------------------------<br><br><span>Not to worry at all !&nbsp;</span>View your invoice and take the easy way out by making an&nbsp;<a href=\"https://books.zoho.com/portal/zilliuminc/index#/invoices/invoice/2000000007037 \">online payment</a>.<br><br>If you have already paid, please accept our apologies and kindly ignore this payment reminder.<br><br><br>Regards,<br><br>David Sujin<br>Zillium Inc<br><br><br>",
                                "send_from_org_email_id": false
                            }

        :return:
                {
                "code": 0,
                "message": "success",
                "info": {
                    "email_success_info": {
                        "message": "The reminders were successfully sent",
                        "sent_count": 2
                    },
                    "email_errors_info": [
                        {
                            "message": "The reminders were successfully sent",
                            "ids": "2000000007037"
                        }
                    ],
                    "code": 4083
                }

        """
        if queryparams:
            get_response = requests.post(
                f'https://books.zoho.com/api/v3/invoices/paymentreminder?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers,data=queryparams)

            if get_response.status_code == 200:
                response_json = {
                                 "info": get_response.json().get("info"),
                                 "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
            else:
                response_json = {
                                "info":{},
                                "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
        else:
            response_json = {
                             "info": {},
                             "status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def bulk_export_invoices_pdf(self, queryparams):
        """
            ### Description ###
                - Maximum of 25 invoices can be exported in a single pdf.

            ### Query Parameters ###
                - invoice_ids | Required | Array of invoice ids for which the reminder has to be sent.

        :param
                - Example: {
                                "invoice_ids": "12355321356,51231554123,12315434251",
                            }

        :return:
                {
                    "code": 0,
                    "message": "success"
                }

        """
        if queryparams:
            get_response = requests.get(
                f'https://books.zoho.com/api/v3/invoices/pdf?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers,data=queryparams)

            if get_response.status_code == 200:
                response_json = {
                                 "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
            else:
                response_json = {
                                "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
        else:
            response_json = {
                             "status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def enable_payment_reminder(self, invoice_id):
        """
            ### Description ###
                - Enable automated payment reminders for an invoice.

            ### Query Parameters ###
                - invoice_id | Required | Invoice id for which the reminder has to be enabled.

        :param invoice_id

        :return:
                {
                    "code": 0,
                    "message": "Reminders enabled."
                }

        """
        if invoice_id:
            get_response = requests.post(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}/paymentreminder/enable?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers)

            if get_response.status_code == 200:
                response_json = {
                                 "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
            else:
                response_json = {
                                "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
        else:
            response_json = {
                             "status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def write_off_invoice(self, invoice_id):
        """
            ### Description ###
                - Write off the invoice balance amount of an invoice.

            ### Query Parameters ###
                - invoice_id | Required | Invoice id for which the reminder has to be enabled.

        :param invoice_id

        :return:
                {
                    "code": 0,
                    "message": "Invoice has been written off."
                }

        """
        if invoice_id:
            get_response = requests.post(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}/writeoff?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers)

            if get_response.status_code == 200:
                response_json = {
                                 "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
            else:
                response_json = {
                                "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
        else:
            response_json = {
                             "status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json

    def cancel_write_off_invoice(self, invoice_id):
        """
            ### Description ###
                - Cancel the Write off amount of an invoice.

            ### Query Parameters ###
                - invoice_id | Required | Invoice id for which the reminder has to be enabled.

        :param invoice_id

        :return:
                {
                    "code": 0,
                    "message": "The write off done for this invoice has been cancelled."
                }

        """
        if invoice_id:
            get_response = requests.post(
                f'https://books.zoho.com/api/v3/invoices/{invoice_id}/writeoff/cancel?organization_id={ZBOOKS_ORGANITATION_ID}',
                headers=self.headers)

            if get_response.status_code == 200:
                response_json = {
                                 "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
            else:
                response_json = {
                                "status_code": get_response.status_code,
                                 "code": get_response.json().get("code"),
                                 "message": get_response.json().get("message")}
        else:
            response_json = {
                             "status_code": 404,
                             "code": 404,
                             "message": "You must specify some valid params."}

        return response_json


