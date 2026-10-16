-- Executable dialect: SQLite 3.25+. All records are synthetic.
DROP VIEW IF EXISTS shipment_quality;
DROP VIEW IF EXISTS case_metrics;
DROP TABLE IF EXISTS shipments_raw;
DROP TABLE IF EXISTS cases;
CREATE TABLE cases (
 case_id TEXT PRIMARY KEY, received_date TEXT NOT NULL, payer TEXT NOT NULL,
 program TEXT NOT NULL, complete_date TEXT, verified_date TEXT, approved_date TEXT,
 first_paid_ship_date TEXT, status TEXT NOT NULL CHECK(status IN ('Started','Pending','Closed')),
 bridge_requested_date TEXT, bridge_dispensed_date TEXT, as_of_date TEXT NOT NULL
);
-- Raw feed intentionally allows invalid business keys and values for QA demonstrations.
CREATE TABLE shipments_raw (
 source_row_id INTEGER PRIMARY KEY, shipment_id TEXT, case_id TEXT, ship_date TEXT,
 days_supply INTEGER, quantity INTEGER, shipment_type TEXT, payer TEXT, program TEXT
);
