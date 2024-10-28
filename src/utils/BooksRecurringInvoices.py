import requests

from src.utils.BooksConnection import BooksConnection


class BooksRecurringInvoices(BooksConnection):
    ZBOOKS_ORGANITATION_ID="696634191"
    def __init__(self):
        super().__init__()
        self.headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

    #Returns all invoices of zohobooks filtering by queryparams
    def get_records(self, queryparams, page = 1):

        request_query = {
            "url": f'https://books.zoho.com/api/v3/recurringinvoices?page={str(page)}&organization_id={self.ZBOOKS_ORGANITATION_ID}',
            "headers": self.headers,
        }
        if queryparams:
            for key, value in queryparams.items():
                request_query['url'] = f"{request_query['url']}&{key}={value}"
            # request_query['data'] = queryparams
        get_invoices_list_response = requests.get(**request_query)
        invoices_collected = []

        if get_invoices_list_response.status_code == 200:
            invoices_collected = invoices_collected + get_invoices_list_response.json().get("invoices")
            has_more_pages = get_invoices_list_response.json().get("page_context").get("has_more_page")
            actual_page = get_invoices_list_response.json().get("page_context").get("page")

            result = {"invoices":invoices_collected, "has_more_pages":has_more_pages,"page":actual_page,"status_code":200}
        else:
            result = {"invoices":invoices_collected, "has_more_pages":False,"page":0,"status_code":404}

        return result

    def find_record(self,queryparams=1):
        get_single_invoice = requests.get(
            f'https://books.zoho.com/api/v3/invoices?organization_id={self.ZBOOKS_ORGANITATION_ID}&due_date_after=2022-07-01', headers=self.headers)

        

        if get_single_invoice.status_code == 200:
            response_json={"invoice":get_single_invoice.json().get("invoice"),"status_code":get_single_invoice.status_code,"code":get_single_invoice.json().get("code"),"message":get_single_invoice.json().get("message")}
        else:
            response_json={"invoice":{},"status_code":get_single_invoice.status_code,"code":get_single_invoice.json().get("code"),"message":get_single_invoice.json().get("message")}

        return response_json


    #Returns a single contact of Zoho Books, invoice_id required
    def get_record(self, invoice_id):
        get_single_invoice = requests.get(
            f'https://books.zoho.com/api/v3/recurringinvoices/{invoice_id}?organization_id={self.ZBOOKS_ORGANITATION_ID}', headers=self.headers)

        if get_single_invoice.status_code == 200:
            
            response_json={"recurringinvoice":get_single_invoice.json().get("recurring_invoice"),"status_code":get_single_invoice.status_code,"code":get_single_invoice.json().get("code"),"message":get_single_invoice.json().get("message")}
        else:
            response_json={"recurringinvoice":{},"status_code":get_single_invoice.status_code,"code":get_single_invoice.json().get("code"),"message":get_single_invoice.json().get("message")}

        return response_json


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
                f'https://books.zoho.com/api/v3/recurringinvoices/{invoice_id}?organization_id={self.ZBOOKS_ORGANITATION_ID}',
                headers=self.headers,data=queryparams)

            if get_single_invoice.status_code == 200:
                response_json = {"recurringinvoices": get_single_invoice.json().get("recurring_invoices"),
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"recurringinvoices": {}, "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {"recurringinvoices": {}, "status_code": 404,
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
                f'https://books.zoho.com/api/v3/recurringinvoices?organization_id={self.ZBOOKS_ORGANITATION_ID}',
                headers=self.headers,data=queryparams)

            if get_single_invoice.status_code == 200:
                response_json = {"recurringinvoices": get_single_invoice.json().get("recurringinvoices"),
                                 "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
            else:
                response_json = {"recurringinvoices": {}, "status_code": get_single_invoice.status_code,
                                 "code": get_single_invoice.json().get("code"),
                                 "message": get_single_invoice.json().get("message")}
        else:
            response_json = {"recurringinvoices": {}, "status_code": 404,
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
                f'https://books.zoho.com/api/v3/recurringinvoices/{invoice_id}?organization_id={self.ZBOOKS_ORGANITATION_ID}',
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


