#!/usr/bin/env node
// يولّد صفحات الاختبار في جذر المستودع من src/ (بيانات + قوالب + محرك + تنسيق)
const fs=require('fs'),path=require('path');const {ROOT,SRC,readJSON,render,pages,progressGroupsJS}=require('./lib.js');
let n=0,changed=0;
for(const {stem,file} of pages()){const html=render(stem,readJSON(file));const out=path.join(ROOT,stem+'.html');
  if(!fs.existsSync(out)||fs.readFileSync(out,'utf8')!==html){fs.writeFileSync(out,html);changed++;}n++;}
// الملفات المشتركة: المحرك والتنسيق
for(const [d,e] of [['engine','.js'],['assets','.css']]){fs.mkdirSync(path.join(ROOT,d),{recursive:true});
  for(const f of fs.readdirSync(path.join(SRC,d)).filter(f=>f.endsWith(e))){const a=fs.readFileSync(path.join(SRC,d,f)),b=path.join(ROOT,d,f);
    if(!fs.existsSync(b)||!fs.readFileSync(b).equals(a)){fs.writeFileSync(b,a);changed++;}}}
{const o=path.join(ROOT,'progress-groups.js'),c=progressGroupsJS();if(!fs.existsSync(o)||fs.readFileSync(o,'utf8')!==c){fs.writeFileSync(o,c);changed++;}}

// نص صفحة التلاوة: src/recitation/<مفتاح>.json → recitation-data/<مفتاح>.js (يُحمَّل عند اختيار السورة فقط)
{const dir=path.join(SRC,'recitation'),out=path.join(ROOT,'recitation-data');
  if(fs.existsSync(dir)){fs.mkdirSync(out,{recursive:true});const want=new Set();
    for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.json')).sort()){const k=f.slice(0,-5);const j=readJSON(path.join(dir,f));
      const js='AYAHS['+JSON.stringify(k)+']='+JSON.stringify(j.ayahs)+';TEXTS['+JSON.stringify(k)+']='+JSON.stringify(j.text)+';\n';
      const o=path.join(out,k+'.js');want.add(k+'.js');
      if(!fs.existsSync(o)||fs.readFileSync(o,'utf8')!==js){fs.writeFileSync(o,js);changed++;}}
    for(const f of fs.readdirSync(out))if(f.endsWith('.js')&&!want.has(f)){fs.unlinkSync(path.join(out,f));changed++;}
    const man=JSON.stringify([...want].sort())+'\n',mo=path.join(out,'manifest.json');
    if(!fs.existsSync(mo)||fs.readFileSync(mo,'utf8')!==man){fs.writeFileSync(mo,man);changed++;}}}

// حذف الملفات القديمة المدرجة في tools/obsolete_files.txt (مع حماية الملفات الأساسية)
{const lst=path.join(__dirname,'obsolete_files.txt');
  if(fs.existsSync(lst)){const PROTECT=[/^\.github\//,/^src\//,/^tools\//,/^Scripts\/quran-uthmani\.txt$/,/^Scripts\/send_reminders\.py$/,/^CNAME$/,/^index\.html$/,/^\.git\//];
    for(const raw of fs.readFileSync(lst,'utf8').split('\n')){const rel=raw.trim();if(!rel||rel.startsWith('#'))continue;
      const abs=path.resolve(ROOT,rel);if(!abs.startsWith(ROOT+path.sep)||PROTECT.some(r=>r.test(rel))){console.log('تجاهل مسار محمي:',rel);continue;}
      if(fs.existsSync(abs)&&fs.statSync(abs).isFile()){fs.unlinkSync(abs);changed++;console.log('حُذف:',rel);
        let d=path.dirname(abs);while(d!==ROOT&&fs.existsSync(d)&&fs.readdirSync(d).length===0){fs.rmdirSync(d);d=path.dirname(d);}}}}}

// sitemap.xml: الإدخالات الموجودة تبقى حرفياً؛ تُضاف صفحات src/data الجديدة بتاريخ اليوم، وتُحذف صفحات اختبار لم يعد لها ملف
{const o=path.join(ROOT,'sitemap.xml');if(fs.existsSync(o)){const old=fs.readFileSync(o,'utf8');
  const stems=new Set(pages().map(p=>p.stem));const base=(old.match(/<loc>(https?:\/\/[^/<]+\/)/)||[0,'https://quran-darbi.com/'])[1];
  const today=new Date().toISOString().slice(0,10);const have=new Set();
  let xml=old.replace(/[ \t]*<url>\s*<loc>([^<]+)<\/loc>[\s\S]*?<\/url>\n?/g,(m,u)=>{
    const f=u.split('/').pop().replace(/\.html$/,'');have.add(f);
    const isQuiz=/\.html$/.test(u)&&!['about','privacy','recitation','progress','index'].includes(f);
    return(isQuiz&&!stems.has(f))?'':m;});
  const add=[...stems].sort().filter(st=>!have.has(st)).map(st=>'  <url>\n    <loc>'+base+st+'.html</loc>\n    <lastmod>'+today+'</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n').join('');
  if(add)xml=xml.replace('</urlset>',add+'</urlset>');
  if(xml!==old){fs.writeFileSync(o,xml);changed++;console.log('sitemap.xml: حُدّث (أُضيف '+(add.match(/<url>/g)||[]).length+')');}}}
console.log('تم توليد',n,'صفحة | ملفات تغيّرت:',changed);
