import os
from fastapi import APIRouter
import subprocess
import json
from app.utils.parser import parse_message_info
from app.utils.message_obtaining import extract_first_non_space_substring, extract_message_list, extract_message_info

router = APIRouter()

modem_path = os.path.join(os.path.dirname(__file__), "..", "resources", "modem_info.json")

@router.post("/last_message")
async def obtain_last_message():
    try:
        output = subprocess.check_output("mmcli -L", shell=True).decode("utf-8")
        modems = output.splitlines()#[1:]  # Exclude the first line
        # Now, for each line, get the first not spacebar string

        modems_paths = [extract_first_non_space_substring(line) for line in modems]
        modems_indexes = [modem.split("/")[-1] for modem in modems_paths]

        modems_info = {}
        for modem_index in modems_indexes:
            messages = extract_message_list(modem_index)
            if messages:
                for message_index in messages:
                    message_info = extract_message_info(modem_index, message_index)
                    message = parse_message_info(message_info)
                    message_hash = hash(message["number"] + message["text"])
                    message_identifier = message["timestamp"] + " " + message_hash
                    message_identifier = str(message["timestamp"]) + " " + str(message_hash)
                    if message_info:
                        modems_info[message_identifier] = parse_message_info(message_info)

        with open(modem_path, "w") as f:
            json.dump(modems_info, f, indent=4)
        return "Modem info updated"
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"