from codemie_tools.base.models import ToolMetadata

SQL_TOOL = ToolMetadata(
    name="sql",
    description="""
    Converts natural language to SQL queries and executes them.
    If you do not know exact table name and columns, you must fetch them first.
    """.strip(),
    label="SQL",
    user_description="""
    Enables the AI assistant to execute SQL queries on supported database systems. This tool allows for data retrieval, manipulation, and analysis using SQL commands on MySQL or PostgreSQL databases.
    Before using it, it is necessary to add a new integration for the tool by providing:
    1. Alias (A friendly name for the database connection)
    2. Database Dialect (MySQL or PostgreSQL)
    3. URL (Database server address)
    4. PORT (Database server port)
    5. Database or schema name
    6. Username
    7. Password
    """.strip()
)
