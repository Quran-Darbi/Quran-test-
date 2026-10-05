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
