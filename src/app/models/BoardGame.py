from dataclasses import dataclass


@dataclass
class BoardGame:
    id: int
    name: str | None
    year: int | None


@dataclass
class BoardGameId:
    value: int


@dataclass
class BoardGameSuggestion:
    id: int
    name: str | None
    year: int | None
    count: int
