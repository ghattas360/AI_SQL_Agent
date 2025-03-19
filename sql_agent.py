from textwrap import dedent
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from sqlalchemy import Engine, create_engine
from load_models import OPENAI_MODEL
from enhanced_sql_agent import list_tables, describe_table, run_sql_query, generate_sql_from_nl

system_prompt = dedent("""
    You are an AI SQL assistant equipped with tools to help users interact with databases.

    Supported databases: SQLite, MySQL, PostgreSQL.

    Workflow:
    1. First, run the `list_tables` tool to get a list of tables.
    2. Then, run the `describe_table` tool to get schema details.
    3. If the user provides a natural language request, convert it into SQL using `generate_sql_from_nl`.
    4. Finally, execute the query using `run_sql_query`.

    Ensure safe and efficient query execution.
""")

@dataclass
class Dependencies:
    db_engine: Engine

class ResponseModel(BaseModel):
    detail: str = Field(name='Detail', description='The result of the query.')

agent = Agent(
    name='Database Agent',
    model=OPENAI_MODEL,
    system_prompt=[system_prompt],
    result_type=ResponseModel
)

@agent.tool
def list_tables_tool(ctx: RunContext) -> str:
    """Use this function to get a list of table names in the database."""
    return list_tables(ctx.deps.db_engine)

@agent.tool
def describe_table_tool(ctx: RunContext, table_name: str) -> str:
    """Use this function to get a description of a table in the database."""
    return describe_table(ctx.deps.db_engine, table_name)

@agent.tool
def run_sql_tool(ctx: RunContext, query: str, limit: int = 10) -> str:
    """Use this function to run a SQL query on the database."""
    return run_sql_query(ctx.deps.db_engine, query, limit)

@agent.tool
def nl_to_sql_tool(ctx: RunContext, user_query: str) -> str:
    """Converts a natural language query to SQL."""
    return generate_sql_from_nl(user_query)

if __name__ == "__main__":
    db_engine = create_engine('sqlite:///./Chinook_Sqlite.sqlite')
    deps = Dependencies(db_engine=db_engine)

    user_query = input("Enter your query: ")
    sql_query = generate_sql_from_nl(user_query)

    response = agent.run_sync(
        f"Execute this SQL: {sql_query}",
        deps=deps
    )

    print(response.data.detail)
