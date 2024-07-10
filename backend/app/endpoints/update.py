import os
from fastapi import APIRouter
import subprocess
import json
from app.utils.parser import parse_message_info
from app.utils.message_obtaining import extract_first_non_space_substring, extract_message_list, extract_message_info
from app.config.database import Session, engine, Base
from app.models.messages import Message
from app.classifier_smish.classify_text import classify_text
from app.utils.normalize_time import parse_timezone
import hashlib

router = APIRouter()

message_table = []

Base.metadata.create_all(bind=engine)

modem_path = os.path.join(os.path.dirname(__file__), "..", "resources", "modem_info.json")

@router.post("/update_modem_info")
async def update_modem_info():
    try:
        output = subprocess.check_output("mmcli -L", shell=True).decode("utf-8")
        modems = output.splitlines()
        
        modems_paths = [extract_first_non_space_substring(line) for line in modems]
        modems_indexes = [modem.split("/")[-1] for modem in modems_paths]

        modems_info = {}
        for modem_index in modems_indexes:
            messages = extract_message_list(modem_index)
            if messages:
                for message_index in messages:
                    message_info = extract_message_info(modem_index, message_index)
                    if message_info:
                        message = parse_message_info(message_info)
                        message_timestamp = parse_timezone(message["timestamp"])
                        hashed_message = hash(f"{message['number']}_{message['text']}")
                        message_identifier = f"{message_timestamp}_{hashed_message}"
                        modems_info[message_identifier] = message
        
        sorted_messages = dict(sorted(modems_info.items(), key=lambda item: item[1]["timestamp"], reverse=True))

        session = Session()
        for message_key, message in sorted_messages.items():
            if not session.query(Message).filter_by(id=message_key).first():
                message_to_save = Message(
                    id=message_key,
                    type=classify_text(message["text"]),
                    path=message["path"],
                    number=message["number"],
                    text=message["text"],
                    pdu_type=message.get("pdu_type", None),
                    state=message["state"],
                    storage=message["storage"],
                    smsc=message["smsc"],
                    timestamp=message_timestamp  # Use the normalized timestamp here
                )
                session.add(message_to_save)
        session.commit()
        session.close()
        return "Modem info updated"
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"
