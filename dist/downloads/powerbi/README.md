# Build the Power BI report

**Included:** refreshable CSV inputs, complete Power Query imports, DAX table/measure definitions, theme, page specification, and expected checks. **Not included:** a compiled PBIX/PBIT or a verified Desktop execution. Build and validate this report in Power BI Desktop; the website's dashboard is a separate working browser implementation.

## 1. Import
1. Run the Python pipeline or use the included `data/` outputs.
2. In a new Power BI Desktop report, open Transform data. Create a text parameter named `RootPath` pointing to your extracted `data/` folder, with a trailing separator (example `C:\Portfolio\data\`).
3. Create a blank query named `ImportCsv` and paste `ImportCsv.pq` in its Advanced Editor.
4. Create blank queries named **Cases** and **ShipmentQuality**, pasting the matching `.pq` files. Ensure their final queries are enabled for load. The helper function itself is not a fact table.
5. Check dates, whole-number flags and blank dates before Close & Apply. These queries consume modeled extracts; Python/SQL performs the upstream QA.

## 2. Model
Create the six calculated tables from `tables.dax`, one definition at a time. Create four active one-to-many relationships with **single-direction** filtering:

| One side | Many side |
|---|---|
| DimPayer[payer] | Cases[payer] |
| DimPayer[payer] | ShipmentQuality[payer] |
| DimProgram[program] | Cases[program] |
| DimProgram[program] | ShipmentQuality[program] |

Do not relate Cases directly to ShipmentQuality: preserving orphan feed rows and avoiding fact fan-out are intentional. Delete auto-detected fact-to-fact relationships if created. AccessStage, QualityReason, ProcessStage and AgeBand are disconnected selector tables used by SWITCH measures. Sort each display column by its Order column.

No date dimension is necessary for the supplied fixed-cohort report. If adding time trends later, use separate role-playing intake and shipment date dimensions; explicitly label which date drives each visual. Do not silently mix intake cohort filtering with shipment activity filtering.

## 3. Measures and style
Create each measure in `measures.dax` separately, attached to Cases or ShipmentQuality as appropriate. Format rates as percentages (DAX returns fractions), durations to one decimal, counts as whole numbers. Import `theme.json` with View → Themes → Browse for themes. Use a 16:9 canvas, light paper background, teal charts, and clear text contrast.

## 4. Three report pages
On **every page**, add synced slicers for `DimPayer[payer]` and `DimProgram[program]`. Keep a visible banner: “Synthetic portfolio data · Jan–Jun 2026 intake · As of 01 Jul 2026.” Do not add page-level status filters to the overview; they change metric denominators.

### Patient access
- Four cards: Referrals, Snapshot Start Rate, Pending Cases, Closed Cases.
- Horizontal bar: AccessStage[Stage] by Stage Cases; sort by Order.
- Bar: DimPayer[payer] by Snapshot Start Rate.
- Detail table: Cases case_id, payer, program, received_date, status, first_paid_ship_date.
- Tooltip: numerator, denominator, and reminder about unequal follow-up.
- Disable cross-filtering from the stage chart into other visuals; it represents overlapping milestones.

### Shipment quality
- Cards: Raw Shipment Rows, Flagged Rows, Flagged Rate, Accepted Shipments.
- Horizontal bar: QualityReason[Reason] by Exception Count.
- Card: Reconciliation Difference, expected 0 under every payer/program filter.
- Detail table: shipment_id, source_row_id, case_id, flags. Add is_flagged as a table-level filter only if making an exception-only queue.
- Note that reason counts overlap; avoid pie charts for these counts. Disable exception-chart filtering of overview cards.

### Turnaround
- Cards: Median Paid Start Days, P90 Paid Start Days, Pending Over 14 Days, Median Bridge Days.
- Horizontal bar: ProcessStage[Stage] by Mean Stage Days.
- Horizontal bar: AgeBand[Band] by Pending Age Count.
- Small cards: Completed Within 14 Days Rate and Open Bridge Requests.
- Detail table: case_id, status, days_to_start, pending_age_days, bridge_days.
- Completed-case calculations exclude pending cases. The 14-day threshold is an example, not a healthcare standard.

## 5. Acceptance checks
With all slicers cleared: Referrals 1,200; Paid Starts 975; rate 0.8125 before display rounding; Pending 82; Closed 143; Median Paid Start Days 16; Raw Shipment Rows 1,776; Flagged Rows 232; Accepted 1,544; Reconciliation Difference 0. Use `data/turnaround_summary.csv` for grouped median and bridge mean comparisons (the report's bridge card is a median, not that CSV's mean).

For each of the 12 payer/program combinations, reconcile against CSV summary files and browser dashboard. Blanks must remain blank rather than zero. Ensure selecting a payer filters both facts while orphan source rows remain included. Check the percentage formatting and P90 interpolation. Validate export totals before presenting the report as complete.

## 6. Refresh and publish
Rerun Python, refresh Desktop, and validate before saving PBIX. A service refresh of a local file source needs a supported gateway or a suitable hosted data source; configure that in your environment. Review sharing access explicitly. Do not use public embedding for any future confidential dataset. Add a published report link to the portfolio only after it actually exists and works for the intended audience.

Official references:
- Relationships: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-create-and-manage-relationships
- Star schema: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema
- PERCENTILEX.INC: https://learn.microsoft.com/en-us/dax/percentilex-inc-function-dax
