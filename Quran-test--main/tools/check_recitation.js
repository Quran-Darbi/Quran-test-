// يتحقق أن نص صفحة التلاوة (src/recitation/*.json: ayahs وtext) يطابق نص src/data (AYAT) على مستوى الكلمات والإملاء.
// الغاية: ألا يتباعد النصان إذا صُحّح أحدهما دون الآخر. الفروق الشكلية (علامات الوقف، شكل التنوين) لا تُعدّ خطأ.
const fs=require('fs'),path=require('path');
const {ROOT,readJSON,pages}=require('./lib.js');const {norm}=require('./quran_ref.js');
function checkRecitation(E){
  const dir=path.join(ROOT,'src','recitation');if(!fs.existsSync(dir))return;
  const AY={},TX={};
  for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.json'))){const k=f.slice(0,-5);try{const j=readJSON(path.join(dir,f));AY[k]=j.ayahs;TX[k]=j.text;if(!Array.isArray(j.ayahs)||typeof j.text!=='string')E('src/recitation/'+f,'الهيكل المتوقع: {ayahs:[...], text:"..."}');}catch(e){E('src/recitation/'+f,'JSON غير صالح: '+e.message);}}
  const src={};for(const {stem,file:f} of pages()){const j=readJSON(f);src[(j.meta&&j.meta.recId)||stem]={stem,t:norm((j.data.AYAT||[]).join(' '))};}
  for(const k of Object.keys(src))if(!(k in AY))E('src/recitation','الصفحة '+src[k].stem+' ('+k+') ليس لها ملف في src/recitation');
  for(const k of Object.keys(AY)){
    if(!(k in src)){E('src/recitation/'+k+'.json','لا يقابله ملف في src/data');continue;}
    if(!Array.isArray(AY[k]))continue;
    const a=norm(AY[k].join(' ')),t=norm(String(TX[k]||''));
    if(a!==src[k].t)E('src/recitation/'+k+'.json','ayahs تخالف AYAT في '+src[k].stem+' — '+firstDiff(a,src[k].t));
    if(t!==src[k].t)E('src/recitation/'+k+'.json','text تخالف AYAT في '+src[k].stem+' — '+firstDiff(t,src[k].t));}
}
function firstDiff(a,b){const x=a.split(' '),y=b.split(' ');let i=0;while(i<x.length&&i<y.length&&x[i]===y[i])i++;return 'عند الكلمة '+(i+1)+': «'+(x[i]||'∅')+'» ≠ «'+(y[i]||'∅')+'»';}
module.exports={checkRecitation};
if(require.main===module){const errs=[];checkRecitation((s,m)=>errs.push(s+': '+m));console.log('فروق recitation مقابل src:',errs.length);errs.slice(0,40).forEach(x=>console.log('  ✗',x));process.exit(errs.length?1:0);}
