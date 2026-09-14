import sys
from pathlib import Path

from core.models import Card
from core.scryfall import ScryfallClient
from core.storage import CollectionStorage


class MainMenu:
    def __init__(self, storage_path: str = "data/collection.json"):
        self.storage = CollectionStorage(storage_path)

    def run(self) -> None:
        while True:
            print("\nMTG Card Tracker")
            print("1. Add Card")
            print("2. Remove Card")
            print("3. View Card Collection")
            print("4. Exit")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_card_prompt()
            elif choice == "2":
                self.remove_card_prompt()
            elif choice == "3":
                self.view_collection()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_card_prompt(self) -> None:
        print("\nAdd Card")
        data = {
            "card_name": input("Card Name: ").strip(),
            "finish": input("Finish (Normal/Foil/Etched Foil): ").strip(),
            "set_edition": input("Set Edition: ").strip(),
            "collection_number": input("Collection Number: ").strip(),
            "card_type": input("Card Type: ").strip(),
            "language": input("Language: ").strip(),
            "condition": input("Condition: ").strip(),
            "price": input("Price: ").strip(),
            "quantity": int(input("Quantity: ").strip()),
        }

        card = Card(**data)
        collection_path = Path(self.storage.file_path)
        image_url = ScryfallClient.lookup_card_image_url(card)
        image_path = ScryfallClient.download_card_image(card, collection_path, image_url)
        if image_path:
            card.image_path = image_path
            card.image_url = image_url

        self.storage.add_card(card)
        print(f"Added card: {card.card_name}")

    def remove_card_prompt(self) -> None:
        name = input("Card Name to remove: ").strip()
        if self.storage.remove_card(name):
            print(f"Removed {name}")
        else:
            print(f"No matching card found: {name}")

    def view_collection(self) -> None:
        cards = self.storage.load_collection()
        if not cards:
            print("The collection is empty.")
            return

        print("\nCard Collection")
        headers = [
            "#", "Card Name", "Finish", "Set Edition", "Collection #",
            "Card Type", "Language", "Condition", "Price", "Quantity", "Image"
        ]
        print(" | ".join(headers))
        print("-" * 140)

        for index, card in enumerate(cards, start=1):
            row = [
                str(index), card.card_name, card.finish, card.set_edition,
                card.collection_number, card.card_type, card.language,
                card.condition, card.price, str(card.quantity),
                card.image_path or "Missing"
            ]
            print(" | ".join(row))


if __name__ == "__main__":
    MainMenu().run()
