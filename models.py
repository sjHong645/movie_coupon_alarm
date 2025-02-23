from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint
from database import Base 

class lottecinema_event_list(Base) : 

    __tablename__ = "lottecinema_event_list"

    __table_args = {
        PrimaryKeyConstraint('movie_title', 'start_timestamp')
    }

    movie_title = Column(String(80))
    start_timestamp = Column(DateTime)
    update_timestamp = Column(DateTime)
    