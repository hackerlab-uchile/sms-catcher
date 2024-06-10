# File to run the update of the database
# and the sending of the messages to the api

# First, we send a post request to the update_modem_info endpoint
# to update the database with the new information

# Then, we send a post request to the send_message endpoint
# to send the messages to the external API

import requests

# Update the database
response = requests.post("http://localhost:8000/update_modem_info")
print(response.text)

# Send the messages to the external API
response = requests.post("http://localhost:8000/send_message")
print(response.text)