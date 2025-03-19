# AI-Powered SQL Agent 🚀  

An AI-driven SQL assistant that allows users to interact with databases using natural language or SQL queries. It supports **SQLite, MySQL, and PostgreSQL**, ensuring **secure query execution** with AI-powered assistance.

---

## ✨ Key Features  

✅ **Natural Language to SQL (NL-to-SQL) Conversion**  
- Converts natural language queries into SQL using OpenAI’s GPT-4o.  
- Example: `"Show me all customers from France"` → AI generates SQL automatically.  

✅ **Multi-Database Support**  
- Works with **SQLite, MySQL, PostgreSQL** via SQLAlchemy.  
- Can dynamically switch between databases.  

✅ **AI-Driven Query Execution**  
- Uses AI to **list tables**, **describe schemas**, and **execute queries**.  
- Automates query building with structured steps.  

✅ **Secure Query Execution (SQL Injection Prevention)**  
- Blocks dangerous SQL statements (`DROP`, `DELETE`, `ALTER`).  
- Confirms queries before execution.  

✅ **Query Logging & Audit Trail**  
- Logs every query with timestamps for auditing.  
- Helps track database interactions and maintain security.  

✅ **Command-Line Interface (CLI) for Easy Interaction**  
- Users can interact with the database via a **simple terminal-based CLI**.  
- Supports listing tables, describing schemas, and executing queries.  

✅ **Environment-Based API Key Management**  
- Uses a **`.env` file** for storing API keys securely.  
- Prevents hardcoding sensitive credentials.  

---

## 📥 Installation  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/ghattas360/AI_SQL_Agent.git
cd AI_SQL_Agent
