// توحيد التشكيل والرسم للمقارنة مع النص المرجعي (Scripts/quran-uthmani.txt)
const fs=require('fs');
const norm=s=>s
  .replace(/[ـً-ٰٟۖ-ۭ࣓-ࣿ۞۩۞]/g,'')
  .replace(/[أإآٱ]/g,'ا').replace(/ؤ/g,'و').replace(/ئ/g,'ي').replace(/ء/g,'').replace(/ى/g,'ي').replace(/ة/g,'ه')
  .replace(/ی/g,'ي').replace(/\s+/g,' ').trim();
function loadCorpus(p){const rows=fs.readFileSync(p,'utf8').split('\n').filter(Boolean).map(l=>l.split('|'));
  const text=rows.map(r=>norm(r.slice(2).join('|'))).join(' ');return {text,words:new Set(text.split(' '))};}
module.exports={norm,loadCorpus};
