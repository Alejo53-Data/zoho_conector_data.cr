import requests

from settings import ZBOOKS_ORGANITATION_ID
from utils.BooksConnection import BooksConnection

class BooksContactPersons(BooksConnection):

    def __init__(self):
        super().__init__()
        self.headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

    #Create a contact person for contact.
    def create_record(self,json_client):
        """
            Required *  optional -
            Query Params
            contact_id * string Contact id of the contact
            salutation string Salutation for the contact. Max-length [25]
            first_name string (Required)
            First name of the contact person. Max-length [100]
            last_name string Last name of the contact person. Max-length [100]
            email string Email address of the contact person. Max-length [100]
            phone string Max-length [50]
            mobile string Max-length [50]
            skype string skype address. Max-length [50]
            designation string designation of a person. Max-length [50]
            department string department on which a person belongs. Max-length [50]
            enable_portal boolean option to enable the portal access. allowed values true,false

            {
            "contact_id": 460000000026049,
            "salutation": "Mr",
            "first_name": "Will",
            "last_name": "Smith",
            "email": "willsmith@bowmanfurniture.com",
            "phone": "+1-925-921-9201",
            "mobile": "+1-4054439562",
            "skype": "zoho",
            "designation": "Sales Engineer",
            "department": "Sales",
            "enable_portal": true
        }
        """
        json_data = json_client
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_create = requests.post(
            f'https://books.zoho.com/api/v3/contacts/contactpersons?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)
        return json_create.json()

    #Update an existing contact person.
    def update_record(self,contact_id ,json_client):
        """
            contact_id  string  (Required) Contact id of the contact
            salutation string Salutation for the contact. Max-length [25]
            first_name string (Required) First name of the contact person. Max-length [100]
            last_name string  Last name of the contact person. Max-length [100]
            email string Email address of the contact person. Max-length [100]
            phone string  Max-length [50]
            mobile string  Max-length [50]
            skype string skype address. Max-length [50]
            designation string designation of a person. Max-length [50]
            department string department on which a person belongs. Max-length [50]
            enable_portal boolean option to enable the portal access. allowed values true,false
            is_primary_contact boolean To mark contact person as primary for contact


            Response
            {
    "code": 0,
    "message": "The contactperson details has been updated.",
    "contact_person": [
        {
            "contact_id": 460000000026049,
            "contact_person_id": 460000000026051,
            "salutation": "Mr",
            "first_name": "Will",
            "last_name": "Smith",
            "email": "willsmith@bowmanfurniture.com",
            "phone": "+1-925-921-9201",
            "mobile": "+1-4054439562",
            "is_primary_contact": true,
            "skype": "zoho",
            "designation": "Sales Engineer",
            "department": "Sales",
            "is_added_in_portal": true
        },


        """
        json_data = json_client
        headers = {
            "Content-Type": "application/json", "Authorization": f"Zoho-oauthtoken {self.access_token}"}
        json_create = requests.put(
            f'https://books.zoho.com/api/v3/contacts/contactpersons/{contact_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=headers, data=json_data)
        return json_create.json()




    #ist all contacts with pagination. que pasa si tienes mas paginas? Need 1
    def get_records(self, client_id):
        """
        Arguments
        client_id

        Response
            {
        "code": 0,
        "message": "success",
        "contact_persons": [
            {
                "contact_person_id": 460000000026051,
                "salutation": "Mr",
                "first_name": "Will",
                "last_name": "Smith",
                "email": "willsmith@bowmanfurniture.com",
                "phone": "+1-925-921-9201",
                "mobile": "+1-4054439562",
                "is_primary_contact": true,
                "skype": "zoho",
                "designation": "Sales Engineer",
                "department": "Sales",
                "is_added_in_portal": true
            },
            {...},
            {...}
        ],
        "page_context": {
            "page": 1,
            "per_page": 200,
            "has_more_page": false,
            "sort_column": "contact_person_id",
            "sort_order": "A"
        }
    }
        """
        get_contacts = requests.get(
            f'https://books.zoho.com/api/v3/contacts/{client_id}/contactpersons?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=self.headers)

        return get_contacts.json()

    #Mark a contact person as primary for the contact
    def mark_record(self,contact_id):
        """
        Arguments
        contact_id
        client_id

        Response:
        {
            "code": 0,
            "message": "This contact person has been marked as your primary contact person."
        }
        """
        del_contact = requests.post(
            f'https://books.zoho.com/api/v3/contacts/contactpersons/{contact_id}/primary?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=self.headers)
        return del_contact.json()

    #Get the contact person details.
    def get_record(self, contact_id,client_id):
        """
            Arguments
            contact_id
            client_id

            Response:
            {
                "code": 0,
                "message": "success",
                "contact_person": {
                    "contact_id": 460000000026049,
                    "contact_person_id": 460000000026051,
                    "salutation": "Mr",
                    "first_name": "Will",
                    "last_name": "Smith",
                    "email": "willsmith@bowmanfurniture.com",
                    "phone": "+1-925-921-9201",
                    "mobile": "+1-4054439562",
                    "is_primary_contact": true,
                    "skype": "zoho",
                    "designation": "Sales Engineer",
                    "department": "Sales",
                    "is_added_in_portal": true
                }
            }
            """
        get_contact = requests.get(
            f'https://books.zoho.com/api/v3/contacts/{client_id}/contactpersons/{contact_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=self.headers)
        return get_contact.json()

    #Delete an existing contact person.
    def delete_record(self,contact_id):
        """
        Argument
        contact_id

        response

        {
            "code": 0,
            "message": "The contact person has been deleted."
        }
        """
        del_contact = requests.delete(
            f'https://books.zoho.com/api/v3/contacts/contactpersons/{contact_id}?organization_id={ZBOOKS_ORGANITATION_ID}',
            headers=self.headers)
        return del_contact.json()

