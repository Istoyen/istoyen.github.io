# Patient access & enrollment

> Synthetic portfolio demonstration. No real patient or employer data. Results are not actual career achievements.

## Business question
Where do referrals stall between intake and first paid shipment?

A cohort-based view of the access journey, from referral intake to paid therapy start. The analysis separates open work from closed cases so a single conversion metric does not hide the operational backlog.

## Decision supported
Use the intake funnel and payer comparison to identify stages that deserve a workflow review, then inspect individual synthetic cases before drawing conclusions.

## Method
1. Define one referral case as the analysis grain, with sequential intake, verification, approval, and first paid shipment dates.
2. Calculate snapshot conversion against every referral in the selected intake cohort; show pending and closed cases separately.
3. Slice the same denominator by payer and program, and inspect stage completion counts without double-counting cases.

## Observed synthetic findings
975 of 1,200 synthetic referrals had a first paid shipment by July 1, 2026 (81.25% before rounding). Another 82 remained pending. These are snapshot outcomes, not real employer performance.

## Files and reproduction
Run `python3 python/build_data.py` from the repository root, followed by `python3 python/validate.py`.
Inspect `sql/03_patient_access.sql` and the matching `data/*_summary.csv` output. `sql/02_models.sql` defines the shared views. Read `docs/metric-dictionary.md` before interpreting the results.

## Limitations
Recent intake cohorts have had less time to reach treatment. Comparing their raw conversion with older cohorts is misleading. The generator also deliberately adds approval delay for Medicaid cases; any payer difference reflects that assumption, not evidence about a real population.

## Potential business value
A real deployment could give access teams a consistent intake denominator and a prioritized backlog. Measure usefulness through reconciled case counts and documented follow-up decisions before claiming faster access.

## Next iteration
Confirm operational definitions with stakeholders; validate business keys and timestamp semantics; reconcile with an authorized source; establish acceptance criteria and ownership for exceptions. For access analysis, add fixed follow-up cohorts or time-to-event analysis before comparing eventual conversion. For shipment feeds, incorporate reversals and versioned corrections. For turnaround, add a holiday calendar if business-day SLAs are required.

## Interview walkthrough
Explain the decision first, establish the grain and denominator, walk through one query, reproduce the synthetic finding, then discuss the limitation and how you would validate the method on authorized real data.
