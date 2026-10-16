-- Intake cohort; snapshot conversion, not an eventual treatment-start probability.
SELECT payer,program, COUNT(*) AS referrals,
 SUM(status='Started') AS started, SUM(status='Pending') AS pending,
 SUM(status='Closed') AS closed,
 ROUND(100.0*SUM(status='Started')/COUNT(*),1) AS snapshot_start_pct,
 SUM(complete_date IS NOT NULL) AS completed_intake,
 SUM(verified_date IS NOT NULL) AS verified,
 SUM(approved_date IS NOT NULL) AS approved
FROM case_metrics GROUP BY payer,program ORDER BY payer,program;
