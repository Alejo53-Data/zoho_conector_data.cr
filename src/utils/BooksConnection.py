import json
from datetime import datetime, timedelta
import requests


#Zoho Books  Api Credentials
ZBOOKS_CLIENT_ID="1000.ODFVF4TA4TKUU6D0ZFHAXRWK63WTRH"
ZBOOKS_CLIENT_SECRECT="e1128e2f6d734d63b2dc1b758850f401ca087b80cd"
ZBOOKS_REFRESH_TOKEN="1000.cc7b875d37ff1a1c7183cf680f8b915d.72fcc336800831dde6a04765ea60a19b"
ZBOOKS_GRAND_TYPE="refresh_token"
#ZBOOKS_ORGANITATION_ID="762683427" ## SAND BOX Organization ID
ZBOOKS_ORGANITATION_ID="696634191" ## American Data Organization ID

class BooksConnection:

    def __init__(self) -> None:
        self.client_id = ZBOOKS_CLIENT_ID
        self.client_secret = ZBOOKS_CLIENT_SECRECT
        self.refresh_token = ZBOOKS_REFRESH_TOKEN
        self.grant_type = ZBOOKS_GRAND_TYPE
        #LOAD Access Token from File
        with open('src/json/zbooks_persistance.json', 'r') as openfile:
            zbooks_persistance_object = json.load(openfile)

        self.access_token = zbooks_persistance_object.get("access_token")
        self.check_connection()


    def check_connection(self):
        #FIXME  must select and API without IDS
        request_query = {
            "url": f'https://books.zoho.com/api/v3/organizations',
            "headers": {"Authorization": f"Zoho-oauthtoken {self.access_token}"},
        }

        get_more_contacts_list_response = requests.get(**request_query)
        if get_more_contacts_list_response.status_code == 200:
            return True
        else:
            return self.refresh_access_token()

    def refresh_access_token(self):

        form_body = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': self.grant_type,
        }
        access_token_response = requests.post('https://accounts.zoho.com/oauth/v2/token', data=form_body)

        if access_token_response.status_code == 200:
            access_token = access_token_response.json().get("access_token")
            _current_datetime = datetime.now()
            try:
                # Data to be written
                dictionary = {
                    "access_token": access_token,
                    "token_state": "Active"
                }

                # Serializing json
                json_object = json.dumps(dictionary, indent=2)

                # Writing to sample.json
                with open("zbooks_persistance.json", "w") as outfile:
                    json.dump(dictionary, outfile)

                self.access_token = access_token
                return True
            except Exception as error:
                print(error)
                self.access_token = None
                return False
        else:
            print(f"Error: {access_token_response.status_code}")
            self.access_token = None
            return False

    def create_record(self,**kwargs):
        pass

    def list_record(self,**kwargs):
        pass

    def update_record(self, **kwargs):
        pass

    def delete_record(self,**kwargs):
        pass

    def get_record(self, **kwargs):
        pass

    def get_records(self, **kwargs):
        pass

    def enable_record(self,**kwargs):
        pass

    def disable_record(self,**kwargs):
        pass

    def add_comment(self):
        pass

    def mark_record(self,**kwargs):
        pass

    def void_record(self,**kwargs):
        pass

    def submit_record(self):
        pass

    def del_comment(self):
        pass

    def activate_record(self):
        pass

    def inactivate_record(self):
        pass

    def email_record(self,**kwargs):
        pass

    def email_records(self,**kwargs):
        pass

    def approve_record(self):
        pass