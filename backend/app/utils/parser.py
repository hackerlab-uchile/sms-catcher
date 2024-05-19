import re

def parse_message_info(message_info):
    key_values = ["path", "number", "text", "pdu type", "state", "storage", "smsc", "class", "timestamp"]
    # First, get rid of all the lines with "-----------------------"
    lines = message_info.split('\n')
    lines = [line for line in lines if not re.match(r'^\s*[-]+\s*$', line)]
    # Then, let's get rid of all the text before the first | and the | itself
    lines = [re.sub(r'^.*\|', '', line) for line in lines]
    # Now, let's split the lines by the first colon
    parsed_info = {}
    last_key = None
    for line in lines:
        key_value = line.split(':', 1)
        if len(key_value) == 2:
            key = key_value[0].strip()
            value = key_value[1].strip()
            if key in key_values:
                parsed_info[key] = value
                last_key = key
            elif last_key:
                parsed_info[last_key] += " " + line.strip()
        else:
            print("Error: Unable to parse line:", line)
    return parsed_info
