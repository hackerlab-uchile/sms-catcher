from dotenv import load_dotenv
import subprocess

load_dotenv()

# Using sudo su in a script, but only use if absolutely necessary
command = "sudo su"
subprocess.run(command, shell=True)

def execute_mmcli_command(command):
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        return output
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
        return output.split("\n")[1:]
    return None

def extract_message_info(modem_index, message_index):
    command = f"mmcli -m {modem_index} --sms {message_index}"
    return execute_mmcli_command(command)

try:
    # Use subprocess.check_output for running commands and handle exceptions
    output = subprocess.check_output("mmcli -L", shell=True).decode("utf-8")
    # We want to extract the modem paths from the output and store them in a list
    modems = output.splitlines()[1:]  # Exclude the first line

    # The modems list should look like this:
    # ['/org/freedesktop/ModemManager1/Modem/0,
    # '/org/freedesktop/ModemManager1/Modem/1,
    # '/org/freedesktop/ModemManager1/Modem/2]
    modems_paths = [line.split(" ")[0] for line in modems]

    # Extract the modem indexes from the paths and store them in a list
    modems_indexes = [modem.split("/")[-1] for modem in modems_paths]

    # Extract the modem information for each modem and store it in a dictionary with the modem index as the key
    modems_info = {}
    for modem_index in modems_indexes:
        output = subprocess.check_output(f"mmcli -m {modem_index}", shell=True).decode("utf-8")
        modems_info[modem_index] = output
    

except subprocess.CalledProcessError as e:
    # Handle subprocess errors gracefully
    print(f"Error executing command: {e}")

except Exception as e:
    # Handle other exceptions gracefully
    print(f"An error occurred: {e}")
