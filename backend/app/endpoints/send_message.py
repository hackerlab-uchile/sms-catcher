import base64
from datetime import datetime
import dateutil
from fastapi import APIRouter
import json
import requests
import os
from app.utils.database_querys import get_messages_with_timestamp_after
from app.utils.get_page_info import extract_url, get_dns_and_certificate, capture_page_info
from datetime import timedelta

router = APIRouter()

messages_sent_path = os.path.join(os.path.dirname(__file__), "..", "resources", "last_messages_sent.txt")
modem_path = os.path.join(os.path.dirname(__file__), "..", "resources", "modem_info.json")

# Post a message from a specific modem to
# an external API
@router.post("/send_message")
async def post_modem_info(x_minutes=17820):
    # We get the messages of the last x_minutes minutes
    time_to_query = datetime.now() - timedelta(minutes=int(x_minutes))
    messages = get_messages_with_timestamp_after(time_to_query.astimezone(dateutil.tz.gettz('Chile/Continental')))
    # now we only keep the smishing messages
    messages = [message for message in messages if message.type == "smish"]

    for message in messages:
        print(message.text)
    # now we create an empty json to fill up with the messages
    messages_json = {}
    # now we fill up the json
    for message in messages:
        # First, we get the message text
        message_text = message.text
        # now we extract the URL from the message text
        url = extract_url(message_text)
        print(f'URL: {url}')
        # # now we generate the screenshot in a temporary file located in ../temp/{screenshoot_name}.jpg
        screenshot_name = f"{message.id.split(' ')[-1]}.jpg"
        title, urls, screenshot = await capture_page_info(url, screenshot_name)

        # now we get the DNS and certificate information
        page_dns = {}
        if urls is not None:
            for url in urls:
                dns_info, cert_info = get_dns_and_certificate(url)
                page_dns[url] = {
                    "dns": dns_info,
                    "certificate": cert_info
                }
        # now we fill up the message json
        messages_json[message.id] = {
            "number": message.number,
            "text": message_text,
            "pdu_type": message.pdu_type,
            "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            "url": url,
            "title": title,
            "screenshot": screenshot,
            "page_info_with_redirects": page_dns
        }
    # now we make it to json format
    messages_json = json.dumps(messages_json, indent = 4)
    # now we send the messages to the external API
    response = requests.post("http://127.0.0.1:8002/", json=messages_json)
    if response.status_code == 200:
        return "Messages sent"
    else:
        return "Error sending messages"
