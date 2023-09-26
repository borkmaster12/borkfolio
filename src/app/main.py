import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import clear_suggestions, refresh_collection
from app.jinja2.templating import get_templates
from app.routers import board_games, html

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.include_router(html.router)
app.include_router(board_games.router)


app.mount("/static", StaticFiles(directory="src/app/static"), name="static")
templates: Jinja2Templates = get_templates()


@app.on_event("startup")
async def app_startup():
    await clear_suggestions()
    await refresh_collection()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
