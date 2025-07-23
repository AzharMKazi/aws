-- Athena query to get top selling products
SELECT product_id, SUM(amount) AS total_sales
FROM transactions
GROUP BY product_id
ORDER BY total_sales DESC
LIMIT 10;