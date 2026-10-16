-- Flags overlap; never sum reason counts to report affected rows.
SELECT payer, program, COUNT(*) AS raw_rows, SUM(is_flagged) AS flagged_rows,
 SUM(is_flagged=0) AS clean_rows, SUM(duplicate_flag) AS duplicate_excess_rows,
 SUM(orphan_flag) AS orphan_rows, SUM(date_flag) AS invalid_date_rows,
 SUM(supply_flag) AS invalid_supply_rows, SUM(quantity_flag) AS invalid_quantity_rows
FROM shipment_quality GROUP BY payer,program ORDER BY payer,program;
