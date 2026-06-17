from datetime import datetime
from python_app.storage import Storage

class Transaction:
    def __init__(self, tx_id, date, tx_type, category, amount, description):
        self.id = tx_id
        self.date = date  # YYYY-MM-DD format string
        self.type = tx_type  # 'income' or 'expense'
        self.category = category
        self.amount = float(amount)
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "type": self.type,
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            tx_id=data["id"],
            date=data["date"],
            tx_type=data["type"],
            category=data["category"],
            amount=data["amount"],
            description=data["description"]
        )

class ExpenseTracker:
    def __init__(self, data_dir=None):
        self.storage = Storage(data_dir)
        self.transactions = []
        self.categories = {}
        self.load_data()

    def load_data(self):
        """Loads data from storage and initializes objects."""
        tx_data = self.storage.load_transactions()
        self.transactions = [Transaction.from_dict(tx) for tx in tx_data]
        self.categories = self.storage.load_categories()

    def save_data(self):
        """Saves current state to storage."""
        self.storage.save_transactions([tx.to_dict() for tx in self.transactions])
        self.storage.save_categories(self.categories)

    def generate_id(self):
        """Generates a simple incremental ID for transactions."""
        if not self.transactions:
            return 1
        return max(tx.id for tx in self.transactions) + 1

    def add_transaction(self, date_str, tx_type, category, amount, description):
        """Adds a transaction and saves data."""
        # Validation
        if tx_type not in ["income", "expense"]:
            raise ValueError("Type must be either 'income' or 'expense'.")
        
        # Verify date format
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")
        
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")
            
        if category not in self.categories.get(tx_type, []):
            raise ValueError(f"Category '{category}' is not valid for {tx_type}. Please add it to your categories list first.")

        tx_id = self.generate_id()
        new_tx = Transaction(tx_id, date_str, tx_type, category, amount, description)
        self.transactions.append(new_tx)
        self.save_data()
        return new_tx

    def edit_transaction(self, tx_id, date_str=None, tx_type=None, category=None, amount=None, description=None):
        """Edits an existing transaction's details."""
        tx = self.get_transaction_by_id(tx_id)
        if not tx:
            raise ValueError(f"Transaction with ID {tx_id} not found.")

        # Temporary copy for validation
        new_type = tx_type if tx_type is not None else tx.type
        new_category = category if category is not None else tx.category
        new_amount = amount if amount is not None else tx.amount
        new_date = date_str if date_str is not None else tx.date

        if new_type not in ["income", "expense"]:
            raise ValueError("Type must be 'income' or 'expense'.")

        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

        if float(new_amount) <= 0:
            raise ValueError("Amount must be a positive number.")

        if new_category not in self.categories.get(new_type, []):
            raise ValueError(f"Category '{new_category}' is not valid for {new_type}. Add the category first.")

        # Update values
        tx.date = new_date
        tx.type = new_type
        tx.category = new_category
        tx.amount = float(new_amount)
        if description is not None:
            tx.description = description

        self.save_data()
        return tx

    def delete_transaction(self, tx_id):
        """Deletes a transaction by ID."""
        tx = self.get_transaction_by_id(tx_id)
        if not tx:
            raise ValueError(f"Transaction with ID {tx_id} not found.")
        self.transactions.remove(tx)
        self.save_data()
        return True

    def get_transaction_by_id(self, tx_id):
        """Helper to find transaction by ID."""
        for tx in self.transactions:
            if tx.id == int(tx_id):
                return tx
        return None

    def add_category(self, tx_type, category_name):
        """Adds a custom category for income or expense."""
        if tx_type not in ["income", "expense"]:
            raise ValueError("Type must be 'income' or 'expense'.")
        
        category_name = category_name.strip()
        if not category_name:
            raise ValueError("Category name cannot be empty.")
            
        if category_name in self.categories[tx_type]:
            raise ValueError(f"Category '{category_name}' already exists for {tx_type}.")
            
        self.categories[tx_type].append(category_name)
        self.save_data()
        return True

    def get_categories(self, tx_type=None):
        """Gets all categories or categories for a specific type."""
        if tx_type:
            if tx_type not in ["income", "expense"]:
                raise ValueError("Type must be 'income' or 'expense'.")
            return self.categories.get(tx_type, [])
        return self.categories

    def search_transactions(self, start_date=None, end_date=None, category=None, min_amount=None, max_amount=None, tx_type=None, search_query=None):
        """Filters transactions based on multiple criteria."""
        filtered = self.transactions
        
        if tx_type:
            filtered = [t for t in filtered if t.type == tx_type]
            
        if category:
            filtered = [t for t in filtered if t.category.lower() == category.lower()]
            
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            filtered = [t for t in filtered if datetime.strptime(t.date, "%Y-%m-%d") >= start_dt]
            
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            filtered = [t for t in filtered if datetime.strptime(t.date, "%Y-%m-%d") <= end_dt]
            
        if min_amount is not None:
            filtered = [t for t in filtered if t.amount >= float(min_amount)]
            
        if max_amount is not None:
            filtered = [t for t in filtered if t.amount <= float(max_amount)]
            
        if search_query:
            q = search_query.lower()
            filtered = [t for t in filtered if q in t.description.lower() or q in t.category.lower()]
            
        # Sort by date descending, then ID descending
        filtered.sort(key=lambda t: (t.date, t.id), reverse=True)
        return filtered
