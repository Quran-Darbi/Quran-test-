/*
  دربي لحفظ القرآن — نظام الترجمة الداخلي (i18n)
  ------------------------------------------------
  يستبدل الاعتماد على "Google Translate" (اللي كان بيظهر شريط
  "Translated to..." وبيترجم غلط، زي "اختبر تلاوتك" → "Test your memory")
  بترجمة حقيقية مبنية يدويًا، معمولة بجافاسكريبت خالص، من غير أي
  إعادة تحميل للصفحة ومن غير أي شريط خارجي.

  - النص القرآني (الآيات، الاختيارات، الإجابات) يفضل عربي دايمًا —
    مالوش ترجمة هنا أصلًا، ومحمي بـ notranslate في الـHTML.
  - اللي بيتترجم: واجهة الموقع بالكامل + صياغة الأسئلة/التعليمات
    (زي "اختر الإجابة الصحيحة"، "أكمل الفراغ"...) وكل رسائل
    النتيجة/التغذية الراجعة.

  إضافة لغة جديدة مستقبلًا = إضافة كائن جديد جوه DICT بعد مراجعته،
  ثم إضافته لمصفوفة SUPPORTED. من غير كده الزر ميتفعّلش.
*/
(function(){
'use strict';

var DICT = {

ar: {
  // ===== عام / التنقل =====
  'nav.tools_title':'الأدوات',
  'nav.lang_label':'اللغة',
  'nav.feedback':'الاقتراحات',
  'nav.share':'مشاركة الصفحة',
  'nav.qr':'كود QR',
  'nav.about':'📖 عن المشروع',
  'nav.progress':'📊 تقدّمي',
  'nav.back':'← الرجوع',

  // ===== الصفحة الرئيسية =====
  'home.title':'دربي لحفظ القرآن',
  'home.subtitle':'اختبر حفظك صفحةً بصفحة — اختبارات تفاعلية لمراجعة الحفظ وتثبيته',
  'home.recite_btn':'🎤 اختبر حفظك',
  'home.progress_btn':'📊 تقدّمي',
  'home.progress_btn_sub':'تقدّمي بالتفصيل ◀',
  'home.stat_tests':'اختباراً متاحاً',
  'home.stat_parts':'أجزاء',
  'home.stat_surahs':'سورة',
  'home.beta_tag':'✦ الإطلاق التجريبي',
  'home.beta_text_prefix':'نرحب بـ',
  'home.beta_link':'ملاحظاتكم واقتراحاتكم',
  'home.search_placeholder':'ابحث عن سورة أو صفحة...',
  'home.filter_all':'كل الأجزاء',
  'home.filter_built':'متاح الآن',
  'home.filter_soon':'قريبًا',
  'home.filter_empty':'لا يوجد أجزاء مطابقة لهذا الفلتر حاليًا.',
  'home.juz_prefix':'الجزء',
  'home.juz_soon':'قريبًا',
  'home.juz_surahs_count':'{n} سور',
  'home.juz_available_count':'{n} متاح',
  'home.juz_completed_count':'{done} / {total} مكتمل',
  'home.card_soon_badge':'قريباً',
  'home.card_complete_badge':'✓ مكتمل',
  'home.lvl_easy_title':'سهل',
  'home.lvl_medium_title':'متوسط',
  'home.lvl_hard_title':'صعب',
  'home.hero_progress_line':'أنجزت {done} من {total} صفحة ({pct}٪)',
  'home.hero_last_visited':'آخر مراجعة: {name}',
  'home.about_title':'عن المشروع',
  'home.about_p1':'«دربي لحفظ القرآن» منصة تفاعلية تهدف إلى مساعدة الجميع على حفظ كتاب الله ومراجعته، من خلال اختبارات متنوعة.',
  'home.about_p2':'مصممة بعناية لتثبيت الحفظ وتعزيز إتقانه، مع التركيز على متشابهات القرآن الكريم.',
  'home.footer_copy':'دربي لحفظ القرآن — جميع الحقوق محفوظة',

  // ===== نافذة الملاحظات =====
  'fdbk.title':'💬 شاركنا رأيك',
  'fdbk.type_label':'نوع الملاحظة',
  'fdbk.type_quran':'خطأ في النص القرآني',
  'fdbk.type_question':'خطأ في السؤال أو الإجابة',
  'fdbk.type_voice':'مشكلة في التسجيل الصوتي',
  'fdbk.type_design':'مشكلة تصميم أو عرض',
  'fdbk.type_suggestion':'اقتراح تحسين',
  'fdbk.type_other':'أخرى',
  'fdbk.note_label':'تفاصيل الملاحظة (اختياري)',
  'fdbk.note_placeholder':'اكتب ملاحظتك هنا...',
  'fdbk.send':'إرسال عبر واتساب',
  'fdbk.cancel':'إلغاء',

  // ===== نافذة كود QR =====
  'qr.title':'🔲 امسح الكود لفتح الصفحة',
  'qr.caption':'امسح الكود لفتح الموقع على موبايلك',
  'qr.copy_btn':'📋 نسخ الرابط',
  'qr.copied':'✅ تم النسخ',
  'qr.copy_failed':'تعذر النسخ',
  'qr.close_btn':'إغلاق',

  // ===== صفحات الاختبار: الرأس/المعلومات =====
  'quiz.stat_question':'السؤال',
  'quiz.stat_wrong':'خطأ',
  'quiz.stat_correct':'صحيح',
  'quiz.resume_text':'📌 لديك اختبار لم يكتمل. هل ترغب في المتابعة من حيث توقفتَ، أم البدء من جديد؟',
  'quiz.resume_continue':'المتابعة من هنا',
  'quiz.resume_restart':'البدء من جديد',
  'quiz.recite_test_link':'🎤 اختبر تلاوتك',

  // ===== اختيار المستوى =====
  'level.choose_title':'اختر مستوى الاختبار',
  'level.choose_sub':'كل مستوى له طريقة مختلفة في الاختبار',
  'level.easy_name':'سهل',
  'level.easy_desc':'اختر الإجابة الصحيحة',
  'level.medium_name':'متوسط',
  'level.medium_desc':'أكمل الفراغ',
  'level.hard_name':'صعب',
  'level.hard_desc':'اكتب الآية كاملة',
  'level.order_name':'ترتيب',
  'level.order_desc':'رتّب الآيات',
  'level.start_btn':'ابدأ الاختبار ←',
  'level.prev_page':'⏮️ الصفحة السابقة',
  'level.next_page':'الصفحة التالية ⏭️',

  // ===== أثناء الاختبار =====
  'quiz.q_number':'السؤال {cur} من {total}',
  'quiz.q_number_short':'السؤال {cur} /',
  'quiz.prev_q':'→ السؤال السابق',
  'quiz.skip_q':'⏭ تخطي',
  'quiz.next_q':'السؤال التالي ←',
  'quiz.return_to_levels':'🔄 اختر اختباراً آخر',
  'quiz.medium_placeholder':'اكتب الكلمة الناقصة...',
  'quiz.hard_placeholder':'اكتب الآية كاملة...',
  'quiz.submit_check':'تحقق ✓',
  'quiz.ayah_label':'الآية {n}',

  // ===== الترتيب =====
  'order.instruction':'رتّب الآيات — اضغط على الآية فتُوضَع بالتسلسل. تريد تخطّي خانة؟ اضغط على الخانة التي تريد المتابعة منها',
  'order.help_btn':'؟ كيف يعمل الترتيب',
  'order.help_title':'طريقة الترتيب',
  'order.help_prev':'← السابق',
  'order.help_stop':'⏸ إيقاف',
  'order.help_play':'▶ تشغيل',
  'order.help_next':'التالي →',
  'order.help_start_btn':'ابدأ الترتيب',
  'order.reveal_btn':'💡 أظهر الترتيب الصحيح',
  'order.check_btn':'تحقق ✓',
  'order.selected_label':'المحدَّدة: ',
  'order.selected_suffix':' — سجّل البديل',
  'order.delete_btn':'✕ حذف',
  'order.select_title':'اضغط لتحديدها ثم سجّل البديل',
  'order.deselect_title':'اضغط لإلغاء التحديد',
  'order.final_step_caption':'✓ وهذه كل الحركات',
  'order.final_step_why':'عند امتلاء جميع الخانات يظهر زر «تحقق ✓» لتصحيح الترتيب.',

  // ===== النتيجة =====
  'result.perfect_title':'ممتاز! حفظ مثالي',
  'result.perfect_msg':'ما شاء الله! أتقنت السورة بالكامل',
  'result.great_title':'أحسنت!',
  'result.great_msg':'نتيجة رائعة، استمر في المراجعة',
  'result.good_title':'جيد',
  'result.good_msg':'راجع السورة مرة أخرى وأعد الاختبار',
  'result.weak_title':'تحتاج مراجعة',
  'result.weak_msg':'لا تيأس، المراجعة المستمرة هي المفتاح',
  'result.score_line':'{wc} / {wt} كلمة — {pct}%  |  {cc} / {qt} سؤال',
  'result.review_mistakes':'📝 راجع أخطائي',
  'result.retry':'🔄 اختر اختباراً آخر',
  'result.home_link':'← الرئيسية',

  // ===== مراجعة الأخطاء =====
  'review.prev':'→ السابق',
  'review.next':'التالي ←',
  'review.end':'إنهاء المراجعة',

  // ===== المساعدة (صعب) =====
  'hint.btn':'💡 مساعدة (أول 3 كلمات)',
  'voice.record_btn':'🎤 تسجيل صوتي',
  'voice.text_btn':'⌨️ كتابة',
  'voice.press_to_record':'🎤 اضغط للتسجيل',
  'voice.recording':'⏸ إيقاف التسجيل',
  'voice.paused':'▶️ استمر في التسجيل',
  'voice.clear_btn':'🗑️ مسح الكل والبدء من جديد',
  'voice.not_supported':'⚠️ المتصفح لا يدعم التسجيل',
  'voice.https_only':'🔒 يعمل على الموقع الرسمي فقط',

  // ===== التغذية الراجعة (صحيح/خطأ) =====
  'feedback.correct_full':'✓ أحسنت! إجابة صحيحة تماماً 🌟',
  'feedback.correct_mcq':'✓ أحسنت! 🌟',
  'feedback.wrong_full_prefix':'✗ الإجابة الصحيحة:',
  'feedback.wrong_mcq_prefix':'✗ الإجابة الصحيحة: ',
  'feedback.skip_prefix':'⬅ الإجابة الصحيحة:',
  'feedback.words_correct_count':'{correct} / {total} كلمة صحيحة',
  'feedback.words_extra':' — و{extra} كلمة زيادة',
  'feedback.accuracy_line':'دقة هذه الإجابة: {pct}% ({matched} من {total} كلمة)',
  'feedback.accuracy_total_line':'الإجمالي: {pct}% ({correct} من {total} كلمة)',

  // ===== المراجعة/الترتيب — نصوص إضافية =====
  'review.number_label':'مراجعة {cur} من {total}',
  'order.dot_active_title':'الخانة النشطة الآن',
  'order.dot_jump_title':'اضغط للمتابعة من هنا',
  'order.result_line':'{correct} / {total} في الترتيب الصحيح',
  'order.result_review_label':'الترتيب الصحيح للمراجعة:',
  'oh.step1_act':'ضَع آية في الترتيب',
  'oh.step1_why':'اضغط على أي آية في الأسفل، فتُوضَع في الخانة النشطة (الدائرة الخضراء).',
  'oh.step2_act':'اختر خانة ثم ضَع فيها',
  'oh.step2_why':'الدوائر المتقطّعة هي الخانات الفارغة. اضغط أي واحدة لتصبح هي النشطة، ثم اضغط آية فتُوضَع فيها هي — لا في التي تليها.',
  'oh.step3_act':'حدِّد آية للتبديل',
  'oh.step3_why':'اضغط على رقم الآية — لا على نصّها — فيظهر حوله إطار ذهبي.',
  'oh.step4_act':'بدِّل الآيتين',
  'oh.step4_why':'اضغط رقم آية أخرى، فتتبادلان مكانهما. واضغط الرقم نفسه لإلغاء التحديد.',
  'oh.step5_act':'اسحب آية من الترتيب',
  'oh.step5_why':'اضغط على نصّ الآية داخل مربّعها، فتعود إلى الأسفل وتفرغ خانتها.'
},

en: {
  // ===== General / navigation =====
  'nav.tools_title':'Tools',
  'nav.lang_label':'Language',
  'nav.feedback':'Feedback',
  'nav.share':'Share page',
  'nav.qr':'QR code',
  'nav.about':'📖 About',
  'nav.progress':'📊 My Progress',
  'nav.back':'← Back',

  // ===== Home page =====
  'home.title':'Quran Darbi — Memorization',
  'home.subtitle':'Test your memorization page by page — interactive quizzes to review and reinforce it',
  'home.recite_btn':'🎤 Test your recitation',
  'home.progress_btn':'📊 My Progress',
  'home.progress_btn_sub':'Full progress details ◀',
  'home.stat_tests':'quizzes available',
  'home.stat_parts':'parts',
  'home.stat_surahs':'surahs',
  'home.beta_tag':'✦ Beta launch',
  'home.beta_text_prefix':'We welcome your ',
  'home.beta_link':'feedback and suggestions',
  'home.search_placeholder':'Search for a surah or page...',
  'home.filter_all':'All parts',
  'home.filter_built':'Available now',
  'home.filter_soon':'Coming soon',
  'home.filter_empty':'No parts match this filter right now.',
  'home.juz_prefix':'Juz’',
  'home.juz_soon':'Coming soon',
  'home.juz_surahs_count':'{n} surahs',
  'home.juz_available_count':'{n} available',
  'home.juz_completed_count':'{done} / {total} complete',
  'home.card_soon_badge':'Soon',
  'home.card_complete_badge':'✓ Done',
  'home.lvl_easy_title':'Easy',
  'home.lvl_medium_title':'Medium',
  'home.lvl_hard_title':'Hard',
  'home.hero_progress_line':'You’ve completed {done} of {total} pages ({pct}%)',
  'home.hero_last_visited':'Last reviewed: {name}',
  'home.about_title':'About the project',
  'home.about_p1':'"Darbi" is an interactive platform that helps everyone memorize and review the Book of God through a variety of quizzes.',
  'home.about_p2':'Carefully designed to consolidate memorization and sharpen mastery, with a focus on the Quran’s similar/recurring verses (mutashabihat).',
  'home.footer_copy':'Darbi — Quran Memorization. All rights reserved',

  // ===== Feedback modal =====
  'fdbk.title':'💬 Share your feedback',
  'fdbk.type_label':'Feedback type',
  'fdbk.type_quran':'Error in the Quranic text',
  'fdbk.type_question':'Error in a question or answer',
  'fdbk.type_voice':'Voice recording issue',
  'fdbk.type_design':'Design or display issue',
  'fdbk.type_suggestion':'Improvement suggestion',
  'fdbk.type_other':'Other',
  'fdbk.note_label':'Details (optional)',
  'fdbk.note_placeholder':'Write your note here...',
  'fdbk.send':'Send via WhatsApp',
  'fdbk.cancel':'Cancel',

  // ===== QR modal =====
  'qr.title':'🔲 Scan to open this page',
  'qr.caption':'Scan the code to open the site on your phone',
  'qr.copy_btn':'📋 Copy link',
  'qr.copied':'✅ Copied',
  'qr.copy_failed':'Copy failed',
  'qr.close_btn':'Close',

  // ===== Quiz page header/info =====
  'quiz.stat_question':'Question',
  'quiz.stat_wrong':'Wrong',
  'quiz.stat_correct':'Correct',
  'quiz.resume_text':'📌 You have an unfinished quiz. Continue where you left off, or start over?',
  'quiz.resume_continue':'Continue',
  'quiz.resume_restart':'Start over',
  'quiz.recite_test_link':'🎤 Test your recitation',

  // ===== Level selection =====
  'level.choose_title':'Choose a quiz level',
  'level.choose_sub':'Each level tests you in a different way',
  'level.easy_name':'Easy',
  'level.easy_desc':'Choose the correct answer',
  'level.medium_name':'Medium',
  'level.medium_desc':'Fill in the blank',
  'level.hard_name':'Hard',
  'level.hard_desc':'Write the full ayah',
  'level.order_name':'Order',
  'level.order_desc':'Put the ayahs in order',
  'level.start_btn':'Start the quiz ←',
  'level.prev_page':'⏮️ Previous page',
  'level.next_page':'Next page ⏭️',

  // ===== During the quiz =====
  'quiz.q_number':'Question {cur} of {total}',
  'quiz.q_number_short':'Question {cur} /',
  'quiz.prev_q':'→ Previous question',
  'quiz.skip_q':'⏭ Skip',
  'quiz.next_q':'Next question ←',
  'quiz.return_to_levels':'🔄 Choose another quiz',
  'quiz.medium_placeholder':'Type the missing word...',
  'quiz.hard_placeholder':'Type the full ayah...',
  'quiz.submit_check':'Check ✓',
  'quiz.ayah_label':'Ayah {n}',

  // ===== Ordering =====
  'order.instruction':'Put the ayahs in order — tap an ayah to place it in sequence. Want to skip a slot? Tap the slot you want to continue from.',
  'order.help_btn':'? How ordering works',
  'order.help_title':'How ordering works',
  'order.help_prev':'← Previous',
  'order.help_stop':'⏸ Stop',
  'order.help_play':'▶ Play',
  'order.help_next':'Next →',
  'order.help_start_btn':'Start ordering',
  'order.reveal_btn':'💡 Show the correct order',
  'order.check_btn':'Check ✓',
  'order.selected_label':'Selected: ',
  'order.selected_suffix':' — tap a replacement',
  'order.delete_btn':'✕ Remove',
  'order.select_title':'Tap to select it, then tap a replacement',
  'order.deselect_title':'Tap to deselect',
  'order.final_step_caption':'✓ That’s all the moves',
  'order.final_step_why':'Once every slot is filled, the "Check ✓" button appears to grade your order.',

  // ===== Result =====
  'result.perfect_title':'Excellent! Perfect memorization',
  'result.perfect_msg':'Mashallah! You’ve mastered the whole page',
  'result.great_title':'Well done!',
  'result.great_msg':'Great result — keep up the review',
  'result.good_title':'Good',
  'result.good_msg':'Review the surah again and retake the quiz',
  'result.weak_title':'Needs more review',
  'result.weak_msg':'Don’t worry — consistent review is the key',
  'result.score_line':'{wc} / {wt} words — {pct}%  |  {cc} / {qt} questions',
  'result.review_mistakes':'📝 Review my mistakes',
  'result.retry':'🔄 Choose another quiz',
  'result.home_link':'← Home',

  // ===== Mistake review =====
  'review.prev':'→ Previous',
  'review.next':'Next ←',
  'review.end':'End review',

  // ===== Hint (hard level) =====
  'hint.btn':'💡 Hint (first 3 words)',
  'voice.record_btn':'🎤 Voice recording',
  'voice.text_btn':'⌨️ Typing',
  'voice.press_to_record':'🎤 Tap to record',
  'voice.recording':'⏸ Stop recording',
  'voice.paused':'▶️ Resume recording',
  'voice.clear_btn':'🗑️ Clear all and start over',
  'voice.not_supported':'⚠️ This browser doesn’t support recording',
  'voice.https_only':'🔒 Works on the official site only',

  // ===== Feedback (correct/wrong) =====
  'feedback.correct_full':'✓ Well done! Fully correct 🌟',
  'feedback.correct_mcq':'✓ Well done! 🌟',
  'feedback.wrong_full_prefix':'✗ The correct answer:',
  'feedback.wrong_mcq_prefix':'✗ The correct answer: ',
  'feedback.skip_prefix':'⬅ The correct answer:',
  'feedback.words_correct_count':'{correct} / {total} words correct',
  'feedback.words_extra':' — plus {extra} extra word(s)',
  'feedback.accuracy_line':'This answer’s accuracy: {pct}% ({matched} of {total} words)',
  'feedback.accuracy_total_line':'Overall: {pct}% ({correct} of {total} words)',

  // ===== Review / ordering — extra strings =====
  'review.number_label':'Review {cur} of {total}',
  'order.dot_active_title':'Currently active slot',
  'order.dot_jump_title':'Tap to continue from here',
  'order.result_line':'{correct} / {total} in the correct order',
  'order.result_review_label':'Correct order for review:',
  'oh.step1_act':'Place an ayah in the sequence',
  'oh.step1_why':'Tap any ayah below to place it in the active slot (the green circle).',
  'oh.step2_act':'Pick a slot, then fill it',
  'oh.step2_why':'The dashed circles are the empty slots. Tap one to make it active, then tap an ayah to place it there — not in the next one.',
  'oh.step3_act':'Select an ayah to swap',
  'oh.step3_why':'Tap the ayah’s number — not its text — and a gold outline appears around it.',
  'oh.step4_act':'Swap the two ayahs',
  'oh.step4_why':'Tap another ayah’s number to swap their places. Tap the same number again to deselect.',
  'oh.step5_act':'Pull an ayah out of the sequence',
  'oh.step5_why':'Tap the ayah’s text inside its box to send it back down and empty its slot.'
}

};

var SUPPORTED = ['ar','en'];
var LANG_LABELS = {ar:'العربية', en:'🇬🇧 English'};

function getLang(){
  var v='ar';
  try{ v = localStorage.getItem('darbi_lang') || 'ar'; }catch(e){}
  if(SUPPORTED.indexOf(v)===-1) v='ar';
  return v;
}
function setLangPref(code){
  try{ localStorage.setItem('darbi_lang', code); }catch(e){}
}

function t(key, vars){
  var lang = getLang();
  var dict = DICT[lang] || DICT.ar;
  var str = (dict[key] != null) ? dict[key] : (DICT.ar[key] != null ? DICT.ar[key] : key);
  if(vars){
    Object.keys(vars).forEach(function(k){
      str = str.split('{'+k+'}').join(vars[k]);
    });
  }
  return str;
}

function applyStaticText(root){
  var scope = root || document;
  scope.querySelectorAll('[data-i18n]').forEach(function(el){
    el.textContent = t(el.getAttribute('data-i18n'));
  });
  scope.querySelectorAll('[data-i18n-html]').forEach(function(el){
    el.innerHTML = t(el.getAttribute('data-i18n-html'));
  });
  scope.querySelectorAll('[data-i18n-placeholder]').forEach(function(el){
    el.setAttribute('placeholder', t(el.getAttribute('data-i18n-placeholder')));
  });
  scope.querySelectorAll('[data-i18n-title]').forEach(function(el){
    el.setAttribute('title', t(el.getAttribute('data-i18n-title')));
  });
  scope.querySelectorAll('[data-i18n-alt]').forEach(function(el){
    el.setAttribute('alt', t(el.getAttribute('data-i18n-alt')));
  });
}

function updateLangMenuUI(code){
  var cur=document.getElementById('tools-lang-cur');
  if(cur) cur.textContent = LANG_LABELS[code] || LANG_LABELS.ar;
  document.querySelectorAll('#tools-lang-list button[data-code]').forEach(function(b){
    b.classList.toggle('lang-active', b.getAttribute('data-code')===code);
  });
}

function applyLang(code){
  if(SUPPORTED.indexOf(code)===-1) code='ar';
  setLangPref(code);
  document.documentElement.setAttribute('lang', code);
  document.documentElement.setAttribute('dir', code==='ar' ? 'rtl' : 'ltr');
  applyStaticText();
  updateLangMenuUI(code);
  if(typeof window.onDarbiLangChange === 'function'){
    try{ window.onDarbiLangChange(code); }catch(e){}
  }
}

// واجهة عامة تستخدمها كل الصفحات
window.darbiT = t;
window.darbiLang = getLang;
window.darbiApplyLang = applyLang;
window.langSelect = function(code){ applyLang(code); };

// أول ما يوصل الـDOM، طبّق اللغة المحفوظة فورًا (بدون انتظار أي حاجة تانية)
if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', function(){ applyLang(getLang()); });
}else{
  applyLang(getLang());
}
})();
