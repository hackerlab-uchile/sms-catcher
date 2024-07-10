from http.client import HTTPException
import os
from fastapi import APIRouter
from app.utils.database_querys import get_all_messages
import json
from app.utils.get_page_info import extract_url

router = APIRouter()

modem_path = os.path.join(os.path.dirname(__file__), "..", "resources", "modem_info.json")

# returns all messages in json format
@router.get("/modem_info")
async def get_modem_info():
    all_messages = get_all_messages()
    messages_json = {}

    for message in all_messages:
        message_text = message.text
        url = extract_url(message_text)
        
        messages_json[message.id] = {
            "number": message.number,
            "text": message_text,
            "url": url,
        }
    return messages_json