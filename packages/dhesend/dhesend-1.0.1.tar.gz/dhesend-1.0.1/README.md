# Dhesend Python SDK

A Python library for interacting with the Dhesend API, designed to make email sending simple and efficient.
For full documentation, visit the [official website](https://dhesend.com/docs/introduction).

## Installation

Install the SDK using your preferred package manager:

```bash
pip install dhesend
```

## Examples

Discover example integrations with various frameworks:

- [Python Example](https://github.com/dhesend-org/dhesend-python-example)
- [Django Example)](https://github.com/dhesend-org/dhesend-django-example)
- [Flask](https://github.com/dhesend-org/dhesend-nextjs-pages-router-example)

## Setup

1. **Obtain an API Key:**  
      Get your API key from the [Dhesend Dashboard](https://dhesend.com).

2. **Initialize the SDK:**  
      Use your API key to create an instance of the Dhesend client.

```py
from dhesend import Dhesend

dhesend = Dhesend('your_api_key_here'); # Replace with your actual API key
```

## Usage

### Sending Your First Email

```py
from dhesend import Dhesend, SendEmailPayload

dhesend = Dhesend("your-apikey")

params: SendEmailPayload = {
    "from": "Dhesend <example@domain.com>",
    "to": ['example@dhesend.com'],
    "subject": 'Welcome to Dhesend',
    "textBody": 'Have a nice day!',
}

response = dhesend.Email.send(params)
print(response)
```

### Sending Emails with Custom HTML

```py
from dhesend import Dhesend, SendEmailPayload

dhesend = Dhesend("your-apikey")

params: SendEmailPayload = {
    "from": "Dhesend <example@domain.com>",
    "to": ['example@dhesend.com'],
    "subject": 'Welcome to Dhesend',
    "htmlBody": '<strong>Have a nice day!</strong>',
}

response = dhesend.Email.send(params)
print(response)
```

## License
MIT License.