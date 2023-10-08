# from fastapi import APIRouter, HTTPException, Query
# from datetime import datetime
# from app.models.matches import LiveSoccerScores,TomorrowSoccerScores
# from app.scrapers.matches.matches import scrape_and_store_soccer_scores
# from app.database import SessionLocal
# from typing import Optional

# router = APIRouter(
#     prefix='/matches',  # Set the prefix to 'matches'
#     tags=['matches']
# )

# @router.get("/scrape-scores/")
# def scrape_and_save_live_scores(date:  Optional[str] = None):
#     try:
#         scrape_and_store_soccer_scores(date)
#         return {"message": f"Live soccer scores for {date} scraped and saved successfully!"}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @router.get("/scores/")
# def get_scores_by_date(date: Optional[str] = None):
#     if date is not None:
#         # User provided a specific date
#         query_date = date
#     else:
#         # Default to today's date if no date provided
#         query_date = datetime.now().strftime("%Y-%m-%d")

#     db = SessionLocal()

#     # Query both tables for scores on the specified date
#     live_scores = db.query(LiveSoccerScores).filter(LiveSoccerScores.match_date == query_date).all()
#     tomorrow_scores = db.query(TomorrowSoccerScores).filter(TomorrowSoccerScores.match_date == query_date).all()

#     db.close()

#     return {"live_scores": live_scores, "tomorrow_scores": tomorrow_scores}





