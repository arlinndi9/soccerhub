import datetime
from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LiveSoccerScores(Base):
    __tablename__ = 'live_soccer_scores'

    id = Column(Integer, primary_key=True)
    league = Column(String)
    round = Column(String)
    home_team = Column(String)
    home_team_img = Column(String)
    away_team = Column(String)
    away_team_img = Column(String)
    score = Column(String)
    match_date = Column(DateTime)
    date_scraped = Column(DateTime)

class TomorrowSoccerScores(Base):
    __tablename__ = 'tomorrow_soccer_scores'

    id = Column(Integer, primary_key=True)
    league = Column(String)
    round = Column(String)
    home_team = Column(String)
    home_team_img = Column(String)
    away_team = Column(String)
    away_team_img = Column(String)
    score = Column(String)
    match_date = Column(DateTime)
    date_scraped = Column(DateTime)


