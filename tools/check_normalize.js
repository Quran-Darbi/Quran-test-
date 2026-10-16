// حارس دالة normalize في voice-engine.js (النسخة الوحيدة المعتمدة). لا يغيّر الدالة ولا يمسّ الموقع.
// 1) يتحقق من القواعد الأساسية المتفق عليها. 2) يقارن بصمة ناتج normalize على كل كلمات AYAT بالبصمة المحفوظة،
// فإذا تغيّر ناتج الدالة على أي كلمة (ولو دون قصد) يفشل الفحص ويعرض أمثلة الفروق.
// التشغيل: node tools/check_normalize.js   |   بعد تعديل مقصود ومراجَع: node tools/check_normalize.js --update
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {ROOT,readJSON,pages}=require('./lib.js');
const SNAP=path.join(__dirname,'normalize_snapshot.json');
const src=fs.readFileSync(path.join(ROOT,'voice-engine.js'),'utf8');
const i=src.indexOf('function normalize(str){');
if(i<0){console.error('✗ لم أجد function normalize في voice-engine.js');process.exit(1);}
const j=src.indexOf('\n}\n',i);
const normalize=new Function(src.slice(i,j+2)+'\nreturn normalize;')();
let fail=0;
const rules=[
 ['الألف الخنجرية → ا','مَٰلِكِ','مالك'],
 ['حذف الكشيدة','ـ','' ],
 ['حذف الهمزة المنفصلة','سَأَلَ','سال'],
 ['رحمان → رحمن','ٱلرَّحۡمَٰنِ','الرحمن'],
 ['تقليص الشدة/تكرار الحرف','ٱلَّذِينَ','الذين'],
];
for(const [n,inp,exp] of rules){const got=normalize(inp);if(got!==exp){fail++;console.error('✗ قاعدة: '+n+' — المتوقع «'+exp+'» والناتج «'+got+'»');}}
const words=new Set();
for(const p of pages()){const A=readJSON(p.file).data.AYAT||[];for(const a of A)for(const w of String(a).split(/\s+/))if(w)words.add(w);}
const list=[...words].sort();
const map=list.map(w=>w+'\t'+normalize(w));
const hash=crypto.createHash('sha256').update(map.join('\n')).digest('hex');
if(process.argv.includes('--update')){fs.writeFileSync(SNAP,JSON.stringify({words:list.length,hash,sample:Object.fromEntries(list.filter((_,k)=>k%50===0).map(w=>[w,normalize(w)]))},null,1)+'\n');console.log('تم تحديث البصمة: '+list.length+' كلمة');process.exit(fail?1:0);}
if(!fs.existsSync(SNAP)){console.error('✗ لا توجد بصمة محفوظة؛ شغّل --update مرة واحدة بعد المراجعة');process.exit(1);}
const s=JSON.parse(fs.readFileSync(SNAP,'utf8'));
if(s.hash!==hash){fail++;console.error('✗ تغيّر ناتج normalize على كلمات AYAT (كلمات اليوم: '+list.length+'، المحفوظ: '+s.words+').');
 let c=0;for(const [w,v] of Object.entries(s.sample)){if(normalize(w)!==v&&c++<10)console.error('   مثال: «'+w+'» كان «'+v+'» وصار «'+normalize(w)+'»');}
 console.error('   إن كان هذا مقصودًا ومراجَعًا: node tools/check_normalize.js --update');}
console.log(fail?'فشل: '+fail:'✓ normalize مطابقة للبصمة المحفوظة ('+list.length+' كلمة)');process.exit(fail?1:0);
