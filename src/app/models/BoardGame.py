from dataclasses import dataclass


@dataclass
class BoardGame:
    id: int
    name: str | None
    year: int | None


@dataclass
class BoardGameId:
    id: int
