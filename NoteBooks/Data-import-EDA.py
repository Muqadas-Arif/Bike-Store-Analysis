# Import libraries
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
server = 'DESKTOP-DBOU3LA'         
database = 'BIKESTOREDB'
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)
print(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")

print("Connection ready!")
# Test query – orders table se top 5 rows
query = "SELECT TOP 5 * FROM orders"
df = pd.read_sql(query, engine)
df
query = "SELECT TOP 5 * FROM categories"
df = pd.read_sql(query, engine)
df
query = "SELECT TOP 5 * FROM customers"
df = pd.read_sql(query, engine)
df
query = "SELECT TOP 5 * FROM brands"
df = pd.read_sql(query, engine)
df
query = "SELECT TOP 5 * FROM order_items"
df = pd.read_sql(query, engine)
df
query = "SELECT TOP 5 * FROM staffs"
df = pd.read_sql(query, engine)
df
query = "SELECT TOP 5 * FROM products"
df = pd.read_sql(query, engine)
df
query = "SELECT TOP 5 * FROM stocks"
df = pd.read_sql(query, engine)
df
query = "SELECT TOP 5 * FROM stores"
df = pd.read_sql(query, engine)
df
tables = ['categories', 'customers', 'brands', 'order_items', 'staffs', 'products', 'stocks', 'stores']
for table in tables:
    query= f'select count(*) from {table}'
    df=pd.read_sql(query,engine)
    print(f'Table {table} has rows: {df.iloc[0,0]}')
    

query="select * from customers"
df_customers=pd.read_sql(query,engine)
df_customers.info()
df_customers.describe()
query="select * from orders"
df_orders=pd.read_sql(query,engine)
df_orders.info()
df_orders.describe()
query="select * from stores"
df_stores=pd.read_sql(query,engine)
df_stores.info()
df_stores.describe()
query="select * from products"
df_products=pd.read_sql(query,engine)
df_products.info()
df_products.describe()
for table in tables:
    
   df = pd.read_sql(f"SELECT * FROM {table}", engine)
   nulls = df.isnull().sum()
   print(f"\n{table} null values:\n{nulls[nulls > 0]}")
query = """
SELECT 
    MIN(order_date) AS first_order,
    MAX(order_date) AS last_order,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(quantity * list_price * (1 - discount)) AS total_revenue  -- From order_items join
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
"""
df_summary = pd.read_sql(query, engine)
df_summary










