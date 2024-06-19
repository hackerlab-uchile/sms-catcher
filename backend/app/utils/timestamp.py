import os

LAST_SENT_TIMESTAMP_FILE = os.path.join(os.path.dirname(__file__), "..", "resources", "last_sent_timestamp.txt")

def get_last_sent_timestamp():
    if os.path.exists(LAST_SENT_TIMESTAMP_FILE):
        with open(LAST_SENT_TIMESTAMP_FILE, 'r') as f:
            timestamp = f.read().strip()
            if timestamp:
                return timestamp
    return None

def set_last_sent_timestamp(timestamp):
    with open(LAST_SENT_TIMESTAMP_FILE, 'w') as f:
        f.write(timestamp)
