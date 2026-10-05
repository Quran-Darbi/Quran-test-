#!/usr/bin/env node
// فحص جودة بيانات الصفحات قبل البناء: الهيكل، الأسئلة، والمطابقة مع النص المرجعي
const fs=require('fs'),path=require('path');const {ROOT,SRC,readJSON,pages}=require('./lib.js');const {norm,loadCorpus}=require('./quran_ref.js');const {checkRecitation}=require('./check_recitation.js');
const REF=path.join(ROOT,'Scripts','quran-uthmani.txt');const C=loadCorpus(REF);
const KI=fs.existsSync(path.join(__dirname,'known_issues.json'))?readJSON(path.join(__dirname,'known_issues.json')):{};
const errors=[],warns=[],known=[];
const E=(s,m)=>errors.push(s+': '+m),W=(s,m)=>warns.push(s+': '+m);
const all=new Set(pages().map(p=>p.stem));let nAyat=0,nQ=0;
for(const {stem,file} of pages()){
  let j;try{j=readJSON(file);}catch(e){E(stem,'JSON غير صالح: '+e.message);continue;}
  const m=j.meta||{},d=j.data||{};
  for(const k of ['title','description','surah','range','pageInfo'])if(typeof m[k]!=='string'||!m[k].trim())E(stem,'meta.'+k+' ناقص');
  for(const k of ['prev','next'])if(m[k]&&!all.has(m[k].replace(/\.html$/,''))&&!fs.existsSync(path.join(ROOT,m[k])))E(stem,'meta.'+k+' يشير إلى صفحة غير موجودة: '+m[k]);
  if(!fs.existsSync(path.join(SRC,'templates',j.shell+'.html')))E(stem,'قالب غير موجود: '+j.shell);
  if(!fs.existsSync(path.join(SRC,'engine',j.engine+'.js')))E(stem,'محرك غير موجود: '+j.engine);
  if(typeof d.RESUME_KEY!=='string')E(stem,'RESUME_KEY ناقص');
  if(!Array.isArray(d.AYAT)||!d.AYAT.length||d.AYAT.some(a=>typeof a!=='string'||!a.trim()))E(stem,'AYAT غير صالح');
  if(d.AYAT_NUMS&&(!Array.isArray(d.AYAT_NUMS)||d.AYAT_NUMS.length!==(d.AYAT||[]).length))E(stem,'AYAT_NUMS لا يطابق عدد AYAT');
  if(!d.BAD_SPELL||!('$regex' in d.BAD_SPELL))E(stem,'BAD_SPELL (حارس الإملاء) مفقود');
  const joined=norm((d.AYAT||[]).join(' '));
  // 1) مطابقة النص القرآني مع المرجع
  (d.AYAT||[]).forEach((a,i)=>{nAyat++;const n=norm(a);if(n&&!C.text.includes(n)){const key=stem+'#'+i;if((KI.ayat||[]).includes(key))known.push(key);else E(stem,'AYAT['+i+'] لا يطابق النص المرجعي: '+a.slice(0,50));}});
  // 2) الأسئلة
  const seen=new Set();
  (d.EASY_Q||[]).forEach((q,i)=>{nQ++;const t='EASY_Q['+i+']';
    if(!q.q||!Array.isArray(q.choices)||q.choices.length<2)return E(stem,t+' هيكل غير صالح');
    if(!Number.isInteger(q.answer)||q.answer<0||q.answer>=q.choices.length)E(stem,t+' فهرس الإجابة خارج الخيارات');
    if(new Set(q.choices).size!==q.choices.length)E(stem,t+' خيارات مكررة');
    if(seen.has(q.q))W(stem,t+' نص السؤال مكرر (قد يكون مقصوداً لآية مكرّرة)');seen.add(q.q);
    if(q.q.includes('___')&&Number.isInteger(q.answer)){const parts=q.q.replace(/[«»]/g,'').split('___');const full=norm(parts[0]+' '+q.choices[q.answer]+' '+(parts[1]||''));if(full&&!joined.includes(full))W(stem,t+' نص السؤال مع الإجابة لا يظهر متصلاً في AYAT');}});
  for(const k of ['MEDIUM_Q','HARD_Q'])(d[k]||[]).forEach((q,i)=>{nQ++;const t=k+'['+i+']';
    if(!q.q||typeof q.answer!=='string'||!q.answer.trim())return E(stem,t+' هيكل غير صالح');
    if(!C.text.includes(norm(q.answer))&&!(KI.answers||[]).includes(stem+':'+k+':'+i))W(stem,t+' الإجابة ليست متصلة في النص المرجعي (قد تكون جمعاً مقصوداً لأجزاء)');});
}
// 3) كل صفحة اختبار يجب أن تظهر مرة واحدة في src/progress_groups.json (صفحة «تقدّمي»)
try{const pg=readJSON(path.join(SRC,'progress_groups.json'));const inG=new Map();
  pg.forEach(g=>g.pages.forEach(p=>{if(!all.has(p.stem))E('progress_groups',p.stem+' غير موجودة في src/data');inG.set(p.stem,(inG.get(p.stem)||0)+1);}));
  inG.forEach((n,k)=>{if(n>1)E('progress_groups',k+' مكررة');});
  for(const st of all)if(!inG.has(st))E('progress_groups',st+' ليست في progress_groups.json (لن تظهر في «تقدّمي»)');
}catch(e){E('progress_groups','تعذّرت القراءة: '+e.message);}
// 4a) كل صفحة يجب أن تظهر في الصفحة الرئيسية (index.html مكتوبة يدوياً حتى الآن)
try{const ix=fs.readFileSync(path.join(ROOT,'index.html'),'utf8');for(const st of all)if(!ix.includes(st+'.html'))E(st,'غير مربوطة في index.html (لن تظهر بطاقتها في الرئيسية)');}catch(e){E('index.html','تعذّرت القراءة: '+e.message);}
// 4) نص صفحة التلاوة (recitation.html) يطابق src/data
checkRecitation(E);
console.log('صفحات:',pages().length,'| أسطر الآيات:',nAyat,'| أسئلة:',nQ);
console.log('أخطاء:',errors.length,'| تنبيهات:',warns.length,'| مشكلات معروفة مؤجّلة:',known.length);
errors.slice(0,40).forEach(x=>console.log('  ✗',x));
if(process.argv.includes('--warnings'))warns.forEach(x=>console.log('  ⚠',x));
process.exit(errors.length?1:0);
