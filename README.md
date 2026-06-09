# Shift Handover Note Generator

## Project Overview

Shift Handover Note Generator is an AI-powered operations communication tool designed to automate the creation of engineering shift handover reports.

The system analyzes engineering chat logs and ticket records, identifies incidents, removes duplicate information, classifies severity levels, and generates a structured shift handover report for the incoming operations team.

This project was developed as part of the AI Prototype Challenge.

---

# Problem Statement

Enterprise support engineers work in continuous shifts and must transfer critical operational information to the next team.

Traditionally, handover information is scattered across:

* Engineering chat platforms
* Incident management systems
* Operational ticket records

Manual handovers often lead to:

* Missing incident information
* Duplicate reporting
* Loss of operational context
* Increased troubleshooting time

The objective of this project is to automate the handover process using Artificial Intelligence.

---

# Solution

The Shift Handover Note Generator ingests:

1. Engineering Chat Logs (JSON)
2. Ticket Records (CSV)

The system then:

* Filters data from the last 12 hours
* Performs multi-source summarization
* Identifies duplicate incidents
* Merges overlapping issues
* Assigns severity levels
* Generates a structured handover report
* Saves the report as Markdown

---

# Key Features

## Multi-Source Data Ingestion

Accepts operational data from:

* JSON chat exports
* CSV ticket records

---

## 12-Hour Operational Filtering

Automatically filters records created within the previous 12 hours to ensure report relevance.

---

## AI-Powered Incident Analysis

Uses a local Large Language Model (Gemma3 via Ollama) to:

* Identify incidents
* Categorize events
* Generate operational summaries

---

## Incident Deduplication

Detects duplicate incidents appearing across multiple sources and merges them into a single incident record.

Example:

Database timeout observed

Database connection timeout

DB timeout

All are merged into:

Database connection timeout in production

---

## Severity Classification

Incidents are classified into:

### Critical

Production outages

Database failures

Service unavailable

---

### Medium

Performance degradation

CPU spikes

Resource utilization warnings

---

### Low

Monitoring activities

Watchlist items

Informational updates

---

## Agent Loop Architecture

The project implements an Agent Loop using two AI agents.

### Summarizer Agent

Responsibilities:

* Analyze chat logs
* Analyze ticket records
* Merge incidents
* Generate report

### Review Agent

Responsibilities:

* Validate generated report
* Verify categorization
* Verify severity labels
* Verify markdown structure

This creates an AI Agent Loop where one agent generates and another reviews the output.

---

# Project Architecture

Chat Logs (JSON)
+
Ticket Records (CSV)
↓
12-Hour Filter
↓
Summarizer Agent
↓
Incident Deduplication
↓
Review Agent
↓
Final Markdown Report

---

# Technology Stack

## Frontend

* Streamlit

## Programming Language

* Python

## AI Model

* Ollama
* Gemma3

## Data Formats

* JSON
* CSV

---

# Project Structure

ShiftHandoverGenerator/

├── app.py

├── requirements.txt

├── README.md

├── prompt_documentation.md

│

├── modules/

│   ├── data_loader.py

│   ├── filter_data.py

│   ├── summarizer.py

│   └── review_agent.py

│

├── test_data/

│   ├── sample_chats.json

│   └── sample_tickets.csv

│

└── output/

```
└── handover_note.md
```

---

# Installation

Clone the repository:

git clone <repository-url>

cd ShiftHandoverGenerator

Install dependencies:

pip install -r requirements.txt

---

# Running the Application

Start Ollama:

ollama serve

Pull Gemma3 model:

ollama pull gemma3

Run Streamlit:

streamlit run app.py

---

# Usage

1. Upload engineering chat logs in JSON format.
2. Upload ticket records in CSV format.
3. Click Generate Report.
4. Review the generated handover note.
5. Download the generated report.

---

# Sample Input Files

Sample files are available inside:

test_data/

* sample_chats.json
* sample_tickets.csv

---

# Sample Output

The generated report contains:

### 1. High Priority Unresolved Fires

Critical unresolved incidents requiring immediate attention.

### 2. General System Fixes Delivered

Issues successfully resolved during the shift.

### 3. Critical Infrastructure Monitor Watchlist

Systems requiring continuous monitoring.

### 4. Recommended Actions

Actionable recommendations for the incoming team.

---

# AI Capability Demonstration

This project demonstrates:

✅ Multi-Source Summarization

✅ Incident Deduplication

✅ Agent Loop Architecture

✅ AI-Assisted Report Generation

These capabilities satisfy the AI Prototype Challenge requirements.

---

# Team Contribution

All team members contributed to:

* Design
* Development
* Testing
* Documentation
* Demonstration

---

# License

This project is developed for educational and prototype demonstration purposes.
