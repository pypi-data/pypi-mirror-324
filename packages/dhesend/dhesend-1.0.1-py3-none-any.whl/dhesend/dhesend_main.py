from typing import Literal, Union, Dict, Any
from requests import request
from requests.exceptions import JSONDecodeError, InvalidJSONError, ConnectionError

from .constants import BASE_URL, USER_AGENT
from ._email import Email
from .domain import Domain
from .apikey import Apikey
from .webhook import Webhook

class Dhesend:
    def __init__(self, api_key: str, user_agent=USER_AGENT, base_url=BASE_URL):
        if not api_key:
            raise ValueError("Missing API key. Pass it to constructor `Dhesend(api_key)`")
        
        self.__key = api_key
        self.user_agent = user_agent
        self.base_url = base_url
        self.Email = Email(self)
        self.Domain = Domain(self)
        self.Apikey = Apikey(self)
        self.Webhook = Webhook(self)
    
    def fetch_request(
        self, 
        path: str, 
        method: Literal["get", "post"] = "get",
        headers: Dict[str, str] = {},
        options: Dict[str, Any] = {},
    ):
        try:
            headers = { **headers, **self.get_headers() }
            response = request(
                method=method,
                url=f'{self.base_url}/{path}',
                headers=headers,
                **options
            )
            
            if not response.ok:
                try:
                    error = response.json()
                    return {
                        "data": None,
                        "error": error["error"] if isinstance(error, object) and error["error"] else error or "Oops! Something went wrong, please try again later.",
                    }
                except:
                    return {
                        "data": None,
                        "error": f"Cannot proceed your request, with status code: {response.status_code}"
                    }
            data = response.json()
            return {
                "data": data,
                "error": None
            }
        except JSONDecodeError or InvalidJSONError:
            return {
                "data": None,
                "error": "Oops! Could not parse data into json."
            }
        except ConnectionError:
            return {
                "data": None,
                "error": "Failed to establish a connection."
            }
        except Exception as exception:
            return {
                "data": None,
                "error": f"Unexpected exception ocurred: {exception}"
            }
    
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.__key}",
            "User-Agent": self.user_agent,
        }
    
    def post(
        self, 
        path: str,
        body: Dict[str, Any], 
        headers: Dict[str, str] = {}, 
        files: Union[Dict[str, Any], None] = None
    ):
        options = {
            "json": body,
            "files": files
        }
        
        if not files:
            headers["Content-Type"] = "application/json"
        
        return self.fetch_request(
            path=path,
            method="post",
            headers=headers,
            options=options
        )
    
    def get(self, path: str, headers: Dict[str, str] = {}):
        headers["Content-Type"] = "application/json"
        
        return self.fetch_request(
            path=path,
            method="get",
            headers=headers,
        )
        