from ollama import chat


def review_report(report):

    print("Review Agent Running...")

    prompt = f"""
You are a quality review agent.

Review the report and correct it.

Validation Rules:

1. Merge duplicate incidents.
2. No incident should appear more than once.
3. A single incident cannot belong to multiple sections.
4. High Priority Unresolved Fires must contain ONLY unresolved issues.
5. General System Fixes Delivered must contain ONLY resolved issues.
6. Critical Infrastructure Monitor Watchlist must contain ONLY monitoring/watchlist items.
7. Every issue must have a severity label.
8. Recommended Actions must exist.
9. Markdown formatting must be correct.

Use EXACTLY these headings:

### 1. High Priority Unresolved Fires

### 2. General System Fixes Delivered

### 3. Critical Infrastructure Monitor Watchlist

### 4. Recommended Actions

IMPORTANT:

If an issue appears in Open Issues,
remove it from Resolved Issues.

If an issue appears in Resolved Issues,
remove it from Open Issues.

Do not duplicate incidents.

Return ONLY the corrected markdown.

Report:

{report}
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

    return response["message"]["content"]