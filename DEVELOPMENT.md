# دليل التطوير — دربي لحفظ القرآن

صفحات الاختبار (الـ220 ملفاً في الجذر) **مولَّدة** من `src/`، ولا تُعدَّل يدوياً.

| أين | ماذا |
|---|---|
| `src/data/<صفحة>.json` | الآيات والأسئلة والمشتتات وعنوان الصفحة والتنقل — هنا فقط يُكتب المحتوى |
| `src/engine/engine1.js` | محرك الاختبار الموحّد (يعمل لكل الصفحات) |
| `src/assets/quiz.css` + `src/templates/page.html` | التنسيق والقالب المشتركان |
| `tools/validate.js` | فحص الهيكل والأسئلة ومطابقة كل آية مع `Scripts/quran-uthmani.txt` |
| `tools/build.js` | يولّد صفحات الجذر و`engine/` و`assets/` |
| `tools/new_page.js` | ينشئ هيكل صفحة جديدة جاهزاً للملء |
| `legacy/` | أدوات الإصلاح القديمة (`fix_files.py`) — لم تعد تعمل على الصفحات |

ملاحظة: جميع الصفحات (220) تستخدم الآن قالباً واحداً `src/templates/page.html`.

## إضافة صفحة جديدة
```
node tools/new_page.js maryam_p310 --surah "مريم" --from 65 --to 76 --page 310 --info "وصف" --prev maryam_p309
# املئي AYAT وAYAT_NUMS والأسئلة في src/data/maryam_p310.json
node tools/validate.js && node tools/build.js
```
ثم اربطي الصفحة في `index.html` و`sitemap.xml`، وحدّثي `meta.next` في الصفحة السابقة.

## تعديل السلوك أو الشكل لكل الصفحات
عدّلي `src/engine/engine1.js` أو `src/assets/quiz.css` مرة واحدة ثم `node tools/build.js`.

## ملاحظات
- GitHub Actions (`build.yml`) يشغّل الفحص والبناء تلقائياً عند أي تعديل في `src/` أو `tools/`.
- `tools/known_issues.json` يسجّل مشكلات نصية موثّقة قيد الاعتماد (تُحذف منه فور تصحيحها).
- 7 صفحات قديمة (عبس، الضحى، الفاتحة، الغاشية، المطففين، النبأ، النازعات) ما زالت على قوالب قديمة في `src/templates/shell*.html`.

## تنبيه: recitation.html
ملف اختبار التلاوة ينسخ نصوص الآيات داخله (AYAHS) ولا يقرؤها من `src/data`.
أي تصحيح نصي في صفحة سورة يجب أن يُطبَّق أيضاً في `recitation.html` (مرحلة لاحقة: توليده تلقائياً من `src/data`).
تم توحيد رسم النازعات (الألف المقصورة قبل الألف الخنجرية) في الملفين.
