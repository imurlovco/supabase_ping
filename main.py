import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from typing import cast

load_dotenv()

KST = timezone(timedelta(hours=9))
PING_TABLE = "ping_counter"
PING_ID = 1


def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL or SUPABASE_KEY is not set.")

    return create_client(url, key)


def send_ping():
    now = datetime.now(KST)
    supabase = get_supabase()

    response = supabase.table(PING_TABLE).select("count").eq("id", PING_ID).execute()

    if not response.data:
        print("No data found. Check table setting.")
        return

    row = cast(dict, response.data[0])
    new_count: int = row["count"] + 1

    supabase.table(PING_TABLE).update({
        "count": new_count,
        "last_pinged": now.isoformat(),
    }).eq("id", PING_ID).execute()

    print(f"Ping sent at {now.strftime('%Y-%m-%d %H:%M:%S')} | Count: {new_count}")


if __name__ == "__main__":
    try:
        send_ping()
    except Exception as e:
        print(f"An error occurred: {e}")