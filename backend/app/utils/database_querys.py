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

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_messages_with_timestamp_after(time_to_query):
    if not isinstance(time_to_query, datetime):
        raise ValueError("time_to_query must be a datetime object")
    
    session = Session()
    try:
        # # Log the query parameters
        # logger.info(f"Querying messages with timestamp after: {time_to_query}")
        
        messages = session.query(Message).filter(getattr(Message, 'timestamp') > time_to_query).all()
        
        # # Log the number of messages found
        # logger.info(f"Number of messages found: {len(messages)}")
        # for message in messages:
        #     logger.info(f"Message found: {message.id}")
        return messages
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []
    finally:
        session.close()