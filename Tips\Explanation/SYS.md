### Database Constraints & Foreign Keys Fix

**Why needed?**  
During CSV import via SSMS Import Wizard, column data types were inconsistent (e.g., `category_id` as `nvarchar` in `categories` but `tinyint` in `products`), and some columns were nullable. This prevented primary keys and foreign keys from being created.

**What the script does:**
- Uses **SQL Server system views** (`sys.foreign_key_columns`, `sys.key_constraints`) to safely check and drop existing constraints.
- Handles NULL values with safe defaults (e.g., `UPDATE ... SET column = 0 WHERE column IS NULL`).
- Changes column types to match (e.g., `nvarchar` → `INT`, `tinyint` → `SMALLINT`) and makes them `NOT NULL` (required for PK).
- Re-adds primary keys and composite keys where needed.
- Adds foreign key constraints for referential integrity.

**Key system views used:**
- `sys.foreign_key_columns`: To list and verify foreign keys.
- `sys.key_constraints`: To check and drop primary keys before altering columns.

**Result:**  
All tables now have proper relationships:
- orders → customers, staffs, stores
- order_items → orders, products
- products → categories

This ensures clean joins and prevents invalid data insertion.
