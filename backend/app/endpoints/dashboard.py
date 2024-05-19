from datetime import datetime, timedelta
import os
import subprocess
from fastapi import APIRouter
import json
from app.utils.database_querys import get_all_messages, get_messages_by

router = APIRouter()

dashboard_path = os.path.join(os.path.dirname(__file__), "..", "resources", "dashboard_info.json")

@router.get("/dashboard")
async def get_dashboard_info():
    # Get the number of connected working modems counting the lines in the output of the command 'mmcli -L'
    connected_modems = len(subprocess.getoutput('mmcli -L').split('\n'))

    # Get the total number of messages
    all_messages = get_all_messages()
    total_messages = len(all_messages)

    # Get the number of messages per day during the last week
    last_week_messages = {}
    for i in range(7):
        last_week_messages[(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')] = len([m for m in all_messages if m.timestamp.startswith((datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'))])
    
    # Now we reverse the order of the dictionary
    last_week_messages = dict(reversed(last_week_messages.items()))

    # Get the number of messages per month during the last year
    last_months_messages = {}
    current_month = datetime.now().replace(day=1)  # Start from the first day of the current month

    for i in range(12):
        # Calculate the month for the current iteration
        month_str = current_month.strftime('%Y-%m')
        
        # Filter messages for the current month and count them
        messages_count = len([m for m in all_messages if m.timestamp.startswith(month_str)])
        
        # Store the count in the dictionary with the month as key
        last_months_messages[month_str] = messages_count
        
        # Move to the previous month
        current_month -= timedelta(days=current_month.day)

    # now we reverse the order of the dictionary
    last_months_messages = dict(reversed(last_months_messages.items()))

    # Get the number of messages per year during the last 5 years
    last_years_messages = {}
    for i in range(5):
        last_years_messages[str(datetime.now().year - i)] = len([m for m in all_messages if m.timestamp.startswith(str(datetime.now().year - i))])

    # now we reverse the order of the dictionary
    last_years_messages = dict(reversed(last_years_messages.items()))

    # Get the number of messages per phone number
    phone_numbers = list(set([m.number for m in all_messages]))
    messages_per_phone_number = {}
    for phone_number in phone_numbers:
        messages_per_phone_number[phone_number] = len([m for m in all_messages if m.number == phone_number])

    # Now, we get the total number of smishings using get_messages_by(type, smish)
    smishings = get_messages_by('type', 'smish')
    total_smishings = len(smishings)

    # Now, we get the total number of legit messages using get_messages_by(type, legit)
    legit_messages = get_messages_by('type', 'legit')
    total_legit = len(legit_messages)

    # Now we do the same as all the other dictionaries, but only for messages with smishing type
    # We get the smishing messages using get_messages_by(type, smish)
    last_week_smishings = {}
    for i in range(7):
        last_week_smishings[(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')] = len([m for m in smishings if m.timestamp.startswith((datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'))])

    # Now we reverse the order of the dictionary
    last_week_smishings = dict(reversed(last_week_smishings.items()))

    # Get the number of messages per month during the last year
    last_months_smishings = {}
    current_month = datetime.now().replace(day=1)
    for i in range(12):
        month_str = current_month.strftime('%Y-%m')
        messages_count = len([m for m in smishings if m.timestamp.startswith(month_str)])
        last_months_smishings[month_str] = messages_count
        current_month -= timedelta(days=current_month.day)

    # now we reverse the order of the dictionary
    last_months_smishings = dict(reversed(last_months_smishings.items()))

    # Get the number of messages per year during the last 5 years
    last_years_smishings = {}
    for i in range(5):
        last_years_smishings[str(datetime.now().year - i)] = len([m for m in smishings if m.timestamp.startswith(str(datetime.now().year - i))])

    # now we reverse the order of the dictionary
    last_years_smishings = dict(reversed(last_years_smishings.items()))
    
    # Lastly, we count the number of messages per phone number for smishing messages and get the top 10
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