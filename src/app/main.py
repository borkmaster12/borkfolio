import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/app/static"), name="static")
templates: Jinja2Templates = Jinja2Templates(directory="src/app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {"page": "Home page"}
    return templates.TemplateResponse(
        name="index.html.j2", context={"request": request, "data": data}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
