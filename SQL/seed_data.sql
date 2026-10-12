SELECT COUNT(*) AS total_customers
FROM customers;
SELECT COUNT(*) AS total_products
FROM products;
SELECT COUNT(*) AS total_orders
FROM orders;
SELECT COUNT(*) AS unrated_orders
FROM orders
WHERE rating IS NULL;
SELECT COUNT(*) AS unrated_orders
FROM orders
WHERE rating IS NULL;
SELECT COUNT(*) AS null_discounts
FROM orders
WHERE discount_pct IS NULL;
