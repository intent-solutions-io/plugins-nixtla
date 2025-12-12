{% macro nixtla_anomaly_detect(
    source_table,
    timestamp_col='ds',
    value_col='y',
    group_by_col='unique_id',
    level=95
) %}

{#
    Nixtla TimeGPT Anomaly Detection Macro for dbt

    Detects anomalies in time series data using TimeGPT.

    Parameters:
        source_table: Name of the source table or CTE
        timestamp_col: Column containing timestamps (default: 'ds')
        value_col: Column containing values (default: 'y')
        group_by_col: Column for grouping time series (default: 'unique_id')
        level: Confidence level for anomaly detection (default: 95)

    Returns:
        CTE with anomaly flags and scores
#}

{% if target.type == 'bigquery' %}
    {{ nixtla_anomaly_detect_bigquery(source_table, timestamp_col, value_col, group_by_col, level) }}
{% elif target.type == 'snowflake' %}
    {{ nixtla_anomaly_detect_snowflake(source_table, timestamp_col, value_col, group_by_col, level) }}
{% else %}
    {{ exceptions.raise_compiler_error("Unsupported target type for anomaly detection: " ~ target.type) }}
{% endif %}

{% endmacro %}


{% macro nixtla_anomaly_detect_bigquery(source_table, timestamp_col, value_col, group_by_col, level) %}
SELECT
    {{ group_by_col }},
    {{ timestamp_col }} as ds,
    {{ value_col }} as y,
    is_anomaly,
    anomaly_score
FROM ML.DETECT_ANOMALIES(
    MODEL `{{ var('nixtla_bq_model', 'nixtla.timegpt_model') }}`,
    STRUCT({{ level / 100 }} as contamination),
    TABLE {{ source_table }}
)
{% endmacro %}


{% macro nixtla_anomaly_detect_snowflake(source_table, timestamp_col, value_col, group_by_col, level) %}
SELECT *
FROM TABLE(
    NIXTLA.DETECT_ANOMALIES(
        INPUT_TABLE => '{{ source_table }}',
        TIMESTAMP_COL => '{{ timestamp_col }}',
        VALUE_COL => '{{ value_col }}',
        GROUP_BY_COL => '{{ group_by_col }}',
        LEVEL => {{ level }}
    )
)
{% endmacro %}
