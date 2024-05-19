import subprocess
import re

def extract_first_non_space_substring(s):
    match = re.search(r'\S+', s)
    if match:
        return match.group()
    return None

def execute_mmcli_command(command):
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        return output.strip()  # Strip any leading/trailing whitespace
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_message_list(modem_index):
    command = f"mmcli -m {modem_index} --messaging-list-sms"
    output = execute_mmcli_command(command)
    if output:
        # print("Message list output:", output)
        return [re.search(r'/(\d+)', line).group(1) for line in output.split("\n")[:] if line.strip()]
    return None

def extract_last_message(modem_index):
    command = f"mmcli -m {modem_index} --messaging-list-sms"
    output = execute_mmcli_command(command)
    if output:
        # print("Last message output:", output)
        return re.search(r'/(\d+)', output.split("\n")[-1]).group(1)
    return None
    

def extract_message_info(modem_index, message_index):
    command = f"mmcli -m {modem_index} --sms {message_index}"
    output = execute_mmcli_command(command)
    if output:
        # print("Message info output:", output)
        return output
    return None