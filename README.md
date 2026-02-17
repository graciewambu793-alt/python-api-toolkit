# 🐍 Python API Toolkit – Beginner's Guide to Web APIs
> Moringa School Capstone Project | February 2026

## What This Project Does
Fetches 20 todo items from the free [JSONPlaceholder API](https://jsonplaceholder.typicode.com),
processes the JSON response using **pandas**, and saves the result as `todos.csv`.

## Quick Start

```bash
# 1. Clone and enter the project
git clone <your-repo-url>
cd capstone

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # macOS / Linux
# venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the script
python fetch_todos.py
```

## Expected Output
```
======================================================================
  Python API Toolkit – Fetch & Save Todo Data
  Moringa School Capstone | February 2026
======================================================================

📡  Fetching data from: https://jsonplaceholder.typicode.com/todos
    Parameters        : {'_limit': 20}

✅  Success! Received 20 records.

🔧  Processing data with pandas...
    Total tasks   : 20
    Completed     : 11
    Pending       : 9

💾  Data saved to 'todos.csv'

📋  Preview (first 5 rows):
 todo_id  user_id                               task  is_completed    status
       1        1                 delectus aut autem         False Pending ⏳
       ...

🎉  Done! Open 'todos.csv' to see your data.
```

## Project Structure
```
capstone/
├── fetch_todos.py       # Main script
├── requirements.txt     # Dependencies
├── todos.csv            # Output (generated on run)
└── README.md            # This file
```

## Requirements
- Python 3.7+
- Internet connection (to reach the API)
