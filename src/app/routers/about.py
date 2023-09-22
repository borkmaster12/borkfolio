from app.jinja2.templating import get_templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates: Jinja2Templates = get_templates()


@router.get("/about", response_class=HTMLResponse)
async def home(request: Request):
    data = {"page": "Borkfolio - About Site"}
    return templates.TemplateResponse(
        name="about.html", context={"request": request, "data": data}
    )
