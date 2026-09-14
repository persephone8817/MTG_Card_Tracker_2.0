import json
from pathlib import Path
from typing import Iterable, List

from core.models import Card


class CollectionStorage:
    """JSON-backed collection storage for the requested CLI foundation."""

    def __init__(self, file_path: str | Path = "data/collection.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def add_card(self, card: Card) -> None:
        cards = self.load_collection()
        cards.append(card)
        self._save(cards)

    def remove_card(self, card_name: str) -> bool:
        cards = self.load_collection()
        original_len = len(cards)
        cards = [card for card in cards if card.card_name.lower() != card_name.lower()]
        if len(cards) == original_len:
            return False
        self._save(cards)
        return True

    def load_collection(self) -> List[Card]:
        if not self.file_path.exists():
            return []
        try:
            data = json.loads(self.file_path.read_text())
        except json.JSONDecodeError:
            return []
        if not isinstance(data, list):
            return []
        return [Card.from_dict(item) for item in data]

    def _save(self, cards: Iterable[Card]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [card.to_dict() for card in cards]
        self.file_path.write_text(json.dumps(payload, indent=2))

    def clear(self) -> None:
        self._save([])
