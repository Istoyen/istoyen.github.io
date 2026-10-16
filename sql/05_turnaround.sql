-- Median includes completed paid starts only. Calendar days; same-day = 0.
WITH ranked AS (
 SELECT payer,program,days_to_start,
 ROW_NUMBER() OVER(PARTITION BY payer,program ORDER BY days_to_start,case_id) AS rn,
 COUNT(*) OVER(PARTITION BY payer,program) AS n
 FROM case_metrics WHERE status='Started'
), medians AS (
 SELECT payer,program,AVG(days_to_start*1.0) AS median_days
 FROM ranked WHERE rn IN ((n+1)/2,(n+2)/2) GROUP BY payer,program
)
SELECT c.payer,c.program,m.median_days,
 SUM(c.status='Started') AS completed_starts,
 ROUND(100.0*SUM(c.within_14_days)/NULLIF(SUM(c.status='Started'),0),1) AS started_within_14_days_pct,
 SUM(c.status='Pending' AND c.pending_age_days>14) AS pending_over_14_days,
 AVG(c.bridge_days) AS mean_completed_bridge_days,
 SUM(c.bridge_requested_date IS NOT NULL AND c.bridge_dispensed_date IS NULL) AS open_bridge_requests
FROM case_metrics c LEFT JOIN medians m USING(payer,program)
GROUP BY c.payer,c.program ORDER BY c.payer,c.program;
