import argparse
from sqlalchemy import create_engine
from enhanced_sql_agent import list_tables, describe_table, run_sql_query


def main():
    parser = argparse.ArgumentParser(description="AI-Powered SQL Query CLI")
    parser.add_argument("--db", type=str, required=True,
                        help="Database URL (e.g., sqlite:///Chinook_Sqlite.sqlite, postgresql://user:pass@localhost/db)")
    parser.add_argument("--action", type=str, choices=["list", "describe", "query"], required=True,
                        help="Action to perform: list tables, describe table, or execute query")
    parser.add_argument("--table", type=str, help="Table name (required for describe action)")
    parser.add_argument("--query", type=str, help="SQL query (required for query action)")

    args = parser.parse_args()

    # Create database engine
    db_engine = create_engine(args.db)

    if args.action == "list":
        print("Tables:", list_tables(db_engine))
    elif args.action == "describe":
        if not args.table:
            print("Error: --table argument is required for describe action.")
            return
        print(f"Schema for {args.table}:", describe_table(db_engine, args.table))
    elif args.action == "query":
        if not args.query:
            print("Error: --query argument is required for query action.")
            return
        print("Query Result:", run_sql_query(db_engine, args.query, user_query=args.query))


if __name__ == "__main__":
    main()