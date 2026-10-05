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
console.log('أُنشئ: '+path.relative(process.cwd(),out));
console.log('التالي: املئي AYAT وAYAT_NUMS والأسئلة، ثم: node tools/validate.js && node tools/build.js');
console.log('وتذكّري: ربط الصفحة في index.html وsitemap.xml، وتحديث meta.next في الصفحة السابقة.');
