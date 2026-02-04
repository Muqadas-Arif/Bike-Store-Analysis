# ================================================
# Fix Foreign Keys in BikeStore Database
# ================================================
# Purpose: Add foreign key constraints to maintain referential integrity.
#          This script:
#          - Handles NULL values
#          - Makes columns NOT NULL where needed
#          - Adds primary keys if missing
#          - Adds foreign keys between tables
# Author: Muqadas (with Grok assistance)
# ================================================

from sqlalchemy import create_engine, text

# Change these to your server details
SERVER = 'DESKTOP-DBOU3LA'  # Your server name
DATABASE = 'BIKESTOREDB'

# Connection string (Windows Authentication)
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")

# Helper function to run SQL safely
def run_sql(sql):
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print(f"Executed successfully: {sql[:80]}...")

print("Starting foreign keys fix...\n")

# 1. Drop existing constraints if they exist (safe)
constraints_to_drop = [
    "FK_order_items_product", "FK_order_items_order",
    "FK_orders_customer", "FK_orders_staff", "FK_orders_store",
    "FK_products_category", "PK_products", "PK_order_items", "PK_categories"
]

for const in constraints_to_drop:
    run_sql(f"IF EXISTS (SELECT * FROM sys.objects WHERE name = '{const}') "
            f"ALTER TABLE {const.split('_')[1]} DROP CONSTRAINT {const};")

# 2. Fix categories.category_id (was nvarchar → int)
run_sql("UPDATE categories SET category_id = 0 WHERE category_id IS NULL OR TRY_CAST(category_id AS INT) IS NULL;")
run_sql("ALTER TABLE categories ALTER COLUMN category_id INT NOT NULL;")
run_sql("ALTER TABLE categories ADD CONSTRAINT PK_categories PRIMARY KEY (category_id);")

# 3. Fix products.category_id to match
run_sql("ALTER TABLE products ALTER COLUMN category_id INT NOT NULL;")

# 4. Fix products.product_id (ensure NOT NULL for PK)
run_sql("UPDATE products SET product_id = 0 WHERE product_id IS NULL;")
run_sql("ALTER TABLE products ALTER COLUMN product_id SMALLINT NOT NULL;")
run_sql("ALTER TABLE products ADD CONSTRAINT PK_products PRIMARY KEY (product_id);")

# 5. Fix order_items.product_id
run_sql("ALTER TABLE order_items ALTER COLUMN product_id SMALLINT NOT NULL;")

# 6. Add composite PK to order_items
run_sql("ALTER TABLE order_items ADD CONSTRAINT PK_order_items PRIMARY KEY (order_id, item_id);")

# 7. Add all foreign keys
fk_commands = [
    ("orders", "customer_id", "customers", "customer_id", "FK_orders_customer"),
    ("orders", "staff_id", "staffs", "staff_id", "FK_orders_staff"),
    ("orders", "store_id", "stores", "store_id", "FK_orders_store"),
    ("order_items", "order_id", "orders", "order_id", "FK_order_items_order"),
    ("order_items", "product_id", "products", "product_id", "FK_order_items_product"),
    ("products", "category_id", "categories", "category_id", "FK_products_category")
]

for parent, col, ref_table, ref_col, fk_name in fk_commands:
    run_sql(f"ALTER TABLE {parent} ADD CONSTRAINT {fk_name} FOREIGN KEY ({col}) REFERENCES {ref_table}({ref_col});")

print("\nAll foreign keys added successfully!")

# Final check - show all FKs
print("\nAll Foreign Keys in Database:")
pd.read_sql("""
    SELECT 
        OBJECT_NAME(fkc.constraint_object_id) AS FK_Name,
        OBJECT_NAME(fkc.parent_object_id) AS Table_Name,
        COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS Column_Name,
        OBJECT_NAME(fkc.referenced_object_id) AS Referenced_Table
    FROM sys.foreign_key_columns fkc
    ORDER BY Table_Name;
""", engine)
-------------------------------------------------------------------------------------------------------------------------------------------------------------
=================================----------------------------------=======================================--------------------------------------------------
### Database Setup & Foreign Keys Fix

 
**Purpose:**  
This script fixes data type mismatches and adds foreign key constraints to the BikeStore database.  

**Why we did this:**  
- During CSV import using SSMS Import Wizard, some columns got wrong data types (e.g., category_id as nvarchar in categories but tinyint in products).  
- Foreign keys could not be created due to type mismatch and nullable columns on PKs.  
- We:  
  - Replaced NULLs with default values  
  - Changed column types to match (mostly INT or SMALLINT NOT NULL)  
  - Dropped and re-added primary keys where needed  
  - Added all necessary foreign keys for referential integrity  

**Result:**  
All tables now have correct relationships (e.g., orders → customers, order_items → products, products → categories). Joins work perfectly and data consistency is maintained.

**Run this before any analysis notebooks.**









