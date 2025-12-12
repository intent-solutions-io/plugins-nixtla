{% macro nixtla_forecast(
    source_table,
    timestamp_col='ds',
    value_col='y',
    group_by_col='unique_id',
    horizon=14,
    freq='D',
    level=[80, 90, 95]
) %}

{#
    Nixtla TimeGPT Forecasting Macro for dbt

    Generates forecasts using TimeGPT via warehouse-specific integrations.

    Parameters:
        source_table: Name of the source table or CTE
        timestamp_col: Column containing timestamps (default: 'ds')
        value_col: Column containing values to forecast (default: 'y')
        group_by_col: Column for grouping time series (default: 'unique_id')
        horizon: Number of periods to forecast (default: 14)
        freq: Frequency of data (D, H, W, M) (default: 'D')
        level: Confidence levels for prediction intervals (default: [80, 90, 95])

    Returns:
        CTE with forecasted values and prediction intervals
#}

{% if target.type == 'bigquery' %}
    {{ nixtla_forecast_bigquery(source_table, timestamp_col, value_col, group_by_col, horizon, freq, level) }}
{% elif target.type == 'snowflake' %}
    {{ nixtla_forecast_snowflake(source_table, timestamp_col, value_col, group_by_col, horizon, freq, level) }}
{% elif target.type == 'databricks' %}
    {{ nixtla_forecast_databricks(source_table, timestamp_col, value_col, group_by_col, horizon, freq, level) }}
{% else %}
    {{ exceptions.raise_compiler_error("Unsupported target type: " ~ target.type ~ ". Supported: bigquery, snowflake, databricks") }}
{% endif %}

{% endmacro %}


{% macro nixtla_forecast_bigquery(source_table, timestamp_col, value_col, group_by_col, horizon, freq, level) %}
-- BigQuery implementation using external connection
SELECT
    {{ group_by_col }},
    forecast_date as ds,
    forecast_value as yhat,
    forecast_lo_{{ level[0] }} as yhat_lower,
    forecast_hi_{{ level[0] }} as yhat_upper
FROM ML.FORECAST(
    MODEL `{{ var('nixtla_bq_model', 'nixtla.timegpt_model') }}`,
    STRUCT(
        {{ horizon }} as horizon,
        {{ level | join(', ') }} as confidence_level
    )
)
WHERE source_table = '{{ source_table }}'
{% endmacro %}


{% macro nixtla_forecast_snowflake(source_table, timestamp_col, value_col, group_by_col, horizon, freq, level) %}
-- Snowflake implementation using Nixtla Native App
SELECT *
FROM TABLE(
    NIXTLA.FORECAST(
        INPUT_TABLE => '{{ source_table }}',
        TIMESTAMP_COL => '{{ timestamp_col }}',
        VALUE_COL => '{{ value_col }}',
        GROUP_BY_COL => '{{ group_by_col }}',
        HORIZON => {{ horizon }},
        FREQUENCY => '{{ freq }}',
        LEVEL => ARRAY_CONSTRUCT({{ level | join(', ') }})
    )
)
{% endmacro %}


{% macro nixtla_forecast_databricks(source_table, timestamp_col, value_col, group_by_col, horizon, freq, level) %}
-- Databricks implementation using Python UDF
SELECT *
FROM nixtla_forecast_udf(
    table('{{ source_table }}'),
    '{{ timestamp_col }}',
    '{{ value_col }}',
    '{{ group_by_col }}',
    {{ horizon }},
    '{{ freq }}'
)
{% endmacro %}
