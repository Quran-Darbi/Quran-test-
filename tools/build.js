#!/usr/bin/env node
// يولّد صفحات الاختبار في جذر المستودع من src/ (بيانات + قوالب + محرك + تنسيق)
const fs=require('fs'),path=require('path');const {ROOT,SRC,readJSON,render,pages}=require('./lib.js');
let n=0,changed=0;
for(const {stem,file} of pages()){const html=render(stem,readJSON(file));const out=path.join(ROOT,stem+'.html');
  if(!fs.existsSync(out)||fs.readFileSync(out,'utf8')!==html){fs.writeFileSync(out,html);changed++;}n++;}
// الملفات المشتركة: المحرك والتنسيق
for(const [d,e] of [['engine','.js'],['assets','.css']]){fs.mkdirSync(path.join(ROOT,d),{recursive:true});
  for(const f of fs.readdirSync(path.join(SRC,d)).filter(f=>f.endsWith(e))){const a=fs.readFileSync(path.join(SRC,d,f)),b=path.join(ROOT,d,f);
    if(!fs.existsSync(b)||!fs.readFileSync(b).equals(a)){fs.writeFileSync(b,a);changed++;}}}
console.log('تم توليد',n,'صفحة | ملفات تغيّرت:',changed);
