from typing import List, TYPE_CHECKING

from .api_paths import CREATE_APIKEY_PATH, LIST_APIKEY_PATH, DELETE_APIKEY_PATH
from .project_type import Apikey, FetchResponse

if TYPE_CHECKING:
    from .dhesend_main import Dhesend
    
class Apikey:
    def __init__(self, dhesend: "Dhesend"):
        self.dhesend = dhesend
    
    def create(self, title = None) -> FetchResponse[Apikey]:
        return self.dhesend.post(path=CREATE_APIKEY_PATH, body={ "title": title })
    
    def list(self) -> FetchResponse[List[Apikey]]:
        return self.dhesend.get(path=LIST_APIKEY_PATH)
    
    def delete(self, token: str):
        return self.dhesend.post(path=DELETE_APIKEY_PATH, body={ "token": token })