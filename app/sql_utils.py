import sqlite3

def run_sql_query(query: str):
    conn = sqlite3.connect('db/ecommerce.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
    except Exception as e:
        result = str(e)
        columns = []
    conn.close()
    return {"columns": columns, "rows": result} 