import os
import re
import sqlite3
import subprocess
import sys
import traceback
from datetime import datetime
from pathlib import Path
from subprocess import PIPE

storage_file = Path(Path(__file__).parent, "history.sqlite").absolute()


def run_backup():
    print(f"New job run at {datetime.now()}")

    copyq_script_file = Path(Path(__file__).parent, "copyq_script.js").absolute()

    try:
        print("Attempting to run copyq script")
        result = subprocess.run(
            ["/Applications/CopyQ.app/Contents/MacOS/CopyQ", "eval", "-"],
            stdin=open(str(copyq_script_file), "rb"),
            stdout=PIPE,
            stderr=PIPE,
        )
    except Exception:
        print("Error when attempting to run copyq command.", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)

    if result.stderr:
        print("Subprocess ran but returned an error", file=sys.stderr)
        print(result.stderr, file=sys.stderr)

    print("Parsing copyq output")
    items = []
    last_item = ""
    for item in result.stdout.decode().split("\n"):
        if re.match("record number [0-9]*", item):
            # we've reached a new record, store and reset the placeholder string
            if last_item:
                items.append(last_item.strip("\n"))
                last_item = ""
            # don't keep the 'record number' row as a record
            continue
        last_item += item + "\n"
    # store the last one
    items.append(last_item.strip("\n"))

    print("Storing parsed items")
    if not storage_file.exists():
        connection = sqlite3.connect(str(storage_file))
        cursor = connection.cursor()
        cursor.execute(
            """
        CREATE TABLE clipboard_item (
            -- auto indexed as it's an alias for rowid
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content text,
            first_seen int,
            last_seen int
        )
        """
        )
    else:
        connection = sqlite3.connect(str(storage_file))
        cursor = connection.cursor()

    session_timestamp = datetime.now().timestamp()
    for item in items:
        cursor.execute("SELECT id FROM clipboard_item WHERE content=?", (item,))
        result = cursor.fetchone()
        if result:
            cursor.execute(
                "UPDATE clipboard_item SET last_seen=? WHERE id=?",
                (session_timestamp, result[0]),
            )
        else:
            cursor.execute(
                "INSERT INTO clipboard_item (content,first_seen,last_seen) VALUES (?,?,?)",
                (item, session_timestamp, session_timestamp),
            )

    connection.commit()


def search(search_query):
    connection = sqlite3.connect(str(storage_file))
    cursor = connection.cursor()
    cursor.execute(
        "select content from clipboard_item where content like ?",
        (f"%{search_query}%",),
    )
    separator = "*" * 20 + " NEXT CLIP " + "*" * 20 + "\n"
    [print(separator + z[0]) for z in cursor.fetchall()]
