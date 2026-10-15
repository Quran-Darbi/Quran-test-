// يكشف أسئلة المستوى المتوسط الغامضة: سؤال يقبل نصُّه أكثر من تكملة صحيحة في المصحف، فيُحسب خطأً من يجيب بتكملة صحيحة أخرى.
// تنبيه فقط (لا يُفشل الفحص). يُستثنى السؤال الموسوم بـ "tag":"mutashabih" (متشابهة مقصودة) أو "ambiguityOk":true.
// الطريقة: يُحوَّل نص السؤال إلى نمط (كلمات ثابتة + فراغات) ويُبحث عنه في آيات المصحف كلها.
//   - فراغ واحد: طوله = عدد كلمات الإجابة. فراغات متعددة: كل فراغ كلمة (ويجب أن يساوي عددها كلمات الإجابة).
//   - إن لم يطابق النمطُ الآيةَ الأصلية نفسها فالسؤال غير قابل للفحص (نصّه غير متصل) ويُتجاهل بدل أن يُحسب غامضاً.
// الاستعمال المستقل:  node tools/check_ambiguity.js [--report ملف.txt] [--scope page|quran]
const fs=require('fs'),path=require('path');
const {ROOT,readJSON,pages}=require('./lib.js');const {norm}=require('./quran_ref.js');

function mkIdx(verses){const idx=new Map();verses.forEach((v,vi)=>v.w.forEach((x,p)=>{let a=idx.get(x);if(!a)idx.set(x,a=[]);a.push([vi,p]);}));return {verses,idx};}
function loadVerses(){
  const rows=fs.readFileSync(path.join(ROOT,'Scripts','quran-uthmani.txt'),'utf8').split('\n').filter(Boolean).map(l=>l.split('|'));
  const verses=rows.map(r=>({ref:r[0]+':'+r[1],w:norm(r.slice(2).join('|')).split(' ').filter(Boolean)}));
  return mkIdx(verses);
}
const clean=s=>s.replace(/[«»]/g,'').replace(/^\s*(أكملِ الفراغ|أكمل)\s*:/,'').trim();
// يرجع {status:'skip'|'unverifiable'|'ok', fills:[{fill,ref}]}
function analyse(q,C){
  const toks=norm(clean(q.q)).split(' ').filter(Boolean),ans=norm(q.answer).split(' ').filter(Boolean);
  const nb=toks.filter(t=>t==='___').length;
  if(!nb||!ans.length)return {status:'skip'};
  if(nb!==1&&nb!==ans.length)return {status:'skip'};
  const pat=[];toks.forEach(t=>{if(t==='___'){for(let i=0;i<(nb===1?ans.length:1);i++)pat.push(null);}else pat.push(t);});
  const L=pat.length,k=pat.findIndex(x=>x!==null);
  if(k<0)return {status:'ok',fills:[{fill:'*',ref:'*'}],blankOnly:true};
  const found=new Map();let selfMatch=false;
  for(const [vi,p] of C.idx.get(pat[k])||[]){
    const s=p-k,w=C.verses[vi].w;if(s<0||s+L>w.length)continue;
    let ok=true;for(let j=0;j<L;j++)if(pat[j]!==null&&pat[j]!==w[s+j]){ok=false;break;}
    if(!ok)continue;
    const fill=pat.map((x,j)=>x===null?w[s+j]:null).filter(x=>x!==null).join(' ');
    if(fill===ans.join(' '))selfMatch=true;
    if(!found.has(fill))found.set(fill,C.verses[vi].ref);}
  if(!selfMatch)return {status:'unverifiable'};
  return {status:'ok',self:ans.join(' '),fills:[...found].map(([fill,ref])=>({fill,ref}))};
}
// يرجع قائمة الأسئلة الغامضة مرتبة من الأسوأ
// النطاق الافتراضي: آيات الصفحة نفسها (المستخدم يعرف الصفحة التي يختبرها)؛ scope:'quran' يفحص المصحف كله.
function findAmbiguous(opt){
  const scope=(opt&&opt.scope)||'page';const Q=scope==='quran'?loadVerses():null,out=[],stat={checked:0,skipped:0,unverifiable:0,exempt:0};
  for(const {stem,file} of pages()){
    const d=(readJSON(file).data)||{};
    const C=Q||mkIdx((d.AYAT||[]).map((a,i)=>({ref:stem+'#'+(i+1),w:norm(a).split(' ').filter(Boolean)})));
    (d.MEDIUM_Q||[]).forEach((q,i)=>{
      if(!q||typeof q.q!=='string'||typeof q.answer!=='string'||!q.q.includes('___'))return;
      if(q.tag==='mutashabih'||q.ambiguityOk===true){stat.exempt++;return;}
      const r=analyse(q,C);
      if(r.status==='skip'){stat.skipped++;return;}
      if(r.status==='unverifiable'){stat.unverifiable++;return;}
      stat.checked++;
      if(r.fills.length>1)out.push({stem,index:i,q:q.q,answer:q.answer,count:r.fills.length,alts:r.fills.filter(f=>f.fill!==r.self).slice(0,3).map(f=>f.ref)});});
  }
  out.sort((a,b)=>b.count-a.count);return {out,stat};
}
const kind=n=>n>=20?'سياق غير كافٍ — يلزم توسيعه':n>=4?'سياق ضعيف — يُفضَّل توسيعه':'غالباً متشابهة — إمّا وسمها mutashabih أو توسيع السياق';
function checkAmbiguity(W){const {out}=findAmbiguous();
  out.forEach(x=>W(x.stem,'[غموض] MEDIUM_Q['+x.index+'] «'+clean(x.q)+'» له '+x.count+' تكملات صحيحة في الصفحة نفسها ('+(x.alts.length?'مثلاً '+x.alts.join('، '):'')+')'));
  return out.length;}
module.exports={checkAmbiguity,findAmbiguous,analyse};
if(require.main===module){
  const scope=process.argv.includes('--scope')?process.argv[process.argv.indexOf('--scope')+1]:'page';
  const {out,stat}=findAmbiguous({scope});console.log('النطاق:',scope==='quran'?'المصحف كله':'آيات الصفحة نفسها');
  console.log('أسئلة متوسطة فُحصت:',stat.checked,'| غامضة:',out.length,'| غير قابلة للفحص (نص غير متصل):',stat.unverifiable,'| متخطّاة:',stat.skipped,'| مستثناة بالوسم:',stat.exempt);
  const ri=process.argv.indexOf('--report');
  if(ri>0){const f=process.argv[ri+1]||'ambiguity_report.txt';
    const by={};out.forEach(x=>(by[x.stem]=by[x.stem]||[]).push(x));
    let t='تقرير غموض أسئلة المستوى المتوسط — للمراجعة فقط، لا يغيّر شيئاً\n'
      +'الغامض: سؤال له أكثر من تكملة صحيحة '+(scope==='quran'?'في المصحف كله':'داخل آيات صفحته نفسها')+'.\nعدد الأسئلة الغامضة: '+out.length+' في '+Object.keys(by).length+' صفحة\n\n'
      +'══ الأسوأ أولاً ══\n';
    out.slice(0,15).forEach(x=>{t+=x.stem+' | MEDIUM_Q['+x.index+'] | '+x.count+' تكملة\n  '+clean(x.q)+'\n  الإجابة: '+x.answer+'\n';});
    t+='\n══ حسب الصفحة ══\n';
    Object.keys(by).sort().forEach(s=>{t+='\n▸ '+s+' ('+by[s].length+')\n';by[s].forEach(x=>{t+='  - ['+x.index+'] '+clean(x.q)+'\n      الإجابة: '+x.answer+' | '+x.count+' تكملات | بدائل في: '+x.alts.join('، ')+' | '+kind(x.count)+'\n';});});
    fs.writeFileSync(f,t,'utf8');console.log('كُتب التقرير:',f);}
  else out.slice(0,15).forEach(x=>console.log('  ⚠',x.stem+'['+x.index+']',x.count,clean(x.q)));
}
