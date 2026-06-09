from ollama import chat
from modules.review_agent import review_report


def generate_handover(chats, tickets):

    context = "CHAT LOGS:\n"

    for msg in chats:
        context += f"- {msg['user']}: {msg['message']}\n"

    context += "\nTICKET DATA:\n"

    for _, row in tickets.iterrows():
        context += (
            f"- Ticket {row['ticket_id']} "
            f"({row['status']}): "
            f"{row['description']}\n"
        )

    prompt = f"""
You are an Enterprise Operations Shift Handover Assistant.

Analyze the engineering chat logs and ticket records.

GOAL:
Generate a professional shift handover report for the next operations team.

CRITICAL RULES:

1. Merge duplicate incidents.
2. Merge related incidents.
3. Do not repeat incidents.
4. A single incident must appear in ONLY ONE section.
5. Open incidents must NOT appear in resolved incidents.
6. Resolved incidents must NOT appear in open incidents.
7. Monitoring items must appear ONLY in watchlist.
8. Use ticket status to determine category.

SECTION MAPPING:

OPEN:
- Open
- Critical
- High

RESOLVED:
- Resolved
- Closed
- Fixed

WATCHLIST:
- Monitoring
- Watchlist

SEVERITY:

🔴 Critical
- Production outage
- Database failure
- Service unavailable

🟡 Medium
- High CPU
- Performance degradation
- Resource warning

🟢 Resolved
- Fixed incidents

🟢 Low
- Monitoring items

OUTPUT FORMAT:

### 1. High Priority Unresolved Fires

List only unresolved incidents.

### 2. General System Fixes Delivered

List only resolved incidents.

### 3. Critical Infrastructure Monitor Watchlist

List only monitoring items.

### 4. Recommended Actions

Provide actions for every open incident.

EXAMPLES:

Database timeout observed
Database connection timeout

MUST become:

🔴 Critical: Database connection timeout in production

NOT:

Database timeout observed
Database connection timeout

DO NOT:

- Add explanations
- Add notes
- Add assumptions
- Add extra headings
- Repeat incidents

ONLY RETURN MARKDOWN.

DATA:

{context}
"""

    response = chat(
        model="gemma3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    draft_report = response["message"]["content"]

    final_report = review_report(
        draft_report
    )

    return final_report