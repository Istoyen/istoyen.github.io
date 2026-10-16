// Create a blank query named Cases; requires ImportCsv and RootPath.
let
    Source = ImportCsv("case_metrics.csv"),
    Typed = Table.TransformColumnTypes(Source, {
        {"case_id", type text}, {"payer", type text}, {"program", type text}, {"status", type text},
        {"received_date", type date}, {"complete_date", type date}, {"verified_date", type date},
        {"approved_date", type date}, {"first_paid_ship_date", type date}, {"as_of_date", type date},
        {"bridge_requested_date", type date}, {"bridge_dispensed_date", type date},
        {"days_to_start", Int64.Type}, {"intake_days", Int64.Type}, {"verification_days", Int64.Type},
        {"approval_days", Int64.Type}, {"fulfillment_days", Int64.Type}, {"bridge_days", Int64.Type},
        {"pending_age_days", Int64.Type}, {"within_14_days", Int64.Type}
    }, "en-US")
in Typed
