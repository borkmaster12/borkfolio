from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import get_db, refresh_collection
from app.routers import boardgames, html, pets
from app.templating import get_templates

app = FastAPI(title="Borkfolio")
app.include_router(html.router)
app.include_router(boardgames.router)
app.include_router(pets.router)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates: Jinja2Templates = get_templates()


@app.on_event("startup")
async def app_startup():
    await refresh_collection(db=get_db())
