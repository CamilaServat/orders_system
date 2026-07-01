import json
import shutil
import unittest
from pathlib import Path

from services.order_service import (
    load_data,
    find_order,
    get_allowed_next_statuses,
    update_order_status,
)

DATA_FILE = Path("data/orders.json")
BACKUP_FILE = Path("data/orders_backup.json")


class TestOrderStatus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Faz backup do JSON antes dos testes
        shutil.copy(DATA_FILE, BACKUP_FILE)

    @classmethod
    def tearDownClass(cls):
        # Restaura o JSON original
        shutil.copy(BACKUP_FILE, DATA_FILE)
        BACKUP_FILE.unlink()

    def setUp(self):
        # Antes de cada teste, restaura o JSON original
        shutil.copy(BACKUP_FILE, DATA_FILE)

    def test_find_existing_order(self):
        data = load_data()
        order = find_order(data, 1001)

        self.assertIsNotNone(order)
        self.assertEqual(order["id"], 1001)

    def test_find_non_existing_order(self):
        data = load_data()
        order = find_order(data, 9999)

        self.assertIsNone(order)

    def test_allowed_next_status_pending(self):
        allowed = get_allowed_next_statuses(1003)

        self.assertIn("paid", allowed)
        self.assertIn("cancelled", allowed)

    def test_valid_status_transition(self):
        result = update_order_status(1003, "paid")

        self.assertTrue(result["success"])

        data = load_data()
        order = find_order(data, 1003)

        self.assertEqual(order["status"], "paid")

    def test_invalid_transition(self):
        result = update_order_status(1003, "delivered")

        self.assertFalse(result["success"])

    def test_invalid_status(self):
        result = update_order_status(1003, "abc")

        self.assertFalse(result["success"])

    def test_order_not_found(self):
        result = update_order_status(9999, "paid")

        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()