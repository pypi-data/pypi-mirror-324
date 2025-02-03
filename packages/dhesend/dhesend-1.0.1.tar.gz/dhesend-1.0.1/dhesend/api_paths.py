
# Email paths
SEND_EMAIL_PATH = "email/send"
LIST_EMAIL_PATH = "email/list"
def GET_EMAIL_PATH(id: str): return f"email/{id}"

# Domain paths
CREATE_DOMAIN_PATH = "domain/create"
def GET_DOMAIN_PATH(domain: str): return f"domain/${domain}"
LIST_DOMAIN_PATH = "domain/list"
DELETE_DOMAIN_PATH = "domain/delete"

# Api key paths
CREATE_APIKEY_PATH = "apikey/create"
LIST_APIKEY_PATH = "apikey/list"
DELETE_APIKEY_PATH = "apikey/delete"

# Webhook paths
CREATE_WEBHOOK_PATH = "webhook/create"
def GET_WEBHOOK_PATH(id: str): return f"webhook/${id}"
LIST_WEBHOOK_PATH = "webhook/list"
DELETE_WEBHOOK_PATH = "webhook/delete"
REFRESH_WEBHOOK_SECRET_PATH = "webhook/refresh-secret"
UPDATE_WEBHOOK_STATUS_PATH="webhook/update-status"
