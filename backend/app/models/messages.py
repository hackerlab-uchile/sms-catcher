from app.config.database import Base
from sqlalchemy import Column, Integer, String, DateTime

# a message must have: 
# - id: represented by a string of the timestamp concatenated with the hash of the phone number+message
# - path: represented by a string
# - number: represented by a string
# - text: represented by a string
# - pdu_type: represented by a string
# - state: represented by a string
# - storage: represented by a string
# - smsc: represented by a string
# - class: represented by an integer
# - timestamp: represented by a timestamp string

class Message(Base):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True)
    type = Column(Integer)
    path = Column(String)
    number = Column(String)
    text = Column(String)
    pdu_type = Column(String)
    state = Column(String)
    storage = Column(String)
    smsc = Column(String)
    timestamp = Column(DateTime)
