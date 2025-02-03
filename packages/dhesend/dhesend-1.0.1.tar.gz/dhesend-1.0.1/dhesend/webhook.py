from typing import TYPE_CHECKING, List, Literal
from re import match

if TYPE_CHECKING:
    from .dhesend_main import Dhesend

from .project_type import (
    CreateWebhookResponse,
    ListWebhookResponse,
    WebhookEvent,
    FetchResponse,
    UpdateWebhookStatusResponse,
    RefreshWebhookSecretResponse,
    DeleteWebhookResponse,
)
from .api_paths import (
    CREATE_WEBHOOK_PATH,
    LIST_WEBHOOK_PATH,
    DELETE_WEBHOOK_PATH,
    REFRESH_WEBHOOK_SECRET_PATH,
    UPDATE_WEBHOOK_STATUS_PATH,
    GET_WEBHOOK_PATH
)


class Webhook:
    def __init__(self, dhesend: "Dhesend"):
        self.dhesend = dhesend

    def create(self, endpoint: str, events: List[WebhookEvent]) -> FetchResponse[CreateWebhookResponse]:
        if not self.is_valid_endpoint(endpoint):
            return {
                "data": None,
                "error": "Invalid webhook endpoint. Provide a valid URL, e.g., `https://xyz.com/api/webhook`."
            }

        supported_events = [event.value for event in WebhookEvent]
        if not set(events).issubset(supported_events):
            return {
                "data": None,
                "error": f"Invalid events. Supported events: {', '.join(supported_events)}"
            }

        return self.dhesend.post(
            path=CREATE_WEBHOOK_PATH,
            body={
                "endpoint": endpoint,
                "events": events,
            },
        )

    def get(self, webhookId: str) -> FetchResponse[ListWebhookResponse]:
        return self.dhesend.get(GET_WEBHOOK_PATH(webhookId))

    def list(self) -> FetchResponse[List[ListWebhookResponse]]:
        return self.dhesend.get(path=LIST_WEBHOOK_PATH)

    def update_status(self, webhook_id: str, status: Literal["enabled", "disabled"]) -> FetchResponse[UpdateWebhookStatusResponse]:
        return self.dhesend.post(
            path=UPDATE_WEBHOOK_STATUS_PATH,
            body={
                "webhookId": webhook_id,
                "status": status,
            },
        )

    def refresh_secret(self, webhook_id: str) -> FetchResponse[RefreshWebhookSecretResponse]:
        return self.dhesend.post(
            path=REFRESH_WEBHOOK_SECRET_PATH,
            body={"webhookId": webhook_id},
        )

    def delete(self, webhook_id: str) -> FetchResponse[DeleteWebhookResponse]:
        return self.dhesend.post(
            path=DELETE_WEBHOOK_PATH,
            body={"webhookId": webhook_id},
        )

    @staticmethod
    def is_valid_endpoint(endpoint: str) -> bool:
        pattern = r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(/[\w\-./?%&=]*)?$'
        return bool(match(pattern, endpoint))
