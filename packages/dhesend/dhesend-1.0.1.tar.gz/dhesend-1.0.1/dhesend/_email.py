from typing import TYPE_CHECKING, List

from .api_paths import GET_EMAIL_PATH, SEND_EMAIL_PATH, LIST_EMAIL_PATH
from .project_type import (
    SendEmailPayload, 
    FetchResponse,
    GetEmailDetails,
    SendEmailResponse,
    ListEmailResponse,
    AttachmentFile,
)

if TYPE_CHECKING:
    from .dhesend_main import Dhesend

class Email:
    def __init__(self, dhesend: "Dhesend"):
        self.dhesend = dhesend
    
    def send(self, payload: SendEmailPayload) -> FetchResponse[SendEmailResponse]:                
        payload["from"] = payload.get("from_")
        payload.pop("from_", None)
        
        attachments = payload.get("attachments")
        if attachments and isinstance(attachments, AttachmentFile):
            payload.pop("attachments", None)
            
            return self.dhesend.post(
                path=SEND_EMAIL_PATH,
                body={ **payload },
                files=attachments
            )
        
        return self.dhesend.post(
            path=SEND_EMAIL_PATH,
            body=payload,
        )
    
    def list(self) -> FetchResponse[List[ListEmailResponse]]:
        return self.dhesend.get(LIST_EMAIL_PATH)

    def get(self, id: str) -> FetchResponse[GetEmailDetails]:
        return self.dhesend.get(GET_EMAIL_PATH(id=id))        
    