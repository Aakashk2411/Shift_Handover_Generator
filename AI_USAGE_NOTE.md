# AI Usage Note

## Project Title

Shift Handover Note Generator

---

# Purpose

This document describes how Artificial Intelligence was used during the development and execution of the Shift Handover Note Generator.

The project was developed using an AI-assisted workflow and incorporates AI capabilities for incident analysis, summarization, deduplication, and report generation.

---

# AI Tools Used During Development

The following AI tools were used during project development:

* ChatGPT
* Claude
* Ollama
* Gemma3

---

# Role of Each AI Tool

## ChatGPT

ChatGPT was used for:

* Project planning
* Architecture design
* Python development assistance
* Streamlit implementation guidance
* Prompt engineering
* Debugging support
* Documentation generation
* GitHub setup guidance

---

## Claude

Claude was used for:

* UI enhancement ideas
* Dashboard styling improvements
* Layout optimization
* Modern enterprise dashboard design
* Visual refinement of the Streamlit interface

---

## Ollama

Ollama was used as the local AI runtime environment.

Responsibilities:

* Hosting the Large Language Model locally
* Processing prompts
* Running inference without external cloud APIs

---

## Gemma3

Gemma3 was used as the Large Language Model responsible for:

* Incident analysis
* Multi-source summarization
* Incident deduplication
* Severity classification
* Operational recommendation generation
* Shift handover report creation

---

# AI-Assisted Development Activities

Artificial Intelligence assisted in the following development activities:

## Project Planning

* Understanding challenge requirements
* Designing the project workflow
* Creating the application architecture

---

## Code Development

* Streamlit user interface development
* Python module development
* Data processing implementation
* Report generation workflow

---

## Prompt Engineering

* Designing prompts for incident analysis
* Designing prompts for deduplication
* Designing prompts for report validation
* Improving output consistency

---

## Debugging and Testing

* Resolving implementation issues
* Identifying logic errors
* Improving reliability and maintainability

---

## Documentation

* README generation
* Prompt documentation creation
* Project explanation and reporting

---

# AI Capability Implemented

The Shift Handover Note Generator uses Artificial Intelligence to process operational data and automatically generate structured handover reports.

The project demonstrates the following AI capabilities:

### Multi-Source Summarization

The system combines information from:

* Engineering chat logs (JSON)
* Ticket records (CSV)

and generates a unified operational summary.

---

### Incident Deduplication

The AI identifies duplicate incidents appearing across multiple sources and merges them into a single consolidated incident record.

Example:

Database timeout observed

Database connection timeout

DB timeout

↓

Database connection timeout in production

---

### Severity Classification

The AI categorizes incidents into:

* Critical
* Medium
* Resolved
* Low

based on operational impact.

---

### Operational Recommendation Generation

The AI generates actionable recommendations for the incoming shift team.

---

# Agent Loop Implementation

The project implements a two-agent workflow.

## Agent 1: Summarizer Agent

Responsibilities:

* Analyze chat logs
* Analyze ticket records
* Perform multi-source summarization
* Perform deduplication
* Generate draft reports

Output:

Draft Shift Handover Report

---

## Agent 2: Review Agent

Responsibilities:

* Validate generated reports
* Verify severity classifications
* Check markdown structure
* Ensure consistency

Output:

Final Shift Handover Report

---

# Agent Workflow

Chat Logs (JSON)

*

Ticket Records (CSV)

↓

12-Hour Filter

↓

Summarizer Agent

↓

Draft Report

↓

Review Agent

↓

Final Report

↓

Markdown Export

This architecture demonstrates an Agent Loop capability.

---

# AI Runtime

The application uses:

* Ollama
* Gemma3

The AI model runs locally and does not require external cloud APIs.

Benefits:

* Offline operation
* Reduced infrastructure cost
* Improved data privacy
* No dependency on external AI services

---

# Benefits of AI Usage

The use of AI provides:

* Faster report generation
* Reduced manual effort
* Improved consistency
* Better incident consolidation
* Automated severity classification
* Structured operational communication

---

# Challenge Requirement Compliance

The project satisfies the AI Prototype Challenge requirements by demonstrating:

✅ AI-Assisted Development

✅ Prompt Engineering

✅ Multi-Source Summarization

✅ Incident Deduplication

✅ Agent Loop Architecture

✅ Automated Report Generation

---

# Conclusion

Artificial Intelligence was used both during development and during application execution.

ChatGPT assisted with architecture design, implementation guidance, debugging, prompt engineering, documentation, and project setup.

Claude assisted with UI enhancement, dashboard design, and user experience improvements.

Ollama and Gemma3 provide the AI-powered incident analysis and report generation capabilities of the system.

The Shift Handover Note Generator demonstrates AI-assisted development, prompt engineering, multi-source summarization, incident deduplication, and Agent Loop architecture to automate operational handover reporting.
