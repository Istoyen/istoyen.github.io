# Specialty pharmacy shipment quality

> Synthetic portfolio demonstration. No real patient or employer data. Results are not actual career achievements.

## Business question
Which incoming shipment rows should be quarantined before reporting?

A transparent SQL quality gate for a specialty pharmacy shipment feed. Every source row is preserved, defects are labeled, and the accepted extract can be reconciled back to the raw input.

## Decision supported
Route flagged rows to an exception queue and publish only accepted rows to the demonstration shipment report. Treat exception reason counts as overlapping signals.

## Method
1. Keep the raw feed immutable and identify duplicates using shipment_id with a deterministic source-row tie breaker.
2. Check missing case references, impossible dates, invalid days of supply, and nonpositive quantities.
3. Quarantine the union of failed checks; reconcile raw rows = accepted rows + flagged rows before releasing the extract.

## Observed synthetic findings
The generated feed contains 1,776 rows. The quality gate flags 232 rows (13.1%), leaving 1,544 accepted rows. The defects were deliberately injected to demonstrate detection; this is not a measured production error rate.

## Files and reproduction
Run `python3 python/build_data.py` from the repository root, followed by `python3 python/validate.py`.
Inspect `sql/04_shipment_quality.sql` and the matching `data/*_summary.csv` output. `sql/02_models.sql` defines the shared views. Read `docs/metric-dictionary.md` before interpreting the results.

## Limitations
The earliest source row is the canonical duplicate for this exercise. Production feeds may need revision timestamps, reversal rules, shipment-line keys, and adjudicated corrections. A first record that fails a check is not silently replaced by a later row.

## Potential business value
A real implementation could make recurring reporting auditable and reduce manual reconciliation. Quantify those benefits only after measuring an actual baseline and observing a comparable post-change period.

## Next iteration
Confirm operational definitions with stakeholders; validate business keys and timestamp semantics; reconcile with an authorized source; establish acceptance criteria and ownership for exceptions. For access analysis, add fixed follow-up cohorts or time-to-event analysis before comparing eventual conversion. For shipment feeds, incorporate reversals and versioned corrections. For turnaround, add a holiday calendar if business-day SLAs are required.

## Interview walkthrough
Explain the decision first, establish the grain and denominator, walk through one query, reproduce the synthetic finding, then discuss the limitation and how you would validate the method on authorized real data.
