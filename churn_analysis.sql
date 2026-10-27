USE saas_churn_db;

SELECT COUNT(*) AS total_customers
FROM cleaned_customers;

SELECT *
FROM cleaned_customers
LIMIT 10;



SELECT
    Churn,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM cleaned_customers),
        2
    ) AS percentage
FROM cleaned_customers
GROUP BY Churn;



SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM cleaned_customers;



SELECT
    COUNT(*) AS retained_customers,
    ROUND(SUM(MonthlyCharges), 2)
        AS retained_monthly_revenue,
    ROUND(AVG(MonthlyCharges), 2)
        AS average_monthly_charge
FROM cleaned_customers
WHERE Churn = 'No';


SELECT
    customerID,
    tenure,
    Contract,
    MonthlyCharges,
    Churn,
    RiskScore,
    RiskLevel
FROM cleaned_customers
ORDER BY RiskScore DESC
LIMIT 10;