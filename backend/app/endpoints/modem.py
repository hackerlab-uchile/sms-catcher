from http.client import HTTPException
import os
from fastapi import APIRouter
from app.utils.message_obtaining import extract_first_non_space_substring, extract_message_list, extract_message_info
from app.utils.parser import parse_message_info
import json

router = APIRouter()

modem_path = os.path.join(os.path.dirname(__file__), "..", "resources", "modem_info.json")

@router.get("/modem_info")
async def get_modem_info():
    with open(modem_path, "r") as f:
        return json.load(f)
