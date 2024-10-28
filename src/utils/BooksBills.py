import requests
from ADNBooksAPI.settings import ZBOOKS_ORGANITATION_ID
from czohobooks.utils.BooksConnection import BooksConnection

class BooksBills(BooksConnection):
    def __init__(self):
        super().__init__()
        self.headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}

    def create_record(self,**kwargs):
        """
        
        """
        pass