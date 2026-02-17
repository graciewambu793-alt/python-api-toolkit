"""
=============================================================
  Python API Toolkit – Beginner's Guide to Web APIs
  Capstone Project | Moringa School | February 2026
=============================================================
  Author  : [Your Name]
  Tech    : Python, requests, pandas
  API     : JSONPlaceholder (https://jsonplaceholder.typicode.com)
  Goal    : Fetch 20 todo items from a public API,
            process them with pandas, and save to todos.csv
=============================================================
"""

import requests       # Makes HTTP requests to the API
import pandas as pd   # Processes JSON data into a structured table
import sys            # Used for exiting on critical errors


# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────

API_URL  = "https://jsonplaceholder.typicode.com/todos"
PARAMS   = {"_limit": 20}   # Fetch only the first 20 todos
OUTPUT   = "todos.csv"       # Output filename


# ─────────────────────────────────────────────
#  STEP 1 – Fetch Data from the API
# ─────────────────────────────────────────────

def fetch_todos(url: str, params: dict) -> list:
    """
    Send a GET request to the API and return the JSON response.

    Args:
        url    : The API endpoint to call.
        params : Query parameters (e.g. pagination limits).

    Returns:
        A list of todo dictionaries.

    Raises:
        SystemExit on any network or HTTP error.
    """
    print(f"\n📡  Fetching data from: {url}")
    print(f"    Parameters        : {params}\n")

    try:
        # Timeout prevents the script from hanging indefinitely
        response = requests.get(url, params=params, timeout=10)

        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()

        data = response.json()
        print(f"✅  Success! Received {len(data)} records.")
        return data

    except requests.exceptions.ConnectionError:
        print("❌  ERROR: Could not connect. Check your internet connection.")
        sys.exit(1)

    except requests.exceptions.Timeout:
        print("❌  ERROR: The request timed out. The server may be slow.")
        sys.exit(1)

    except requests.exceptions.HTTPError as e:
        print(f"❌  HTTP ERROR: {e}")
        print(f"    Status Code: {response.status_code}")
        sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"❌  UNEXPECTED ERROR: {e}")
        sys.exit(1)


# ─────────────────────────────────────────────
#  STEP 2 – Process Data with pandas
# ─────────────────────────────────────────────

def process_data(data: list) -> pd.DataFrame:
    """
    Convert the raw JSON list into a clean pandas DataFrame.

    Args:
        data : List of todo dictionaries from the API.

    Returns:
        A cleaned, processed DataFrame.
    """
    print("\n🔧  Processing data with pandas...")

    # Convert list of dicts → DataFrame
    df = pd.DataFrame(data)

    # Rename columns for clarity
    df.rename(columns={
        "userId"    : "user_id",
        "id"        : "todo_id",
        "title"     : "task",
        "completed" : "is_completed"
    }, inplace=True)

    # Add a human-readable status column
    df["status"] = df["is_completed"].map({True: "Done ✅", False: "Pending ⏳"})

    # Reorder columns for readability
    df = df[["todo_id", "user_id", "task", "is_completed", "status"]]

    # Quick summary statistics
    total     = len(df)
    completed = df["is_completed"].sum()
    pending   = total - completed

    print(f"    Total tasks   : {total}")
    print(f"    Completed     : {completed}")
    print(f"    Pending       : {pending}")

    return df


# ─────────────────────────────────────────────
#  STEP 3 – Save to CSV
# ─────────────────────────────────────────────

def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    """
    Save the DataFrame to a CSV file.

    Args:
        df       : The processed DataFrame to save.
        filename : The output file path/name.
    """
    df.to_csv(filename, index=False)
    print(f"\n💾  Data saved to '{filename}'")
    print(f"    Rows    : {len(df)}")
    print(f"    Columns : {list(df.columns)}")


# ─────────────────────────────────────────────
#  STEP 4 – Preview in Terminal
# ─────────────────────────────────────────────

def preview(df: pd.DataFrame, n: int = 5) -> None:
    """
    Print a preview of the first n rows in the terminal.

    Args:
        df : The DataFrame to preview.
        n  : Number of rows to show (default 5).
    """
    print(f"\n📋  Preview (first {n} rows):\n")
    print(df.head(n).to_string(index=False))
    print("\n" + "─" * 70)


# ─────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  Python API Toolkit – Fetch & Save Todo Data")
    print("  Moringa School Capstone | February 2026")
    print("=" * 70)

    # Step 1: Fetch
    raw_data = fetch_todos(API_URL, PARAMS)

    # Step 2: Process
    df = process_data(raw_data)

    # Step 3: Save
    save_to_csv(df, OUTPUT)

    # Step 4: Preview
    preview(df)

    print("\n🎉  Done! Open 'todos.csv' to see your data.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
