import tempfile
import unittest

from core.models import Card
from core.storage import CollectionStorage


class CollectionStorageRoundTripTest(unittest.TestCase):
    def test_collection_storage_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            collection_path = f"{tmp}/collection.json"
            storage = CollectionStorage(collection_path)

            card = Card(
                card_name="Lightning Bolt",
                finish="Foil",
                set_edition="M20",
                collection_number="123",
                card_type="Instant",
                language="English",
                condition="Near Mint",
                price="0.50",
                quantity=2,
            )

            storage.add_card(card)
            loaded = storage.load_collection()

            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0].card_name, "Lightning Bolt")
            self.assertEqual(loaded[0].finish, "Foil")
            self.assertEqual(loaded[0].language, "English")
            self.assertEqual(loaded[0].quantity, 2)


if __name__ == "__main__":
    unittest.main()
