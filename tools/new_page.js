#!/usr/bin/env node
// ينشئ ملف بيانات لصفحة اختبار جديدة (هيكل جاهز يُملأ بالآيات والأسئلة)
// الاستعمال:
//   node tools/new_page.js maryam_p310 --surah "مريم" --from 65 --to 76 --page 310 --info "وصف قصير للصفحة" [--prev maryam_p309] [--next maryam_p311] [--rec maryam_p310]
const fs=require('fs'),path=require('path');const {SRC,readJSON}=require('./lib.js');
const a=process.argv.slice(2),stem=a[0];const opt=k=>{const i=a.indexOf('--'+k);return i>=0?a[i+1]:null;};
if(!stem||stem.startsWith('--')||!opt('surah')||!opt('from')||!opt('to')||!opt('page')){console.error('الاستعمال: node tools/new_page.js <اسم_الصفحة> --surah "اسم السورة" --from N --to N --page N --info "وصف" [--prev x --next y --rec z]');process.exit(1);}
const out=path.join(SRC,'data',stem+'.json');if(fs.existsSync(out)){console.error('الصفحة موجودة مسبقاً: '+out);process.exit(1);}
const surah=opt('surah'),from=opt('from'),to=opt('to'),page=opt('page'),info=opt('info')||'';
const sample=readJSON(path.join(SRC,'data',fs.readdirSync(path.join(SRC,'data')).find(f=>f.endsWith('.json'))));
const title='اختبار حفظ سورة '+surah+' — صفحة '+page+(info?' | '+info:'');
const j={meta:{title,description:'اختبر حفظك لسورة '+surah+' (من الآية '+from+' إلى الآية '+to+')، بمستويات متدرّجة: اختيار، وإكمال الفراغ، وكتابة الآيات وترتيبها، مع اختبار تلاوة بصوتك.',
  surah:'سورة '+surah,range:'من الآية '+from+' إلى الآية '+to,pageInfo:'صفحة '+page+' من المصحف'+(info?' — '+info:'')},
  shell:'page',engine:'engine1',
  data:{RESUME_KEY:'quranResume_'+stem,AYAT:[],AYAT_NUMS:[],EASY_Q:[],MEDIUM_Q:[],HARD_Q:[],BAD_SPELL:sample.data.BAD_SPELL}};
if(opt('prev'))j.meta.prev=opt('prev')+'.html';if(opt('next'))j.meta.next=opt('next')+'.html';if(opt('rec'))j.meta.recId=opt('rec');
fs.writeFileSync(out,JSON.stringify(j,null,1)+'\n');

// تسجيل الصفحة في قائمة «تقدّمي» (src/progress_groups.json) — تظهر تلقائياً بعد البناء
{const gp=path.join(SRC,'progress_groups.json');const G=readJSON(gp);const label='سورة '+surah;let g=G.find(x=>x.label===label);
  const pg=parseInt(page,10);if(!g){g={label,juz:Math.min(30,Math.max(1,Math.floor((pg-2)/20)+1)),pages:[]};G.push(g);}
  if(!g.pages.some(x=>x.stem===stem))g.pages.push({stem,name:surah+' ص '+page,range:from===to?String(from):from+'–'+to});
  fs.writeFileSync(gp,JSON.stringify(G,null,1)+'\n');console.log('أُضيفت إلى src/progress_groups.json (مجموعة: '+label+' — الجزء '+g.juz+')');}
console.log('أُنشئ: '+path.relative(process.cwd(),out));
console.log('التالي: املئي AYAT وAYAT_NUMS والأسئلة، ثم: node tools/validate.js && node tools/build.js');
console.log('وتذكّري: ربط الصفحة في index.html (يفحصه validate.js)، وإضافتها إلى recitation.html إن لزم، وتحديث meta.next في الصفحة السابقة. أما sitemap.xml وقائمة «تقدّمي» فيتحدّثان تلقائياً.');
