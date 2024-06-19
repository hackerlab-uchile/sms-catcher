from datetime import datetime, timedelta
import os
import subprocess
from fastapi import APIRouter
import json
from app.utils.database_querys import get_all_messages, get_messages_by
from app.utils.normalize_time import parse_timezone

router = APIRouter()

dashboard_path = os.path.join(os.path.dirname(__file__), "..", "resources", "dashboard_info.json")

@router.get("/dashboard")
async def get_dashboard_info():
    # Get the number of connected working modems counting the lines in the output of the command 'mmcli -L'
    connected_modems = len(subprocess.getoutput('mmcli -L').split('\n'))

    # Get the total number of messages
    all_messages = get_all_messages()
    total_messages = len(all_messages)

    # Parse and normalize timestamps for all messages
    for message in all_messages:
        message.timestamp = parse_timezone(message.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    # Get the number of messages per day during the last week
    last_week_messages = {}
    for i in range(7):
        day_str = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        last_week_messages[day_str] = len([m for m in all_messages if m.timestamp.strftime('%Y-%m-%d').startswith(day_str)])
    
    # Reverse the order of the dictionary
    last_week_messages = dict(reversed(last_week_messages.items()))

    # Get the number of messages per month during the last year
    last_months_messages = {}
    current_month = datetime.now().replace(day=1)  # Start from the first day of the current month

    for i in range(12):
        month_str = current_month.strftime('%Y-%m')
        
        # Filter messages for the current month and count them
        messages_count = len([m for m in all_messages if m.timestamp.strftime('%Y-%m').startswith(month_str)])
        
        # Store the count in the dictionary with the month as key
        last_months_messages[month_str] = messages_count
        
        # Move to the previous month
        current_month -= timedelta(days=current_month.day)

    # Reverse the order of the dictionary
    last_months_messages = dict(reversed(last_months_messages.items()))

    # Get the number of messages per year during the last 5 years
    last_years_messages = {}
    for i in range(5):
        year_str = str(datetime.now().year - i)
        last_years_messages[year_str] = len([m for m in all_messages if m.timestamp.strftime('%Y').startswith(year_str)])

    # Reverse the order of the dictionary
    last_years_messages = dict(reversed(last_years_messages.items()))

    # Get the number of messages per phone number
    phone_numbers = list(set([m.number for m in all_messages]))
    messages_per_phone_number = {}
    for phone_number in phone_numbers:
        messages_per_phone_number[phone_number] = len([m for m in all_messages if m.number == phone_number])

    # Get the total number of smishings
    smishings = get_messages_by('type', 'smish')
    total_smishings = len(smishings)

    # Get the total number of legitimate messages
    legit_messages = get_messages_by('type', 'legit')
    total_legit = len(legit_messages)

    # Parse and normalize timestamps for smishing messages
    for smish in smishings:
        smish.timestamp = parse_timezone(smish.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    # Get the number of smishings per day during the last week
    last_week_smishings = {}
    for i in range(7):
        day_str = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        last_week_smishings[day_str] = len([m for m in smishings if m.timestamp.strftime('%Y-%m-%d').startswith(day_str)])

    # Reverse the order of the dictionary
    last_week_smishings = dict(reversed(last_week_smishings.items()))

    # Get the number of smishings per month during the last year
    last_months_smishings = {}
    current_month = datetime.now().replace(day=1)
    for i in range(12):
        month_str = current_month.strftime('%Y-%m')
        messages_count = len([m for m in smishings if m.timestamp.strftime('%Y-%m').startswith(month_str)])
        last_months_smishings[month_str] = messages_count
        current_month -= timedelta(days=current_month.day)

    # Reverse the order of the dictionary
    last_months_smishings = dict(reversed(last_months_smishings.items()))

    # Get the number of smishings per year during the last 5 years
    last_years_smishings = {}
    for i in range(5):
        year_str = str(datetime.now().year - i)
        last_years_smishings[year_str] = len([m for m in smishings if m.timestamp.strftime('%Y').startswith(year_str)])

    # Reverse the order of the dictionary
    last_years_smishings = dict(reversed(last_years_smishings.items()))

    # Count the number of smishings per phone number and get the top 10
    smishings_per_phone_number = {}
    for phone_number in phone_numbers:
        smishings_per_phone_number[phone_number] = len([m for m in smishings if m.number == phone_number])
    
    smishings_per_phone_number = dict(sorted(smishings_per_phone_number.items(), key=lambda x: x[1], reverse=True)[:10])

    dashboard_info = {
        "smishing_count": total_smishings,
        "legitimate_count": total_legit,
        "connected_modems": connected_modems,
        "messages_per_phone_number": messages_per_phone_number,
        "smishings_per_phone_number": smishings_per_phone_number,
        "total_messages": total_messages,
        "daily_messages": last_week_messages,
        "monthly_messages": last_months_messages,
        "yearly_messages": last_years_messages,
        "daily_smishings": last_week_smishings,
        "monthly_smishings": last_months_smishings,
        "yearly_smishings": last_years_smishings
    }

    with open(dashboard_path, 'w') as f:
        json.dump(dashboard_info, f, indent=4)

    return dashboard_info
