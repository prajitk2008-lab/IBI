import pandas as pd
from tabulate import tabulate

class FinancialReports:
    @staticmethod
    def _to_dataframe(transactions):
        """Converts a list of Transaction objects to a pandas DataFrame."""
        if not transactions:
            return pd.DataFrame(columns=["id", "date", "type", "category", "amount", "description"])
        
        data = [t.to_dict() for t in transactions]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        return df

    @classmethod
    def get_financial_summary(cls, transactions):
        """Calculates total income, total expenses, net balance, and savings rate."""
        df = cls._to_dataframe(transactions)
        if df.empty:
            return {
                "total_income": 0.0,
                "total_expense": 0.0,
                "net_balance": 0.0,
                "savings_rate": 0.0
            }

        income_df = df[df['type'] == 'income']
        expense_df = df[df['type'] == 'expense']

        total_income = income_df['amount'].sum()
        total_expense = expense_df['amount'].sum()
        net_balance = total_income - total_expense
        
        savings_rate = 0.0
        if total_income > 0:
            savings_rate = (net_balance / total_income) * 100

        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_balance": float(net_balance),
            "savings_rate": float(savings_rate)
        }

    @classmethod
    def get_monthly_breakdown(cls, transactions):
        """Groups transactions by month and calculates Income vs Expense."""
        df = cls._to_dataframe(transactions)
        if df.empty:
            return "No data available."

        # Add Month column
        df['month'] = df['date'].dt.to_period('M')
        
        # Pivot table to group by month and type
        pivot = df.pivot_table(
            index='month',
            columns='type',
            values='amount',
            aggfunc='sum',
            fill_value=0.0
        )
        
        # Ensure both columns exist
        if 'income' not in pivot.columns:
            pivot['income'] = 0.0
        if 'expense' not in pivot.columns:
            pivot['expense'] = 0.0
            
        pivot['net_savings'] = pivot['income'] - pivot['expense']
        pivot['savings_rate (%)'] = pivot.apply(
            lambda row: (row['net_savings'] / row['income'] * 100) if row['income'] > 0 else 0.0,
            axis=1
        )
        
        # Format for tabular display
        pivot.index = pivot.index.astype(str)
        pivot = pivot.reset_index()
        pivot.columns.name = None
        
                # Rename columns for presentation
        pivot.rename(columns={
            'month': 'Month',
            'income': 'Income (₹)',
            'expense': 'Expense (₹)',
            'net_savings': 'Net Savings (₹)',
            'savings_rate (%)': 'Savings Rate (%)'
        }, inplace=True)
        
        # Format floats
        for col in pivot.columns:
            if col != 'Month':
                pivot[col] = pivot[col].map(lambda x: f"{x:,.2f}")

        return tabulate(pivot, headers='keys', tablefmt='fancy_grid', showindex=False)

    @classmethod
    def get_category_breakdown(cls, transactions, tx_type='expense'):
        """Groups transactions of a specific type by category and sorts by amount descending."""
        df = cls._to_dataframe(transactions)
        if df.empty:
            return "No data available."

        filtered_df = df[df['type'] == tx_type]
        if filtered_df.empty:
            return f"No {tx_type} records found."

        grouped = filtered_df.groupby('category')['amount'].sum().reset_index()
        total_type_amount = grouped['amount'].sum()
        
        grouped['percentage (%)'] = (grouped['amount'] / total_type_amount) * 100
        grouped = grouped.sort_values(by='amount', ascending=False)
        
        grouped.rename(columns={
            'category': 'Category',
            'amount': f'Total Amount (₹)',
            'percentage (%)': 'Percentage (%)'
        }, inplace=True)
        
        # Format floats
        grouped[f'Total Amount (₹)'] = grouped[f'Total Amount (₹)'].map(lambda x: f"{x:,.2f}")
        grouped['Percentage (%)'] = grouped['Percentage (%)'].map(lambda x: f"{x:.1f}%")

        return tabulate(grouped, headers='keys', tablefmt='fancy_grid', showindex=False)

    @classmethod
    def get_transactions_table(cls, transactions):
        """Formats a list of transactions as a clean tabular view."""
        df = cls._to_dataframe(transactions)
        if df.empty:
            return "No transactions to display."
        
        # Prepare for print
        print_df = df.copy()
        print_df['date'] = print_df['date'].dt.strftime('%Y-%m-%d')
        print_df['type'] = print_df['type'].str.upper()
        print_df['amount'] = print_df.apply(
            lambda row: f"+₹{row['amount']:,.2f}" if row['type'] == 'INCOME' else f"-₹{row['amount']:,.2f}",
            axis=1
        )

        
        # Select columns to display
        display_df = print_df[['id', 'date', 'type', 'category', 'amount', 'description']]
        display_df.columns = ['ID', 'Date', 'Type', 'Category', 'Amount', 'Description']
        
        return tabulate(display_df, headers='keys', tablefmt='fancy_grid', showindex=False)
