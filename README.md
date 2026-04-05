# 💰 Personal Finance Tracker
### Cross-Platform Desktop Application — Python · Flet · SQLite

> Built across 8 progressive lab sessions | B.Sc. IT, Don State Technical University | 2026

---

## Overview

A fully functional personal finance management application built with Python and the 
[Flet](https://flet.dev) framework — deployable as a desktop, mobile, or web app 
from a single Python codebase.

The app allows users to track income and expenses, manage category budgets, view 
spending reports, and navigate between modules using a sidebar navigation rail.

---

## Features

- 📊 **Income & Expense Tracking** — log and categorise transactions
- 💼 **Budget Management** — set and monitor category budgets
- 📈 **Spending Reports** — visualise spending patterns
- 🔍 **Search & Filtering** — live SQL-style partial matching across records
- 💾 **Persistent Storage** — SQLite database, data survives restart
- 🧩 **Modular Architecture** — clean separation of views, models, and repository layer

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | [Flet](https://flet.dev) (Flutter-based Python UI) |
| Language | Python 3.x |
| Database | SQLite (via Python sqlite3) |
| Architecture | Repository pattern, modular MVC-style |
| Platform | Desktop / Mobile / Web (single codebase) |

---

## Project Structure
finance-tracker/
├── main.py                 # App entry point
├── models/
│   ├── transaction.py      # Transaction data model
│   └── category.py         # Category/budget model
├── repository/
│   └── db_repository.py    # SQLite CRUD operations
├── views/
│   ├── transactions_view.py
│   ├── budget_view.py
│   ├── reports_view.py
│   └── search_view.py
├── components/
│   └── nav_rail.py         # Sidebar navigation
├── finance.db              # SQLite database (auto-created)
└── README.md
---

## Development Progress

| Lab | Feature | Status |
|---|---|---|
| Lab 1 | Environment setup & Flet entry point | ✅ Complete |
| Lab 2 | UI components & layout | ✅ Complete |
| Lab 3 | Modular architecture | ✅ Complete |
| Lab 4 | Multi-view NavigationRail routing | ✅ Complete |
| Lab 5 | Data models & state management | ✅ Complete |
| Lab 6 | CRUD operations & forms | ✅ Complete |
| Lab 7 | Search & filtering | ✅ Complete |
| Lab 8 | SQLite persistence | ✅ Complete |

---

## Installation & Running
```bash
# Clone the repo
git clone https://github.com/UmarMaishanu/finance-tracker.git
cd finance-tracker

# Install dependencies
pip install flet

# Run the app
python main.py
```

---

## Author

**Umar Hamza Maishanu**  
B.Sc. Information Technology, DSTU Russia  
[LinkedIn](https://www.linkedin.com/mwlite/profile/in/umar-hamza-maishanu-8721a6222?trk=contact-info) · [GitHub](https://github.com/UmarMaishanu)
