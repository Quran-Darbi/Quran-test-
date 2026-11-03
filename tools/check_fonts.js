#!/usr/bin/env node
/* فحص الخط — دربي لحفظ القرآن
   القاعدة: خط الواجهة = Almarai لكل حرف في الموقع.
   الاستثناء الوحيد: نصوص القرآن (الآيات والبسملة) تبقى بخط المصحف: Amiri / Scheherazade New.
   يفشل الفحص إن وُجد font-family بخط المصحف على عنصر ليس في قائمة عناصر القرآن أدناه.
   التشغيل: node tools/check_fonts.js */
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const QURAN_FONT = /Amiri|Scheherazade/i;
/* عناصر القرآن المسموح لها بخط المصحف (أضيفي هنا أي عنصر جديد يعرض آية) */
const QURAN_SELECTORS = ['.q-text','.choice-btn','.answer-input','.feedback','.hint-box','.rec-transcript','.rec-word','.order-item','.order-help','.order-slot','.order-filled-grid','.order-empty-strip','.oh-tap','.mushaf-block','.ayah-end','.notranslate','.ayah-text','.footer-ayah','.about-dua','.about-ayah-text','.hero-bismillah','.rev-verse','.rec-weak-chips','.reveal-box','.ayah-display','.transcript-box','.help-chips'];
const files = [];
(function walk(d) { for (const f of fs.readdirSync(d)) {
  if (['node_modules','.git','src','legacy','tools','Scripts','recitation-data'].includes(f)) continue;
  const p = path.join(d, f), st = fs.statSync(p);
  if (st.isDirectory()) walk(p); else if (/\.(html|css|js)$/.test(f)) files.push(p);
} })(ROOT);
let bad = 0;
for (const f of files) {
  const lines = fs.readFileSync(f, 'utf8').split('\n');
  lines.forEach((ln, i) => {
    const re = /([^{}]*)\{[^{}]*font-family\s*:\s*([^;}]*)/g; let m;
    while ((m = re.exec(ln))) {
      const sel = m[1].trim(), fam = m[2];
      if (!QURAN_FONT.test(fam)) continue;
      if (/^['"]?Almarai/i.test(fam.trim().replace(/^['"]/, ''))) continue; /* Almarai أولًا ثم احتياطي = مسموح */
      const ok = sel.split(',').every(s => QURAN_SELECTORS.some(q => { const t = s.trim(); return t.endsWith(q) || t.startsWith(q + ' '); }));
      if (!ok) { bad++; console.log(`${path.relative(ROOT, f)}:${i + 1}  ${sel.slice(-60)}  ->  ${fam.trim()}`); }
    }
  });
}
console.log(bad ? `\n✗ ${bad} موضع بخط قديم — استبدليه بـ 'Almarai'` : '✓ الخط موحّد: Almarai للواجهة، وخط المصحف لنصوص القرآن فقط');
process.exit(bad ? 1 : 0);
