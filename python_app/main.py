import os
import sys
from datetime import datetime
# Add parent directory to path so python_app can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_app.tracker import ExpenseTracker
from python_app.reports import FinancialReports
from python_app.visualizer import FinancialVisualizer

# Color codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"

def print_header(title):
    print(f"\n{BOLD}{CYAN}{'=' * 50}{RESET}")
    print(f"{BOLD}{MAGENTA}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 50}{RESET}")

def print_success(msg):
    print(f"{GREEN}✔ Success: {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✘ Error: {msg}{RESET}")

def get_input(prompt, val_type=str, default=None, validator=None, error_msg="Invalid input."):
    while True:
        try:
            val_str = input(prompt).strip()
            if not val_str:
                if default is not None:
                    return default
                else:
                    raise ValueError("Input cannot be empty.")
            
            # Type conversions
            if val_type == float:
                val = float(val_str)
            elif val_type == int:
                val = int(val_str)
            else:
                val = val_str

            # Custom validator check
            if validator and not validator(val):
                raise ValueError(error_msg)
                
            return val
        except ValueError as e:
            print_error(str(e) if str(e) else error_msg)

def seed_sample_data(tracker):
    """Pre-populates the tracker with mock data for dynamic visualization."""
    samples = [
        # Income
        ("2026-04-01", "income", "Salary", 4500.0, "Monthly Salary Payment"),
        ("2026-04-15", "income", "Freelance", 850.0, "Website Redesign Client"),
        ("2026-05-01", "income", "Salary", 4500.0, "Monthly Salary Payment"),
        ("2026-05-20", "income", "Freelance", 1200.0, "Mobile App Consultation"),
        ("2026-05-25", "income", "Investment", 150.0, "Quarterly Dividends"),
        ("2026-06-01", "income", "Salary", 4700.0, "Salary with Promotion Bonus"),
        ("2026-06-10", "income", "Freelance", 600.0, "Consulting Hours"),

        # Expenses - April
        ("2026-04-02", "expense", "Rent", 1200.0, "Apartment Rent"),
        ("2026-04-03", "expense", "Utilities", 180.0, "Electricity & Internet"),
        ("2026-04-05", "expense", "Food", 150.0, "Weekly Grocery Shopping"),
        ("2026-04-12", "expense", "Food", 120.0, "Groceries & Snacks"),
        ("2026-04-14", "expense", "Transport", 45.0, "Monthly Transit Pass"),
        ("2026-04-18", "expense", "Entertainment", 80.0, "Concert Ticket"),
        ("2026-04-20", "expense", "Healthcare", 60.0, "Dental Checkup"),
        ("2026-04-25", "expense", "Shopping", 140.0, "Spring Jacket"),

        # Expenses - May
        ("2026-05-02", "expense", "Rent", 1200.0, "Apartment Rent"),
        ("2026-05-03", "expense", "Utilities", 195.0, "Power, Water & Internet"),
        ("2026-05-06", "expense", "Food", 165.0, "Supermarket Groceries"),
        ("2026-05-10", "expense", "Entertainment", 120.0, "Dinner with Friends"),
        ("2026-05-15", "expense", "Education", 250.0, "Python Programming Course Certification"),
        ("2026-05-22", "expense", "Transport", 80.0, "Fuel refill"),
        ("2026-05-28", "expense", "Shopping", 95.0, "Wireless Earbuds"),

        # Expenses - June
        ("2026-06-02", "expense", "Rent", 1200.0, "Apartment Rent"),
        ("2026-06-03", "expense", "Utilities", 175.0, "Monthly Utilities Pack"),
        ("2026-06-04", "expense", "Food", 180.0, "Fresh Groceries"),
        ("2026-06-08", "expense", "Shopping", 350.0, "Desk Ergonomic Chair"),
        ("2026-06-12", "expense", "Entertainment", 50.0, "Movie Ticket & Popcorn"),
        ("2026-06-15", "expense", "Transport", 65.0, "Ride-share and Fuel"),
    ]

    print("\nSeeding mock data for immediate evaluation...")
    for date_str, tx_type, category, amount, description in samples:
        # Check and add categories if custom/missing
        if category not in tracker.get_categories(tx_type):
            tracker.add_category(tx_type, category)
        tracker.add_transaction(date_str, tx_type, category, amount, description)
    print_success("Mock database seeded successfully with 29 historical transactions!")

def display_dashboard_summary(tracker):
    summary = FinancialReports.get_financial_summary(tracker.transactions)
    print(f"\n{BOLD}{YELLOW}📈 FINANCIAL DASHBOARD QUICK VIEW{RESET}")
    print(f"  Total Income:   {BOLD}{GREEN}₹{summary['total_income']:,.2f}{RESET}")
    print(f"  Total Expenses: {BOLD}{RED}₹{summary['total_expense']:,.2f}{RESET}")
    print(f"  Net Savings:    {BOLD}{BLUE if summary['net_balance'] >= 0 else RED}₹{summary['net_balance']:,.2f}{RESET}")
    print(f"  Savings Rate:   {BOLD}{CYAN}{summary['savings_rate']:.1f}%{RESET}")
    print(f"{YELLOW}{'-' * 40}{RESET}")

def main():
    # Force ANSI escape sequences on Windows Command Prompts
    if sys.platform.startswith('win'):
        os.system('color')
        
    tracker = ExpenseTracker()
    visualizer = FinancialVisualizer()

    # ASCII Art Title
    print(f"""{BOLD}{CYAN}
  ██████╗███╗   ███╗ █████╗ ██████╗ ████████╗
 ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
 ╚█████╗ ██╔████╔██║███████║██████╔╝   ██║   
  ╚═══██╗██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
 ██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
 ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
  EXPENSE TRACKER & PERSONAL FINANCE SYSTEM {RESET}""")

    # Check if empty, and offer to seed data
    if not tracker.transactions:
        seed_choice = get_input(
            f"\n{YELLOW}Empty database detected. Would you like to seed 3 months of mock transactions to explore reports/charts immediately? (y/n): {RESET}",
            validator=lambda x: x.lower() in ['y', 'n', 'yes', 'no']
        )
        if seed_choice.lower() in ['y', 'yes']:
            seed_sample_data(tracker)

    while True:
        display_dashboard_summary(tracker)
        print(f"\n{BOLD}MAIN MENU{RESET}")
        print("1. Add Transaction (Income/Expense)")
        print("2. Search & Filter Transactions")
        print("3. Edit Transaction Details")
        print("4. Delete Transaction")
        print("5. Category Management")
        print("6. Financial Reports")
        print("7. Export Data Visualizations (Charts)")
        print("8. Exit Application")
        
        choice = get_input(f"\n{BOLD}Select an option (1-8): {RESET}", val_type=int, validator=lambda x: 1 <= x <= 8)

        if choice == 1:
            print_header("ADD TRANSACTION")
            tx_type = get_input("Transaction Type (income/expense): ", validator=lambda x: x.lower() in ['income', 'expense']).lower()
            
            # Show categories for validation
            cats = tracker.get_categories(tx_type)
            print(f"Available Categories: {', '.join(cats)}")
            
                        category = get_input("Category: ", validator=lambda x: x in cats, error_msg="Invalid category. Use option 5 to add custom ones.")
            amount = get_input("Amount (₹): ", val_type=float, validator=lambda x: x > 0)
            
            today_str = datetime.today().strftime('%Y-%m-%d')
            date_str = get_input(f"Date (YYYY-MM-DD) [Default: {today_str}]: ", default=today_str, 
                                 validator=lambda x: datetime.strptime(x, "%Y-%m-%d") is not None)
            
            description = get_input("Description: ")
            
            try:
                tx = tracker.add_transaction(date_str, tx_type, category, amount, description)
                print_success(f"Added Transaction ID {tx.id} ({tx.category} - ₹{tx.amount:,.2f})")
            except Exception as e:
                print_error(f"Failed to add transaction: {e}")

        elif choice == 2:
            print_header("SEARCH & FILTER TRANSACTIONS")
            print("Press Enter to skip any filter (no filter will be applied).")
            
            tx_type_in = input("Filter by Type (income/expense/skip): ").strip().lower()
            tx_type = tx_type_in if tx_type_in in ['income', 'expense'] else None
            
            cat_in = input("Filter by Category (skip): ").strip()
            category = cat_in if cat_in else None
            
            start_date_in = input("Start Date (YYYY-MM-DD / skip): ").strip()
            start_date = start_date_in if start_date_in else None
            
            end_date_in = input("End Date (YYYY-MM-DD / skip): ").strip()
            end_date = end_date_in if end_date_in else None
            
            min_amt_in = input("Min Amount (₹ / skip): ").strip()
            min_amount = float(min_amt_in) if min_amt_in else None
            
            max_amt_in = input("Max Amount (₹ / skip): ").strip()
            max_amount = float(max_amt_in) if max_amt_in else None
            
            search_query_in = input("Keyword Search in description (skip): ").strip()
            search_query = search_query_in if search_query_in else None
            
            try:
                results = tracker.search_transactions(
                    start_date=start_date, end_date=end_date, category=category,
                    min_amount=min_amount, max_amount=max_amount, tx_type=tx_type,
                    search_query=search_query
                )
                print_header(f"SEARCH RESULTS ({len(results)} matches)")
                print(FinancialReports.get_transactions_table(results))
            except Exception as e:
                print_error(f"Search failed: {e}")

        elif choice == 3:
            print_header("EDIT TRANSACTION")
            tx_id = get_input("Enter Transaction ID to edit: ", val_type=int)
            tx = tracker.get_transaction_by_id(tx_id)
            if not tx:
                print_error("Transaction ID not found.")
                continue
                
            print(f"\nCurrent Transaction details:")
            print(f"ID: {tx.id} | Date: {tx.date} | Type: {tx.type.upper()} | Category: {tx.category} | Amount: ₹{tx.amount:,.2f} | Desc: {tx.description}")
            print("\nEnter new values (Press Enter to keep current value):")
            
            tx_type_in = input(f"Type ({tx.type}): ").strip().lower()
            tx_type = tx_type_in if tx_type_in in ['income', 'expense'] else None
            
            # Show categories based on updated type or current type
            category_type = tx_type if tx_type else tx.type
            cats = tracker.get_categories(category_type)
            print(f"Available Categories for {category_type.upper()}: {', '.join(cats)}")
            
            cat_in = input(f"Category ({tx.category}): ").strip()
            category = cat_in if cat_in else None
            
            amt_in = input(f"Amount (₹{tx.amount}): ").strip()
            amount = float(amt_in) if amt_in else None
            
            date_in = input(f"Date ({tx.date}): ").strip()
            date_str = date_in if date_in else None
            
            desc_in = input(f"Description ({tx.description}): ").strip()
            description = desc_in if desc_in else None
            
            try:
                updated_tx = tracker.edit_transaction(
                    tx_id=tx_id, date_str=date_str, tx_type=tx_type,
                    category=category, amount=amount, description=description
                )
                print_success(f"Updated Transaction ID {updated_tx.id} successfully!")
            except Exception as e:
                print_error(f"Update failed: {e}")

        elif choice == 4:
            print_header("DELETE TRANSACTION")
            tx_id = get_input("Enter Transaction ID to delete: ", val_type=int)
            tx = tracker.get_transaction_by_id(tx_id)
            if not tx:
                print_error("Transaction ID not found.")
                continue
                
            confirm = get_input(f"Are you sure you want to delete ID {tx.id} ({tx.category} - ₹{tx.amount:,.2f})? (y/n): ", 
                                validator=lambda x: x.lower() in ['y', 'n', 'yes', 'no'])
            if confirm.lower() in ['y', 'yes']:
                tracker.delete_transaction(tx_id)
                print_success(f"Deleted Transaction ID {tx_id}")
            else:
                print("Deletion cancelled.")

        elif choice == 5:
            while True:
                print_header("CATEGORY MANAGEMENT")
                print("1. List Income Categories")
                print("2. List Expense Categories")
                print("3. Add Custom Category")
                print("4. Back to Main Menu")
                
                cat_choice = get_input("\nSelect category option (1-4): ", val_type=int, validator=lambda x: 1 <= x <= 4)
                
                if cat_choice == 1:
                    print(f"\n{BOLD}Income Categories:{RESET}")
                    for c in tracker.get_categories("income"):
                        print(f" - {c}")
                elif cat_choice == 2:
                    print(f"\n{BOLD}Expense Categories:{RESET}")
                    for c in tracker.get_categories("expense"):
                        print(f" - {c}")
                elif cat_choice == 3:
                    tx_type = get_input("Add to which type (income/expense): ", validator=lambda x: x.lower() in ['income', 'expense']).lower()
                    cat_name = get_input("Enter new category name: ").strip()
                    try:
                        tracker.add_category(tx_type, cat_name)
                        print_success(f"Added '{cat_name}' to {tx_type} categories.")
                    except Exception as e:
                        print_error(f"Failed to add category: {e}")
                else:
                    break

        elif choice == 6:
            while True:
                print_header("FINANCIAL REPORTS")
                print("1. Full List of Transactions")
                print("2. Monthly Financial Breakdown")
                print("3. Category-Wise Expense Report")
                print("4. Category-Wise Income Report")
                print("5. Back to Main Menu")
                
                rep_choice = get_input("\nSelect report option (1-5): ", val_type=int, validator=lambda x: 1 <= x <= 5)
                
                if rep_choice == 1:
                    print_header("ALL TRANSACTIONS")
                    # Sort default view chronologically descending
                    sorted_tx = sorted(tracker.transactions, key=lambda t: (t.date, t.id), reverse=True)
                    print(FinancialReports.get_transactions_table(sorted_tx))
                elif rep_choice == 2:
                    print_header("MONTHLY breakdown")
                    print(FinancialReports.get_monthly_breakdown(tracker.transactions))
                elif rep_choice == 3:
                    print_header("EXPENSE BY CATEGORY")
                    print(FinancialReports.get_category_breakdown(tracker.transactions, 'expense'))
                elif rep_choice == 4:
                    print_header("INCOME BY CATEGORY")
                    print(FinancialReports.get_category_breakdown(tracker.transactions, 'income'))
                else:
                    break

        elif choice == 7:
            print_header("EXPORT DATA VISUALIZATIONS")
            print("Generating financial charts...")
            
            try:
                # Generate charts
                pie_path = visualizer.generate_expense_pie_chart(tracker.transactions)
                bar_path = visualizer.generate_income_vs_expense_bar_chart(tracker.transactions)
                line_path = visualizer.generate_net_balance_line_chart(tracker.transactions)
                
                if pie_path or bar_path or line_path:
                    print_success(f"Charts generated successfully! Saved in:")
                    print(f"  Pie chart (Expense distribution): [expense_distribution.png](file:///{pie_path.replace(os.sep, '/')})")
                    print(f"  Bar chart (Income vs Expense):   [income_vs_expense.png](file:///{bar_path.replace(os.sep, '/')})")
                    print(f"  Line chart (Net Balance Trend):  [net_balance_trend.png](file:///{line_path.replace(os.sep, '/')})")
                else:
                    print_error("No transactions found to visualize. Add some transactions first.")
            except Exception as e:
                print_error(f"Failed to generate charts: {e}")

        elif choice == 8:
            print(f"\n{BOLD}{GREEN}Thank you for using Smart Expense Tracker System! Good bye.{RESET}\n")
            break

if __name__ == "__main__":
    main()
