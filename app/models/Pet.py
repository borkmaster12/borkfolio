from dataclasses import dataclass


@dataclass(slots=True)
class Pet:
    name: str
    type: str
    age: int
    notes: list[str]
    likes: list[str]
    dislikes: list[str]
    specialties: list[str]
    pics: list[str]
