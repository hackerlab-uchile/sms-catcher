import base64
from datetime import datetime
import dateutil
from fastapi import APIRouter
import json
import requests
import os
from app.utils.database_querys import get_messages_with_timestamp_after
from app.utils.get_page_info import get_webpage_title, generate_screenshot, extract_url, get_dns_and_certificate
from datetime import timedelta

router = APIRouter()

messages_sent_path = os.path.join(os.path.dirname(__file__), "..", "resources", "last_messages_sent.txt")
modem_path = os.path.join(os.path.dirname(__file__), "..", "resources", "modem_info.json")

# Post a message from a specific modem to
# an external API
@router.post("/send_message")
async def post_modem_info():
    messages_to_save = 10
    # first, we open the last_messages_sent.txt file to check the last messages sent
    with open(messages_sent_path, "r") as f:
        last_messages_sent = f.read().splitlines()
    # Now we get the modem_info.json file
    with open(modem_path, "r") as f:
        modem_info = json.load(f)
    # Now we send every message wich key is not in last_messages_sent
    for message_key, message in modem_info.items():
        if message_key not in last_messages_sent:
            response = requests.post("http://127.0.0.1:8002/", json=message)
            if response.status_code == 200:
                last_messages_sent.append(message_key)
    # Now we update the last_messages_sent.txt file
    # Sidenote: we are supposed to only have the last X messages sent
    # for efficiency
    with open(messages_sent_path, "w") as f:
        for message_key in last_messages_sent[-messages_to_save:]:
            f.write(message_key + "\n")
    return "Messages sent"

# Post a message from a specific modem to
# an external API
@router.post("/send_message2")
async def post_modem_info2(x_minutes=17820):
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
        # now we get the webpage title
        #webpage_title = get_webpage_title(url)

        # # now we generate the screenshot in a temporary file located in ../temp/{screenshoot_name}.jpg
        # screenshot_name = f"../temp/{message.id}.jpg"
        # generate_screenshot(url, screenshot_name)
        # with open(screenshot_name, "rb") as f:
        #     screenshot = base64.b64encode(f.read()).decode("utf-8")
        # os.remove(screenshot_name)

        # now we get the DNS and certificate information
        page_dns = get_dns_and_certificate(url)
        # now we fill up the message json
        messages_json[message.id] = {
            "number": message.number,
            "text": message_text,
            "pdu_type": message.pdu_type,
            "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            "url": url,
            #"webpage_title": webpage_title,
            # "screenshot": screenshot,
            "page_info": page_dns

        }
    # now we send the messages to the external API
    response = requests.post("http://127.0.0.1:8002/", json=messages_json)
    if response.status_code == 200:
        return "Messages sent"
    else:
        return "Error sending messages"
