"""Reproducible, fictional healthcare operations data. Python 3.9+, stdlib only."""
from pathlib import Path
import csv, json, random, sqlite3, statistics
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
ROOT = Path(__file__).resolve().parents[1]
(ROOT/'dist'/'assets').mkdir(parents=True, exist_ok=True)
(ROOT/'data').mkdir(parents=True, exist_ok=True)
AS_OF = date(2026, 7, 1)
rng = random.Random(42)
def write_csv(name, rows):
    with (ROOT/'data'/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def iso(d): return d.isoformat() if d else None
cases=[]; shipments=[]
for i in range(1,1201):
    received=date(2026,1,1)+timedelta(days=rng.randrange(181))
    payer=rng.choice(['Commercial','Medicare','Medicaid','Uninsured'])
    program=rng.choice(['Immunology','Oncology','Neurology'])
    complete=received+timedelta(days=rng.choices([0,1,2,3,5,8],[15,22,25,18,13,7])[0])
    verified=complete+timedelta(days=rng.randrange(1,7))
    approved=verified+timedelta(days=rng.randrange(1,12)+(4 if payer=='Medicaid' else 0))
    first=approved+timedelta(days=rng.randrange(1,6))
    closed = rng.random()<0.12
    close_date=received+timedelta(days=rng.randrange(2,10)) if closed else None
    if closed: complete=verified=approved=first=None
    complete=complete if complete and complete<=AS_OF else None
    verified=verified if verified and verified<=AS_OF else None
    approved=approved if approved and approved<=AS_OF else None
    first=first if first and first<=AS_OF else None
    bridge=rng.random()<0.29
    bridge_req=received+timedelta(days=1) if bridge else None
    bridge_disp=bridge_req+timedelta(days=rng.randrange(1,8)) if bridge else None
    if bridge_req and bridge_req>AS_OF: bridge_req=bridge_disp=None
    if bridge_disp and bridge_disp>AS_OF: bridge_disp=None
    status='Started' if first else ('Closed' if close_date and close_date<=AS_OF else 'Pending')
    row=dict(case_id=f'SYN-{i:05}',received_date=iso(received),payer=payer,program=program,
        complete_date=iso(complete),verified_date=iso(verified),approved_date=iso(approved),first_paid_ship_date=iso(first),
        status=status,bridge_requested_date=iso(bridge_req),bridge_dispensed_date=iso(bridge_disp),as_of_date=iso(AS_OF))
    cases.append(row)
    if first:
        for seq in range(rng.randrange(1,4)):
            ship=first+timedelta(days=28*seq)
            if ship>AS_OF: continue
            sid=f'SHP-{len(shipments)+1:05}'
            record=dict(source_row_id=len(shipments)+1,shipment_id=sid,case_id=row['case_id'],ship_date=iso(ship),
                days_supply=28,quantity=28,shipment_type='Paid',payer=payer,program=program)
            n=rng.random()
            if n<.025: record['case_id']='SYN-UNKNOWN'
            elif n<.05: record['ship_date']=iso(received-timedelta(days=1))
            elif n<.075: record['days_supply']=0
            elif n<.10: record['quantity']=-1
            shipments.append(record)
            if rng.random()<.035:
                dup=dict(record); dup['source_row_id']=len(shipments)+1; shipments.append(dup)
write_csv('cases.csv',cases); write_csv('shipments_raw.csv',shipments)
con=sqlite3.connect(ROOT/'data'/'analytics.sqlite')
con.executescript((ROOT/'sql'/'01_schema.sql').read_text())
for table, rows in [('cases',cases),('shipments_raw',shipments)]:
    cols=list(rows[0]); con.executemany(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})", [[r[c] for c in cols] for r in rows])
con.executescript((ROOT/'sql'/'02_models.sql').read_text())
con.row_factory=sqlite3.Row
facts=[dict(x) for x in con.execute('SELECT * FROM case_metrics')]
quality=[dict(x) for x in con.execute('SELECT * FROM shipment_quality')]
write_csv('case_metrics.csv',facts); write_csv('shipment_quality.csv',quality)
for name in ['03_patient_access','04_shipment_quality','05_turnaround']:
    rows=[dict(x) for x in con.execute((ROOT/'sql'/(name+'.sql')).read_text())]
    write_csv(name[3:]+'_summary.csv',rows)
started=[x for x in facts if x['status']=='Started']; tt=[x['days_to_start'] for x in started]
summary=dict(as_of=str(AS_OF),cases=len(cases),started=len(started),conversion=float((Decimal(len(started))*100/Decimal(len(cases))).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)),
    pending=sum(x['status']=='Pending' for x in facts),median_days=statistics.median(tt),
    raw_shipments=len(quality),flagged_rows=sum(x['is_flagged'] for x in quality),
    clean_shipments=sum(x['is_flagged']==0 for x in quality))
(ROOT/'data'/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(ROOT/'dist'/'assets'/'data.js').write_text('window.PORTFOLIO_DATA = '+json.dumps(dict(summary=summary,cases=facts,quality=quality),separators=(',',':'))+';\n')
con.commit(); con.close(); print(json.dumps(summary,indent=2))
