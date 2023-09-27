from dataclasses import dataclass


@dataclass(slots=True)
class BoardGame:
    id: int
    name: str | None
    year: int | None


@dataclass()
class BoardGameId:
    value: int


@dataclass(slots=True)
class BoardGameSuggestion:
    id: int
    name: str | None
    year: int | None
    count: int
