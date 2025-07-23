Ecom_Agent: AI Agent for E-commerce Data Querying

Ecom_Agent is an AI-powered system that intelligently answers user queries related to e-commerce metrics. It integrates a Large Language Model (LLM), SQL database, and API endpoints to simulate a smart data analyst that responds in real-time.

---

Objective
To build an AI Agent that:
- Accepts natural language questions via an API.
- Converts them into SQL queries.
- Fetches results from structured datasets.
- Responds in a human-readable format.
- Provides visualizations and simulates live response.

---

Datasets Used

1. Product-Level Ad Sales and Metrics  
2. Product-Level Total Sales and Metrics  
3. Product-Level Eligibility Table

These are structured and imported into a local SQL database.

---

How It Works

1. Data Preprocessing  
   Convert CSV datasets into SQL tables using SQLite.

2. LLM Integration  
   A local or free LLM (e.g., Gemini 2.5 API) is used to understand user questions and generate SQL queries.

3. Query Execution  
   The generated SQL query is run on the database to retrieve accurate results.

4. Response Generation
   Answers are returned in a clean, human-readable format, and optionally with visualizations.

---

Example Questions

- What is my total sales?
- Calculate the RoAS (Return on Ad Spend).
- Which product had the highest CPC (Cost Per Click)?

---
