import os
import unittest
import tempfile
import shutil
from datetime import datetime

from python_app.tracker import ExpenseTracker, Transaction
from python_app.reports import FinancialReports

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test storage
        self.test_dir = tempfile.mkdtemp()
        self.tracker = ExpenseTracker(data_dir=self.test_dir)

    def tearDown(self):
        # Remove the temporary directory after tests complete
        shutil.rmtree(self.test_dir)

    def test_default_categories(self):
        """Test default categories are set up properly."""
        income_cats = self.tracker.get_categories("income")
        expense_cats = self.tracker.get_categories("expense")
        self.assertIn("Salary", income_cats)
        self.assertIn("Food", expense_cats)

    def test_add_custom_category(self):
        """Test adding custom categories."""
        self.tracker.add_category("expense", "Crypto Gas Fees")
        self.assertIn("Crypto Gas Fees", self.tracker.get_categories("expense"))

        with self.assertRaises(ValueError):
            # Duplicate category should raise an error
            self.tracker.add_category("expense", "Crypto Gas Fees")

    def test_add_transaction_valid(self):
        """Test adding valid transactions."""
        tx = self.tracker.add_transaction(
            date_str="2026-06-15",
            tx_type="income",
            category="Salary",
            amount=5000.00,
            description="Software Engineering monthly salary"
        )
        self.assertEqual(tx.id, 1)
        self.assertEqual(tx.amount, 5000.00)
        self.assertEqual(tx.category, "Salary")
        self.assertEqual(tx.type, "income")

    def test_add_transaction_invalid_amount(self):
        """Test adding transaction with invalid amount raises error."""
        with self.assertRaises(ValueError):
            self.tracker.add_transaction("2026-06-15", "expense", "Food", -10.0, "Negative amount")
            
        with self.assertRaises(ValueError):
            self.tracker.add_transaction("2026-06-15", "expense", "Food", 0.0, "Zero amount")

    def test_add_transaction_invalid_date(self):
        """Test adding transaction with invalid date format raises error."""
        with self.assertRaises(ValueError):
            self.tracker.add_transaction("15-06-2026", "expense", "Food", 20.0, "Wrong date format")

    def test_add_transaction_invalid_category(self):
        """Test adding transaction with a category not in the list raises error."""
        with self.assertRaises(ValueError):
            self.tracker.add_transaction("2026-06-15", "expense", "InvalidCategoryXYZ", 20.0, "Invalid category")

    def test_edit_transaction(self):
        """Test editing an existing transaction."""
        tx = self.tracker.add_transaction("2026-06-15", "expense", "Food", 20.0, "Lunch")
        
        # Edit amount and description
        updated = self.tracker.edit_transaction(tx.id, amount=25.50, description="Fancy Lunch")
        self.assertEqual(updated.amount, 25.50)
        self.assertEqual(updated.description, "Fancy Lunch")

    def test_delete_transaction(self):
        """Test deleting a transaction."""
        tx = self.tracker.add_transaction("2026-06-15", "expense", "Food", 20.0, "Lunch")
        tx_id = tx.id
        
        # Confirm it exists
        self.assertIsNotNone(self.tracker.get_transaction_by_id(tx_id))
        
        # Delete it
        success = self.tracker.delete_transaction(tx_id)
        self.assertTrue(success)
        self.assertIsNone(self.tracker.get_transaction_by_id(tx_id))

    def test_search_and_filters(self):
        """Test searching and filtering transactions."""
        self.tracker.add_transaction("2026-04-10", "income", "Salary", 4000.00, "Base pay")
        self.tracker.add_transaction("2026-04-15", "expense", "Food", 50.00, "Grocery supermarket")
        self.tracker.add_transaction("2026-05-01", "expense", "Rent", 1200.00, "Rent May")
        self.tracker.add_transaction("2026-05-10", "expense", "Food", 15.00, "Burgers fast food")

        # Filter by type
        expenses = self.tracker.search_transactions(tx_type="expense")
        self.assertEqual(len(expenses), 3)

        # Filter by category
        food_items = self.tracker.search_transactions(category="Food")
        self.assertEqual(len(food_items), 2)

        # Filter by date range
        april_items = self.tracker.search_transactions(start_date="2026-04-01", end_date="2026-04-30")
        self.assertEqual(len(april_items), 2)

        # Filter by amount range
        amount_filtered = self.tracker.search_transactions(min_amount=20.0, max_amount=200.0)
        self.assertEqual(len(amount_filtered), 1) # Just the $50 grocery
        self.assertEqual(amount_filtered[0].amount, 50.0)

        # Combined keyword search
        keyword_search = self.tracker.search_transactions(search_query="supermarket")
        self.assertEqual(len(keyword_search), 1)
        self.assertEqual(keyword_search[0].category, "Food")

    def test_financial_reports_math(self):
        """Test report calculations like net balance and savings rate."""
        self.tracker.add_transaction("2026-04-10", "income", "Salary", 5000.00, "Salary")
        self.tracker.add_transaction("2026-04-12", "income", "Freelance", 1000.00, "Freelance")
        self.tracker.add_transaction("2026-04-15", "expense", "Rent", 1500.00, "Rent")
        self.tracker.add_transaction("2026-04-18", "expense", "Food", 500.00, "Food")

        summary = FinancialReports.get_financial_summary(self.tracker.transactions)
        self.assertEqual(summary["total_income"], 6000.00)
        self.assertEqual(summary["total_expense"], 2000.00)
        self.assertEqual(summary["net_balance"], 4000.00)
        self.assertEqual(summary["savings_rate"], (4000.00 / 6000.00) * 100)

if __name__ == '__main__':
    unittest.main()
