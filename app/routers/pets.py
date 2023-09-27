from fastapi import APIRouter, Request

from app.models.Pet import Pet

router = APIRouter(prefix="/api/pets", tags=["pets"])


@router.get("/monty", response_model=Pet)
async def get_monty_info(request: Request) -> Pet:
    """Get information about Monty.

    Returns:
        Pet: His illustrious highness
    """
    return Pet(
        name="Montegue (Monty) Fairbanks",
        type="cat",
        age=7,
        notes=["Sovereign of the flying circus"],
        likes=[
            "Playing hide-and-go-treat",
            "Monitoring local wildlife from atop his cat tree (royal throne)",
        ],
        dislikes=[
            "Treat rationing",
            "Getting sniffed by Lilah for more than 10 consecutive seconds",
        ],
        specialties=["cursing", "sleeping"],
        pics=[
            f"{request.base_url}static/img/379986294_982995286328998_5782154564252338453_n.jpg",
            f"{request.base_url}static/img/380632215_1049008186255377_7190735956088332287_n.jpg",
        ],
    )


@router.get("/pups", response_model=list[Pet])
async def get_pups_info(request: Request) -> list[Pet]:
    """Get information about Luna and Lilah.

    Returns:
        list[Pet]: The dynamic duo
    """
    luna = Pet(
        name="Luna",
        type="dog",
        age=4,
        notes=["Dreams of being a professional wrestler"],
        likes=[
            "Sneaking Lilah's leftovers when no one is looking",
            "Pushing the 'go outside' button right after coming back in",
        ],
        dislikes=[
            "Having her sleeping spot stolen by Lilah",
            "Bath time",
        ],
        specialties=["brute force", "cunning"],
        pics=[
            f"{request.base_url}static/img/379896654_296836483048473_3487578070392932379_n.jpg",
            f"{request.base_url}static/img/380523617_657248069834716_8092252126681897164_n.jpg",
        ],
    )

    lilah = Pet(
        name="Lilah",
        type="dog",
        age=4,
        notes=["For instant hype mode, play 'Gourmet Race' from the Kirby ost"],
        likes=[
            "Sniffing Monty for more than 10 consecutive seconds",
            "Holding onto Luna's tail while Luna bolts across the yard",
        ],
        dislikes=[
            "When Luna gets more attention",
            "Car rides",
        ],
        specialties=["speed", "evasion"],
        pics=[
            f"{request.base_url}static/img/379987414_640016554930235_7967718570286921746_n.jpg",
        ],
    )

    return [luna, lilah]
