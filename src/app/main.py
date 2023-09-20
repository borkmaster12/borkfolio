import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.jinja2.templating import get_templates
from app.routers import index

app = FastAPI()
app.include_router(index.router)

app.mount("/static", StaticFiles(directory="src/app/static"), name="static")
templates: Jinja2Templates = get_templates()


@app.get("/api/test")
async def test():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
