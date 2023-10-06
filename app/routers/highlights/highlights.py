from fastapi import APIRouter, HTTPException, Query
from app.models.highlights import HighlightsDB
from app.scrapers.highlights.highlights import highlights_scraped, insert_data_into_database
from app.database import SessionLocal

router = APIRouter(
    prefix='/highlights',
    tags=['highlights']
)

@router.get("/scrapehighlights")
def scrape_and_save_to_db():
    try:
        scraped_data = highlights_scraped() 
        db = SessionLocal()
        insert_data_into_database(db, scraped_data)

        return {"message": "Highlights scraped and saved successfully!"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/highlights")
def highlights_data(q: str = Query(None)):
    db = SessionLocal()
    if q:
        highlights = db.query(HighlightsDB).filter(HighlightsDB.competition.ilike(f"%{q}%")).all()
    else:
        highlights = db.query(HighlightsDB).all()
    db.close()
    return highlights