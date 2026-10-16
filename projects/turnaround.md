# Onboarding & bridge turnaround

> Synthetic portfolio demonstration. No real patient or employer data. Results are not actual career achievements.

## Business question
Which onboarding stages and open cases need operational attention?

A turnaround analysis that combines completed-case latency with the age of unresolved work. Bridge support is modeled separately from paid therapy starts so the two pathways are not conflated.

## Decision supported
Use median and tail latency to frame process variation, stage duration to locate delay, and aging thresholds to build a review queue. The 14-day threshold is a demonstration target, not a clinical or contractual standard.

## Method
1. Calculate elapsed calendar days from intake to first paid shipment, with same-day completion equal to zero.
2. Compare completed-case median and 90th percentile while showing pending cases older than 14 days alongside them.
3. Analyze completed bridge requests and open bridge requests separately; never substitute bridge dispensing for a paid start.

## Observed synthetic findings
The synthetic completed paid-start cohort has a median onboarding time of 16 calendar days. The dashboard recalculates turnaround and aging as payer and program filters change.

## Files and reproduction
Run `python3 python/build_data.py` from the repository root, followed by `python3 python/validate.py`.
Inspect `sql/05_turnaround.sql` and the matching `data/*_summary.csv` output. `sql/02_models.sql` defines the shared views. Read `docs/metric-dictionary.md` before interpreting the results.

## Limitations
Completed-case turnaround excludes unresolved cases and can look artificially favorable. The backlog view mitigates that blind spot but is not a survival analysis. Calendar days include weekends; bridge and paid workflows may overlap. No intervention or causal improvement is estimated.

## Potential business value
A real team could use this view to focus daily work and establish a shared turnaround definition. Any claim about reduced time to therapy would need a verified baseline, follow-up data, and a defensible comparison.

## Next iteration
Confirm operational definitions with stakeholders; validate business keys and timestamp semantics; reconcile with an authorized source; establish acceptance criteria and ownership for exceptions. For access analysis, add fixed follow-up cohorts or time-to-event analysis before comparing eventual conversion. For shipment feeds, incorporate reversals and versioned corrections. For turnaround, add a holiday calendar if business-day SLAs are required.

## Interview walkthrough
Explain the decision first, establish the grain and denominator, walk through one query, reproduce the synthetic finding, then discuss the limitation and how you would validate the method on authorized real data.
