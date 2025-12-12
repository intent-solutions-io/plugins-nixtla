view: nixtla_forecasts {
  sql_table_name: NIXTLA.FORECAST_RESULTS ;;

  dimension: unique_id {
    type: string
    sql: ${TABLE}.unique_id ;;
    description: "Time series identifier"
  }

  dimension_group: forecast {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    sql: ${TABLE}.forecast_date ;;
    description: "Forecast date"
  }

  dimension: forecast_value {
    type: number
    sql: ${TABLE}.forecast_value ;;
    description: "Point forecast value"
  }

  dimension: forecast_lo_80 {
    type: number
    sql: ${TABLE}.forecast_lo_80 ;;
    description: "Lower bound (80% confidence)"
  }

  dimension: forecast_hi_80 {
    type: number
    sql: ${TABLE}.forecast_hi_80 ;;
    description: "Upper bound (80% confidence)"
  }

  dimension: forecast_lo_95 {
    type: number
    sql: ${TABLE}.forecast_lo_95 ;;
    description: "Lower bound (95% confidence)"
  }

  dimension: forecast_hi_95 {
    type: number
    sql: ${TABLE}.forecast_hi_95 ;;
    description: "Upper bound (95% confidence)"
  }

  measure: count {
    type: count
    drill_fields: [unique_id, forecast_date, forecast_value]
  }

  measure: avg_forecast {
    type: average
    sql: ${forecast_value} ;;
  }

  measure: total_forecast {
    type: sum
    sql: ${forecast_value} ;;
  }
}
