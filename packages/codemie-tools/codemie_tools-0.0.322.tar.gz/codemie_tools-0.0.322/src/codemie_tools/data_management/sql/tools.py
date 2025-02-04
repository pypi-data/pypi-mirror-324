import logging
from typing import Any, Union, Optional

from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text, inspect, Engine
from sqlalchemy.orm import sessionmaker

from typing import Type

from codemie_tools.base.codemie_tool import CodeMieTool
from codemie_tools.data_management.sql.models import SQLConfig, SQLDialect
from codemie_tools.data_management.sql.tools_vars import SQL_TOOL

logger = logging.getLogger(__name__)


class SQLToolInput(BaseModel):
    sql_query: str = Field(
        title="SQL Query",
        description="The SQL query to execute.",
    )


class SQLTool(CodeMieTool):
    name: str = SQL_TOOL.name
    description: str = SQL_TOOL.description
    args_schema: Type[BaseModel] = SQLToolInput
    sql_config: Optional[SQLConfig] = Field(exclude=True, default=None)

    def execute(self, sql_query: str):
        if self.sql_config is None:
            raise ValueError("SQL configuration is not provided.")
        engine = self.create_db_connection()
        init_data = self.list_tables_and_columns(engine)
        try:
            data = self.execute_sql(engine, sql_query)
        except Exception as exc:
            data = f"""
            There is an error: {exc}.\n
            Try to change your query to get the desired result according available details. \n
            Available tables with columns: {init_data}. \n
            """.strip()
        return data

    def execute_sql(self, engine: Engine, sql_query: str) -> Union[list, str]:
        maker_session = sessionmaker(bind=engine)
        session = maker_session()
        try:
            result = session.execute(text(sql_query))
            session.commit()

            if result.returns_rows:
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in result.fetchall()]
                return data
            else:
                return f"Query {sql_query} executed successfully"

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()

    def list_tables_and_columns(self, engine):
        inspector = inspect(engine)
        data = {}
        tables = inspector.get_table_names()
        for table in tables:
            columns = inspector.get_columns(table)
            columns_list = []
            for column in columns:
                columns_list.append({
                    'name': column['name'],
                    'type': column['type']
                })
            data[table] = {
                'table_name': table,
                'table_columns': columns_list
            }
        return data

    def create_db_connection(self):
        host = self.sql_config.host
        username = self.sql_config.username
        password = self.sql_config.password
        database_name = self.sql_config.database_name
        port = self.sql_config.port
        dialect = self.sql_config.dialect
        if dialect == SQLDialect.POSTGRES:
            connection_string = f'postgresql+psycopg://{username}:{password}@{host}:{port}/{database_name}'
        elif dialect == SQLDialect.MYSQL:
            connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
        else:
            raise ValueError(f"Unsupported database type. Supported types are: {[e.value for e in SQLDialect]}")

        return create_engine(connection_string)
