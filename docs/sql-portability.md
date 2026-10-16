# SQL runtime and production adaptation

The supplied runnable dialect is **SQLite**, not Snowflake or SQL Server. The included Python pipeline executes all queries using `sqlite3`; no database server is required.

For Snowflake, use DATE columns, `DATEDIFF('day', start_date, end_date)` instead of `julianday(end)-julianday(start)`, and `COUNT_IF(condition)` or `SUM(CASE WHEN condition THEN 1 ELSE 0 END)` instead of SQLite Boolean sums. Snowflake supports `MEDIAN(days_to_start)` and `PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY days_to_start)` for completed durations. `ROW_NUMBER()` and CTEs preserve the approach; `QUALIFY` can simplify rank filters.

For SQL Server, use `DATEDIFF(day, start_date, end_date)` and explicit CASE expressions. Do not execute this SQLite schema unchanged against another engine. These are adaptation notes, not tested ports.

Before production use, define shipment vs shipment-line grain, reversals and adjustments, time zones, source precedence, revision timestamps, full timestamp validity, incremental load strategy, error ownership, and reconciliation tolerances. Current data uses ISO date-only strings and a fixed snapshot. SQLite date parsing is not a complete validator for arbitrary incoming feed formats.
