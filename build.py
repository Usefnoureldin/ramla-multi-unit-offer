from pathlib import Path
from PIL import Image,ImageOps
from pypdf import PdfReader
import re,json,shutil
root=Path(__file__).parent;d=root/'dist';r5=d/'r5-46';r1=d/'r1-78';base='https://ramla-multi-unit-offer.vercel.app'
# Keep each unit self-contained, including its original brochure and page archive.
for name in ['beach.jpg','logo.png']:
 shutil.copy(r1/'assets'/name,r5/'assets'/name)
# Use the source coastal location map shared by both brochures; all R5 original pages remain available.
shutil.copy(r1/'assets/page-02.jpg',r5/'assets/coast-map.jpg')
for name in ['exterior','living','bedroom']:
 im=Image.open(r5/f'assets/{name}.jpg');w,h=im.size
 if name=='exterior': im=im.crop((0,int(h*.095),w,int(h*.91)))
 im.save(r5/f'assets/{name}.jpg',quality=93)
ImageOps.fit(Image.open(r5/'assets/exterior.jpg'),(1200,630)).save(r5/'assets/whatsapp-preview.jpg',quality=92)
# The room coordinates follow the source C6 drawing, normalized to the UI SVG canvas.
roomdata=[('Living & dining','9.5 × 5.3 m',[226,783,538,285]),('Covered terrace','59 sqm',[180,507,580,243]),('Master bedroom','4.7 × 3.5 m',[797,556,261,196]),('Bedroom 2','4.4 × 3.5 m',[1028,785,200,183]),('Bedroom 3','4.2 × 3.5 m',[1038,1251,222,189]),('Bedroom 4','3.8 × 3.5 m',[800,1251,201,189]),('Kitchen','3.1 × 4.1 m',[359,1101,170,219]),('Master bathroom','2.8 × 3.5 m',[1076,585,162,171]),('Dressing room','1.6 × 2.7 m',[863,785,96,143]),('Bathroom 2','2.9 × 1.5 m',[1108,997,157,72]),('Bathroom 3','2.2 × 2.3 m',[1148,1104,115,121]),('Bathroom 4','1.8 × 2.2 m',[797,1105,110,119]),('Guest bathroom','2.8 × 1.5 m',[549,1101,71,151]),('Nanny’s room','2.1 × 2.1 m',[230,1216,108,103]),('Nanny’s bathroom','2.0 × 1.1 m',[231,1140,104,49]),('Driver’s bedroom','2.2 × 2.0 m',[73,1441,124,107]),('Driver’s bathroom','2.2 × 1.0 m',[73,1566,124,40]),('Utility','1.5 × 0.9 m',[876,950,80,39]),('Staff area','As shown on plan',[70,1100,90,238])]
rooms=[[name,size,'Explore this space in the original C6 villa layout.', [round(v*1287/1460) for v in box]] for name,size,box in roomdata]
(r5/'rooms.json').write_text(json.dumps(rooms));p=PdfReader(r5/'assets/Ramla-R5-46-Offer.pdf')
plans={}
for key,pages,title,sub,cheques in [('seven',[19,20],'7 years','5% down + 5% after 3 months',[29,13]),('front',[22,23],'8 years · frontloaded','5% down + 5% after 3 months',[32,13]),('bullet',[25,26],'8 years · bullet','10% down + bullet at installment 14',[32,4])]:
 rows=[]
 for page in pages:
  for line in p.pages[page].extract_text().splitlines():
   m=re.match(r'(Down Payment|Installment No\. \d+) (\d{2}-\w{3}-\d{4}) ([\d,]+) ([\d.]+%) ([\d.]+%) (?:([\d,]+) )?([\d,]+) EGP',line)
   if m:
    v=list(m.groups());rows.append([v[0],v[1],int(v[2].replace(',','')),v[3],v[4],int((v[5] or '0').replace(',','')),int(v[6].replace(',',''))])
 assert len(rows)==cheques[0] and sum(x[2] for x in rows)==87240000 and sum(x[5] for x in rows)==7851600
 assert all(x[2]+x[5]==x[6] for x in rows)
 plans[key]={'title':title,'subtitle':sub,'price':87240000,'maintenance':7851600,'total':95091600,'cheques':cheques,'rows':rows}
(r5/'payments.json').write_text(json.dumps(plans))
html=(r1/'index.html').read_text()
for old,new in [('R1-78','R5-46'),('r1-78','r5-46'),('DUNES','ACACIA'),('Dunes','Acacia'),('C3','C6'),('245','246'),('660','681'),('57','59'),('three payment','four payment'),('Three payment','Four payment'),('three payment','four payment'),('22 original','34 original'),('Parcel R1','Acacia')]:html=html.replace(old,new)
# Link each original-image button to the correct page in the new brochure.
page_map={2:3,3:6,5:11,18:30,19:31,20:33}
for old,new in page_map.items():html=html.replace(f'assets/page-{old:02}.jpg',f'assets/remap-{new:02}.jpg')
html=html.replace('assets/remap-','assets/page-')
html=html.replace('<image href="assets/page-03.jpg" width="1800" height="1147"/>','<image href="assets/coast-map.jpg" width="1800" height="1147"/>')
html=html.replace('viewBox="695 0 1105 1147"','viewBox="200 0 700 1147"').replace('1090,405 1121,422 1093,469 1064,452','578,419 607,429 595,460 569,451')
html=html.replace('1555','1494').replace('Ramla-R5-46-Offer.pdf','Ramla-R5-46-Offer.pdf')
html=html.replace('Ramla-r5-46-offer','Ramla-r5-46-offer')
html=html.replace('https://ramla-r5-46-offer.vercel.app/',base+'/r5-46/')
html=html.replace('with a portfolio including Mall of Arabia, Mall of Tanta, Town Center, D5M, Mall of Mansoura, Aeon towers and District Five residences and offices.','with a portfolio including District 5, AEON, Crescent Walk, Mall of Arabia, Mall of Tanta, Town Center, D5M and Mall of Mansoura.')
html=html.replace('Your place at Acacia.','Your place at Acacia.')
html=html.replace('A four-bedroom villa at Ramla Acacia.','A four-bedroom villa in Ramla’s Acacia neighborhood, on the west side of the project.')
names=['Acacia · R5-46','The soul of Ramla','North Coast location','Real-life Ramla','Beachside life','Vision & destinations','Ramla aerial','Adrère Amellal partnership','The Ramla Nature Lodge','The neighborhoods','Full masterplan','Acacia masterplan','R5-46 location & specifications','Villa C6 exterior','C6 floor plan & dimensions','Living & dining','Bedroom','Payment plans','7-year option','7-year schedule I','7-year schedule II','8-year frontloaded option','Frontloaded schedule I','Frontloaded schedule II','8-year bullet option','Bullet schedule I','Bullet schedule II','Cash offer','Finishing specifications','Interior inspiration','Finishing schedule','More interiors','About Marakez & partners','Your contact']
archive=''.join(f'<button class="page" data-image="assets/page-{i:02}.jpg" data-caption="{n} · Page {i} of 34"><img loading="lazy" src="assets/page-{i:02}.jpg" alt="{n}"><span>{i:02} / {n}</span></button>' for i,n in enumerate(names,1))
html=re.sub(r'<div class="pages">.*?</div><details class="disclaimers">','<div class="pages">'+archive+'</div><details class="disclaimers">',html,flags=re.S)
tabs='<div class="payment-tabs" role="tablist" aria-label="Payment options">'+''.join(f'<button id="tab-{key}" role="tab" aria-controls="payment-panel" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}" data-plan="{key}"><span>OPTION 0{i+1}</span><strong>{title}</strong><small>{sub}</small></button>' for i,(key,title,sub) in enumerate([('seven','7 years','5% + 5% · Quarterly'),('front','8 years','Frontloaded · 5% + 5%'),('bullet','8 years','10% DP · Bullet at #14'),('cash','Cash','Cash price & discount')]))+'</div>'
html=re.sub(r'<div class="payment-tabs".*?</div><div class="payment-panel"',tabs+'<div class="payment-panel"',html,flags=re.S)
html=html.replace('aria-labelledby="tab-quarterly"','aria-labelledby="tab-seven"').replace('85,703,000','87,240,000').replace('UNIT PRICE / QUARTERLY PLAN','UNIT PRICE / 7-YEAR PLAN')
html=html.replace('<head>','<head><base href="/r5-46/">')
html=re.sub(r'<section class="section archive">.*?</section>', '', html, flags=re.S)
(r5/'index.html').write_text(html)
js=(r1/'app.js').read_text()
for old,new in [('R1-78','R5-46'),('Dunes','Acacia'),('DUNES','ACACIA'),('245','246'),('660','681'),('C3','C6'),('1555','1494'),('[695,0,1105,1147]','[200,0,700,1147]'),('[951,297,300,300]','[440,290,300,300]')]:js=js.replace(old,new)
start=js.index('const money=');end=js.index('async function loadData()',start)
js=js[:start]+'''const money=n=>new Intl.NumberFormat('en-US').format(n);let payments={};
function showPlan(key){$$('[data-plan]').forEach(b=>{const yes=b.dataset.plan===key;b.setAttribute('aria-selected',String(yes));b.tabIndex=yes?0:-1});$('#payment-panel').setAttribute('aria-labelledby',`tab-${key}`);const p=payments[key];$('#price-label').textContent=key==='cash'?'CASH PRICE':`UNIT PRICE / ${p.title.toUpperCase()}`;$('#price').innerHTML=`${money(key==='cash'?55650396:p.price)}<small> EGP</small>`;
if(key==='cash'){$('#price-details').innerHTML='<div><span>Cash discount</span><b>31,589,604 EGP</b><small>As stated in the original cash offer</small></div>';$('#payment-schedule').innerHTML='<p class="fine">The cash page states the cash price and discount. It does not specify a cash maintenance payment schedule.</p><button class="text-button" id="original-cash">View original cash offer ↗</button>';$('#original-cash').onclick=()=>openImage('assets/page-28.jpg','R5-46 · Original cash offer');}
else{$('#price-details').innerHTML=`<div><span>Down payment</span><b>${money(p.rows[0][2])}</b><small>16 September 2026 · EGP</small></div><div><span>Maintenance</span><b>${money(p.maintenance)}</b><small>EGP · ${p.cheques[1]} maintenance cheques</small></div><div><span>Total including maintenance</span><b>${money(p.total)}</b><small>EGP · ${p.cheques[0]+p.cheques[1]} cheques in total</small></div>`;const note=key==='bullet'?'<p class="source-note"><b>A date detail to confirm.</b> The brochure labels this an “8 years” plan and its payment term “Yearly,” but lists quarterly dates, a jump from December 2029 to December 2039, and payments through December 2044. The schedule below preserves the dates exactly as issued. Confirm the intended dates with the sales team.</p>':'';$('#payment-schedule').innerHTML=note+`<details class="schedule"><summary>Explore the full ${p.title} payment schedule <span>+</span></summary><div class="schedule-scroll" tabindex="0" aria-label="Payment table. Scroll horizontally for all columns."><table><thead><tr>${['Installment','Due date','Unit (EGP)','Percentage','Cumulative','Maintenance','Total due (EGP)'].map(x=>`<th scope="col">${x}</th>`).join('')}</tr></thead><tbody>${p.rows.map(r=>`<tr>${r.map(v=>`<td>${typeof v==='number'?(v===0?'—':money(v)):v}</td>`).join('')}</tr>`).join('')}</tbody></table></div><p class="fine">${p.cheques[0]} unit cheques + ${p.cheques[1]} maintenance cheques = ${p.cheques[0]+p.cheques[1]} cheques. Amounts, percentages and dates reproduced as issued in the brochure. Scroll sideways to see every column.</p></details>`;}animateContent($('#payment-panel'));}
$$('[data-plan]').forEach((b,i)=>{b.onclick=()=>showPlan(b.dataset.plan);b.onkeydown=e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const j=e.key==='Home'?0:e.key==='End'?3:(i+(e.key==='ArrowRight'?1:3))%4;const next=$$('[data-plan]')[j];next.focus();showPlan(next.dataset.plan)}}});
'''+js[end:]
js=js.replace("showPlan('quarterly')","showPlan('seven')")
(r5/'app.js').write_text(js)
css=(r1/'style.css').read_text().replace('1287/1555','1287/1494')+'\n.payment-tabs{grid-template-columns:repeat(4,1fr)}.payment-tabs strong{font-size:32px}.source-note{font-size:13px;line-height:1.7;padding:22px;background:#fff3cc;border-left:3px solid #bf8834}.source-note b{display:block;margin-bottom:8px}@media(max-width:640px){.payment-tabs{grid-template-columns:repeat(2,1fr)}.payment-tabs strong{font-size:29px}}\n'
(r5/'style.css').write_text(css)
# Persistent navigation keeps both offers one click apart.
for slug,label,other,otherlabel in [('r1-78','Dunes · R1-78','r5-46','Acacia · R5-46'),('r5-46','Acacia · R5-46','r1-78','Dunes · R1-78')]:
 f=d/slug/'index.html';s=f.read_text()
 if '<base' not in s:s=s.replace('<head>',f'<head><base href="/{slug}/">')
 s=s.replace('https://ramla-r1-78-offer.vercel.app/',base+'/r1-78/')
 bar=f'<div class="unit-switcher"><a href="/">← Multi unit offer</a><span>{label}</span><a href="/{other}">View {otherlabel} ↗</a></div>'
 s=s.replace('<main>',bar+'<main>');s=s.replace('<title>','<title>Multi Unit Offer · ')
 f.write_text(s)
 with (d/slug/'style.css').open('a') as out:out.write('\n.unit-switcher{position:sticky;top:0;z-index:35;display:flex;justify-content:space-between;gap:15px;padding:13px 4vw;background:#f7f3ebf2;backdrop-filter:blur(14px);font-size:11px;border-bottom:1px solid var(--line)}header{top:42px}.unit-switcher a{font-weight:600}@media(max-width:640px){.unit-switcher{font-size:9px;padding:13px 15px}.unit-switcher>span{display:none}header{top:40px}}\n')
print('Validated all 93 R5-46 installment rows and maintenance totals. Both unit experiences generated.')
