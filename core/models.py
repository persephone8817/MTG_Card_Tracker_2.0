from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Card:
    card_name: str
    finish: str
    set_edition: str
    collection_number: str
    card_type: str
    language: str
    condition: str
    price: str
    quantity: int
    image_path: Optional[str] = None
    image_url: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Card":
        return cls(**data)
