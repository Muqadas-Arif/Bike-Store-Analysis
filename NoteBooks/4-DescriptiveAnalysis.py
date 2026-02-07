
Strong Descriptive Analysis-----------------------------------------------------------------------------------------------------
Overall Business Summary (Total Orders, Customers, Revenue);;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Python................................................

query_summary = """
SELECT 
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    ROUND(SUM(oi.quantity * oi.list_price * (1 - oi.discount)), 2) AS total_revenue,
    ROUND(AVG(oi.quantity * oi.list_price * (1 - oi.discount)), 2) AS avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
"""
df_summary = pd.read_sql(query_summary, engine)
print("Overall Business Summary:")
df_summary
Date Range of Sales
query_dates = """
SELECT 
    MIN(order_date) AS first_order,
    MAX(order_date) AS last_order,
    DATEDIFF(YEAR, MIN(order_date), MAX(order_date)) AS years_covered
FROM orders
"""
pd.read_sql(query_dates, engine)
Monthly Revenue Trend (Line Plot)
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

query_monthly = """
SELECT 
    YEAR(o.order_date) AS year,
    MONTH(o.order_date) AS month,
    ROUND(SUM(oi.quantity * oi.list_price * (1 - oi.discount)), 2) AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY YEAR(o.order_date), MONTH(o.order_date)
ORDER BY year, month
"""
df_monthly = pd.read_sql(query_monthly, engine)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df_monthly['month'], df_monthly['monthly_revenue'], marker='o', linewidth=2, color='royalblue')
plt.title('Monthly Revenue Trend (All Years Combined)', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.xticks(range(1, 13), ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
Revenue by Store (Bar Plot)
query_stores = """
SELECT 
    s.store_name,
    ROUND(SUM(oi.quantity * oi.list_price * (1 - oi.discount)), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN stores s ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY revenue DESC
"""
df_stores = pd.read_sql(query_stores, engine)
df_stores
query_stores = """
SELECT 
    s.store_name,
    ROUND(SUM(oi.quantity * oi.list_price * (1 - oi.discount)), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN stores s ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY revenue DESC
"""
df_stores = pd.read_sql(query_stores, engine)

plt.figure(figsize=(9, 5))
sns.barplot(y='revenue', x='store_name', data=df_stores, palette='viridis')
plt.title('Revenue by Store', fontsize=14)
plt.xlabel('Store Name', fontsize=12)
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
Top 10 Products by Revenue
query_products = """
SELECT TOP 10
    p.product_name,
    ROUND(SUM(oi.quantity * oi.list_price * (1 - oi.discount)), 2) AS revenue,
    SUM(oi.quantity) AS total_quantity_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
"""
df_top_products = pd.read_sql(query_products, engine)
print("Top 10 Products by Revenue:")
df_top_products
#Revenue by Category (Bar Plot)
query_category = """
SELECT 
    c.category_name,
    ROUND(SUM(oi.quantity * oi.list_price * (1 - oi.discount)), 2) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY revenue DESC
"""
df_category = pd.read_sql(query_category, engine)

plt.figure(figsize=(10, 6))
sns.barplot(x='revenue', y='category_name', data=df_category, palette='plasma')
plt.title('Revenue by Product Category')
plt.xlabel('Revenue ($)')
plt.ylabel('Category')
plt.tight_layout()
plt.show()





