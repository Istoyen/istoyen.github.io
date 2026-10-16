# Data dictionary

All entities are fictional. No names, dates of birth, contact data, prescriptions, or real patient identifiers are used. Case IDs are generated `SYN-xxxxx` labels; no mapping to real people exists.

## Files, grain, and relationships
| File/table | Grain | Key | Use |
|---|---|---|---|
| cases.csv / cases | One synthetic referral | case_id | Source timeline and status |
| shipments_raw.csv / shipments_raw | One source feed row, including duplicates | source_row_id | Immutable QA input |
| case_metrics.csv / case_metrics view | One referral | case_id | Modeled patient access and turnaround |
| shipment_quality.csv / shipment_quality view | One source feed row | source_row_id | Individual QA flags and release decision |
| *_summary.csv | One payer × program group | payer + program | SQL aggregate outputs |

`shipments_raw.case_id` logically references `cases.case_id` but is deliberately not enforced: orphans are injected. `shipment_id` is the shipment-level business key and deliberately repeats for duplicate records. A valid accepted shipment can include repeat monthly fills for the same case. Do not join referral and shipment facts to calculate case counts: fan-out would inflate them.

## Case source fields
- `case_id`: synthetic referral key, text.
- `payer`: Commercial, Medicare, Medicaid, Uninsured (illustrative operational categories).
- `program`: Immunology, Oncology, Neurology (fictional groupings).
- `received_date`: intake date, January 1–June 30, 2026 inclusive.
- `complete_date`, `verified_date`, `approved_date`, `first_paid_ship_date`: stage dates in ISO YYYY-MM-DD; blank if not observed by the snapshot or if closed in the simplified generator.
- `status`: Started if a paid start is observed, Closed if closed before the snapshot, Pending otherwise.
- `bridge_requested_date`, `bridge_dispensed_date`: separate optional bridge pathway, not a substitute for paid start. Bridge may overlap the paid pathway or occur for a case later closed.
- `as_of_date`: fixed 2026-07-01; current date is never used for aging.

## Derived fields
`days_to_start`, `intake_days`, `verification_days`, `approval_days`, `fulfillment_days`, `bridge_days`: integer calendar-date differences; blank unless both endpoints exist. `pending_age_days` exists only for Pending cases. `within_14_days` is 0/1 for completed paid starts and blank otherwise.

## Shipment source fields and flags
`source_row_id`: integer unique row. `shipment_id`: text business key. `case_id`: text reference. `ship_date`: ISO date. `days_supply`, `quantity`: integers. `shipment_type`: Paid. `payer`, `program`: attributes carried in the source feed, retained even on orphan rows.

`duplicate_rank` orders source rows within shipment_id. `duplicate_flag`: rank >1. `orphan_flag`: no matching case. `date_flag`: missing/unparseable date, shipment before referral or after snapshot. `supply_flag`: null, <=0, or >90. `quantity_flag`: null or <=0. `is_flagged`: union of the five flags. Flags are integers 0/1 and overlap. Empty fields in CSV represent null, not zero.

## Generation assumptions
Seed 42 creates 1,200 referrals, approximately 12% early closure, approximately 29% bridge requests, and variable stage delays. Medicaid approval receives four additional days by design. Future milestones are censored at the snapshot. Closed cases have no completed milestones, a simplifying assumption. Paid shipments recur every 28 days with 1–3 attempted fills, truncated at the snapshot. Corrupt references, dates, supply and quantity plus duplicate rows are deliberately injected. The generated timelines and rows support demonstrations, not clinical, demographic, insurance-policy, or causal conclusions.
