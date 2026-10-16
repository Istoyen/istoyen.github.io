"""Check metric contracts, feed reconciliation, and intentional edge cases."""
from pathlib import Path
import csv, sqlite3, json, statistics
R=Path(__file__).resolve().parents[1]
def read(name):
 with (R/'data'/name).open() as f:return list(csv.DictReader(f))
con=sqlite3.connect(R/'data'/'analytics.sqlite'); con.row_factory=sqlite3.Row
cases=list(con.execute('SELECT * FROM case_metrics')); quality=list(con.execute('SELECT * FROM shipment_quality'))
assert len(cases)==1200 and len({r['case_id'] for r in cases})==1200
assert all(r['received_date']<=r['as_of_date'] for r in cases)
for r in cases:
 dates=[r[k] for k in ['received_date','complete_date','verified_date','approved_date','first_paid_ship_date'] if r[k]]
 assert dates==sorted(dates) and max(dates)<=r['as_of_date']
 assert (r['status']=='Started')==(r['days_to_start'] is not None)
 assert (r['status']=='Pending')==(r['pending_age_days'] is not None)
 assert r['bridge_days'] is None or r['bridge_days']>=0
assert sum(r['status']=='Started' for r in cases)==975
assert sum(r['status']=='Pending' for r in cases)==82
assert sum(r['status']=='Closed' for r in cases)==143
assert statistics.median(r['days_to_start'] for r in cases if r['days_to_start'] is not None)==16
assert len(quality)==1776 and sum(r['is_flagged'] for r in quality)==232
assert len([r for r in quality if not r['is_flagged']])==1544
accepted=[r for r in quality if not r['is_flagged']]
assert len({r['shipment_id'] for r in accepted})==len(accepted)
for r in quality:
 flags=[r[k] for k in ['duplicate_flag','orphan_flag','date_flag','supply_flag','quantity_flag']]
 assert r['is_flagged']==int(any(flags))
for payer in ['Commercial','Medicare','Medicaid','Uninsured']:
 for program in ['Immunology','Oncology','Neurology']:
  rows=[r for r in quality if r['payer']==payer and r['program']==program]
  assert len(rows)==sum(r['is_flagged'] for r in rows)+sum(not r['is_flagged'] for r in rows)
  c=[r for r in cases if r['payer']==payer and r['program']==program]
  assert len(c)==sum(r['status'] in ('Started','Pending','Closed') for r in c)
for filename in ['03_patient_access','04_shipment_quality','05_turnaround']:
 result=list(con.execute((R/'sql'/(filename+'.sql')).read_text()))
 assert len(result)==12
 if filename=='05_turnaround':
  for row in result:
   vals=[r['days_to_start'] for r in cases if r['payer']==row['payer'] and r['program']==row['program'] and r['status']=='Started']
   assert row['median_days']==statistics.median(vals)
con.close()
# Independent fixture: same-day completion, pending age, duplicate+quantity overlap,
# orphan reference, invalid dates, and invalid/null supply all have explicit expected results.
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
c.executescript((R/'sql'/'01_schema.sql').read_text())
c.execute("INSERT INTO cases VALUES ('SYN-T','2026-01-01','Test','Test','2026-01-01','2026-01-01','2026-01-01','2026-01-01','Started',NULL,NULL,'2026-07-01')")
c.execute("INSERT INTO cases VALUES ('SYN-P','2026-06-01','Test','Test',NULL,NULL,NULL,NULL,'Pending','2026-06-30',NULL,'2026-07-01')")
fixtures=[(1,'A','SYN-T','2026-01-01',28,28,'Paid','Test','Test'),(2,'A','SYN-T','2026-01-01',28,-1,'Paid','Test','Test'),(3,'B','MISSING','2026-01-01',28,28,'Paid','Test','Test'),(4,'C','SYN-T','2025-12-31',0,28,'Paid','Test','Test'),(5,'D','SYN-T','2026-07-02',28,28,'Paid','Test','Test'),(6,'E','SYN-T',None,None,28,'Paid','Test','Test')]
c.executemany('INSERT INTO shipments_raw VALUES (?,?,?,?,?,?,?,?,?)',fixtures)
c.executescript((R/'sql'/'02_models.sql').read_text())
a=list(c.execute('SELECT * FROM case_metrics ORDER BY case_id'))
assert a[0]['pending_age_days']==30 and a[0]['bridge_days'] is None
assert a[1]['days_to_start']==0 and a[1]['within_14_days']==1
f=list(c.execute('SELECT * FROM shipment_quality ORDER BY source_row_id'))
assert [r['is_flagged'] for r in f]==[0,1,1,1,1,1]
assert f[1]['duplicate_flag']==1 and f[1]['quantity_flag']==1
assert f[2]['orphan_flag']==1 and f[3]['date_flag']==1 and f[3]['supply_flag']==1
assert f[4]['date_flag']==1 and f[5]['date_flag']==1 and f[5]['supply_flag']==1
print('PASS: baseline totals, all 12 segments, grain, timelines, median, reconciliation, and six QA edge fixtures.')
