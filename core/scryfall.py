import json
import re
from pathlib import Path
from typing import Optional
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


class ScryfallClient:
    """Minimal Scryfall image lookup client using only the Python standard library."""

    BASE_URL = "https://api.scryfall.com"

    @staticmethod
    def clean_name(name: str) -> str:
        return re.sub(r"[^A-Za-z0-9]+", "_", name.strip()).strip("_")

    @staticmethod
    def lookup_card_image_url(card) -> Optional[str]:
        """Try an exact-name endpoint with an edition filter, then fall back to search."""
        # Try exact card search by name + set. Scryfall accepts set codes and releases.
        encoded_name = quote(card.card_name)
        encoded_set = quote(card.set_edition)
        named_url = f"{ScryfallClient.BASE_URL}/cards/named?exact={encoded_name}&set={encoded_set}"
        try:
            payload = ScryfallClient._json_request(named_url)
            image_uris = payload.get("image_uris") or {}
            if "normal" in image_uris:
                return image_uris["normal"]
        except Exception:
            pass

        query = f'name:"{card.card_name}" set:{card.set_edition}'
        search_url = f"{ScryfallClient.BASE_URL}/cards/search?{urlencode({'q': query})}"
        try:
            payload = ScryfallClient._json_request(search_url)
            if payload.get("data"):
                for item in payload["data"]:
                    image_uris = item.get("image_uris") or {}
                    if "normal" in image_uris:
                        return image_uris["normal"]
                    if "small" in image_uris:
                        return image_uris["small"]
        except Exception:
            pass

        return None

    @staticmethod
    def download_card_image(card, collection_path: Path, image_url: Optional[str] = None) -> Optional[str]:
        """Download the image URL returned by Scryfall into the collection directory."""
        image_url = image_url or ScryfallClient.lookup_card_image_url(card)
        if not image_url:
            return None

        image_dir = collection_path.parent / "images"
        image_dir.mkdir(parents=True, exist_ok=True)

        safe_name = ScryfallClient.clean_name(card.card_name)
        safe_set = ScryfallClient.clean_name(card.set_edition)
        safe_number = re.sub(r"[^A-Za-z0-9]+", "_", str(card.collection_number)).strip("_")
        image_path = image_dir / f"{safe_name}_{safe_set}_{safe_number}.jpg"

        try:
            req = Request(image_url, headers={"User-Agent": "MTGCardTracker/1.0", "Accept": "application/json"})
            with urlopen(req, timeout=20) as response:
                data = response.read()
            image_path.write_bytes(data)
            return str(image_path)
        except Exception:
            return None

    @staticmethod
    def _json_request(url: str) -> dict:
        req = Request(url, headers={"User-Agent": "MTGCardTracker/1.0", "Accept": "application/json"})
        with urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
