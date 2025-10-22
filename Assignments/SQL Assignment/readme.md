
-- ----------------------------------------------------------
-- Q1: Count the total number of customers who joined in 2023
-- ----------------------------------------------------------

```
SELECT COUNT(1) as Total_number_of_Customers FROM customers 
WHERE EXTRACT(YEAR FROM join_date) = 2023;
```

-- ----------------------------------------------------------

![alt text](image.png)
