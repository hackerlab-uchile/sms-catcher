from datetime import datetime
import dateutil
from fastapi import APIRouter
import json
import requests
import os
from app.utils.database_querys import get_messages_with_timestamp_after
from app.utils.get_page_info import extract_url, get_ip_and_certificate, capture_page_info
from app.utils.timestamp import get_last_sent_timestamp, set_last_sent_timestamp
from app.utils.normalize_time import parse_timezone
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()

POST_API_URL = os.getenv("POST_API_URL")
API_TOKEN = os.getenv("API_TOKEN")

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

@router.post("/send_message")
async def post_modem_info():
    # Retrieve the last sent timestamp
    last_sent_timestamp_str = get_last_sent_timestamp()
    
    # Parse the last sent timestamp to a datetime object in UTC
    if last_sent_timestamp_str:
        last_sent_timestamp = parse_timezone(last_sent_timestamp_str, timezone='UTC')
    else:
        last_sent_timestamp = datetime.min.replace(tzinfo=dateutil.tz.UTC)

    # Query messages with a timestamp after the last sent timestamp
    messages = get_messages_with_timestamp_after(last_sent_timestamp)
    
    # Filter for smishing messages
    messages = [message for message in messages if message.type == "smish"]

    messages_json = {}

    for message in messages:
        message_text = message.text
        url = extract_url(message_text)
        print(f'URL: {url}')
        
        screenshot_name = f"{message.id.split(' ')[-1]}.jpg"
        title, urls, screenshot = await capture_page_info(url, screenshot_name)
        final_url = urls[-1] if urls else ""
        ip_info, cert_info = get_ip_and_certificate(final_url)
        
        messages_json[message.id] = {
            "number": message.number,
            "text": message_text,
            "pdu_type": message.pdu_type,
            "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            "url": url,
            "title": title,
            "screenshot": screenshot,
            "urls": urls,
            "final_url": final_url,
            "ip_info": ip_info,
            "cert_info": cert_info
        }

    if messages_json == {}:
        return
    
    messages_json = json.dumps(messages_json, indent=4)
    
    response = requests.post(POST_API_URL, headers=headers, json=messages_json)
    
    if response.status_code == 200:
        # Update the last sent timestamp to the latest message timestamp
        if messages:
            latest_timestamp = max(message.timestamp for message in messages)
            set_last_sent_timestamp(latest_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'))
        return "Messages sent"
    else:
        return "Error sending messages"
