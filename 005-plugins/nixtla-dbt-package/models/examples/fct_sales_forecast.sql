{{ config(materialized='table') }}

{#
    Example: Sales Forecast Model

    This model demonstrates how to use the nixtla_forecast macro
    to generate forecasts from historical sales data.
#}

with historical_sales as (
    -- Get historical sales data
    select
        product_id as unique_id,
        sale_date as ds,
        revenue as y
    from {{ ref('stg_sales') }}
    where sale_date >= dateadd(day, -365, current_date)
),

forecast as (
    -- Generate 30-day forecast using TimeGPT
    {{ nixtla_forecast(
        source_table='historical_sales',
        timestamp_col='ds',
        value_col='y',
        group_by_col='unique_id',
        horizon=30,
        freq='D'
    ) }}
)

select
    unique_id as product_id,
    ds as forecast_date,
    yhat as forecasted_revenue,
    yhat_lower as revenue_lower_bound,
    yhat_upper as revenue_upper_bound,
    current_timestamp() as generated_at
from forecast
