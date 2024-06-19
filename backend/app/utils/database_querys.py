from datetime import datetime
from app.models.messages import Message
from app.config.database import Session

def get_all_messages():
    session = Session()
    messages = session.query(Message).all()
    session.close()
    return messages

def get_messages_by(key, value):
    session = Session()
    messages = session.query(Message).filter(getattr(Message, key) == value).all()
    session.close()
    return messages

def get_messages_with_timestamp_after(time_to_query):
    if not isinstance(time_to_query, datetime):
        raise ValueError("time_to_query must be a datetime object")
    
    session = Session()
    try:
        messages = session.query(Message).filter(getattr(Message, 'timestamp') > time_to_query).all()
        return messages
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        session.close()