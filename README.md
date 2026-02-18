
Python API Toolkit – Beginner's Guide to Web APIs


1. Title & Objective
Project Title: Python API Toolkit – Beginner's Guide to Web APIs
Technology Chosen Python with the requests library and pandas — the most widely used combination for fetching, processing, and exporting API data.
Why This Technology? requests is the industry standard for making HTTP calls in Python — used by millions of developers worldwide. pandas transforms raw JSON data into structured tables, enabling filtering, analysis, and export in just a few lines. Together they represent a critical skill stack for data engineering, backend scripting, and automation. The learning curve is gentle, making this an ideal starting point for anyone new to APIs.
End Goal Fetch 20 todo items from the free JSONPlaceholder API, convert the JSON response into a clean pandas DataFrame, enrich it with a human-readable status column, and export the result to todos.csv — all while handling network and HTTP errors gracefully.
The key goals of this project are to fetch data from a live API, process it with pandas, export it as a CSV, and handle errors gracefully throughout.

2. Quick Summary of the Technology
What is the requests library? requests is a Python library that lets you send HTTP requests (GET, POST, PUT, DELETE) with minimal code. It handles authentication, headers, parameters, timeouts, and error responses out of the box — without touching Python's verbose built-in urllib.
What is pandas? pandas is a fast, powerful Python library for data manipulation and analysis. It provides the DataFrame — a 2D table structure similar to a spreadsheet — that makes working with structured data (like API responses) intuitive and efficient.
What is JSONPlaceholder? JSONPlaceholder is a free, public REST API for testing and prototyping. It requires no authentication, returns realistic JSON data, and supports standard HTTP methods — making it the perfect playground for API beginners.
Where are these tools used in the real world?
Tool	Real-World Use Case
requests	Large-scale companies in the social media and tech industry rely on Python and requests for building and maintaining internal API clients
pandas	Companies in the streaming and entertainment industry use pandas for content analytics and A/B test result processing
JSONPlaceholder	Front-end and back-end teams use it as a mock API during rapid prototyping


3. System Requirements
Requirement	Details
Operating System	Windows 10+, macOS 10.14+, or Ubuntu 20.04+
Python Version	3.7 or later (3.10+ recommended)
pip	Version 21+ recommended — comes bundled with Python 3.4+ and is used to install packages
Virtual Environment	venv is recommended as best practice to isolate project dependencies
IDE / Editor	VS Code (recommended), PyCharm, or any text editor
Internet Access	Required to call the JSONPlaceholder API
Packages	requests >= 2.28.0, pandas >= 1.5.0

4. Installation & Setup Instructions
Step 1 – Verify Python is Installed
# Check Python version (needs 3.7+)
python --version

# Check pip is available
pip --version
Step 2 – Create Project Folder
mkdir python-api-toolkit
cd python-api-toolkit
Step 3 – Create & Activate a Virtual Environment
A virtual environment keeps your project's packages isolated from the rest of your system.
# Create the virtual environment
python -m venv venv

# Activate it (macOS / Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Your prompt should now show: (venv)
Step 4 – Install Required Packages
pip install requests pandas

# Or install from requirements.txt:
pip install -r requirements.txt
Step 5 – Create requirements.txt
# Save current packages for reproducibility
pip freeze > requirements.txt

# Minimum contents of requirements.txt:
# requests>=2.28.0
# pandas>=1.5.0
Step 6 – Verify Everything is Ready
python -c "import requests; import pandas; print('All good!')"
# Expected output:
# All good!
✅ Checkpoint — If you see 'All good!' you are fully set up and ready to write the main script.
________________________________________
5. Minimal Working Example
What This Example Does
This script sends a GET request to the JSON Placeholder API with a ?_limit=20 query parameter, parses the JSON response into a Python list of dictionaries, and converts it into a pandas DataFrame with renamed columns for readability. It then adds a human-readable status column that maps True/False values to Done/Pending labels, saves the result as todos.csv, and handles ConnectionError, Timeout, and HTTP errors gracefully throughout.
Repository Structure
python-api-toolkit/
├── fetch_todos.py       # Main script (fully commented)
├── requirements.txt     # Python dependencies
├── todos.csv            # Output file (generated on run)
└── README.md            # Setup & run instructions
The README.md should include a short project description explaining what the script does, step-by-step setup instructions for a new user, and a sample of the expected terminal output so anyone running the project for the first time knows what a successful result looks like.
Step-by-Step: Clone & Run
# 1. Clone the repository
git clone <your-github-url>
cd python-api-toolkit

# 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the script
python fetch_todos.py

# 5. Open the output
# todos.csv will appear in your project folder

File: fetch_todos.py
import requests       # Makes HTTP requests to the API
import pandas as pd   # Processes JSON data into a structured table
import sys            # Used for exiting on critical errors

# ── CONFIGURATION ──────────────────────────────────────────────
API_URL = "https://jsonplaceholder.typicode.com/todos"
PARAMS  = {"_limit": 20}  # Fetch only the first 20 todos
OUTPUT  = "todos.csv"     # Output filename

# ── STEP 1: Fetch Data ─────────────────────────────────────────
def fetch_todos(url: str, params: dict) -> list:
    """
    Sends a GET request to the given URL with query parameters.

    Args:
        url (str): The API endpoint to call.
        params (dict): Query parameters to include in the request.

    Returns:
        list: A list of dictionaries parsed from the JSON response.
    """
    print("======================================================")
    print("  Python API Toolkit – Fetch & Save Todo Data")
    print("  Moringa School Capstone | February 2026")
    print("======================================================\n")
    print(f"  Fetching data from: {url}")
    print(f"  Parameters        : {params}\n")

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()   # Raise error for 4xx/5xx
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

# ── STEP 2: Process Data ───────────────────────────────────────
def process_data(data: list) -> pd.DataFrame:
    """
    Converts raw JSON data into a clean, enriched pandas DataFrame.

    Args:
        data (list): A list of dictionaries from the API response.

    Returns:
        pd.DataFrame: A structured DataFrame with a derived status column.
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

    return df[["todo_id", "user_id", "task", "is_completed", "status"]]

# ── STEP 3: Save to CSV ────────────────────────────────────────
def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    """
    Exports the DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The processed DataFrame to save.
        filename (str): The name of the output CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"  Data saved to '{filename}'\n")

# ── MAIN ───────────────────────────────────────────────────────
if __name__ == "__main__":
    data = fetch_todos(API_URL, PARAMS)
    df   = process_data(data)
    save_to_csv(df, OUTPUT)

    print("  Preview (first 5 rows):")
    print(df.head().to_string(index=False))
    print("\n  Done! Open 'todos.csv' to see your data.")
    print("======================================================")
Expected Terminal Output
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
  todo_id  user_id  task                     is_completed  status
        1        1  delectus aut autem        False         Pending
        2        1  quis ut nam facilis...    False         Pending
        3        1  fugiat veniam minus       False         Pending
        4        1  et porro tempora          True          Done
        5        1  laboriosam mollitia...    False         Pending

  Done! Open 'todos.csv' to see your data.
======================================================
Generated todos.csv Preview
todo_id | user_id | task                          | is_completed | status
--------|---------|-------------------------------|--------------|--------
1       | 1       | delectus aut autem             | False        | Pending
4       | 1       | et porro tempora               | True         | Done
11      | 2       | vero rerum temporibus dolor    | True         | Done
18      | 2       | dolorum est consequatur        | False        | Pending
20      | 2       | ullam nobis libero sapiente    | True         | Done
________________________________________
6. AI Prompt Journal
All prompts were submitted via ai.moringaschool.com (powered by Claude). The journal below records the exact prompts used, what the AI returned, and how helpful each response was.
Prompt 1 – Understanding APIs
Field	Details
Prompt Used	"Explain what a REST API is to a complete beginner. What is JSON? How does a GET request work? Give a real-world analogy."
AI Summary	The AI explained APIs as a 'waiter in a restaurant' — you (client) ask the waiter (API) for something, the waiter goes to the kitchen (server) and brings back your order (response). JSON was described as a structured text format that both humans and machines can read. A GET request was compared to asking a library for a book — you don't change anything, you just retrieve information.
Helpfulness	⭐⭐⭐⭐⭐ – The analogy made the concept click instantly. Used it in peer explanations.
________________________________________
Prompt 2 – Setting Up the requests Library
Field	Details
Prompt Used	"Show me a step-by-step guide to install and use the Python requests library. Include how to send a GET request, check the status code, and parse a JSON response. Use JSONPlaceholder as the example API."
AI Summary	The AI walked through pip install requests, a minimal GET request using requests.get(), checking response.status_code, calling response.json() to parse the response, and using timeout=10 to avoid hanging. It also mentioned raise_for_status() for automatic error detection.
Helpfulness	⭐⭐⭐⭐⭐ – Directly usable. I copy-adapted the boilerplate into my fetch_todos() function.
________________________________________
Prompt 3 – Processing JSON with pandas
Field	Details
Prompt Used	"I have a Python list of dictionaries from a JSON API response. How do I convert it to a pandas DataFrame, rename the columns, add a new derived column, and export it to CSV? Show me with a todo list example."
AI Summary	The AI showed pd.DataFrame(data) to convert a list of dicts, df.rename(columns={...}) to rename keys, df['status'] = df['completed'].map({True: 'Done', False: 'Pending'}) for derived columns, and df.to_csv('output.csv', index=False) to export. It also showed df.head() for a quick preview.
Helpfulness	⭐⭐⭐⭐⭐ – The .map() pattern for derived columns was new to me and extremely useful.
________________________________________
Prompt 4 – Error Handling in API Calls
Field	Details
Prompt Used	"What are the common errors when making API calls in Python with requests? Show me how to handle ConnectionError, Timeout, and HTTPError properly with try/except blocks."
AI Summary	The AI explained three main error types: ConnectionError (no internet), Timeout (server too slow — solved with timeout= parameter), and HTTPError (bad status codes — solved with raise_for_status()). It provided a clean try/except structure catching each exception separately with informative print messages, and recommended sys.exit(1) for unrecoverable errors.
Helpfulness	⭐⭐⭐⭐⭐ – Applied directly. My script now handles all three failure modes gracefully.
________________________________________
Prompt 5 – Refining Code Quality
Field	Details
Prompt Used	"Review this Python function that fetches API data. How can I improve it using Python best practices? I want proper docstrings, type hints, and clean separation of concerns."
AI Summary	The AI restructured the code into three clean functions: fetch_todos(), process_data(), and save_to_csv(), each with a single responsibility. It added type hints (def fetch_todos(url: str, params: dict) -> list:), docstrings with Args and Returns sections, and f-strings for all print statements. It also suggested an if name == 'main': guard.
Helpfulness	⭐⭐⭐⭐ – Code quality improved significantly and the separation of concerns made testing easier. One star deducted as some of the type hint suggestions went slightly beyond beginner scope and required additional research to fully understand.
________________________________________
Learning Reflection
Using AI reduced my setup time by approximately 60%. Instead of reading through scattered documentation, I could ask targeted questions and receive contextual code examples immediately. The most valuable insight was learning raise_for_status() — a single line that replaced 10+ lines of manual status code checking. AI also helped me discover the .map() method in pandas, which I would not have found quickly through trial and error.
If I were to approach this project again, I would start by mapping out all three functions before writing any code, rather than building and refactoring as I went  this would have saved time and reduced the number of revisions needed. Going forward, I plan to explore working with APIs that require authentication, such as OAuth or API key headers, and to learn how to handle paginated responses where data spans multiple pages. I will continue using AI to quickly understand unfamiliar methods while verifying my understanding against official documentation to ensure accuracy.

7. Common Errors & Fixes
Error 1 – ModuleNotFoundError: No module named 'requests'
🔴 ModuleNotFoundError: No module named 'requests'
Cause: The requests package is not installed in your active environment.
Fix:
# Ensure your virtual environment is activated first
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows

# Then install
pip install requests pandas
Error 2 – requests.exceptions.ConnectionError: Failed to establish a new connection
🔴 requests.exceptions.ConnectionError: Failed to establish a new connection
Cause: No internet connection, or the API URL is wrong.
Fix: Check your internet connection and verify the URL. The script catches this automatically and prints a friendly message.
Error 3 – requests.exceptions.ReadTimeout: Read timed out
🔴 requests.exceptions.ReadTimeout: HTTPSConnectionPool: Read timed out
Cause: The server took too long to respond.
Fix:
# Increase the timeout value in fetch_todos()
response = requests.get(url, params=params, timeout=30)  # was 10
Note: If timeouts persist even after increasing the value, the issue is likely on the server side rather than in your code. In that case, wait a few minutes and try again — there is nothing further you can do by increasing the number alone.
Error 4 – requests.exceptions.HTTPError: 404 Client Error: Not Found
🔴 requests.exceptions.HTTPError: 404 Client Error: Not Found for url
Cause: The API endpoint URL is incorrect.
Fix: Verify the URL. For JSONPlaceholder todos the correct URL is:
API_URL = "https://jsonplaceholder.typicode.com/todos"

Error 5 – KeyError: Column name does not exist in the DataFrame
🔴 KeyError: 'userId' – the column name does not exist in the DataFrame
Cause: The JSON field names from the API have changed, or you mistyped a column name.
Fix: Print df.columns immediately after creating the DataFrame to see the actual field names:
df = pd.DataFrame(data)
print(df.columns)   # Debug: check actual column names
print(df.head(2))   # Debug: preview the first two rows
Error 6 – PermissionError: Permission denied: 'todos.csv'
🔴 PermissionError: [Errno 13] Permission denied: 'todos.csv'
Cause: The todos.csv file is open in Excel or another application.
Fix: Close the file in Excel and re-run the script. Alternatively, save to a different filename:
df.to_csv('todos_new.csv', index=False)

8. References
Official Documentation
•	requests library – https://requests.readthedocs.io/en/latest/ 
•	pandas documentation – https://pandas.pydata.org/docs/ 
•	JSONPlaceholder API – https://jsonplaceholder.typicode.com/ 
•	Python json module – https://docs.python.org/3/library/json.html 
Video Tutorials
•	Python requests Tutorial – Corey Schafer (YouTube)
•	pandas Full Course – freeCodeCamp (YouTube)
•	APIs for Beginners – freeCodeCamp (YouTube)
Articles & Blog Posts
•	Real Python: Python's requests Library Guide – https://realpython.com/python-requests/
•	Real Python: pandas DataFrames – https://realpython.com/pandas-dataframe/
•	Stack Overflow: Search for "how to handle requests exceptions in Python" for community-sourced solutions and discussion threads covering a wide range of API error scenarios.
AI Tool
•	 (Claude) – Used for all 5 prompts in the AI Prompt Journal above.
________________________________________
9. Project Structure & How to Run
Repository Structure
python-api-toolkit/
├── fetch_todos.py       # Main script (fully commented)
├── requirements.txt     # Python dependencies
├── todos.csv            # Output file (generated on run)
└── README.md            # Setup & run instructions
The README.md should include a short project description explaining what the script does, step-by-step setup instructions for a new user, and a sample of the expected terminal output so anyone running the project for the first time knows what a successful result looks like.
Step-by-Step: Clone & Run
# 1. Clone the repository
git clone <your-github-url>
cd python-api-toolkit

# 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the script
python fetch_todos.py

# 5. Open the output
# todos.csv will appear in your project folder



