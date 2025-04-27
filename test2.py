import requests
from decouple import config


AUTH_TOKEN = config('AUTH_TOKEN')
PHONE_NUMBER_ID = config('PHONE_NUMBER_ID')
TO_PHONE_NUMBER = config('TO_PHONE_NUMBER')

url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "messaging_product": "whatsapp",
    "to": TO_PHONE_NUMBER,
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": {
        "code": "en_US"
      },
    }
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.json())
