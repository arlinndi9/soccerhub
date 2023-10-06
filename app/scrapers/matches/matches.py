import requests
from bs4 import BeautifulSoup
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.models.matches import LiveSoccerScores,TomorrowSoccerScores

Base = declarative_base()

# class LiveSoccerScores(Base):
#     __tablename__ = 'live_soccer_scores'
#
#     id = Column(Integer, primary_key=True)
#     league = Column(String)
#     round = Column(String)
#     home_team = Column(String)
#     home_team_img = Column(String)
#     away_team = Column(String)
#     away_team_img = Column(String)
#     score = Column(String)
#     match_date = Column(DateTime)
#     date_scraped = Column(DateTime)
#
# class TomorrowSoccerScores(Base):
#     __tablename__ = 'tomorrow_soccer_scores'
#
#     id = Column(Integer, primary_key=True)
#     league = Column(String)
#     round = Column(String)
#     home_team = Column(String)
#     home_team_img = Column(String)
#     away_team = Column(String)
#     away_team_img = Column(String)
#     score = Column(String)
#     match_date = Column(DateTime)
#     date_scraped = Column(DateTime)

database_url = 'postgresql://postgres:1234@localhost:5432/soccer'
engine = create_engine(database_url)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def scrape_and_store_soccer_scores(date):
    url = f'https://www.besoccer.com/livescore/{date}'
    try:
        data_get = requests.get(url)
        data_get.raise_for_status()
        soup = BeautifulSoup(data_get.text, 'html.parser')
        panels = soup.find_all('div', class_='panel')
        for panel in panels:
            panel_titles = panel.find_all('div', class_='panel-title')
            panel_body = panel.find_all('div', class_='panel-body p0 match-list-new panel view-more')
            league = ' '
            round = ' '
            for panel_title in panel_titles:
                spans = panel_title.find_all('span', class_='va-m')
                for span in spans:
                    league = span.get_text()
            for body in panel_body:
                info = body.find_all(class_='middle-info ta-c')
                for i in info:
                    round = i.get_text()
                team_elements = body.find_all(class_='name')
                score_elements = body.find_all(class_='marker')
                team_logo = body.find_all('img')
                for home, away, score, logo in zip(team_elements[::2], team_elements[1::2], score_elements, team_logo):
                    home_team = home.get_text().strip()
                    home_team_img = logo.get('src')
                    away_team = away.get_text()
                    away_team_img = logo.get('src')
                    score_text = score.get_text().strip()
                    match_data = {
                        "league": league,
                        "round": round,
                        "home_team": home_team,
                        "home_team_img": home_team_img,
                        "score": score_text,
                        "away_team": away_team,
                        "away_team_img": away_team_img,
                        "match_date": date,
                    }
                    if match_is_live(match_data):
                        save_to_live_scores_table(match_data)
                    elif match_is_tomorrow(match_data):
                        save_to_tomorrow_scores_table(match_data)
        print(f"Soccer scores for {date} scraped and stored successfully.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def match_is_live(match_data):
    current_date = datetime.date.today()
    match_date = datetime.datetime.strptime(match_data["match_date"], "%Y-%m-%d").date()
    return match_date == current_date

def match_is_tomorrow(match_data):
    match_date = datetime.datetime.strptime(match_data["match_date"], "%Y-%m-%d").date()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return match_date == tomorrow

def save_to_live_scores_table(match_data):
    existing_match = session.query(LiveSoccerScores).filter(
        LiveSoccerScores.match_date == match_data["match_date"],
        LiveSoccerScores.home_team == match_data["home_team"],
        LiveSoccerScores.away_team == match_data["away_team"]
    ).first()
    if existing_match:
        # Update the existing match data
        existing_match.league = match_data["league"]
        existing_match.round = match_data["round"]
        existing_match.home_team_img = match_data["home_team_img"]
        existing_match.away_team_img = match_data["away_team_img"]
        existing_match.score = match_data["score"]
        existing_match.date_scraped = datetime.datetime.now()
    else:
        # Insert a new match record
        live_score = LiveSoccerScores(
            league=match_data["league"],
            round=match_data["round"],
            home_team=match_data["home_team"],
            home_team_img=match_data["home_team_img"],
            away_team=match_data["away_team"],
            away_team_img=match_data["away_team_img"],
            score=match_data["score"],
            match_date=match_data["match_date"],
            date_scraped=datetime.datetime.now()
        )
        session.add(live_score)
    session.commit()

def save_to_tomorrow_scores_table(match_data):
    existing_match = session.query(TomorrowSoccerScores).filter(
        TomorrowSoccerScores.match_date == match_data["match_date"],
        TomorrowSoccerScores.home_team == match_data["home_team"],
        TomorrowSoccerScores.away_team == match_data["away_team"]
    ).first()
    if existing_match:
        # Update the existing match data
        existing_match.league = match_data["league"]
        existing_match.round = match_data["round"]
        existing_match.home_team_img = match_data["home_team_img"]
        existing_match.away_team_img = match_data["away_team_img"]
        existing_match.score = match_data["score"]
        existing_match.date_scraped = datetime.datetime.now()
    else:
        # Insert a new match record
        tomorrow_score = TomorrowSoccerScores(
            league=match_data["league"],
            round=match_data["round"],
            home_team=match_data["home_team"],
            home_team_img=match_data["home_team_img"],
            away_team=match_data["away_team"],
            away_team_img=match_data["away_team_img"],
            score=match_data["score"],
            match_date=match_data["match_date"],
            date_scraped=datetime.datetime.now()
        )
        session.add(tomorrow_score)
    session.commit()

if __name__ == "__main__":
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    scrape_and_store_soccer_scores(today.strftime("%Y-%m-%d"))
    scrape_and_store_soccer_scores(tomorrow.strftime("%Y-%m-%d"))
