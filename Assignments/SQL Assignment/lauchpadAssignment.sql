-- SELECT * FROM customers;
-- SELECT * FROM loyalty_points;
-- SELECT * FROM order_items;
-- SELECT * FROM orders;
-- SELECT * FROM products;

-- ----------------------------------------------------------
-- Q1: Count the total number of customers who joined in 2023
-- ----------------------------------------------------------

SELECT COUNT(1) as Total_number_of_Customers FROM customers 
WHERE EXTRACT(YEAR FROM join_date) = 2023;

-- ----------------------------------------------------------
-- Q2: For each customer return customer_id, full_name, 
-- total_revenue (sum of total_amount from orders). 
-- Sort descending.
-- ----------------------------------------------------------

SELECT c.customer_id, c.full_name, sum(total_amount) as total_revenue
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY 1,2
ORDER BY 3 DESC

-- ----------------------------------------------------------------
-- Q3: Return the top 5 customers by total_revenue with their rank.
-- ----------------------------------------------------------------
WITH ranked as ( 
	SELECT 	c.customer_id, 
			c.full_name, 
			sum(total_amount) as total_revenue,
			RANK() OVER (ORDER BY sum(total_amount) DESC) as nth_rank
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY 1,2
ORDER BY 3 DESC
)

SELECT * FROM ranked
WHERE nth_rank < 6

-- ----------------------------------------------------------------
-- Q4: Produce a table with year, month, monthly_revenue for all 
-- months in 2023 ordered chronologically.
-- ----------------------------------------------------------------
SELECT year, month, SUM() OVER (PARTITION BY month,total_amount) as rggr
FROM (
	SELECT 	EXTRACT(YEAR FROM order_date) as year, 
			EXTRACT(MONTH FROM order_date) as month, 
			total_amount,
			   
	FROM orders) as newTable
-- ----------------------------------------------------------------
-- Q5: Find customers with no orders in the last 60 days relative 
-- to 2023-12-31 (i.e., consider last active date up to 2023-12-31). 
-- Return customer_id, full_name, last_order_date.
-- ----------------------------------------------------------------

SELECT 
		o.customer_id, 
		c.full_name, 
		o.order_date last_order_date 
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.customer_id
WHERE o.order_date NOT BETWEEN DATE '2023-12-31' - INTERVAL '60 DAYS' 
AND DATE '2023-12-31'
ORDER BY 3;


-- ----------------------------------------------------------------
-- Q6: Calculate average order value (AOV) for each customer: return
-- customer_id, full_name, aov (average total_amount of their orders).
-- Exclude customers with no orders.
-- ----------------------------------------------------------------

SELECT 
		o.customer_id, 
		c.full_name, 
		AVG(total_amount) AOV
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.customer_id
WHERE order_id IS NOT NULL  -- excluding all customers with no orders
GROUP BY 1,2

-- ----------------------------------------------------------------
-- Q7: For all customers who have at least one order, compute 
-- customer_id, full_name, total_revenue, spend_rank where spend_rank 
-- is a dense rank, highest spender = rank 1.
-- ----------------------------------------------------------------
SELECT *, DENSE_RANK() OVER (ORDER BY total_revenue DESC) as spend_rank FROM (
SELECT 
		o.customer_id, 
		c.full_name, 
		SUM(total_amount) total_revenue
FROM customers c
LEFT JOIN orders o
ON o.customer_id = c.customer_id
WHERE order_id IS NOT NULL  -- getting all customers with at least one order
GROUP BY 1,2)

-- ----------------------------------------------------------------
-- Q8: List customers who placed more than 1 order and show 
-- customer_id, full_name, order_count, first_order_date, 
-- last_order_date.
-- ----------------------------------------------------------------

SELECT 
		o.customer_id, 
		c.full_name, 
		count(o.order_id) order_count,
		order_date last_order_date,
		LAG() OVER (PARTITION BY c.full_name ORDER BY o.order_date) as jdjijdij
		-- ROW_NUMBER() OVER (PARTITION BY c.full_name ORDER BY o.order_id) as nth_order
FROM customers c
LEFT JOIN orders o
ON o.customer_id = c.customer_id
-- WHERE order_id IS NOT NULL  -- getting all customers with at least one order
GROUP BY 1,2, o.order_id, order_date



-- ----------------------------------------------------------------
-- Q9: Compute total loyalty points per customer. Include customers
-- with 0 points.
-- ----------------------------------------------------------------

SELECT 
		c.customer_id, 
		c.full_name,
		SUM(points_earned) as loyalty_points
FROM customers c
LEFT JOIN loyalty_points l
ON c.customer_id = l.customer_id
GROUP BY 1,2
ORDER BY 3 DESC;

-- ----------------------------------------------------------------
-- Q10: Assign loyalty tiers based on total points:
-- Bronze: < 100
-- Silver: 100–499
-- Gold: >= 500
-- Output: tier, tier_count, tier_total_points
-- ----------------------------------------------------------------

WITH tiers as (
SELECT 
		c.customer_id, 
		c.full_name,
		SUM(points_earned) as loyalty_points,
		CASE
		WHEN SUM(points_earned) < 100 THEN 'Bronze'
		WHEN SUM(points_earned) BETWEEN 100 AND 499 THEN 'Silver'
		WHEN SUM(points_earned) >= 500 THEN 'Gold'
		END as tier
FROM customers c
LEFT JOIN loyalty_points l
ON c.customer_id = l.customer_id
GROUP BY 1,2
ORDER BY 3 DESC)

SELECT tier, COUNT(tier) as tier_count, SUM(loyalty_points) as tier_total_points

FROM tiers
GROUP BY 1

-- ----------------------------------------------------------------
-- Q11: Identify customers who spent more than ₦50,000 in total but 
-- have less than 200 loyalty points. Return customer_id, full_name, 
-- total_spend, total_points.
-- ----------------------------------------------------------------

SELECT 
		c.customer_id, 
		c.full_name,
		points_earned as total_points,
		SUM(total_amount) as total_spend
		
FROM customers c
LEFT JOIN loyalty_points l
ON c.customer_id = l.customer_id
LEFT JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY 1,2,3 
HAVING SUM(total_amount) > 50000 AND points_earned < 200


-- ----------------------------------------------------------------
-- Q12: Flag customers as churn_risk if they have no orders in the 
-- last 90 days (relative to 2023-12-31) AND are in the Bronze tier.
-- Return customer_id, full_name, last_order_date, total_points.
-- ----------------------------------------------------------------

WITH tiers as (
SELECT 
		c.customer_id, 
		c.full_name,
		o.order_date last_order_date,
		SUM(points_earned) as loyalty_points,
		CASE
		WHEN SUM(points_earned) < 100 THEN 'Bronze'
		WHEN SUM(points_earned) BETWEEN 100 AND 499 THEN 'Silver'
		WHEN SUM(points_earned) >= 500 THEN 'Gold'
		END as tier
FROM customers c
LEFT JOIN loyalty_points l
ON c.customer_id = l.customer_id
LEFT JOIN orders o
ON c.customer_id = o.customer_id
WHERE o.order_date NOT BETWEEN DATE '2023-12-31' - INTERVAL '60 DAYS' 
AND DATE '2023-12-31'
GROUP BY 1,2, 3
ORDER BY 3 DESC)

SELECT 	customer_id, 
		full_name,
		last_order_date,
		loyalty_points,
		tier
FROM tiers
WHERE tier = 'Bronze'