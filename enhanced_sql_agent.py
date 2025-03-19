import json
import logging
from typing import Optional
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from load_models import OPENAI_MODEL

# Configure Logging
logging.basicConfig(filename='query_audit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def log_query(user_query: str, sql_query: str, result: str):
    """Logs queries for auditing."""
    log_entry = {
        "user_query": user_query,
        "sql_query": sql_query,
        "result": result,
    }
    logging.info(json.dumps(log_entry))


def list_tables(db_engine: Engine) -> str:
    """List tables in the database."""
    try:
        table_names = inspect(db_engine).get_table_names()
        return json.dumps(table_names)
    except Exception as e:
        return f'Error getting tables: {e}'


def describe_table(db_engine: Engine, table_name: str) -> str:
    """Get schema details of a table."""
    try:
        db_inspector = inspect(db_engine)
        table_schema = db_inspector.get_columns(table_name)
        return json.dumps([str(column) for column in table_schema])
    except Exception as e:
        return f'Error getting table schema for table \"{table_name}\": {e}'


def is_safe_query(query: str) -> bool:
    """Prevents SQL injection by restricting dangerous queries."""
    forbidden_keywords = ["DROP", "DELETE", "ALTER", "TRUNCATE"]
    for keyword in forbidden_keywords:
        if keyword in query.upper():
            return False
    return True


def generate_sql_from_nl(user_query: str) -> str:
    """Uses AI to convert a natural language request into an SQL query."""
    response = OPENAI_MODEL.complete(f"Convert this request into a SQL query: {user_query}")
    return response.text.strip()


def run_sql_query(db_engine: Engine, query: str, limit: Optional[int] = 10, user_query: str = "") -> str:
    """Executes a secure SQL query after validation."""
    if not is_safe_query(query):
        return "Query contains restricted keywords. Execution denied."

    confirmation = input(f"Are you sure you want to run this query? (yes/no): {query} ")
    if confirmation.lower() != "yes":
        return "Query execution canceled by user."

    with Session(db_engine) as session, session.begin():
        result = session.execute(text(query))
        try:
            rows = result.fetchmany(limit) if limit else result.fetchall()
            recordset = [dict(row._mapping) for row in rows]  # Ensure compatibility with SQLAlchemy 2.0+
            query_result = json.dumps(recordset, default=str)
            log_query(user_query, query, query_result)  # Log query execution
            return query_result
        except Exception as e:
            return f"Error executing query: {e}"
