from app.jinja2.templating import get_templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates: Jinja2Templates = get_templates()


@router.get("/", response_class=HTMLResponse, tags=["html"])
async def home(request: Request):
    """Returns the site landing page html."""
    data = {"page": "Borkfolio - Home"}
    return templates.TemplateResponse(
        name="index.html.j2", context={"request": request, "data": data}
    )


@router.get("/about", response_class=HTMLResponse, tags=["html"])
async def about(request: Request):
    """Returns the site about page html."""
    data = {"page": "Borkfolio - About Site"}
    return templates.TemplateResponse(
        name="about.html.j2", context={"request": request, "data": data}
    )


@router.get("/boardgames", response_class=HTMLResponse, tags=["html"])
async def board_games(request: Request):
    """Returns the site board games page html."""
    data = {"page": "Borkfolio - Board Games"}
    return templates.TemplateResponse(
        name="boardgames.html.j2", context={"request": request, "data": data}
    )
