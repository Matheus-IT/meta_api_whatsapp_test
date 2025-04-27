# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

curl -X POST https://graph.facebook.com/v22.0/$PHONE_NUMBER_ID/messages \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "'"$TO_PHONE_NUMBER"'",
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": {
        "code": "en_US"
      },
    }
  }'
