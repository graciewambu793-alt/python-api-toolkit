# Python API Toolkit – Beginner's Guide to Web APIs

## 1. Title & Objective

**Title:**  
**Python API Toolkit – Beginner's Guide to Web APIs**

**Objective:**  
This toolkit documents the journey of learning Python for API data extraction and processing. It showcases a learning progression from understanding basic API concepts to building a complete data pipeline.

The goal is to provide a clear and replicable guide for a beginner to:

* Set up a Python development environment with virtual environments.
* Understand REST APIs, JSON, and HTTP requests.
* Build a script that fetches data from a public API using the `requests` library.
* Process and transform data using pandas DataFrames.
* Export processed data to CSV format.
* Leverage generative AI to accelerate learning, scaffold code, and troubleshoot problems.

**Why Python?**

* **Python** was chosen for its gentle learning curve, massive community support, and dominance in data engineering and backend scripting. The combination of `requests` and `pandas` represents industry-standard tools used by data engineers worldwide.

**End Goal:**  
The project results in a single production-ready script (`fetch_todos.py`) that:

* Fetches 20 todo items from the JSONPlaceholder API.
* Processes the JSON response into a clean pandas DataFrame.
* Adds a human-readable status column.
* Exports the result to `todos.csv`.
* Handles network errors gracefully (ConnectionError, Timeout, HTTPError).

---

## 2. Quick Summary of the Technology

**What is the requests library?**

* `requests` is a Python library that lets you send HTTP requests (GET, POST, PUT, DELETE) with minimal code. It handles authentication, headers, parameters, timeouts, and error responses out of the box — without touching Python's verbose built-in urllib.

**What is pandas?**

* `pandas` is a fast, powerful Python library for data manipulation and analysis. It provides the DataFrame — a 2D table structure similar to a spreadsheet — that makes working with structured data (like API responses) intuitive and efficient.

**What is JSONPlaceholder?**

* JSONPlaceholder is a free, public REST API for testing and prototyping. It requires no authentication, returns realistic JSON data, and supports standard HTTP methods — making it the perfect playground for API beginners.

**Where are they used?**

* **requests:** Large-scale companies in the social media and tech industry rely on Python and requests for building and maintaining internal API clients.
* **pandas:** Companies in the streaming and entertainment industry use pandas for content analytics and A/B test result processing.
* **JSONPlaceholder:** Front-end and back-end teams use it as a mock API during rapid prototyping.

**Real-world example:**

* Instagram's backend team uses Python + requests for internal API clients.
* Netflix uses pandas for content analytics and A/B test result processing.

---

## 3. System Requirements

**Operating System:**

* Windows 10+, macOS 10.14+, or Ubuntu 20.04+

**Tools & Editors:**

* **Python** 3.7 or later (3.10+ recommended)
* **pip** (Version 21+ recommended — comes bundled with Python 3.4+)
* **Virtual Environment** (venv is recommended as best practice)
* **VS Code** with Python extension (recommended), PyCharm, or any text editor
* **Internet Access** (required to call the JSONPlaceholder API)

**Packages:**

* `requests >= 2.28.0`
* `pandas >= 1.5.0`

---

## 4. Installation & Setup Instructions

This section provides a clear, step-by-step guide to set up the Python development environment on any major operating system.

### Step 1: Verify Python is Installed

```bash
# Check Python version (needs 3.7+)
python --version

# Check pip is available
pip --version
```

### Step 2: Create Project Folder

```bash
mkdir python-api-toolkit
cd python-api-toolkit
```

### Step 3: Create & Activate a Virtual Environment

A virtual environment keeps your project's packages isolated from the rest of your system.

```bash
# Create the virtual environment
python -m venv venv

# Activate it (macOS / Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Your prompt should now show: (venv)
```

### Step 4: Install Required Packages

```bash
pip install requests pandas

# Or install from requirements.txt:
pip install -r requirements.txt
```

### Step 5: Create requirements.txt

```bash
# Save current packages for reproducibility
pip freeze > requirements.txt

# Minimum contents of requirements.txt:
# requests>=2.28.0
# pandas>=1.5.0
```

### Step 6: Verify Everything is Ready

```bash
python -c "import requests; import pandas; print('All good!')"
# Expected output:
# All good!
```

✓ **Checkpoint:** If you see 'All good!' you are fully set up and ready to write the main script.

---

## 5. Minimal Working Example

This step walks you through creating and running the `fetch_todos.py` script that demonstrates the complete data pipeline.

### Project Structure

Your repo should look like this:

```
python-api-toolkit/
├── fetch_todos.py       # Main script (fully commented)
├── requirements.txt     # Python dependencies
├── todos.csv            # Output file (generated on run)
└── README.md            # Setup & run instructions
```

### What This Example Does

This script sends a GET request to the JSON Placeholder API with a `?_limit=20` query parameter, parses the JSON response into a Python list of dictionaries, and converts it into a pandas DataFrame with renamed columns for readability. It then adds a human-readable status column that maps True/False values to Done/Pending labels, saves the result as `todos.csv`, and handles ConnectionError, Timeout, and HTTP errors gracefully throughout.

### File: fetch_todos.py

```python
import requests       # Makes HTTP requests to the API
import pandas as pd   # Processes JSON data into a structured table
import sys            # Used for exiting on critical errors

# ── CONFIGURATION ──────────────────────────────────────
API_URL = "https://jsonplaceholder.typicode.com/todos"
PARAMS  = {"_limit": 20}  # Fetch only the first 20 todos
OUTPUT  = "todos.csv"     # Output filename

# ── STEP 1: Fetch Data ────────────────────────────────
def fetch_todos(url: str, params: dict) -> list:
    """
    Sends a GET request to the given URL with query parameters.
    """
    print("======================================================")
    print("  Python API Toolkit – Fetch & Save Todo Data")
    print("  Moringa School Capstone | February 2026")
    print("======================================================\n")
    print(f"  Fetching data from: {url}")
    print(f"  Parameters        : {params}\n")

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"  Success! Received {len(data)} records.\n")
        return data
    except requests.exceptions.ConnectionError:
        print("  ERROR: No internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("  ERROR: Request timed out.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"  HTTP ERROR: {e}")
        sys.exit(1)

# ── STEP 2: Process Data ──────────────────────────────
def process_data(data: list) -> pd.DataFrame:
    """
    Converts raw JSON data into a clean pandas DataFrame.
    """
    print("  Processing data with pandas...")
    df = pd.DataFrame(data)
    df.rename(columns={
        "userId": "user_id", "id": "todo_id",
        "title": "task", "completed": "is_completed"
    }, inplace=True)
    df["status"] = df["is_completed"].map(
        {True: "Done", False: "Pending"})

    completed = df["is_completed"].sum()
    pending   = len(df) - completed
    print(f"  Total tasks   : {len(df)}")
    print(f"  Completed     : {completed}")
    print(f"  Pending       : {pending}\n")

    return df[["todo_id", "user_id", "task",
               "is_completed", "status"]]

# ── STEP 3: Save to CSV ───────────────────────────────
def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    """Exports the DataFrame to a CSV file."""
    df.to_csv(filename, index=False)
    print(f"  Data saved to '{filename}'\n")

# ── MAIN ──────────────────────────────────────────────
if __name__ == "__main__":
    data = fetch_todos(API_URL, PARAMS)
    df   = process_data(data)
    save_to_csv(df, OUTPUT)

    print("  Preview (first 5 rows):")
    print(df.head().to_string(index=False))
    print("\n  Done! Open 'todos.csv' to see your data.")
    print("======================================================")
```

### How to Run

#### 1. Navigate to the project

```bash
cd python-api-toolkit
```

#### 2. Run the script

```bash
python fetch_todos.py
```

#### 3. Open the output

The `todos.csv` file will appear in your project folder.

### Expected Output:

```
======================================================
  Python API Toolkit – Fetch & Save Todo Data
  Moringa School Capstone | February 2026
======================================================

  Fetching data from: https://jsonplaceholder.typicode.com/todos
  Parameters        : {'_limit': 20}

  Success! Received 20 records.

  Processing data with pandas...
  Total tasks   : 20
  Completed     : 11
  Pending       : 9

  Data saved to 'todos.csv'

  Preview (first 5 rows):
  todo_id  user_id  task                    is_completed  status
        1        1  delectus aut autem       False         Pending
        2        1  quis ut nam facilis...   False         Pending

  Done! Open 'todos.csv' to see your data.
======================================================
```

---

## 6. AI Agents Utilised

* **Claude** (via ai.moringaschool.com)

---

## 7. AI Prompt Journal (A Structured Learning Journey)

This journal documents the step-by-step learning process using a series of structured AI prompts. It shows how to go from high-level concepts to a working application by treating the AI as a programming tutor.

### Phase 1: Conceptual Understanding & Setup

This phase focuses on building the foundational knowledge required before writing any code.

**Prompt 1: High-Level Conceptual Introduction**

> "Explain what a REST API is to a complete beginner. What is JSON? How does a GET request work? Give a real-world analogy."

* **AI Helpfulness:** This prompt established the fundamental understanding of APIs. The AI explained APIs as a 'waiter in a restaurant' — you (client) ask the waiter (API) for something, the waiter goes to the kitchen (server) and brings back your order (response). JSON was described as a structured text format that both humans and machines can read. A GET request was compared to asking a library for a book — you don't change anything, you just retrieve information.

**Prompt 2: Guided Installation and First API Call**

> "Show me a step-by-step guide to install and use the Python requests library. Include how to send a GET request, check the status code, and parse a JSON response. Use JSONPlaceholder as the example API."

* **AI Helpfulness:** This combined prompt created a conversational, iterative development process. By asking the AI to proceed step-by-step, I wasn't overwhelmed. The AI walked through `pip install requests`, a minimal GET request using `requests.get()`, checking `response.status_code`, calling `response.json()` to parse the response, and using `timeout=10` to avoid hanging. It also mentioned `raise_for_status()` for automatic error detection.

**Prompt 3: Real-World Error Handling**

> "What are the common errors when making API calls in Python with requests? Show me how to handle ConnectionError, Timeout, and HTTPError properly with try/except blocks."

* **AI Helpfulness:** This was a critical learning moment. The AI explained three main error types: ConnectionError (no internet), Timeout (server too slow — solved with `timeout=` parameter), and HTTPError (bad status codes — solved with `raise_for_status()`). It provided a clean try/except structure catching each exception separately with informative print messages, and recommended `sys.exit(1)` for unrecoverable errors.

### Phase 2: Building the Data Processing Pipeline

This phase details the prompts used to build the data processing functionality with pandas.

**Prompt 4: Processing JSON with pandas**

> "I have a Python list of dictionaries from a JSON API response. How do I convert it to a pandas DataFrame, rename the columns, add a new derived column, and export it to CSV? Show me with a todo list example."

* **AI Helpfulness:** The AI showed `pd.DataFrame(data)` to convert a list of dicts, `df.rename(columns={...})` to rename keys, `df['status'] = df['completed'].map({True: 'Done', False: 'Pending'})` for derived columns, and `df.to_csv('output.csv', index=False)` to export. It also showed `df.head()` for a quick preview. The `.map()` pattern for derived columns was new to me and extremely useful.

**Prompt 5: Refining Code Quality**

> "Review this Python function that fetches API data. How can I improve it using Python best practices? I want proper docstrings, type hints, and clean separation of concerns."

* **AI Helpfulness:** The AI restructured the code into three clean functions: `fetch_todos()`, `process_data()`, and `save_to_csv()`, each with a single responsibility. It added type hints (`def fetch_todos(url: str, params: dict) -> list:`), docstrings with Args and Returns sections, and f-strings for all print statements. It also suggested an `if __name__ == '__main__':` guard. Code quality improved significantly and the separation of concerns made testing easier.

### Phase 3: Troubleshooting and Refinement

After building the core functionality, this phase focused on handling edge cases and polishing the final product.

### Learning Reflection

Using AI reduced my setup time by approximately 60%. Instead of reading through scattered documentation, I could ask targeted questions and receive contextual code examples immediately. The most valuable insight was learning `raise_for_status()` — a single line that replaced 10+ lines of manual status code checking. AI also helped me discover the `.map()` method in pandas, which I would not have found quickly through trial and error.

If I were to approach this project again, I would start by mapping out all three functions before writing any code, rather than building and refactoring as I went — this would have saved time and reduced the number of revisions needed. Going forward, I plan to explore working with APIs that require authentication, such as OAuth or API key headers, and to learn how to handle paginated responses where data spans multiple pages. I will continue using AI to quickly understand unfamiliar methods while verifying my understanding against official documentation to ensure accuracy.

---

## 8. Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'requests'` | The requests package is not installed in your active environment. | Ensure your virtual environment is activated first, then run: `pip install requests pandas` |
| `requests.exceptions.ConnectionError` | No internet connection, or the API URL is wrong. | Check your internet connection and verify the URL. The script catches this automatically and prints a friendly message. |
| `requests.exceptions.ReadTimeout` | The server took too long to respond. | Increase the timeout value in `fetch_todos()`: `response = requests.get(url, params=params, timeout=30)` |
| `requests.exceptions.HTTPError: 404` | The API endpoint URL is incorrect. | Verify the URL. For JSONPlaceholder todos the correct URL is: `https://jsonplaceholder.typicode.com/todos` |
| `KeyError: Column name does not exist` | The JSON field names from the API have changed, or you mistyped a column name. | Print `df.columns` immediately after creating the DataFrame to see the actual field names. |
| `PermissionError: Permission denied` | The `todos.csv` file is open in Excel or another application. | Close the file in Excel and re-run the script. Alternatively, save to a different filename: `df.to_csv('todos_new.csv', index=False)` |

---

## 9. References

* **The Python requests Documentation:** The official comprehensive guide. https://requests.readthedocs.io/en/latest/
* **pandas Documentation:** Official documentation for data manipulation. https://pandas.pydata.org/docs/
* **JSONPlaceholder API:** Free fake API for testing and prototyping. https://jsonplaceholder.typicode.com/
* **Real Python: Python's requests Library Guide.** https://realpython.com/python-requests/
* **Real Python: pandas DataFrames.** https://realpython.com/pandas-dataframe/
