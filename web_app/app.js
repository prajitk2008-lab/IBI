// ==========================================================================
// SMART EXPENSE TRACKER - JAVASCRIPT APPLICATION CODE
// Coordinates stats calculations, transaction lists, categories, and Chart.js
// ==========================================================================

// Global State
let transactions = [];
let categories = {
    income: ["Salary", "Freelance", "Investment", "Gift", "Other"],
    expense: ["Food", "Rent", "Utilities", "Transport", "Entertainment", "Healthcare", "Shopping", "Education", "Other"]
};

// Chart.js Instances
let balanceTrendChart = null;
let incomeVsExpenseChart = null;
let expenseDistributionChart = null;

// DOM Elements
const bodyDisplayDate = document.getElementById('current-date-display');
const totalBalanceDisplay = document.getElementById('total-balance-display');
const totalIncomeDisplay = document.getElementById('total-income-display');
const totalExpensesDisplay = document.getElementById('total-expenses-display');
const savingsRateDisplay = document.getElementById('savings-rate-display');
const savingsProgressFill = document.getElementById('savings-rate-progress');

// Table Bodys
const recentTransactionsTbody = document.getElementById('recent-transactions-tbody');
const allTransactionsTbody = document.getElementById('all-transactions-tbody');
const emptyTransactionsState = document.getElementById('empty-transactions-state');
const filteredCountDisplay = document.getElementById('filtered-count-display');

// Filter Form Controls
const filterSearch = document.getElementById('filter-search');
const filterCategory = document.getElementById('filter-category');
const filterStartDate = document.getElementById('filter-start-date');
const filterEndDate = document.getElementById('filter-end-date');
const filterMinAmount = document.getElementById('filter-min-amount');
const filterMaxAmount = document.getElementById('filter-max-amount');
const sortTransactions = document.getElementById('sort-transactions');
const resetFiltersBtn = document.getElementById('reset-filters-btn');

// Transaction Form & Modal Controls
const transactionModal = document.getElementById('transaction-modal');
const transactionForm = document.getElementById('transaction-form');
const txIdInput = document.getElementById('tx-id-input');
const txAmountInput = document.getElementById('tx-amount');
const txDateInput = document.getElementById('tx-date');
const txCategorySelect = document.getElementById('tx-category');
const txDescriptionInput = document.getElementById('tx-description');
const modalTitle = document.getElementById('modal-title');
const saveModalBtn = document.getElementById('save-modal-btn');

const openAddModalBtn = document.getElementById('open-add-modal-btn');
const closeModalBtn = document.getElementById('close-modal-btn');
const cancelModalBtn = document.getElementById('cancel-modal-btn');

// Categories Controls
const addCategoryForm = document.getElementById('add-category-form');
const catNameInput = document.getElementById('cat-name');
const expenseCategoriesList = document.getElementById('expense-categories-list');
const incomeCategoriesList = document.getElementById('income-categories-list');

// Application Lifecycle Init
document.addEventListener('DOMContentLoaded', () => {
    // Show Today's Date
    const today = new Date();
    bodyDisplayDate.textContent = today.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
    
    // Load Data
    loadFromLocalStorage();
    
    // Seed data if database is empty
    if (transactions.length === 0) {
        seedMockData();
    }
    
    // Bind Event Listeners
    setupEventListeners();
    
    // Initialize Dashboard UI & Render Charts
    refreshAppUI();
    
    // Initialize Lucide Icons
    lucide.createIcons();
});

// Event Listeners Registration
function setupEventListeners() {
    // Navigation Tabs Toggle
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Check if export button
            if (item.id === 'export-data-btn') {
                exportDataAsJSON();
                return;
            }
            
            // Update active menu link
            document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
            item.classList.add('active');
            
            // Show target section
            const targetSectionId = item.getAttribute('data-target');
            document.querySelectorAll('.tab-content').forEach(sec => sec.classList.remove('active'));
            document.getElementById(targetSectionId).classList.add('active');
            
            // Special triggers on view change
            if (targetSectionId === 'transactions-section') {
                populateCategoryFilterOptions();
                applyFilters();
            } else if (targetSectionId === 'categories-section') {
                renderCategoriesLists();
            } else if (targetSectionId === 'dashboard-section') {
                refreshAppUI();
            }
        });
    });

    // Shortcut: View All link on Dashboard
    document.getElementById('view-all-transactions-link').addEventListener('click', () => {
        document.querySelector('[data-target="transactions-section"]').click();
    });

    // Modal Events
    openAddModalBtn.addEventListener('click', () => openTransactionModal());
    closeModalBtn.addEventListener('click', () => closeTransactionModal());
    cancelModalBtn.addEventListener('click', () => closeTransactionModal());
    
    // Type toggles inside modal (updates categories select dropdown)
    document.getElementsByName('tx-type').forEach(radio => {
        radio.addEventListener('change', (e) => {
            updateModalRadioClasses();
            populateModalCategorySelect(e.target.value);
        });
    });

    // Handle transaction submit (Add or Edit)
    transactionForm.addEventListener('submit', handleTransactionFormSubmit);

    // Filters event listeners (real-time filtering)
    [filterSearch, filterCategory, filterStartDate, filterEndDate, filterMinAmount, filterMaxAmount, sortTransactions]
        .forEach(el => el.addEventListener('input', applyFilters));
    
    document.getElementsByName('filter-type').forEach(radio => {
        radio.addEventListener('change', (e) => {
            document.querySelectorAll('input[name="filter-type"]').forEach(input => {
                input.closest('.radio-label').classList.remove('active');
            });
            e.target.closest('.radio-label').classList.add('active');
            applyFilters();
        });
    });

    resetFiltersBtn.addEventListener('click', () => {
        filterSearch.value = '';
        filterCategory.value = 'all';
        filterStartDate.value = '';
        filterEndDate.value = '';
        filterMinAmount.value = '';
        filterMaxAmount.value = '';
        sortTransactions.value = 'date-desc';
        
        document.getElementsByName('filter-type').forEach(radio => {
            radio.checked = radio.value === 'all';
            if (radio.value === 'all') radio.closest('.radio-label').classList.add('active');
            else radio.closest('.radio-label').classList.remove('active');
        });
        
        applyFilters();
        showToast('Filters cleared', 'success');
    });

    // Category Creation Event
    addCategoryForm.addEventListener('submit', handleCategoryFormSubmit);
    
    // Type toggles in Category Form
    document.getElementsByName('cat-type').forEach(radio => {
        radio.addEventListener('change', () => {
            document.querySelectorAll('input[name="cat-type"]').forEach(input => {
                input.closest('.radio-label').classList.remove('active');
            });
            radio.closest('.radio-label').classList.add('active');
        });
    });
}

// Local Storage Management
function saveToLocalStorage() {
    localStorage.setItem('set_transactions', JSON.stringify(transactions));
    localStorage.setItem('set_categories', JSON.stringify(categories));
}

function loadFromLocalStorage() {
    const txData = localStorage.getItem('set_transactions');
    const catData = localStorage.getItem('set_categories');
    
    if (txData) transactions = JSON.parse(txData);
    if (catData) categories = JSON.parse(catData);
}

// Seed Initial Mock Data
function seedMockData() {
    const today = new Date();
    
    // Create dates relative to current date
    const formatDate = (daysAgo) => {
        const d = new Date(today);
        d.setDate(today.getDate() - daysAgo);
        return d.toISOString().split('T')[0];
    };

    const mockTransactions = [
        // Current Month (Income & Expenses)
        { id: 1, date: formatDate(0), type: "expense", category: "Food", amount: 15.40, description: "Lunch sandwich and coffee" },
        { id: 2, date: formatDate(1), type: "expense", category: "Transport", amount: 4.50, description: "Metro ticket" },
        { id: 3, date: formatDate(2), type: "expense", category: "Shopping", amount: 120.00, description: "Mechanical Keyboard" },
        { id: 4, date: formatDate(3), type: "income", category: "Salary", amount: 4500.00, description: "Monthly base salary payout" },
        { id: 5, date: formatDate(5), type: "expense", category: "Rent", amount: 1200.00, description: "Appartment rent charge" },
        { id: 6, date: formatDate(6), type: "expense", category: "Utilities", amount: 165.20, description: "Electric bill & Gas" },
        { id: 7, date: formatDate(8), type: "expense", category: "Entertainment", amount: 48.00, description: "Dinner out with colleagues" },
        { id: 8, date: formatDate(10), type: "income", category: "Freelance", amount: 800.00, description: "Landing page design client" },
        { id: 9, date: formatDate(12), type: "expense", category: "Food", amount: 85.30, description: "Weekly grocery supermarket refill" },
        { id: 10, date: formatDate(14), type: "expense", category: "Healthcare", amount: 35.00, description: "Pharmacy prescription medication" },

        // Previous Month (Income & Expenses)
        { id: 11, date: formatDate(30), type: "income", category: "Salary", amount: 4500.00, description: "Salary Payment May" },
        { id: 12, date: formatDate(32), type: "expense", category: "Rent", amount: 1200.00, description: "Apartment Rent May" },
        { id: 13, date: formatDate(34), type: "expense", category: "Utilities", amount: 175.40, description: "Utilities bundle (May)" },
        { id: 14, date: formatDate(35), type: "expense", category: "Food", amount: 95.00, description: "Groceries supply" },
        { id: 15, date: formatDate(40), type: "income", category: "Freelance", amount: 1150.00, description: "Consulting freelance contract" },
        { id: 16, date: formatDate(42), type: "expense", category: "Shopping", amount: 65.00, description: "New summer shirt" },
        { id: 17, date: formatDate(45), type: "expense", category: "Entertainment", amount: 90.00, description: "Standup comedy show tickets" },
        { id: 18, date: formatDate(50), type: "expense", category: "Education", amount: 120.00, description: "Online Javascript Masterclass" },
        
        // Two Months Ago
        { id: 19, date: formatDate(60), type: "income", category: "Salary", amount: 4500.00, description: "Salary Payment April" },
        { id: 20, date: formatDate(62), type: "expense", category: "Rent", amount: 1200.00, description: "Apartment Rent April" },
        { id: 21, date: formatDate(65), type: "expense", category: "Food", amount: 110.20, description: "Groceries & Kitchen supplies" },
        { id: 22, date: formatDate(68), type: "expense", category: "Transport", amount: 45.00, description: "Monthly train ticket pass" },
        { id: 23, date: formatDate(72), type: "income", category: "Gift", amount: 150.00, description: "Birthday cash gift" },
        { id: 24, date: formatDate(75), type: "expense", category: "Healthcare", amount: 70.00, description: "Doctor consultation" }
    ];

    transactions = mockTransactions;
    saveToLocalStorage();
}

// Refresh KPI values & Recent Transactions List
function refreshAppUI() {
    calculateAndRenderKPIs();
    renderRecentTransactionsList();
    renderCharts();
}

// KPI Dashboard Calculations
function calculateAndRenderKPIs() {
    let totalIncome = 0;
    let totalExpenses = 0;
    
    transactions.forEach(t => {
        if (t.type === 'income') totalIncome += t.amount;
        else totalExpenses += t.amount;
    });
    
    const balance = totalIncome - totalExpenses;
    
    // Render Values
    totalBalanceDisplay.textContent = formatCurrency(balance);
    totalIncomeDisplay.textContent = formatCurrency(totalIncome);
    totalExpensesDisplay.textContent = formatCurrency(totalExpenses);
    
    // Balance delta indicator
    const deltaDisplay = document.getElementById('balance-delta-display');
    if (balance >= 0) {
        deltaDisplay.className = "kpi-delta positive";
        deltaDisplay.innerHTML = `<i data-lucide="trending-up"></i> Net Surplus`;
    } else {
        deltaDisplay.className = "kpi-delta negative";
        deltaDisplay.innerHTML = `<i data-lucide="trending-down"></i> Net Deficit`;
    }

    // Dynamic Income & Expense comparison delta (percentage)
    const incomeDelta = document.getElementById('income-delta-display');
    const expenseDelta = document.getElementById('expense-delta-display');
    
    // Simple mock comparison
    const transactionCount = transactions.length;
    incomeDelta.textContent = `Based on ${transactions.filter(t => t.type==='income').length} source entries`;
    expenseDelta.textContent = `Based on ${transactions.filter(t => t.type==='expense').length} spending logs`;

    // Savings Rate Calculation
    let savingsRate = 0;
    if (totalIncome > 0) {
        savingsRate = Math.round((balance / totalIncome) * 100);
    }
    
    // Prevent negative display for rate progress bar, but allow negative text
    savingsRateDisplay.textContent = `${savingsRate}%`;
    const clampedRate = Math.max(0, Math.min(100, savingsRate));
    savingsProgressFill.style.width = `${clampedRate}%`;
    
    // Re-create lucide icons in delta indicators
    lucide.createIcons();
}

// Render the 5 most recent transactions
function renderRecentTransactionsList() {
    // Sort transactions chronologically descending
    const sorted = [...transactions].sort((a, b) => new Date(b.date) - new Date(a.date) || b.id - a.id);
    const recents = sorted.slice(0, 5);
    
    recentTransactionsTbody.innerHTML = '';
    
    if (recents.length === 0) {
        recentTransactionsTbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center" style="color: var(--text-muted); padding: 40px 0;">
                    No transactions registered yet. Click "Add Transaction" to begin!
                </td>
            </tr>
        `;
        return;
    }

    recents.forEach(t => {
        const row = createTransactionRowHTML(t);
        recentTransactionsTbody.appendChild(row);
    });
    
    // Re-initialize lucide icons inside rows
    lucide.createIcons();
}

// Create Row HTML Node for Tables
function createTransactionRowHTML(t) {
    const tr = document.createElement('tr');
    
    const formattedDate = formatDateString(t.date);
    const typeBadgeClass = t.type === 'income' ? 'income' : 'expense';
    const amountPrefix = t.type === 'income' ? '+' : '-';
    const amountColorClass = t.type === 'income' ? 'positive' : 'negative';
    
    tr.innerHTML = `
        <td>${formattedDate}</td>
        <td><span style="font-weight: 500;">${t.category}</span></td>
        <td><span style="color: var(--text-secondary);">${t.description}</span></td>
        <td><span class="badge-type ${typeBadgeClass}">${t.type}</span></td>
        <td class="text-right ${amountColorClass}" style="font-weight: 600;">
            ${amountPrefix}${formatCurrency(t.amount)}
        </td>
        <td>
            <div class="action-buttons">
                <button class="btn-icon edit-btn" onclick="editTransaction(${t.id})" title="Edit">
                    <i data-lucide="edit-3"></i>
                </button>
                <button class="btn-icon delete-btn" onclick="deleteTransaction(${t.id})" title="Delete">
                    <i data-lucide="trash-2"></i>
                </button>
            </div>
        </td>
    `;
    return tr;
}

// Chart.js Generation
function renderCharts() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') return;

    // Destroy existing charts to reload
    if (balanceTrendChart) balanceTrendChart.destroy();
    if (incomeVsExpenseChart) incomeVsExpenseChart.destroy();
    if (expenseDistributionChart) expenseDistributionChart.destroy();

    if (transactions.length === 0) return;

    // --- CHART 1: Balance Trend (Line/Area) ---
    const sortedChronological = [...transactions].sort((a, b) => new Date(a.date) - new Date(b.date));
    
    let cumulative = 0;
    const trendData = sortedChronological.map(t => {
        cumulative += t.type === 'income' ? t.amount : -t.amount;
        return { x: t.date, y: cumulative };
    });

    const ctx1 = document.getElementById('balanceTrendChart').getContext('2d');
    balanceTrendChart = new Chart(ctx1, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Net Balance ($)',
                data: trendData,
                borderColor: '#3498db',
                borderWidth: 3,
                backgroundColor: 'rgba(52, 152, 219, 0.08)',
                fill: true,
                tension: 0.35,
                pointBackgroundColor: '#3498db',
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    type: 'category',
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { color: '#8E9BAE', font: { size: 10 } }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { color: '#8E9BAE', font: { size: 10 } }
                }
            }
        }
    });

    // --- CHART 2: Income vs Expense comparison (Bar) ---
    // Group totals by Month (YYYY-MM)
    const monthlyGroups = {};
    transactions.forEach(t => {
        const month = t.date.substring(0, 7); // Get 'YYYY-MM'
        if (!monthlyGroups[month]) {
            monthlyGroups[month] = { income: 0, expense: 0 };
        }
        monthlyGroups[month][t.type] += t.amount;
    });

    const sortedMonths = Object.keys(monthlyGroups).sort();
    const incomes = sortedMonths.map(m => monthlyGroups[m].income);
    const expenses = sortedMonths.map(m => monthlyGroups[m].expense);

    const ctx2 = document.getElementById('incomeVsExpenseChart').getContext('2d');
    incomeVsExpenseChart = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: sortedMonths,
            datasets: [
                {
                    label: 'Income',
                    data: incomes,
                    backgroundColor: '#2ecc71',
                    borderRadius: 4
                },
                {
                    label: 'Expenses',
                    data: expenses,
                    backgroundColor: '#e74c3c',
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#8E9BAE', font: { size: 11 } } }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#8E9BAE' }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { color: '#8E9BAE' }
                }
            }
        }
    });

    // --- CHART 3: Expense Categories (Doughnut) ---
    const expenseData = transactions.filter(t => t.type === 'expense');
    const categoryTotals = {};
    expenseData.forEach(t => {
        categoryTotals[t.category] = (categoryTotals[t.category] || 0) + t.amount;
    });

    const expenseCategories = Object.keys(categoryTotals);
    const expenseShares = expenseCategories.map(c => categoryTotals[c]);
    
    // Gorgeous palette
    const colors = [
        '#FF6B6B', '#4D96FF', '#6BCB77', '#FFD93D', 
        '#9B59B6', '#E67E22', '#1ABC9C', '#34495E', '#F1C40F'
    ];

    const ctx3 = document.getElementById('expenseDistributionChart').getContext('2d');
    expenseDistributionChart = new Chart(ctx3, {
        type: 'doughnut',
        data: {
            labels: expenseCategories,
            datasets: [{
                data: expenseShares,
                backgroundColor: colors.slice(0, expenseCategories.length),
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#8E9BAE', boxWidth: 12, font: { size: 10 } }
                }
            },
            cutout: '65%'
        }
    });
}

// Transaction Modal Controls
function openTransactionModal(txId = null) {
    // Setup initial fields
    if (txId) {
        // Edit Mode
        const tx = transactions.find(t => t.id === parseInt(txId));
        if (!tx) return;
        
        modalTitle.textContent = "Edit Transaction";
        txIdInput.value = tx.id;
        txAmountInput.value = tx.amount.toFixed(2);
        txDateInput.value = tx.date;
        txDescriptionInput.value = tx.description;
        
        // Select matching radio type
        document.getElementById('tx-type-expense').checked = tx.type === 'expense';
        document.getElementById('tx-type-income').checked = tx.type === 'income';
        
        updateModalRadioClasses();
        
        // Load correct categories list
        populateModalCategorySelect(tx.type);
        txCategorySelect.value = tx.category;
        
        saveModalBtn.textContent = "Save Changes";
    } else {
        // Create Mode
        modalTitle.textContent = "Add Transaction";
        txIdInput.value = '';
        txAmountInput.value = '';
        txDateInput.value = new Date().toISOString().split('T')[0];
        txDescriptionInput.value = '';
        
        document.getElementById('tx-type-expense').checked = true;
        updateModalRadioClasses();
        
        populateModalCategorySelect('expense');
        saveModalBtn.textContent = "Save Transaction";
    }
    
    transactionModal.classList.add('active');
}

function closeTransactionModal() {
    transactionModal.classList.remove('active');
    transactionForm.reset();
}

function updateModalRadioClasses() {
    const isExpense = document.getElementById('tx-type-expense').checked;
    
    document.getElementById('modal-label-expense').classList.toggle('active', isExpense);
    document.getElementById('modal-label-income').classList.toggle('active', !isExpense);
}

function populateModalCategorySelect(type) {
    txCategorySelect.innerHTML = '';
    const cats = categories[type];
    
    cats.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        txCategorySelect.appendChild(opt);
    });
}

// Transaction Form Submission
function handleTransactionFormSubmit(e) {
    e.preventDefault();
    
    const id = txIdInput.value;
    const type = document.querySelector('input[name="tx-type"]:checked').value;
    const amount = parseFloat(txAmountInput.value);
    const date = txDateInput.value;
    const category = txCategorySelect.value;
    const description = txDescriptionInput.value.trim();
    
    // Validations
    if (isNaN(amount) || amount <= 0) {
        showToast('Please enter a positive numeric amount', 'error');
        return;
    }
    if (!date) {
        showToast('Please select a transaction date', 'error');
        return;
    }
    if (!description) {
        showToast('Description cannot be empty', 'error');
        return;
    }

    if (id) {
        // Edit operation
        const index = transactions.findIndex(t => t.id === parseInt(id));
        if (index !== -1) {
            transactions[index] = { id: parseInt(id), date, type, category, amount, description };
            showToast('Transaction updated successfully', 'success');
        }
    } else {
        // Create operation
        const nextId = transactions.length > 0 ? Math.max(...transactions.map(t => t.id)) + 1 : 1;
        const newTx = { id: nextId, date, type, category, amount, description };
        transactions.push(newTx);
        showToast('Transaction added successfully', 'success');
    }
    
    saveToLocalStorage();
    closeTransactionModal();
    refreshAppUI();
}

// Exposed Functions for global onclick handles
window.editTransaction = function(id) {
    openTransactionModal(id);
};

window.deleteTransaction = function(id) {
    if (confirm('Are you sure you want to delete this transaction record?')) {
        transactions = transactions.filter(t => t.id !== parseInt(id));
        saveToLocalStorage();
        refreshAppUI();
        applyFilters(); // Updates large list if open
        showToast('Transaction deleted', 'success');
    }
};

// Filter Page List Controls
function populateCategoryFilterOptions() {
    // Keeps current category selection
    const prevVal = filterCategory.value;
    filterCategory.innerHTML = '<option value="all">All Categories</option>';
    
    // Add all unique categories from state
    const allCats = [...categories.income, ...categories.expense];
    const uniqueCats = [...new Set(allCats)];
    
    uniqueCats.sort().forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        filterCategory.appendChild(opt);
    });
    
    filterCategory.value = prevVal;
    if (filterCategory.value === '') filterCategory.value = 'all';
}

function applyFilters() {
    const q = filterSearch.value.toLowerCase();
    const type = document.querySelector('input[name="filter-type"]:checked').value;
    const cat = filterCategory.value;
    const start = filterStartDate.value;
    const end = filterEndDate.value;
    const minAmt = parseFloat(filterMinAmount.value);
    const maxAmt = parseFloat(filterMaxAmount.value);
    const sort = sortTransactions.value;
    
    let filtered = [...transactions];
    
    // Apply type filter
    if (type !== 'all') {
        filtered = filtered.filter(t => t.type === type);
    }
    
    // Apply category filter
    if (cat !== 'all') {
        filtered = filtered.filter(t => t.category === cat);
    }
    
    // Apply text search
    if (q) {
        filtered = filtered.filter(t => 
            t.description.toLowerCase().includes(q) || 
            t.category.toLowerCase().includes(q)
        );
    }
    
    // Apply date range
    if (start) {
        filtered = filtered.filter(t => t.date >= start);
    }
    if (end) {
        filtered = filtered.filter(t => t.date <= end);
    }
    
    // Apply amount limits
    if (!isNaN(minAmt)) {
        filtered = filtered.filter(t => t.amount >= minAmt);
    }
    if (!isNaN(maxAmt)) {
        filtered = filtered.filter(t => t.amount <= maxAmt);
    }
    
    // Apply sorting
    filtered.sort((a, b) => {
        if (sort === 'date-desc') return new Date(b.date) - new Date(a.date) || b.id - a.id;
        if (sort === 'date-asc') return new Date(a.date) - new Date(b.date) || a.id - b.id;
        if (sort === 'amount-desc') return b.amount - a.amount;
        if (sort === 'amount-asc') return a.amount - b.amount;
        return 0;
    });
    
    // Render Results
    filteredCountDisplay.textContent = filtered.length;
    allTransactionsTbody.innerHTML = '';
    
    if (filtered.length === 0) {
        emptyTransactionsState.style.display = 'block';
    } else {
        emptyTransactionsState.style.display = 'none';
        filtered.forEach(t => {
            const row = createTransactionRowHTML(t);
            allTransactionsTbody.appendChild(row);
        });
    }
    
    lucide.createIcons();
}

// Category lists operations
function renderCategoriesLists() {
    expenseCategoriesList.innerHTML = '';
    incomeCategoriesList.innerHTML = '';
    
    categories.expense.forEach(c => {
        const li = createCategoryBadgeHTML('expense', c);
        expenseCategoriesList.appendChild(li);
    });

    categories.income.forEach(c => {
        const li = createCategoryBadgeHTML('income', c);
        incomeCategoriesList.appendChild(li);
    });
}

function createCategoryBadgeHTML(type, name) {
    const li = document.createElement('li');
    li.innerHTML = `
        <span>${name}</span>
        <button class="delete-cat-btn" onclick="deleteCategory('${type}', '${name}')" title="Delete Category">&times;</button>
    `;
    return li;
}

function handleCategoryFormSubmit(e) {
    e.preventDefault();
    const type = document.querySelector('input[name="cat-type"]:checked').value;
    const name = catNameInput.value.trim();
    
    if (!name) return;
    
    // Duplicate Check
    if (categories[type].map(c => c.toLowerCase()).includes(name.toLowerCase())) {
        showToast(`Category "${name}" already exists for ${type}s`, 'error');
        return;
    }
    
    categories[type].push(name);
    saveToLocalStorage();
    catNameInput.value = '';
    
    renderCategoriesLists();
    showToast('Category created successfully', 'success');
}

window.deleteCategory = function(type, name) {
    // Check if category is currently used in transactions
    const isUsed = transactions.some(t => t.type === type && t.category === name);
    
    if (isUsed) {
        showToast(`Cannot delete category. It is currently associated with transactions.`, 'error');
        return;
    }
    
    if (confirm(`Are you sure you want to remove the category "${name}"?`)) {
        categories[type] = categories[type].filter(c => c !== name);
        saveToLocalStorage();
        renderCategoriesLists();
        showToast('Category removed', 'success');
    }
};

// JSON Data Exporter
function exportDataAsJSON() {
    const exportPayload = {
        meta: {
            app: "Smart Expense Tracker System",
            exportDate: new Date().toISOString(),
            recordCount: transactions.length
        },
        categories: categories,
        transactions: transactions
    };

    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportPayload, null, 4));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `expense_tracker_export_${new Date().toISOString().split('T')[0]}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    
    showToast('Data exported successfully', 'success');
}

// Utility Helper Functions
function formatCurrency(num) {
    return '₹' + parseFloat(num).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatDateString(dateStr) {
    // Date formats: YYYY-MM-DD
    const parts = dateStr.split('-');
    if (parts.length !== 3) return dateStr;
    
    const date = new Date(parts[0], parts[1] - 1, parts[2]);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? 'check-circle' : 'alert-circle';
    toast.innerHTML = `
        <i data-lucide="${icon}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    lucide.createIcons();
    
    // Auto Remove Toast
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}
