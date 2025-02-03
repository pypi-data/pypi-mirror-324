from typing import (
    Literal, Optional, TypedDict, Tuple, Type, Union, Generic, TypeVar,
    List, Dict, Any
)
from io import IOBase
from enum import Enum

AttachmentFile = Dict[str, Tuple[str, Type[IOBase]]]

class Tag(TypedDict):
    """
    Represents an email tag with a name and value.
    
    - Name and value must contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).
    - Length must not exceed 256 characters.
    """
    name: str
    value: str


class Attachment(TypedDict):
    """
    Represents an email attachment.
    
    - `url`: The URL of the attachment.
    - `filename` (Optional): The file name for the attachment, can be derived from the `url` if not provided.
    - `contentType` (Optional): The content type for the attachment, can be derived from the `url` if not provided.
    """
    url: str
    filename: Optional[str]
    contentType: Optional[str]


class SendEmailPayload(TypedDict):
    """
    Represents the payload for sending an email.
    
    - `from`: The sender's email address. To include a display name, use the format "Your Name <sender@domain.com>".
    - `to`: The recipient's email address(es), accepts an array of strings (max 50 combined `to`, `cc`, `bcc`).
    - `cc`: Optional carbon copy (CC) recipients.
    - `bcc`: Optional blind carbon copy (BCC) recipients.
    - `replyTo`: Optional reply-to email addresses.
    - `subject`: The subject of the email.
    - `htmlBody`: The HTML content of the email (optional).
    - `textBody`: The plain text content of the email (optional).
    - `tags`: Optional tags for categorizing or labeling the email.
    - `attachments`: Optional list of email attachments, can either be a list of `Attachment` or `AttachmentFile` objects. (max 15 files, total size <= 25 MB).
    """
    from_: Optional[str] # type: ignore
    to: List[str]
    cc: Optional[List[str]]
    bcc: Optional[List[str]]
    replyTo: Optional[List[str]]
    subject: str
    htmlBody: Optional[str]
    textBody: Optional[str]
    tags: Optional[List[Tag]]
    attachments: Optional[Union[List[Attachment], AttachmentFile]]


class EmailStatus(Enum):
    DELIVERED = "delivery"
    SCHEDULED = "scheduled"
    SENT = "SENT"
    COMPLAINED = "complaint"
    BOUNCED = "bounce"
    FAILED = "failed" 
    OPENED = "opened" 
    CLICKED = "clicked" 
    
T = TypeVar('T')
class FetchResponse(TypedDict):
    """
    Response of any request sent by `Dhesend`.
    """
    data: Union[None, T]
    error: Union[None, str, Dict[str, Any]]


class SendEmailResponse(TypedDict):
    """
    Response of sent email
     - `id`: The unique identifier of email.
    """
    id: str

class ListEmailResponse(TypedDict):
    to: str
    subject: str
    id: str
    createdAt: str | int
    status: EmailStatus

class GetEmailDetails(TypedDict):
    """
    Details of an email retrieved by ID
    
    - `id`: Unique identifier for the email
    - `from`: Sender's email address
    - `tags`: Tags associated with the email. May be null.
    - `to`: List of recipient email addresses
    - `cc`: List of CC recipients. May be null.
    - `bcc`: List of BCC recipients. May be null.
    - `replyTo`: List of Reply-To email addresses. May be null.
    - `subject`: Subject of the email
    - `htmlBody`: HTML content of the email. May be null.
    - `textBody`: Plain text content of the email. May be null.
    - `status`: Current status of the email
    - `createdAt`: Timestamp when the email was created
    - `completedAt`: Timestamp when the email was completed (if applicable). May be null.
    - `scheduledAt`: Timestamp when the email was scheduled (if applicable). May be null.
    """

    id: str
    from_: str
    tags: Optional[List['Tag']]
    to: List[str]
    cc: Optional[List[str]]
    bcc: Optional[List[str]]
    replyTo: Optional[List[str]]
    subject: str
    htmlBody: Optional[str]
    textBody: Optional[str]
    status: EmailStatus
    createdAt: str
    completedAt: Optional[str]
    scheduledAt: Optional[str]


class TXTRecord(TypedDict):
    """
    Represents a single txt record with name and value.
    """
    name: str
    value: str

class DKIMRecord(TypedDict):
    """
    Represents a single dkim record
    - `name`: Record name
    - `type`: Type of record (e.g., CNAME)
    - `value`: Record value
    """
    name: str
    type: str
    value: str
        
class CreateDomainResponse(TypedDict):
    """
    Response of domain creation
    
    - `name`: Domain name.
    - `message`: Informational message.
    - `txt`: TXT record details to add to the domain's DNS settings
    - `dkim`: DKIM records to add to the domain's DNS settings
    """
    name: str
    message: str
    txt: TXTRecord
    dkim: List[DKIMRecord]

class GetDomainResponse(TypedDict):
    domainName: str
    status: Literal["failed", "verified", "verifying"]
    txt: TXTRecord
    dkim: List[DKIMRecord]
    createdAt: str
    
class ListDomainDetail(TypedDict):
    """
    Response of list domain
    - `domain`: Name of domain
    - `status`: Status of domain
    - `createAt`: Date and time when the domain was created
    - `updatedAt`: Date and time when the domain was last updated
    """
    domainName: str
    status: Literal["failed", "verified", "verifying"]
    createdAt: str
    updatedAt: str
    

class DeleteDomainResponse(TypedDict):
    """
    Delete domain response
    - `success`: Succcess message
    """
    success: str
    
    
class Apikey(TypedDict):
    """
    Api key structure
    - `title`: Title of api key
    - `token`: Token of api key
    """
    title: str
    token: str
    
    
class WebhookEvent(Enum):
    EMAIL_SENT = "email:sent"
    EMAIL_DELIVERED = "email:delivered"
    EMAIL_OPENED = "email:opened"
    EMAIL_CLICKED = "email:clicked"
    EMAIL_BOUNCED = "email:bounced"
    EMAIL_FAILED = "email:failed"
    EMAIL_COMPLAINT = "email:complaint"

class CreateWebhookResponse(TypedDict):
    """
    Response when a webhook is successfully created
    - `id`: Unique identifier for the created webhook
    - `secret`: Secret token to verify incoming webhook requests
    """
    id: str
    secret: str
    

class ListWebhookResponse(TypedDict):
    """
    List webhook response
    - `id`: Unique identifier of the webhook
    - `endpoint`: Endpoint URL of the webhook
    - `events`: List of events the webhook is configured to handle
    - `createdAt`: Date and time the webhook was created
    - `status`: Current status of the webhook
    - `secret`: Webhook secret for request verification
    """
    id: str
    endpoint: str
    events: List[WebhookEvent]
    createdAt: str
    secret: str
    status: Literal["enabled", "disabled"]


class UpdateWebhookStatusResponse(TypedDict):
    """
    Response when a webhook status is updated
    - `id`: Unique identifier of the webhook
    - `status`: Updated status of the webhook
    """
    id: str
    status: Literal["enabled", "disabled"]


class RefreshWebhookSecretResponse(TypedDict):
    """
    Response when a webhook secret is refreshed
    - `id`: Unique identifier of the webhook
    - `secret`: New secret token for webhook verification
    """
    id: str
    secret: str


class DeleteWebhookResponse(TypedDict):
    """
    Response when a webhook is successfully deleted
    - `success`: Confirmation message indicating successful deletion
    """
    success: str
    