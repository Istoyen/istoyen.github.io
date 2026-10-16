// Create a blank query named ShipmentQuality; requires ImportCsv and RootPath.
let
    Source = ImportCsv("shipment_quality.csv"),
    Typed = Table.TransformColumnTypes(Source, {
        {"source_row_id", Int64.Type}, {"shipment_id", type text}, {"case_id", type text},
        {"ship_date", type date}, {"days_supply", Int64.Type}, {"quantity", Int64.Type},
        {"shipment_type", type text}, {"payer", type text}, {"program", type text},
        {"duplicate_rank", Int64.Type}, {"duplicate_flag", Int64.Type}, {"orphan_flag", Int64.Type},
        {"date_flag", Int64.Type}, {"supply_flag", Int64.Type}, {"quantity_flag", Int64.Type},
        {"is_flagged", Int64.Type}
    }, "en-US")
in Typed
