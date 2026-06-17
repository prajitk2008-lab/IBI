import os
import json

DEFAULT_CATEGORIES = {
    "income": ["Salary", "Freelance", "Investment", "Gift", "Other"],
    "expense": ["Food", "Rent", "Utilities", "Transport", "Entertainment", "Healthcare", "Shopping", "Education", "Other"]
}

class Storage:
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Set default data directory relative to the current module file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_dir = os.path.join(current_dir, "data")
        else:
            self.data_dir = data_dir
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.transactions_path = os.path.join(self.data_dir, "transactions.json")
        self.categories_path = os.path.join(self.data_dir, "categories.json")
        
        self._init_files()

    def _init_files(self):
        """Initialize files if they do not exist."""
        if not os.path.exists(self.categories_path):
            self.save_categories(DEFAULT_CATEGORIES)
            
        if not os.path.exists(self.transactions_path):
            self.save_transactions([])

    def load_categories(self):
        """Load categories from JSON."""
        try:
            with open(self.categories_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return DEFAULT_CATEGORIES

    def save_categories(self, categories):
        """Save categories to JSON."""
        with open(self.categories_path, 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=4)

    def load_transactions(self):
        """Load transactions from JSON."""
        try:
            with open(self.transactions_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_transactions(self, transactions):
        """Save transactions to JSON."""
        with open(self.transactions_path, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, indent=4)
