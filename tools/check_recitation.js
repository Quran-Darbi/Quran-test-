// يتحقق أن النص المضمَّن في recitation.html (AYAHS وTEXTS) يطابق نص src/data (AYAT) على مستوى الكلمات والإملاء.
// الغاية: ألا يتباعد النصان إذا صُحّح أحدهما دون الآخر. الفروق الشكلية (علامات الوقف، شكل التنوين) لا تُعدّ خطأ.
const fs=require('fs'),path=require('path'),vm=require('vm');
const {ROOT,readJSON,pages}=require('./lib.js');const {norm}=require('./quran_ref.js');
function extract(html,name){
  const m=html.match(new RegExp('const '+name+'\\s*=\\s*\\{[\\s\\S]*?\\n\\};'));
  if(!m)throw new Error('لم أجد '+name+' في recitation.html');
  return vm.runInNewContext('('+m[0].replace(/^const \w+\s*=\s*/,'').replace(/;\s*$/,'')+')');}
function checkRecitation(E){
  const file=path.join(ROOT,'recitation.html');if(!fs.existsSync(file))return;
  let AY,TX;try{const h=fs.readFileSync(file,'utf8');AY=extract(h,'AYAHS');TX=extract(h,'TEXTS');}catch(e){E('recitation.html','تعذّر قراءة النص المضمَّن: '+e.message);return;}
  const src={};for(const {stem,file:f} of pages()){const j=readJSON(f);src[(j.meta&&j.meta.recId)||stem]={stem,t:norm((j.data.AYAT||[]).join(' '))};}
  for(const k of Object.keys(src))if(!(k in AY))E('recitation.html','الصفحة '+src[k].stem+' ('+k+') ليست في AYAHS');
  for(const k of Object.keys(AY)){
    if(!(k in src)){E('recitation.html','AYAHS['+k+'] لا يقابلها ملف في src/data');continue;}
    const a=norm(AY[k].join(' ')),t=norm(String(TX[k]||''));
    if(a!==src[k].t)E('recitation.html','AYAHS['+k+'] تخالف AYAT في '+src[k].stem+' — '+firstDiff(a,src[k].t));
    if(t!==src[k].t)E('recitation.html','TEXTS['+k+'] تخالف AYAT في '+src[k].stem+' — '+firstDiff(t,src[k].t));}
}
function firstDiff(a,b){const x=a.split(' '),y=b.split(' ');let i=0;while(i<x.length&&i<y.length&&x[i]===y[i])i++;return 'عند الكلمة '+(i+1)+': «'+(x[i]||'∅')+'» ≠ «'+(y[i]||'∅')+'»';}
module.exports={checkRecitation};
if(require.main===module){const errs=[];checkRecitation((s,m)=>errs.push(s+': '+m));console.log('فروق recitation مقابل src:',errs.length);errs.slice(0,40).forEach(x=>console.log('  ✗',x));process.exit(errs.length?1:0);}
