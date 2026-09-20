(()=>{const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;if(!reduced){document.body.classList.add('motion-ready');const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll('.reveal').forEach(e=>io.observe(e));}let queued=false;function paint(){queued=false;const max=document.documentElement.scrollHeight-innerHeight;document.querySelector('.progress').style.width=(max?scrollY/max*100:0)+'%';if(!reduced)document.querySelector('.hero-image').style.transform='translateY('+Math.min(scrollY,innerHeight)*.12+'px) scale(1.02)'}addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(paint)}},{passive:true});paint()})();
(()=>{
const svg=document.querySelector('#masterplan-camera');if(!svg)return;
const stage=document.querySelector('.masterplan-stage'),connectors=document.querySelector('.masterplan-connectors');
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const units={'r1-78':{x:1466,y:947,name:'Dunes · R1-78',copy:'A four-bedroom C3 villa, with 245 sqm built-up area, a 57 sqm covered terrace and a 660 sqm plot.'},'r5-46':{x:723,y:517,name:'Acacia · R5-46',copy:'A four-bedroom C6 villa, with 246 sqm built-up area, a 59 sqm covered terrace and a 681 sqm plot.'}};
let frame,selected=null;
function layoutCallouts(){
 const [vx,vy,vw,vh]=svg.getAttribute('viewBox').split(/\s+/).map(Number),width=stage.clientWidth,height=stage.clientHeight;
 if(!width||!height)return;
 const stageBox=stage.getBoundingClientRect(),mapBox=svg.getBoundingClientRect(),mapX=mapBox.left-stageBox.left,mapY=mapBox.top-stageBox.top,zoomed=selected!==null;
 const cards=[...stage.querySelectorAll('.masterplan-glass')];
 const bottom=zoomed?Math.ceil(Math.max(...cards.map(c=>c.offsetHeight))+30):0;
 if(stage.style.paddingBottom!==`${bottom}px`)stage.style.paddingBottom=`${bottom}px`;
 connectors.setAttribute('viewBox',`0 0 ${width} ${stage.clientHeight}`);
 Object.entries(units).forEach(([id,u])=>{
  const card=stage.querySelector(`.masterplan-glass[data-masterplan-unit="${id}"]`),line=connectors.querySelector(`[data-connector="${id}"]`),left=id==='r5-46';
  const px=mapX+(u.x-vx)/vw*mapBox.width,py=mapY+(u.y-vy)/vh*mapBox.height,visible=px>=mapX&&px<=mapX+mapBox.width&&py>=mapY&&py<=mapY+mapBox.height;
  const cw=card.offsetWidth,ch=card.offsetHeight;
  const x=zoomed?(left?12:width-cw-12):(left?mapX+mapBox.width*.006:mapX+mapBox.width*.985-cw);
  const y=zoomed?mapBox.height+15:(left?Math.max(6,Math.min(mapBox.height*.075,mapBox.height*.225-ch)):Math.min(mapBox.height*.595,mapBox.height*.78-ch));
  card.style.left=`${x}px`;card.style.top=`${y}px`;card.hidden=false;
  line.style.display=visible&&!zoomed?'':'none';
  if(visible&&!zoomed){const ex=left?x+cw+4:x-5,ey=y+Math.min(ch*.30,32),dx=ex-px,dy=ey-py,len=Math.hypot(dx,dy)||1,inset=19*mapBox.width/vw;line.setAttribute('d',`M${px+dx/len*inset} ${py+dy/len*inset} L${ex} ${ey}`)}
 });
}
function moveCamera(target){cancelAnimationFrame(frame);const start=svg.getAttribute('viewBox').split(/\s+/).map(Number),t0=performance.now();function tick(now){const p=reduced?1:Math.min(1,(now-t0)/1150),e=1-Math.pow(1-p,4);svg.setAttribute('viewBox',target.map((v,i)=>start[i]+(v-start[i])*e).join(' '));layoutCallouts();if(p<1)frame=requestAnimationFrame(tick)}frame=requestAnimationFrame(tick)}
function choose(id){selected=id;stage.classList.toggle("is-zoomed",id!==null);const u=units[id];document.querySelectorAll('[data-masterplan-unit]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.masterplanUnit===id)));if(u){const w=850,h=w*2801/2200;moveCamera([Math.max(0,Math.min(2200-w,u.x-w/2)),Math.max(0,Math.min(2801-h,u.y-h*.44)),w,h]);document.querySelector('#masterplan-selection-title').textContent=u.name;document.querySelector('#masterplan-selection-copy').textContent=u.copy;const a=document.querySelector('#masterplan-unit-link');a.hidden=false;a.href='/'+id;a.textContent='Explore '+id.toUpperCase()+' ↗'}else{moveCamera([0,0,2200,2801]);document.querySelector('#masterplan-selection-title').textContent='Both homes. One perspective.';document.querySelector('#masterplan-selection-copy').textContent='Dunes on the east side. Acacia on the west. Explore how each villa sits within Ramla.';document.querySelector('#masterplan-unit-link').hidden=true}}
// Touch double-tap resets without the second compatibility click zooming in again.
let down=null,lastTap=null,suppressClickUntil=0;
stage.addEventListener('pointerdown',e=>{if(e.pointerType!=='touch')return;if(!e.isPrimary){down=null;lastTap=null;return}down={id:e.pointerId,x:e.clientX,y:e.clientY,t:performance.now()}});
stage.addEventListener('pointercancel',()=>{down=null;lastTap=null});
stage.addEventListener('pointerup',e=>{if(e.pointerType!=='touch'||!down||e.pointerId!==down.id)return;const now=performance.now(),tap=down;down=null;if(now-tap.t>300||Math.hypot(e.clientX-tap.x,e.clientY-tap.y)>20){lastTap=null;return}if(lastTap&&now-lastTap.t<340&&Math.hypot(e.clientX-lastTap.x,e.clientY-lastTap.y)<30){e.preventDefault();lastTap=null;suppressClickUntil=now+500;choose(null)}else lastTap={x:e.clientX,y:e.clientY,t:now}},{passive:false});
stage.addEventListener('click',e=>{if(performance.now()<suppressClickUntil){e.preventDefault();e.stopImmediatePropagation()}},true);
stage.addEventListener('dblclick',e=>{e.preventDefault();lastTap=null;choose(null)});
document.querySelectorAll('[data-masterplan-unit]').forEach(el=>{el.addEventListener('click',()=>{choose(el.dataset.masterplanUnit);if(el.classList.contains('masterplan-choice')&&innerWidth<=900)svg.scrollIntoView({behavior:reduced?'auto':'smooth',block:'center'})});if(el.tagName.toLowerCase()==='g')el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(el.dataset.masterplanUnit)}})});
document.querySelector('#masterplan-reset').addEventListener('click',()=>choose(null));
new ResizeObserver(layoutCallouts).observe(stage);layoutCallouts();
})();
