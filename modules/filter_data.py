from datetime import datetime, timedelta
import pandas as pd


def filter_last_12_hours(chats, tickets):

    cutoff = datetime.now() - timedelta(hours=12)

    filtered_chats = []

    for chat in chats:

        try:

            chat_time = pd.to_datetime(
                chat["timestamp"]
            )

            if chat_time >= cutoff:
                filtered_chats.append(chat)

        except Exception:
            pass

    if "timestamp" in tickets.columns:

        tickets["timestamp"] = pd.to_datetime(
            tickets["timestamp"]
        )

        tickets = tickets[
            tickets["timestamp"] >= cutoff
        ]

    return filtered_chats, tickets