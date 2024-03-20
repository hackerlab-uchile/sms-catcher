from fastapi import FastAPI, HTTPException
from subprocess import check_output, CalledProcessError

app = FastAPI()

def execute_mmcli_command(command):
    try:
        output = check_output(command, shell=True).decode("utf-8")
        return output
    except CalledProcessError as e:
        print(f"Error executing command: {e}")
        raise HTTPException(status_code=500, detail="Error executing command")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred")

@app.get("/messages")
async def get_messages():
    try:
        output = execute_mmcli_command("mmcli -L")
        modems = output.splitlines()[1:]  # Exclude the first line
        modems_indexes = [line.split(" ")[0].split("/")[-1] for line in modems]

        modems_messages = {}
        for modem_index in modems_indexes:
            command = f"mmcli -m {modem_index} --messaging-list-sms"
            message_list = execute_mmcli_command(command)
            messages = {}
            for line in message_list.split("\n")[1:]:
                message_index = line.split(" ")[0]
                message_info = execute_mmcli_command(f"mmcli -m {modem_index} --sms {message_index}")
                messages[message_index] = message_info
            modems_messages[modem_index] = messages

        return modems_messages
    except HTTPException:
        raise  # Re-raise HTTPException to return proper HTTP error response

# get_message receives an id of a modem and returns the messages of that modem
@app.get("/messages/{modem_id}")
async def get_message(modem_id: int):
    try:
        output = execute_mmcli_command("mmcli -L")
        modems = output.splitlines()[1:]  # Exclude the first line
        modem_index = None
        for modem in modems:
            if f"Modem{modem_id}" in modem:
                modem_index = modem.split(" ")[0].split("/")[-1]
                break

        if modem_index is None:
            raise HTTPException(status_code=404, detail="Modem not found")

        command = f"mmcli -m {modem_index} --messaging-list-sms"
        message_list = execute_mmcli_command(command)

        messages = {}
        for line in message_list.split("\n")[1:]:
            message_index = line.split(" ")[0]
            message_info = execute_mmcli_command(f"mmcli -m {modem_index} --sms {message_index}")
            messages[message_index] = message_info

        return messages
    except HTTPException:
        raise  # Re-raise HTTPException to return proper HTTP error response

# delete_message receives an id of a modem and a message and deletes that message
@app.delete("/messages/{modem_id}/{message_id}")
async def delete_message(modem_id: int, message_id: int):
    try:
        output = execute_mmcli_command("mmcli -L")
        modems = output.splitlines()[1:]  # Exclude the first line
        modem_index = None
        for modem in modems:
            if f"Modem{modem_id}" in modem:
                modem_index = modem.split(" ")[0].split("/")[-1]
                break

        if modem_index is None:
            raise HTTPException(status_code=404, detail="Modem not found")

        command = f"mmcli -m {modem_index} --delete-sms={message_id}"
        execute_mmcli_command(command)

        return {"message": "Message deleted"}
    except HTTPException:
        raise  # Re-raise HTTPException to return proper HTTP error response
    
