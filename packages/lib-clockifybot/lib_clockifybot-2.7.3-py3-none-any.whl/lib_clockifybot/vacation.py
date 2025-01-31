import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base

from .database import create_database_if_not_exists
from .log import add_log

load_dotenv(os.getenv("CLOCKIFY_ENV"))

VACATION_URL = os.getenv("DATABASE_URL_VACATION")
engine = create_engine(VACATION_URL)
BaseVacation = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Vacation(BaseVacation):
    __tablename__ = "vacation"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String)
    username = Column(String)
    coolname = Column(String)
    clockify_id = Column(String)
    workday = Column(String)
    hours = Column(String)
    status = Column(String)
    is_vacation = Column(Boolean, default=False)
    request_id = Column(Numeric)

    def __repr__(self):
        return f"User('{self.username}') - RoutineVacation('{self.workday}'))"


def init_vacation_db(bot):
    create_database_if_not_exists(VACATION_URL, bot)
    try:
        BaseVacation.metadata.create_all(engine)
    except Exception as e:
        add_log(f"Error creating Vacation table: {e}")
