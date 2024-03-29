import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app.routers.user import user_routes
from app.routers.matches import matches
from app.routers.scrapers_schedulers import scheduler
from app.routers.bets import bet
from app.routers.news import news
from app.routers.players import players
from app.routers.livestream_links import livestream
from app.routers.highlights import highlights
from app.routers.standings import standing
from app.routers.coaches import coaches
from app.routers.media import media
from app.routers.stadiums import stadiums
from app.routers.matchday import matchday
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(user_routes.router, prefix="/api")
app.include_router(players.router)
app.include_router(bet.router)
app.include_router(news.router)
app.include_router(standing.router)
app.include_router(livestream.router)
app.include_router(highlights.router)
app.include_router(matches.router)
app.include_router(coaches.router)
app.include_router(media.router)
app.include_router(stadiums.router)
app.include_router(matchday.router)

@app.on_event("startup")
async def startup():
    scheduler.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
