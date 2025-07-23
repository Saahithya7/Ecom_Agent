from fastapi import FastAPI, Request
from app.llm import ask_llm
from app.sql_utils import run_sql_query
from pydantic import BaseModel
from typing import Optional
import io
import base64
import matplotlib.pyplot as plt
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    chart: Optional[bool] = False

@app.get("/")
def read_root():
    return {"message": "API is running. Use the /ask endpoint with POST to ask questions."}

@app.post("/ask")
async def ask_question(request: AskRequest):
    question = request.question
    chart = request.chart
    prompt = (
        "Given the following question, write an SQLite SQL query to answer it using the tables: "
        "ad_sales_metrics (date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold), "
        "total_sales_metrics (date, item_id, total_sales, total_units_ordered), "
        "eligibility (eligibility_datetime_utc, item_id, eligibility, message). "
        "Only return the SQL query, nothing else. "
        f"Question: {question}"
    )
    sql_query = ask_llm(prompt)
    result = run_sql_query(sql_query)

    print("Result for charting:", result)

    chart_image = None
    if chart and result["columns"] and result["rows"]:
        try:
            columns = result["columns"]
            rows = result["rows"]
            print("Columns:", columns)
            print("Rows:", rows)
            if len(columns) == 2 and len(rows) > 0:
                x = [row[0] for row in rows]
                y = [row[1] for row in rows]
                plt.figure(figsize=(8, 4))
                plt.bar(x, y)
                plt.xlabel(columns[0])
                plt.ylabel(columns[1])
                plt.title(question)
                buf = io.BytesIO()
                plt.tight_layout()
                plt.savefig(buf, format="png")
                plt.close()
                buf.seek(0)
                chart_image = base64.b64encode(buf.read()).decode("utf-8")
        except Exception as e:
            chart_image = f"Error generating chart: {e}"

    # Generate a human-readable answer using the LLM
    # We'll pass the question, the SQL, and a summary of the result to the LLM
    # For brevity, we'll show up to 5 rows in the summary
    result_summary = "\n".join([
        ", ".join(str(cell) for cell in row) for row in (result["rows"][:5] if isinstance(result["rows"], list) else [])
    ])
    answer_prompt = (
        f"Given the following question and the SQL query and its result, "
        f"write a human-readable answer.\n"
        f"Question: {question}\n"
        f"SQL: {sql_query}\n"
        f"Result (first 5 rows):\n{result_summary}\n"
        f"Answer:"
    )
    human_answer = ask_llm(answer_prompt)

    response = {
        "question": question,
        "sql_query": sql_query,
        "result": result,
        "answer": human_answer
    }
    if chart_image:
        response["chart"] = chart_image  # This is a base64-encoded PNG

    return response

@app.get("/test-ollama")
def test_ollama():
    response = ask_llm("Hello!")
    return {"response": response}
