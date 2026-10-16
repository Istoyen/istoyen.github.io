CREATE VIEW case_metrics AS
SELECT *,
 CAST(julianday(first_paid_ship_date)-julianday(received_date) AS INTEGER) AS days_to_start,
 CAST(julianday(complete_date)-julianday(received_date) AS INTEGER) AS intake_days,
 CAST(julianday(verified_date)-julianday(complete_date) AS INTEGER) AS verification_days,
 CAST(julianday(approved_date)-julianday(verified_date) AS INTEGER) AS approval_days,
 CAST(julianday(first_paid_ship_date)-julianday(approved_date) AS INTEGER) AS fulfillment_days,
 CAST(julianday(bridge_dispensed_date)-julianday(bridge_requested_date) AS INTEGER) AS bridge_days,
 CASE WHEN status='Pending' THEN CAST(julianday(as_of_date)-julianday(received_date) AS INTEGER) END AS pending_age_days,
 CASE WHEN first_paid_ship_date IS NOT NULL THEN CASE WHEN julianday(first_paid_ship_date)-julianday(received_date)<=14 THEN 1 ELSE 0 END END AS within_14_days
FROM cases;
CREATE VIEW shipment_quality AS
WITH ranked AS (
 SELECT *, ROW_NUMBER() OVER(PARTITION BY shipment_id ORDER BY source_row_id) AS duplicate_rank
 FROM shipments_raw
), flags AS (
 SELECT r.*, CASE WHEN duplicate_rank>1 THEN 1 ELSE 0 END AS duplicate_flag,
 CASE WHEN c.case_id IS NULL THEN 1 ELSE 0 END AS orphan_flag,
 CASE WHEN ship_date IS NULL OR date(ship_date) IS NULL OR ship_date<c.received_date OR ship_date>c.as_of_date THEN 1 ELSE 0 END AS date_flag,
 CASE WHEN days_supply IS NULL OR days_supply<=0 OR days_supply>90 THEN 1 ELSE 0 END AS supply_flag,
 CASE WHEN quantity IS NULL OR quantity<=0 THEN 1 ELSE 0 END AS quantity_flag
 FROM ranked r LEFT JOIN cases c ON r.case_id=c.case_id
)
SELECT *, CASE WHEN duplicate_flag+orphan_flag+date_flag+supply_flag+quantity_flag>0 THEN 1 ELSE 0 END AS is_flagged
FROM flags;
