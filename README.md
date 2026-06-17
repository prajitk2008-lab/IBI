# Smart Expense Tracker System

A dual-interface personal finance application featuring both a **Python Console-Based Application** and a **Modern Web-Based Dashboard**. This project helps users manage daily income and expense transactions, organize records by category, filter data dynamically, view monthly/annual financial breakdowns, and export visual charts.

## 📌 Key Features

- **Double Interface**: A fully-featured Python CLI console menu and an interactive glassmorphic web dashboard.
- **Transaction Management**: Add, view, search, edit, and delete Income and Expense transactions.
- **Custom Category Management**: Add custom categories dynamically to suit your financial needs.
- **Advanced Real-Time Filtering**: Search and filter transactions by date ranges, category, type, and amount values.
- **Financial Reports**: Get total balance, income, expense, and savings rate calculations.
- **Dynamic Visualizations**: View expense distribution pie charts, income vs. expense bar charts, and net balance trends.
- **Persistent Local Storage**: JSON-based file storage for the Python app, and `localStorage` integration for the web app.

---

## 🛠️ Tech Stack

### Python CLI App
- **Language**: Python 3.x
- **Data Analysis**: Pandas
- **Table Formatting**: Tabulate
- **Plotting/Visualization**: Matplotlib & Seaborn
- **Storage**: JSON File Persistence

### Web Dashboard
- **Structure & Layout**: HTML5 & Semantic markup
- **Styling**: Vanilla CSS3 (Custom Glassmorphism, animations, responsive design)
- **Logics**: Modern ES6+ JavaScript
- **Interactive Charts**: Chart.js (CDN)
- **Icons**: Lucide Icons (CDN)
- **Storage**: Browser `localStorage`

---

## 📁 Repository Structure

```text
smart-expense-tracker/
│
├── python_app/
│   ├── main.py             # CLI Menu & Main Loop
│   ├── tracker.py          # Core OOP Tracker Logic (validations, filters)
│   ├── storage.py          # JSON File Load/Save handler
│   ├── reports.py          # Tabular calculations (Pandas & Tabulate)
│   ├── visualizer.py       # Chart PNG exports (Matplotlib & Seaborn)
│   ├── test_tracker.py     # Automated Unit Tests
│   └── requirements.txt    # Python library dependencies
│
├── web_app/
│   ├── index.html          # Web Dashboard main layout
│   ├── styles.css          # Glassmorphism Obsidian CSS Theme
│   └── app.js              # State management, filtering, and Chart.js binding
│
├── .gitignore              # Files to exclude from Git
└── README.md               # Project documentation
```

---

## 🚀 How to Run the Applications

### 1. Python CLI Console Application

#### Installation
First, ensure you have Python 3 installed. Navigate to the `python_app` folder and install the required dependencies:
```bash
pip install -r python_app/requirements.txt
```

#### Run CLI App
Execute the main application file:
```bash
python python_app/main.py
```
> **Tip**: On your first launch, select **Yes** to seed the tracker with 3 months of mock data so you can test all features and charts instantly!

---

### 2. Web-Based Dashboard

The Web Dashboard runs completely offline in the browser.

#### Option A: Direct Open
Simply double-click the `web_app/index.html` file to open it in your default web browser.

#### Option B: Serve via Python Web Server
For full functionality and standard serving, run a lightweight server from the `web_app` directory:
```bash
python -m http.server 8000
```
Then visit [http://localhost:8000](http://localhost:8000) in your web browser.

---

## 🧪 Running Automated Tests

To verify the core transaction logic and financial math calculations, run the test suite:
```bash
python -m unittest python_app/test_tracker.py
```
