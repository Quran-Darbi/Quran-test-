// مكتبة مشتركة لأدوات البناء — دربي لحفظ القرآن
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'..'),SRC=path.join(ROOT,'src');
const NAMES=['RESUME_KEY','AYAT','AYAT_NUMS','ORDER_AYAT','EASY_Q','MEDIUM_Q','HARD_Q','BAD_SPELL'];
// RegExp لا يُحفظ في JSON: يُخزَّن كعلامة {$regex,flags} ويعود حرفاً عند التوليد
function jsLit(v){
  if(v&&typeof v==='object'&&!Array.isArray(v)&&'$regex' in v)return '/'+v.$regex+'/'+(v.flags||'');
  if(Array.isArray(v))return '['+v.map(jsLit).join(',')+']';
  if(v&&typeof v==='object')return '{'+Object.keys(v).map(k=>JSON.stringify(k)+':'+jsLit(v[k])).join(',')+'}';
  return JSON.stringify(v);}
const readJSON=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const tplCache={};const tpl=n=>tplCache[n]??=fs.readFileSync(path.join(SRC,'templates',n+'.html'),'utf8');
function dataScript(j){
  const opt=j.options?'const PAGE_OPTIONS='+JSON.stringify(j.options)+';\n':'';
  return '<script>\n'+opt+NAMES.filter(k=>k in j.data).map(k=>'const '+k+'='+jsLit(j.data[k])+';').join('\n')+'\n</script>';}
function render(stem,j){
  const P=readJSON(path.join(SRC,'templates','partials.json'));
  const m=Object.assign({stem,recId:(j.meta&&j.meta.recId)||stem},j.meta);
  m.prevBtn=m.prev?P.prevBtn.replace('{{prev}}',m.prev):'';m.nextBtn=m.next?P.nextBtn.replace('{{next}}',m.next):'';
  let s=tpl(j.shell).replace(/\{\{(\w+)\}\}/g,(x,k)=>{if(m[k]==null)throw new Error(stem+': حقل ناقص في meta: '+k);return m[k];});
  return s.replace('«MAIN»',()=>dataScript(j)+'\n<script src="engine/'+j.engine+'.js"></script>');}
function pages(){return fs.readdirSync(path.join(SRC,'data')).filter(f=>f.endsWith('.json')).sort().map(f=>({stem:f.slice(0,-5),file:path.join(SRC,'data',f)}));}
module.exports={ROOT,SRC,NAMES,jsLit,readJSON,render,pages};
