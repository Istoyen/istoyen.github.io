# Metric contract

All metrics use the fixed snapshot **2026-07-01**. Website payer/program filters affect the selected cohort, not the snapshot date.

| Metric | Numerator / definition | Denominator / eligible population |
|---|---|---|
| Referral cases | Count of case rows | Selected intake cohort |
| Paid starts | First paid shipment observed | Selected intake cohort |
| Snapshot start rate | Paid starts × 100 | All selected referrals, including pending and closed |
| Stage reached | Nonblank milestone date | All selected referrals; counts, not mutually exclusive statuses |
| Pending | status = Pending | Selected referrals |
| Completed turnaround | Paid start date minus intake date | Started cases only |
| Median / P90 | Inclusive linear-interpolated quantile | Completed durations; exclude nulls |
| Within 14 days | Completed turnaround <=14 | Completed paid starts only; not all referrals |
| Pending >14 days | Snapshot minus intake >14 | Pending cases only |
| Stage mean | Mean stage duration | Same completed paid-start cohort for every stage |
| Bridge turnaround | Bridge dispense minus request | Completed bridge requests only |
| Open bridge requests | Request exists; dispense absent | All selected referrals |
| Flagged rows | Count where any QA flag =1 | Selected raw feed rows |
| Flagged rate | Flagged rows × 100 | Selected raw feed rows |
| Accepted shipments | All flags =0 | Selected raw feed rows after duplicate screening |
| Reason counts | Rows with the specified flag | Raw rows; reasons overlap |

Calendar days include weekends and holidays; same-day service = 0. A 14-day threshold is solely illustrative. Conversion is a snapshot proportion with right-censoring; never call it an eventual conversion probability. Paid starts and bridge dispensing are distinct outcomes. Shipment payer/program filters use source-feed attributes so orphan rows remain visible. A patient access conversion metric must not be recomputed from accepted shipment rows: QA may remove feed records while the separate case source retains its observed paid-start event.

Rounding: calculate from unrounded values and display one decimal where appropriate. The exported conversion summary uses decimal half-up rounding, matching the website's 81.3% presentation of 975 / 1,200. Compare unrounded source fractions when reconciling across reporting tools.
