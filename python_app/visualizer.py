import os
import matplotlib
# Use non-interactive Agg backend to avoid GUI window popup issues
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class FinancialVisualizer:
    def __init__(self, export_dir=None):
        if export_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.export_dir = os.path.join(current_dir, "exports")
        else:
            self.export_dir = export_dir
            
        os.makedirs(self.export_dir, exist_ok=True)
        # Apply seaborn whitegrid theme for a clean look
        sns.set_theme(style="whitegrid")
        plt.rcParams['font.sans-serif'] = 'Arial'
        plt.rcParams['font.family'] = 'sans-serif'

    def _to_dataframe(self, transactions):
        if not transactions:
            return pd.DataFrame()
        data = [t.to_dict() for t in transactions]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        return df

    def generate_expense_pie_chart(self, transactions, filename="expense_distribution.png"):
        """Generates a pie chart of expenses by category."""
        df = self._to_dataframe(transactions)
        if df.empty:
            return None

        expense_df = df[df['type'] == 'expense']
        if expense_df.empty:
            return None

        # Group by category
        grouped = expense_df.groupby('category')['amount'].sum().reset_index()
        
        plt.figure(figsize=(8, 8))
        colors = sns.color_palette("pastel")
        
        plt.pie(
            grouped['amount'], 
            labels=grouped['category'], 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors,
            wedgeprops={'edgecolor': 'w', 'linewidth': 1.5, 'antialiased': True}
        )
        
        plt.title("Expense Distribution by Category", fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        filepath = os.path.join(self.export_dir, filename)
        plt.savefig(filepath, dpi=300)
        plt.close()
        return filepath

    def generate_income_vs_expense_bar_chart(self, transactions, filename="income_vs_expense.png"):
        """Generates a bar chart comparing income and expenses by month."""
        df = self._to_dataframe(transactions)
        if df.empty:
            return None

        df['month'] = df['date'].dt.to_period('M').astype(str)
        grouped = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0.0)
        
        if 'income' not in grouped.columns:
            grouped['income'] = 0.0
        if 'expense' not in grouped.columns:
            grouped['expense'] = 0.0

        # Sort months chronologically
        grouped = grouped.sort_index()

        plt.figure(figsize=(10, 6))
        
        x = range(len(grouped))
        width = 0.35
        
        # Plot bars
        plt.bar([pos - width/2 for pos in x], grouped['income'], width, label='Income', color='#2ecc71')
        plt.bar([pos + width/2 for pos in x], grouped['expense'], width, label='Expense', color='#e74c3c')
        
        plt.xlabel("Month", fontsize=12, fontweight='bold')
        plt.ylabel("Amount (₹)", fontsize=12, fontweight='bold')
        plt.title("Monthly Income vs Expense Comparison", fontsize=16, fontweight='bold', pad=20)
        plt.xticks(x, grouped.index, rotation=45)
        plt.legend(frameon=True, facecolor='white', framealpha=0.9)
        plt.tight_layout()

        filepath = os.path.join(self.export_dir, filename)
        plt.savefig(filepath, dpi=300)
        plt.close()
        return filepath

    def generate_net_balance_line_chart(self, transactions, filename="net_balance_trend.png"):
        """Generates a line chart showing the trend of net balance over time."""
        df = self._to_dataframe(transactions)
        if df.empty:
            return None

        # Sort by date chronologically
        df = df.sort_values('date')
        
        # Calculate running balance
        df['net_value'] = df.apply(lambda r: r['amount'] if r['type'] == 'income' else -r['amount'], axis=1)
        df['cumulative_balance'] = df['net_value'].cumsum()

        plt.figure(figsize=(10, 6))
        
        plt.plot(
            df['date'], 
            df['cumulative_balance'], 
            marker='o', 
            linestyle='-', 
            linewidth=2.5, 
            color='#3498db',
            markersize=6
        )
        
        # Highlight zero line
        plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)

        plt.xlabel("Date", fontsize=12, fontweight='bold')
        plt.ylabel("Net Balance (₹)", fontsize=12, fontweight='bold')
        plt.title("Cumulative Net Balance Trend", fontsize=16, fontweight='bold', pad=20)
        plt.gcf().autofmt_xdate() # Auto rotate dates for better fit
        plt.tight_layout()

        filepath = os.path.join(self.export_dir, filename)
        plt.savefig(filepath, dpi=300)
        plt.close()
        return filepath
