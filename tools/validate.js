#!/usr/bin/env node
// فحص جودة بيانات الصفحات قبل البناء: الهيكل، الأسئلة، والمطابقة مع النص المرجعي
const fs=require('fs'),path=require('path');const {ROOT,SRC,readJSON,pages}=require('./lib.js');const {norm,loadCorpus}=require('./quran_ref.js');const {checkRecitation}=require('./check_recitation.js');const {checkAmbiguity}=require('./check_ambiguity.js');
const REF=path.join(ROOT,'Scripts','quran-uthmani.txt');const C=loadCorpus(REF);
const KI=fs.existsSync(path.join(__dirname,'known_issues.json'))?readJSON(path.join(__dirname,'known_issues.json')):{};
const GH=new Set(fs.existsSync(path.join(__dirname,'grouped_hard.json'))?readJSON(path.join(__dirname,'grouped_hard.json')).pages:[]);
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
  // قاعدة الإقلاب (ثابتة): علامة واحدة + ميم صغيرة؛ ممنوع تنوين مفتوح (ࣰ ࣱ ࣲ) قبل ۢ / ۭ
  const _iq=JSON.stringify(d).match(/[\u08F0-\u08F2][\u06E2\u06ED]/g);if(_iq)E(stem,'إقلاب بتنوين مفتوح ('+_iq.length+') — القاعدة: فتحة/ضمة/كسرة واحدة + ميم صغيرة (RASM_RULES.md ٨)');
  // الصعب المجمَّع (للصفحات المسجَّلة في tools/grouped_hard.json): الصفحة ٣–٥ أجزاء متتالية، سؤال لكل جزء عن مدى آياته
  if(GH.has(stem)){const H=d.HARD_Q||[],N=d.AYAT_NUMS||(d.AYAT||[]).map((_,i)=>i+1);let pos=0;if(H.length>5||(H.length<3&&(d.AYAT||[]).length>=3))E(stem,'HARD_Q '+H.length+' (المطلوب ٣–٥ أجزاء، قاعدة الصعب المجمَّع)');
    H.forEach((h,i)=>{const m=String(h.q).match(/^اكتب (?:الآيات (\d+)[–-](\d+)|الآية (\d+))$/);if(!m)return E(stem,'HARD_Q['+i+'] صيغة غير صحيحة (المطلوب «اكتب الآيات 6–9»)');const a=N.indexOf(+(m[1]||m[3])),b=N.indexOf(+(m[2]||m[1]||m[3]));
      if(a!==pos||b<a)E(stem,'HARD_Q['+i+'] مجموعة غير متتالية');
      const aw=t=>String(t).split(' ').filter(x=>/[\u0621-\u064A\u0671]/.test(x));const okH=(hint,ay)=>{const hw=aw(hint),w=aw(ay);return hw.length&&hw.join(' ')===w.slice(0,hw.length).join(' ')&&(hw.length===3||hw.length===5||hw.length===w.length);};if(!okH(h.from,d.AYAT[a]))E(stem,'HARD_Q['+i+'] from ليس أول ٣ أو ٥ كلمات من أول آية');if(b>a?!okH(h.to,d.AYAT[b]):('to' in h))E(stem,'HARD_Q['+i+'] to غير صحيح');if(h.answer!==(d.AYAT||[]).slice(a,b+1).join(' '))E(stem,'HARD_Q['+i+'] الإجابة لا تطابق AYAT');pos=b+1;});
    if(H.length&&pos!==(d.AYAT||[]).length)E(stem,'HARD_Q لا يغطي كل آيات الصفحة');}
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
    if(q.q.includes('___')&&Number.isInteger(q.answer)){const qm=q.q.match(/«([^»]*___[^»]*)»/);const body=(qm?qm[1]:q.q).replace(/[«»]/g,'').replace(/﴿[^﴾]*﴾/g,' ').replace(/\([^)]*الآية[^)]*\)/g,' ');
      // فراغ واحد: النص مع الإجابة متصلاً (الفراغ الملاصق لحرف يُوصَل بلا مسافة، مثل «بِ___»)؛ فراغات متعددة: كل مقطع ثابت يُفحص على حدة
      const blanks=body.split('___').length-1;
      let bad;
      if(blanks===1){const m=body.match(/^([\s\S]*?)(\s?)___(\s?)([\s\S]*)$/);const full=norm(m[1]+m[2]+q.choices[q.answer]+m[3]+m[4]);bad=full&&!joined.includes(full);}
      else bad=body.split('___').some(x=>{const n=norm(x);return n&&!joined.includes(n);});
      if(bad)W(stem,t+' نص السؤال مع الإجابة لا يظهر متصلاً في AYAT');}});
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
// 5) تنبيه فقط: أسئلة متوسطة لها أكثر من تكملة صحيحة في المصحف (تفاصيلها: node tools/check_ambiguity.js --report ملف.txt)
checkAmbiguity(W);
console.log('صفحات:',pages().length,'| أسطر الآيات:',nAyat,'| أسئلة:',nQ);
console.log('أخطاء:',errors.length,'| تنبيهات:',warns.length,'| مشكلات معروفة مؤجّلة:',known.length);
errors.slice(0,40).forEach(x=>console.log('  ✗',x));
if(process.argv.includes('--warnings'))warns.forEach(x=>console.log('  ⚠',x));
process.exit(errors.length?1:0);
