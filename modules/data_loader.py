import json
import pandas as pd
from datetime import datetime, timedelta


def load_data():

    with open("data/chats.json", "r") as f:
        chats = json.load(f)

    tickets = pd.read_csv("data/tickets.csv")

    cutoff = datetime.now() - timedelta(hours=12)

    filtered_chats = []

    for chat in chats:
        chat_time = datetime.strptime(
            chat["timestamp"],
            "%Y-%m-%d %H:%M"
        )

        if chat_time >= cutoff:
            filtered_chats.append(chat)

    return filtered_chats, tickets