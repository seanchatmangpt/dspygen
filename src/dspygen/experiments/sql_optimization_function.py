import sqlite3

from dspygen.experiments.lm_call import call
from dspygen.utils.dspy_tools import init_dspy

# Assuming Chinook.db is located in the same directory for simplicity
conn = sqlite3.connect("Chinook.db")

poor_query = """WITH recursive cte_dates AS (
  SELECT 
    DATEADD(day, 1, MIN(order_date)) AS dt
  FROM 
    orders

  UNION ALL

  SELECT 
    DATEADD(day, 1, dt)
  FROM 
    cte_dates
  WHERE 
    dt < (SELECT DATEADD(day, -1, MAX(order_date)) FROM orders)
),

cte_sales AS (
  SELECT 
    p.product_id,
    p.product_name,
    d.dt,
    SUM(oi.quantity * oi.unit_price) AS daily_sales
  FROM 
    cte_dates d
  CROSS JOIN 
    products p
  LEFT JOIN 
    order_items oi ON oi.product_id = p.product_id
                   AND CAST(oi.order_date AS DATE) = CAST(d.dt AS DATE)
  GROUP BY 
    p.product_id,
    p.product_name,
    d.dt
),

cte_max_sales AS (
  SELECT 
    product_id,
    product_name,
    MAX(daily_sales) AS max_daily_sales
  FROM 
    cte_sales
  GROUP BY 
    product_id,
    product_name
)

SELECT 
  product_id,
  product_name,
  dt AS date_of_max_sales,
  max_daily_sales
FROM 
  cte_sales cs
JOIN 
  cte_max_sales cms ON cs.product_id = cms.product_id
                   AND cs.daily_sales = cms.max_daily_sales
"""

from pydantic import BaseModel


class SQLQueryModel(BaseModel):
    query: str


class OptimizedSQLQueryModel(BaseModel):
    rationale: str
    optimized_query: str


def sql_query_optimizer() -> OptimizedSQLQueryModel:
    """Optimize the given SQL query"""


def main():
    init_dspy(max_tokens=3000)

    # result = invoke("What is the name of the album with the most tracks and count?", question_to_chinook_query)

    result = call(sql_query_optimizer, poor_query)

    print(result)


if __name__ == '__main__':
    main()
