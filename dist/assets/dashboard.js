'use strict';
const all = window.PORTFOLIO_DATA;
const el = id => document.getElementById(id);
let view = 'access', downloadUrl;
const fmt = x => x == null || !Number.isFinite(x) ? '—' : x.toLocaleString('en-US',{maximumFractionDigits:1});
const pct = (n,d) => d ? 100*n/d : null;
const quantile = (arr,p) => {if(!arr.length)return null;const a=[...arr].sort((x,y)=>x-y),i=(a.length-1)*p,l=Math.floor(i);return a[l]+(a[Math.ceil(i)]-a[l])*(i-l)};
const avg = arr => arr.length ? arr.reduce((s,x)=>s+x,0)/arr.length : null;
const metric = (value,label) => `<div class="metric"><strong>${value}</strong><span>${label}</span></div>`;
function bars(title,rows,max){return `<div><div class="chart-title">${title}</div>${rows.map(([label,val])=>`<div class="bar-row"><span>${label}</span><div class="bar-track"><div class="bar-fill" style="width:${Math.max(0,Math.min(100,100*(val||0)/(max||1)))}%"></div></div><span class="bar-val">${fmt(val)}</span></div>`).join('')}</div>`}
function render(){
 const payer=el('payer').value,program=el('program').value;
 const matches=r=>(payer==='All'||r.payer===payer)&&(program==='All'||r.program===program);
 const cases=all.cases.filter(matches),quality=all.quality.filter(matches),started=cases.filter(r=>r.status==='Started'),pending=cases.filter(r=>r.status==='Pending');
 let metrics='',charts='',note='',rows=[],keys=[];
 if(view==='access'){
  metrics=metric(fmt(cases.length),'Referral cases')+metric(fmt(pct(started.length,cases.length))+'%','Snapshot paid-start rate')+metric(fmt(pending.length),'Pending cases')+metric(fmt(cases.filter(r=>r.status==='Closed').length),'Closed cases');
  const stages=[['Received',cases.length],['Intake complete',cases.filter(r=>r.complete_date).length],['Verified',cases.filter(r=>r.verified_date).length],['Approved',cases.filter(r=>r.approved_date).length],['Paid start',started.length]];
  const payers=['Commercial','Medicare','Medicaid','Uninsured'].map(p=>[p,pct(started.filter(r=>r.payer===p).length,cases.filter(r=>r.payer===p).length)]);
  charts=bars('Stage reached · case count',stages,cases.length)+bars('Snapshot paid-start rate · %',payers,100);
  note='Denominator: every referral in the selected intake cohort. Recent referrals have less follow-up. A paid start is not the same as a bridge dispense. Closed cases in this simplified generator have no completed milestones.';
  rows=cases;keys=['case_id','payer','program','status','received_date','first_paid_ship_date'];
 }else if(view==='quality'){
  const flagged=quality.filter(r=>r.is_flagged),clean=quality.length-flagged.length;
  metrics=metric(fmt(quality.length),'Raw source rows')+metric(fmt(flagged.length),'Flagged rows')+metric(fmt(pct(flagged.length,quality.length))+'%','Rows with ≥1 defect')+metric(fmt(clean),'Accepted shipments');
  const reasons=[['Duplicates','duplicate_flag'],['Orphan cases','orphan_flag'],['Invalid dates','date_flag'],['Days supply','supply_flag'],['Quantity','quantity_flag']].map(([s,k])=>[s,quality.reduce((n,r)=>n+r[k],0)]);
  charts=bars('Exception reasons · overlapping counts',reasons,Math.max(...reasons.map(r=>r[1]),1))+bars('Release reconciliation · row count',[['Raw feed',quality.length],['Quarantined',flagged.length],['Accepted',clean]],quality.length);
  note='Raw rows = accepted + quarantined. One row may fail multiple rules, so reason counts must not be added to calculate flagged rows. Filters use source-feed payer and program, including orphan records.';
  rows=quality;keys=['source_row_id','shipment_id','case_id','duplicate_flag','orphan_flag','date_flag','supply_flag','quantity_flag','is_flagged'];
 }else{
  const durations=started.map(r=>r.days_to_start),bridge=cases.filter(r=>r.bridge_days!=null);
  metrics=metric(fmt(quantile(durations,.5)),'Median paid-start days')+metric(fmt(quantile(durations,.9)),'P90 paid-start days')+metric(fmt(pending.filter(r=>r.pending_age_days>14).length),'Pending cases >14 days')+metric(fmt(quantile(bridge.map(r=>r.bridge_days),.5)),'Median completed bridge days');
  const stages=[['Intake','intake_days'],['Verification','verification_days'],['Approval','approval_days'],['Fulfillment','fulfillment_days']].map(([s,k])=>[s,avg(started.map(r=>r[k]))]);
  const ages=[['0–7 days',pending.filter(r=>r.pending_age_days<=7).length],['8–14 days',pending.filter(r=>r.pending_age_days>7&&r.pending_age_days<=14).length],['15–30 days',pending.filter(r=>r.pending_age_days>14&&r.pending_age_days<=30).length],['31+ days',pending.filter(r=>r.pending_age_days>30).length]];
  charts=bars('Mean stage days · completed paid starts',stages,Math.max(...stages.map(r=>r[1]||0),1))+bars('Pending case age · case count',ages,Math.max(...ages.map(r=>r[1]),1));
  note=`Calendar days; same-day = 0. Paid-start metrics cover ${started.length} completed cases; bridge median covers ${bridge.length} completed requests. ${cases.filter(r=>r.bridge_requested_date&&!r.bridge_dispensed_date).length} bridge requests remain open. The 14-day review threshold is illustrative. P90 uses linear interpolation. Stage means use the same completed cohort.`;
  rows=cases;keys=['case_id','status','days_to_start','pending_age_days','bridge_days','intake_days','verification_days','approval_days'];
 }
 el('dash-content').innerHTML=`<div class="metrics">${metrics}</div><div class="chart-grid">${charts}</div><p class="dash-note">${note}</p>`;
 el('records').innerHTML=`<table><caption>Selected ${view==='quality'?'shipment':'case'} records · ${rows.length} rows (first 10 shown)</caption><thead><tr>${keys.map(k=>`<th scope="col">${k.replaceAll('_',' ')}</th>`).join('')}</tr></thead><tbody>${rows.slice(0,10).map(r=>`<tr>${keys.map(k=>`<td>${r[k]??'—'}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
 if(downloadUrl)URL.revokeObjectURL(downloadUrl);
 const cell=v=>`"${String(v??'').replaceAll('"','""')}"`;
 downloadUrl=URL.createObjectURL(new Blob([keys.join(',')+'\n'+rows.map(r=>keys.map(k=>cell(r[k])).join(',')).join('\n')],{type:'text/csv'}));el('export').href=downloadUrl;
 el('export').download=`synthetic-${view}-${payer}-${program}.csv`;
}
for(const id of ['payer','program'])el(id).addEventListener('change',render);
for(const button of document.querySelectorAll('[data-view]'))button.addEventListener('click',()=>{view=button.dataset.view;document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));render()});
render();
