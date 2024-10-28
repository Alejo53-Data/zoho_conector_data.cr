
import os
from datetime import date, datetime
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.attachments import Attachment
from zcrmsdk.src.com.zoho.crm.api.tags import Tag
from zcrmsdk.src.com.zoho.crm.api.layouts import Layout
from zcrmsdk.src.com.zoho.crm.api.users import User
from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from zcrmsdk.src.com.zoho.crm.api.util import Choice, StreamWrapper
from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord
class Record(object):
    @staticmethod
    def create_records(module_api_name):

        """
        This method is used to create records of a module and print the response.
        :param module_api_name: The API Name of the module to create records.
        """

        """
        example
        module_api_name = 'Leads'
        """

        # Get instance of RecordOperations Class
        record_operations = RecordOperations()

        # Get instance of BodyWrapper Class that will contain the request body
        request = BodyWrapper()

        # List to hold Record instances
        records_list = []

        # Get instance of Record Class
        record = ZCRMRecord()

        # Value to Record's fields can be provided in any of the following ways

        """
        Call add_field_value method that takes two arguments
        Import the zcrmsdk.src.com.zoho.crm.api.record.field file
        1 -> Call Field "." and choose the module from the displayed list and press "." and choose the field name from the displayed list.
        2 -> Value
        """

        record.add_field_value(Field.Leads.last_name(), 'Python SDK')

        record.add_field_value(Field.Leads.first_name(), 'New')

        record.add_field_value(Field.Leads.company(), 'Zoho')

        record.add_field_value(Field.Leads.city(), 'City')

        """
        Call add_key_value method that takes two arguments
        1 -> A string that is the Field's API Name
        2 -> Value
        """

        record.add_key_value('Custom_field', 'Value')

        record.add_key_value('Custom_field_2', 12)

        record.add_key_value('Date', date(2020, 4, 9))

        record.add_key_value('Discounted', 23.34)

        file_details = []

        file_detail = FileDetails()

        file_detail.set_file_id('479f0f5eebf0fb982f99e3832b35d23e29f67c2868ee4c789f22579895383c8')

        file_details.append(file_detail)

        record.add_key_value('File_Upload_1', file_details)

        """
        Following methods are being used only by Inventory modules
        """
        deal_name = ZCRMRecord()

        deal_name.add_field_value(Field.Deals.id(), 3409643000002000001)

        record.add_field_value(Field.Sales_Orders.deal_name(), deal_name)

        contact_name = ZCRMRecord()

        contact_name.add_field_value(Field.Contacts.id(), 3409643000001074007)

        record.add_field_value(Field.Sales_Orders.contact_name(), contact_name)

        account_name = ZCRMRecord()

        account_name.add_field_value(Field.Accounts.id(), 3409643000000692007)

        record.add_field_value(Field.Sales_Orders.account_name(), account_name)

        record.add_key_value("Discount", 10.5) 
     
        record.add_key_value("Subject", "Abc") 

        inventory_line_item_list = []

        inventory_line_item = InventoryLineItems()

        line_item_product = LineItemProduct()

        line_item_product.set_id(3409643000000986033)

        inventory_line_item.set_product(line_item_product)

        inventory_line_item.set_quantity(3.0)

        inventory_line_item.set_product_description('productDescription')

        inventory_line_item.set_list_price(10.0)

        inventory_line_item.set_discount('5.90')

        product_line_taxes = []

        product_line_tax = LineTax()

        product_line_tax.set_name('Tax1')

        product_line_tax.set_percentage(12.0)

        product_line_taxes.append(product_line_tax)

        inventory_line_item.set_line_tax(product_line_taxes)

        inventory_line_item_list.append(inventory_line_item)

        record.add_key_value('Product_Details', inventory_line_item_list)

        line_taxes = []

        line_tax = LineTax()

        line_tax.set_name('Total-Tax')

        line_tax.set_percentage(5.0)

        line_taxes.append(line_tax)

        record.add_key_value("$line_tax", line_taxes)

        """
        End Inventory
        """

        """
        Following methods are being used only by Activity modules
        """
        record.add_field_value(Field.Tasks.description(), "New Task")
      
        record.add_field_value(Field.Tasks.subject(), "Task subject")

        record.add_key_value('Currency', Choice('INR'))

        remind_at = RemindAt()

        remind_at.set_alarm("FREQ=NONE;ACTION=EMAILANDPOPUP;TRIGGER=DATE-TIME:2020-07-03T12:30:00+05:30")

        record.add_field_value(Field.Tasks.remind_at(), remind_at)

        who_id = ZCRMRecord()

        who_id.set_id(3409643000000836001)

        record.add_field_value(Field.Tasks.who_id(), who_id)

        record.add_field_value(Field.Tasks.status(), Choice('Waiting for Input'))

        record.add_field_value(Field.Tasks.due_date(), date(2020, 10, 10))

        record.add_field_value(Field.Tasks.priority(), Choice('High'))

        what_id = ZCRMRecord()

        what_id.set_id(3409643000000692007)

        record.add_field_value(Field.Tasks.what_id(), what_id)

        record.add_key_value("$se_module", "Accounts")

        # Recurring Activity can be provided in any activity module

        recurring_activity = RecurringActivity()

        recurring_activity.set_rrule('FREQ=DAILY;INTERVAL=10;UNTIL=2020-08-14;DTSTART=2020-07-03')

        record.add_field_value(Field.Events.recurring_activity(), recurring_activity)

        record.add_field_value(Field.Events.description(), "My Event")

        start_date_time = datetime.fromisoformat('2020-07-03T12:30:00+05:30')

        record.add_field_value(Field.Events.start_datetime(), start_date_time)

        participants_list = []

        participant = Participants()

        participant.set_participant('test@gmail.com')

        participant.set_type('email')

        participants_list.append(participant)

        participant = Participants()

        participant.set_participant('3409643000000836001')

        participant.set_type('contact')

        participants_list.append(participant)

        record.add_field_value(Field.Events.participants(), participants_list)

        record.add_key_value("$send_notification", True)

        record.add_field_value(Field.Events.event_title(), "New Automated Event")

        end_date_time = datetime(2020, 9, 3, 10, 10, 10)

        record.add_field_value(Field.Events.end_datetime(), end_date_time)

        remind_at_value = datetime(2020, 7, 3, 8, 10, 10)

        record.add_field_value(Field.Events.remind_at(), remind_at_value)

        record.add_field_value(Field.Events.check_in_status(), 'PLANNED')

        what_id = ZCRMRecord()

        what_id.set_id(3409643000002157023)

        record.add_field_value(Field.Events.what_id(), what_id)

        record.add_key_value("$se_module", "Leads")

        """
        End Activity
        """

        """
        Following methods are being used only by Price_Books module
        """
        pricing_details_list = []

        pricing_detail = PricingDetails()

        pricing_detail.set_from_range(1.0)

        pricing_detail.set_to_range(5.0)

        pricing_detail.set_discount(2.0)

        pricing_details_list.append(pricing_detail)

        pricing_detail = PricingDetails()

        pricing_detail.add_key_value('from_range', 6.0)

        pricing_detail.add_key_value('to_range', 11.0)

        pricing_detail.add_key_value('discount', 3.0)

        pricing_details_list.append(pricing_detail)

        record.add_field_value(Field.Price_Books.pricing_details(), pricing_details_list)

        record.add_key_value("Email", "z1@zoho.com")

        record.add_field_value(Field.Price_Books.description(), "My Price Book")

        record.add_field_value(Field.Price_Books.price_book_name(), 'book_name')

        record.add_field_value(Field.Price_Books.pricing_model(), Choice('Flat'))

        """
        End of Price_Books
        """

        # Used when GDPR is enabled
        data_consent = Consent()

        data_consent.set_consent_remarks("Approved.")
        
        data_consent.set_consent_through('Email')

        data_consent.set_contact_through_email(True)

        data_consent.set_contact_through_social(False)

        record.add_field_value('Data_Processing_Basis_Details', data_consent)

        tags_list = []

        tag = Tag()

        tag.set_name("My Record")

        tags_list.append(tag)

        record.add_key_value('Tag', tags_list)

        # Add Record instance to the list
        records_list.append(record)

        # Set the list to data in BodyWrapper instance
        request.set_data(records_list)

        trigger = ["approval", "workflow", "blueprint"]

        # Set the list containing the trigger operations to be run
        request.set_trigger(trigger)

        lar_id = '3409643000002157065'

        # Set the larId
        request.set_lar_id(lar_id)

        process = ["review_process"]

        # Set the array containing the process to be run
        request.set_process(process)

        header_instance = HeaderMap()

        # Call create_records method that takes BodyWrapper instance and module_api_name as parameters
        response = record_operations.create_records(module_api_name, request, header_instance)

        if response is not None:
            # Get the status code from response
            print('Status Code: ' + str(response.get_status_code()))

            # Get object from response
            response_object = response.get_object()

            if response_object is not None:

                # Check if expected ActionWrapper instance is received.
                if isinstance(response_object, ActionWrapper):

                    # Get the list of obtained ActionResponse instances
                    action_response_list = response_object.get_data()

                    for action_response in action_response_list:

                        # Check if the request is successful
                        if isinstance(action_response, SuccessResponse):
                            # Get the Status
                            print("Status: " + action_response.get_status().get_value())

                            # Get the Code
                            print("Code: " + action_response.get_code().get_value())

                            print("Details")

                            # Get the details dict
                            details = action_response.get_details()

                            for key, value in details.items():
                                print(key + ' : ' + str(value))

                            # Get the Message
                            print("Message: " + action_response.get_message().get_value())

                        # Check if the request returned an exception
                        elif isinstance(action_response, APIException):
                            # Get the Status
                            print("Status: " + action_response.get_status().get_value())

                            # Get the Code
                            print("Code: " + action_response.get_code().get_value())

                            print("Details")

                            # Get the details dict
                            details = action_response.get_details()

                            for key, value in details.items():
                                print(key + ' : ' + str(value))

                            # Get the Message
                            print("Message: " + action_response.get_message().get_value())

                # Check if the request returned an exception
                elif isinstance(response_object, APIException):
                    # Get the Status
                    print("Status: " + response_object.get_status().get_value())

                    # Get the Code
                    print("Code: " + response_object.get_code().get_value())

                    print("Details")

                    # Get the details dict
                    details = response_object.get_details()

                    for key, value in details.items():
                        print(key + ' : ' + str(value))

                    # Get the Message
                    print("Message: " + response_object.get_message().get_value())
 