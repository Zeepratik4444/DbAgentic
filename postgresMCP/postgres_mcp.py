from fastmcp import FastMCP
from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from model import EmployeeCreate
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()

db_engine = os.getenv("db_engine")
db_username = os.getenv("db_username")
db_password = os.getenv("db_password")
rds_endpoint = os.getenv("rds_endpoint")
db_port = os.getenv("db_port")
db_name = os.getenv("db_name")
WHITELISTED_TABLES =os.getenv("WHITELIST")
db_url = f"{db_engine}://{db_username}:{db_password}@{rds_endpoint}:{db_port}/{db_name}"



db_mcp=FastMCP("postgresMCP")

@db_mcp.tool()
def create_record(employee_data: EmployeeCreate):
  """
  Create a new record in the employees table.
  Args:
    employee_data (EmployeeCreate): The data for the new employee.
  Returns:
    str: The ID of the newly created employee.
  """
  engine = create_engine(db_url)
  try:
      data_dict = employee_data.model_dump()
      columns = ", ".join(data_dict.keys())
      placeholders = ", ".join([f":{key}" for key in data_dict.keys()])
      sql_query = text(f"INSERT INTO employees ({columns}) VALUES ({placeholders}) RETURNING eid")

      with engine.connect() as connection:
          with connection.begin() as transaction:
              new_id = connection.execute(sql_query, data_dict).scalar_one()
              return new_id
  except Exception as e:
      print(f"An error occurred while creating record: {e}")
      return None

@db_mcp.tool()
def get_records(table_name="employees", criteria=None, value=None):
  """
  Get records from the specified table.
  Args:
    table_name (str): The name of the table to get records from.
    criteria (str): The column name to filter records by.
    value (Any): The value to filter records by.
    Returns:
    """
  engine = create_engine(db_url)
  try:
      sql_query = f"SELECT * FROM {table_name}"
      params = {}
      if criteria and value is not None:
          sql_query += f" WHERE {criteria} = :value"
          params = {"value": value}

      with engine.connect() as connection:
          df = pd.read_sql(text(sql_query), connection, params=params)
          return df
  except Exception as e:
      print(f"An error occurred while getting records: {e}")
      return None

@db_mcp.tool()
def update_record(table_name, record_id, update_data):
  """
  Update a record in the specified table.
  Args:
    table_name (str): The name of the table to update the record in.
    record_id (int): The ID of the record to update.
    update_data (Dict[str, Any]): The data to update the record with.
    Returns:
    int: The number of rows updated.
    """
  engine = create_engine(db_url)
  if not update_data:
      print("Error: No update data provided.")
      return 0
  try:
      set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
      sql_query = text(f"UPDATE {table_name} SET {set_clause} WHERE eid = :record_id")
      params = {**update_data, "record_id": record_id}

      with engine.connect() as connection:
          with connection.begin() as transaction:
              result = connection.execute(sql_query, params)
              return result.rowcount
  except Exception as e:
      print(f"An error occurred while updating record {record_id}: {e}")
      return None
    
@db_mcp.tool()
def delete_record(table_name, record_id):
  """
  Delete a record from the specified table.
  Args:
    table_name (str): The name of the table to delete the record from.
    record_id (int): The ID of the record to delete.
    Returns:
    int: The number of rows deleted.
    """
  engine = create_engine(db_url)
  try:
      sql_query = text(f"DELETE FROM {table_name} WHERE eid = :record_id")
      params = {"record_id": record_id}

      with engine.connect() as connection:
          with connection.begin() as transaction:
              result = connection.execute(sql_query, params)
              return result.rowcount
  except Exception as e:
      print(f"An error occurred while deleting record {record_id}: {e}")
      return None


@db_mcp.tool()
def get_data(table_name:str, criteria:Optional[str]=None, value:Optional[str]=None):
  """
  Get data from the specified table.
  Args:
    table_name (str): The name of the table to get data from.
    criteria (str): The column name to filter data by.
    value (Any): The value to filter data by.
  Returns
     The data from the specified table.
    """
  engine = create_engine(db_url)
  try:
      sql_query = f"SELECT * FROM {table_name}"
      params = {}
      if criteria and value is not None:
          sql_query += f" WHERE {criteria} = :value"
          params = {"value": value} 
      with engine.connect() as connection:
          df = pd.read_sql(text(sql_query), connection, params=params)
          return df
  except Exception as e:
    print(f"An error occurred while getting data: {e}")

@db_mcp.tool()
def query_database(query: str,table:str):
  """
  Execute a custom SQL query on the database.
  Args:
    query (str): The SQL query to execute.
    table (str): The table to execute the query on.
  Returns:
    The result of the query.
  """
  engine = create_engine(db_url)
  try:
      with engine.connect() as connection:
          df = pd.read_sql(text(query), connection)
          return df
  except Exception as e:
    print(f"An error occurred while executing query: {e}")


if __name__=="__main__":
  db_mcp.run(
    transport="sse",
    port=8001,
  )