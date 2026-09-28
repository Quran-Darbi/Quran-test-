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
  'qr.img_alt':'كود QR لفتح هذه الصفحة على الموبايل',

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
  'quiz.hard_placeholder_plural':'اكتب الآيات كاملة...',
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
  'oh.step5_why':'اضغط على نصّ الآية داخل مربّعها، فتعود إلى الأسفل وتفرغ خانتها.',
  'oh.seg1':'الآية الأولى',
  'oh.seg2':'الآية الثانية',
  'oh.seg3':'الآية الثالثة'
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
  'qr.img_alt':'QR code to open this page on your phone',

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
  'quiz.hard_placeholder_plural':'Type the full ayahs...',
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
  'oh.step5_why':'Tap the ayah’s text inside its box to send it back down and empty its slot.',
  'oh.seg1':'The first ayah',
  'oh.seg2':'The second ayah',
  'oh.seg3':'The third ayah'
},

fr: {
  // ===== Général / navigation =====
  'nav.tools_title':'Outils',
  'nav.lang_label':'Langue',
  'nav.feedback':'Suggestions',
  'nav.share':'Partager la page',
  'nav.qr':'Code QR',
  'nav.about':'📖 À propos',
  'nav.progress':'📊 Mes progrès',
  'nav.back':'← Retour',

  // ===== Page d’accueil =====
  'home.title':'Darbi — Mémorisation du Coran',
  'home.subtitle':'Testez votre mémorisation page par page — des quiz interactifs pour réviser et consolider',
  'home.recite_btn':'🎤 Testez votre récitation',
  'home.progress_btn':'📊 Mes progrès',
  'home.progress_btn_sub':'Voir le détail de mes progrès ◀',
  'home.stat_tests':'quiz disponibles',
  'home.stat_parts':'parties',
  'home.stat_surahs':'sourates',
  'home.beta_tag':'✦ Lancement bêta',
  'home.beta_text_prefix':'Nous accueillons vos ',
  'home.beta_link':'remarques et suggestions',
  'home.search_placeholder':'Rechercher une sourate ou une page...',
  'home.filter_all':'Toutes les parties',
  'home.filter_built':'Disponible maintenant',
  'home.filter_soon':'Bientôt disponible',
  'home.filter_empty':'Aucune partie ne correspond à ce filtre pour le moment.',
  'home.juz_prefix':'Juz’',
  'home.juz_soon':'Bientôt disponible',
  'home.juz_surahs_count':'{n} sourates',
  'home.juz_available_count':'{n} disponible(s)',
  'home.juz_completed_count':'{done} / {total} terminé(es)',
  'home.card_soon_badge':'Bientôt',
  'home.card_complete_badge':'✓ Terminé',
  'home.lvl_easy_title':'Facile',
  'home.lvl_medium_title':'Moyen',
  'home.lvl_hard_title':'Difficile',
  'home.hero_progress_line':'Vous avez terminé {done} page(s) sur {total} ({pct}%)',
  'home.hero_last_visited':'Dernière révision : {name}',
  'home.about_title':'À propos du projet',
  'home.about_p1':'« Darbi » est une plateforme interactive qui aide chacun à mémoriser et à réviser le Livre de Dieu à travers des quiz variés.',
  'home.about_p2':'Conçue avec soin pour consolider la mémorisation et affiner sa maîtrise, en mettant l’accent sur les versets similaires du Coran (mutashabihat).',
  'home.footer_copy':'Darbi — Mémorisation du Coran. Tous droits réservés',

  // ===== Fenêtre de suggestions =====
  'fdbk.title':'💬 Partagez votre avis',
  'fdbk.type_label':'Type de remarque',
  'fdbk.type_quran':'Erreur dans le texte coranique',
  'fdbk.type_question':'Erreur dans une question ou une réponse',
  'fdbk.type_voice':'Problème d’enregistrement vocal',
  'fdbk.type_design':'Problème de design ou d’affichage',
  'fdbk.type_suggestion':'Suggestion d’amélioration',
  'fdbk.type_other':'Autre',
  'fdbk.note_label':'Détails (facultatif)',
  'fdbk.note_placeholder':'Écrivez votre remarque ici...',
  'fdbk.send':'Envoyer via WhatsApp',
  'fdbk.cancel':'Annuler',

  // ===== Fenêtre du code QR =====
  'qr.title':'🔲 Scannez pour ouvrir cette page',
  'qr.caption':'Scannez le code pour ouvrir le site sur votre téléphone',
  'qr.copy_btn':'📋 Copier le lien',
  'qr.copied':'✅ Copié',
  'qr.copy_failed':'Copie impossible',
  'qr.close_btn':'Fermer',
  'qr.img_alt':'Code QR pour ouvrir cette page sur votre téléphone',

  // ===== Page de quiz : en-tête/infos =====
  'quiz.stat_question':'Question',
  'quiz.stat_wrong':'Faux',
  'quiz.stat_correct':'Correct',
  'quiz.resume_text':'📌 Vous avez un quiz inachevé. Continuer où vous vous étiez arrêté(e), ou recommencer ?',
  'quiz.resume_continue':'Continuer',
  'quiz.resume_restart':'Recommencer',
  'quiz.recite_test_link':'🎤 Testez votre récitation',

  // ===== Choix du niveau =====
  'level.choose_title':'Choisissez un niveau de quiz',
  'level.choose_sub':'Chaque niveau vous teste d’une manière différente',
  'level.easy_name':'Facile',
  'level.easy_desc':'Choisir la bonne réponse',
  'level.medium_name':'Moyen',
  'level.medium_desc':'Compléter le mot manquant',
  'level.hard_name':'Difficile',
  'level.hard_desc':'Écrire le verset complet',
  'level.order_name':'Ordre',
  'level.order_desc':'Remettre les versets dans l’ordre',
  'level.start_btn':'Commencer le quiz ←',
  'level.prev_page':'⏮️ Page précédente',
  'level.next_page':'Page suivante ⏭️',

  // ===== Pendant le quiz =====
  'quiz.q_number':'Question {cur} sur {total}',
  'quiz.q_number_short':'Question {cur} /',
  'quiz.prev_q':'→ Question précédente',
  'quiz.skip_q':'⏭ Passer',
  'quiz.next_q':'Question suivante ←',
  'quiz.return_to_levels':'🔄 Choisir un autre quiz',
  'quiz.medium_placeholder':'Écrivez le mot manquant...',
  'quiz.hard_placeholder':'Écrivez le verset complet...',
  'quiz.hard_placeholder_plural':'Écrivez les versets complets...',
  'quiz.submit_check':'Vérifier ✓',
  'quiz.ayah_label':'Verset {n}',

  // ===== Remise en ordre =====
  'order.instruction':'Remettez les versets dans l’ordre — touchez un verset pour le placer dans la séquence. Vous voulez passer une case ? Touchez la case à partir de laquelle continuer.',
  'order.help_btn':'? Comment fonctionne le classement',
  'order.help_title':'Comment fonctionne le classement',
  'order.help_prev':'← Précédent',
  'order.help_stop':'⏸ Arrêter',
  'order.help_play':'▶ Lecture',
  'order.help_next':'Suivant →',
  'order.help_start_btn':'Commencer le classement',
  'order.reveal_btn':'💡 Afficher l’ordre correct',
  'order.check_btn':'Vérifier ✓',
  'order.selected_label':'Sélectionné : ',
  'order.selected_suffix':' — touchez un remplaçant',
  'order.delete_btn':'✕ Retirer',
  'order.select_title':'Touchez pour sélectionner, puis touchez un remplaçant',
  'order.deselect_title':'Touchez pour désélectionner',
  'order.final_step_caption':'✓ Voilà tous les mouvements',
  'order.final_step_why':'Une fois toutes les cases remplies, le bouton « Vérifier ✓ » apparaît pour corriger votre ordre.',

  // ===== Résultat =====
  'result.perfect_title':'Excellent ! Mémorisation parfaite',
  'result.perfect_msg':'Mashallah ! Vous avez parfaitement maîtrisé la page',
  'result.great_title':'Bravo !',
  'result.great_msg':'Excellent résultat, continuez la révision',
  'result.good_title':'Bien',
  'result.good_msg':'Révisez à nouveau la sourate et refaites le quiz',
  'result.weak_title':'Une révision est nécessaire',
  'result.weak_msg':'Ne vous découragez pas, la révision régulière est la clé',
  'result.score_line':'{wc} / {wt} mots — {pct}%  |  {cc} / {qt} questions',
  'result.review_mistakes':'📝 Revoir mes erreurs',
  'result.retry':'🔄 Choisir un autre quiz',
  'result.home_link':'← Accueil',

  // ===== Revue des erreurs =====
  'review.prev':'→ Précédent',
  'review.next':'Suivant ←',
  'review.end':'Terminer la revue',

  // ===== Aide (niveau difficile) =====
  'hint.btn':'💡 Indice (les 3 premiers mots)',
  'voice.record_btn':'🎤 Enregistrement vocal',
  'voice.text_btn':'⌨️ Saisie',
  'voice.press_to_record':'🎤 Appuyez pour enregistrer',
  'voice.recording':'⏸ Arrêter l’enregistrement',
  'voice.paused':'▶️ Reprendre l’enregistrement',
  'voice.clear_btn':'🗑️ Tout effacer et recommencer',
  'voice.not_supported':'⚠️ Ce navigateur ne prend pas en charge l’enregistrement',
  'voice.https_only':'🔒 Fonctionne uniquement sur le site officiel',

  // ===== Retour (correct/incorrect) =====
  'feedback.correct_full':'✓ Bravo ! Réponse entièrement correcte 🌟',
  'feedback.correct_mcq':'✓ Bravo ! 🌟',
  'feedback.wrong_full_prefix':'✗ La bonne réponse :',
  'feedback.wrong_mcq_prefix':'✗ La bonne réponse : ',
  'feedback.skip_prefix':'⬅ La bonne réponse :',
  'feedback.words_correct_count':'{correct} / {total} mots corrects',
  'feedback.words_extra':' — plus {extra} mot(s) en trop',
  'feedback.accuracy_line':'Précision de cette réponse : {pct}% ({matched} sur {total} mots)',
  'feedback.accuracy_total_line':'Total : {pct}% ({correct} sur {total} mots)',

  // ===== Revue / classement — textes supplémentaires =====
  'review.number_label':'Revue {cur} sur {total}',
  'order.dot_active_title':'Case actuellement active',
  'order.dot_jump_title':'Touchez pour continuer à partir d’ici',
  'order.result_line':'{correct} / {total} dans le bon ordre',
  'order.result_review_label':'Ordre correct pour la révision :',
  'oh.step1_act':'Placez un verset dans la séquence',
  'oh.step1_why':'Touchez n’importe quel verset ci-dessous pour le placer dans la case active (le cercle vert).',
  'oh.step2_act':'Choisissez une case, puis remplissez-la',
  'oh.step2_why':'Les cercles en pointillés sont les cases vides. Touchez-en une pour l’activer, puis touchez un verset pour le placer là — pas dans la case suivante.',
  'oh.step3_act':'Sélectionnez un verset à échanger',
  'oh.step3_why':'Touchez le numéro du verset — pas son texte — un cadre doré apparaît alors autour de lui.',
  'oh.step4_act':'Échangez les deux versets',
  'oh.step4_why':'Touchez le numéro d’un autre verset pour échanger leurs places. Touchez le même numéro à nouveau pour désélectionner.',
  'oh.step5_act':'Retirez un verset de la séquence',
  'oh.step5_why':'Touchez le texte du verset à l’intérieur de sa case pour le renvoyer en bas et vider sa case.',
  'oh.seg1':'Le premier verset',
  'oh.seg2':'Le deuxième verset',
  'oh.seg3':'Le troisième verset'
},

tr: {
  // ===== Genel / gezinme =====
  'nav.tools_title':'Araçlar',
  'nav.lang_label':'Dil',
  'nav.feedback':'Öneriler',
  'nav.share':'Sayfayı paylaş',
  'nav.qr':'QR kodu',
  'nav.about':'📖 Proje hakkında',
  'nav.progress':'📊 İlerlemem',
  'nav.back':'← Geri',

  // ===== Ana sayfa =====
  'home.title':'Darbi — Kur’an Ezberleme',
  'home.subtitle':'Ezberini sayfa sayfa test et — tekrar etmek ve pekiştirmek için etkileşimli testler',
  'home.recite_btn':'🎤 Ezberini test et',
  'home.progress_btn':'📊 İlerlemem',
  'home.progress_btn_sub':'İlerleme ayrıntılarım ◀',
  'home.stat_tests':'test mevcut',
  'home.stat_parts':'bölüm',
  'home.stat_surahs':'sure',
  'home.beta_tag':'✦ Beta sürümü',
  'home.beta_text_prefix':'Şunları bekliyoruz: ',
  'home.beta_link':'geri bildirim ve önerileriniz',
  'home.search_placeholder':'Bir sure veya sayfa ara...',
  'home.filter_all':'Tüm bölümler',
  'home.filter_built':'Şu an mevcut',
  'home.filter_soon':'Yakında',
  'home.filter_empty':'Şu anda bu filtreyle eşleşen bölüm yok.',
  'home.juz_prefix':'Cüz',
  'home.juz_soon':'Yakında',
  'home.juz_surahs_count':'{n} sure',
  'home.juz_available_count':'{n} mevcut',
  'home.juz_completed_count':'{done} / {total} tamamlandı',
  'home.card_soon_badge':'Yakında',
  'home.card_complete_badge':'✓ Tamamlandı',
  'home.lvl_easy_title':'Kolay',
  'home.lvl_medium_title':'Orta',
  'home.lvl_hard_title':'Zor',
  'home.hero_progress_line':'{total} sayfadan {done} tanesini tamamladın (%{pct})',
  'home.hero_last_visited':'Son tekrar: {name}',
  'home.about_title':'Proje hakkında',
  'home.about_p1':'"Darbi", çeşitli testler aracılığıyla herkesin Allah’ın Kitabı’nı ezberlemesine ve tekrar etmesine yardımcı olan etkileşimli bir platformdur.',
  'home.about_p2':'Ezberi pekiştirmek ve ustalığı güçlendirmek için Kur’an’daki benzer/tekrar eden ayetlere (müteşabihat) odaklanılarak dikkatle tasarlanmıştır.',
  'home.footer_copy':'Darbi — Kur’an Ezberleme. Tüm hakları saklıdır',

  // ===== Geri bildirim penceresi =====
  'fdbk.title':'💬 Görüşünü paylaş',
  'fdbk.type_label':'Geri bildirim türü',
  'fdbk.type_quran':'Kur’an metninde hata',
  'fdbk.type_question':'Soru veya cevapta hata',
  'fdbk.type_voice':'Sesli kayıt sorunu',
  'fdbk.type_design':'Tasarım veya görüntüleme sorunu',
  'fdbk.type_suggestion':'İyileştirme önerisi',
  'fdbk.type_other':'Diğer',
  'fdbk.note_label':'Ayrıntılar (isteğe bağlı)',
  'fdbk.note_placeholder':'Notunu buraya yaz...',
  'fdbk.send':'WhatsApp ile gönder',
  'fdbk.cancel':'İptal',

  // ===== QR kod penceresi =====
  'qr.title':'🔲 Bu sayfayı açmak için tara',
  'qr.caption':'Siteyi telefonunda açmak için kodu tara',
  'qr.copy_btn':'📋 Bağlantıyı kopyala',
  'qr.copied':'✅ Kopyalandı',
  'qr.copy_failed':'Kopyalanamadı',
  'qr.close_btn':'Kapat',
  'qr.img_alt':'Bu sayfayı telefonunda açmak için QR kodu',

  // ===== Test sayfası: üst bilgi =====
  'quiz.stat_question':'Soru',
  'quiz.stat_wrong':'Yanlış',
  'quiz.stat_correct':'Doğru',
  'quiz.resume_text':'📌 Tamamlanmamış bir testin var. Kaldığın yerden devam mı etmek istersin, yoksa baştan mı başlamak?',
  'quiz.resume_continue':'Buradan devam et',
  'quiz.resume_restart':'Baştan başla',
  'quiz.recite_test_link':'🎤 Kıraatini test et',

  // ===== Seviye seçimi =====
  'level.choose_title':'Bir test seviyesi seç',
  'level.choose_sub':'Her seviye seni farklı bir şekilde test eder',
  'level.easy_name':'Kolay',
  'level.easy_desc':'Doğru cevabı seç',
  'level.medium_name':'Orta',
  'level.medium_desc':'Boşluğu tamamla',
  'level.hard_name':'Zor',
  'level.hard_desc':'Ayetin tamamını yaz',
  'level.order_name':'Sıralama',
  'level.order_desc':'Ayetleri sıraya diz',
  'level.start_btn':'Testi başlat ←',
  'level.prev_page':'⏮️ Önceki sayfa',
  'level.next_page':'Sonraki sayfa ⏭️',

  // ===== Test sırasında =====
  'quiz.q_number':'Soru {cur} / {total}',
  'quiz.q_number_short':'Soru {cur} /',
  'quiz.prev_q':'→ Önceki soru',
  'quiz.skip_q':'⏭ Geç',
  'quiz.next_q':'Sonraki soru ←',
  'quiz.return_to_levels':'🔄 Başka bir test seç',
  'quiz.medium_placeholder':'Eksik kelimeyi yaz...',
  'quiz.hard_placeholder':'Ayetin tamamını yaz...',
  'quiz.hard_placeholder_plural':'Ayetlerin tamamını yaz...',
  'quiz.submit_check':'Kontrol et ✓',
  'quiz.ayah_label':'{n}. Ayet',

  // ===== Sıralama =====
  'order.instruction':'Ayetleri sıraya diz — sırayla yerleştirmek için bir ayete dokun. Bir hücreyi atlamak mı istiyorsun? Devam etmek istediğin hücreye dokun.',
  'order.help_btn':'? Sıralama nasıl çalışır',
  'order.help_title':'Sıralama nasıl çalışır',
  'order.help_prev':'← Önceki',
  'order.help_stop':'⏸ Durdur',
  'order.help_play':'▶ Oynat',
  'order.help_next':'Sonraki →',
  'order.help_start_btn':'Sıralamaya başla',
  'order.reveal_btn':'💡 Doğru sırayı göster',
  'order.check_btn':'Kontrol et ✓',
  'order.selected_label':'Seçili: ',
  'order.selected_suffix':' — bir değişim seç',
  'order.delete_btn':'✕ Kaldır',
  'order.select_title':'Seçmek için dokun, sonra bir değişim seç',
  'order.deselect_title':'Seçimi kaldırmak için dokun',
  'order.final_step_caption':'✓ İşte bütün hareketler',
  'order.final_step_why':'Tüm hücreler dolduğunda, sıralamanı kontrol etmek için "Kontrol et ✓" düğmesi görünür.',

  // ===== Sonuç =====
  'result.perfect_title':'Mükemmel! Kusursuz ezber',
  'result.perfect_msg':'Maşallah! Sayfayı tamamen öğrendin',
  'result.great_title':'Aferin!',
  'result.great_msg':'Harika bir sonuç, tekrar etmeye devam et',
  'result.good_title':'İyi',
  'result.good_msg':'Sureyi tekrar gözden geçir ve testi yeniden çöz',
  'result.weak_title':'Tekrar gerekiyor',
  'result.weak_msg':'Umutsuzluğa kapılma, düzenli tekrar başarının anahtarıdır',
  'result.score_line':'{wc} / {wt} kelime — %{pct}  |  {cc} / {qt} soru',
  'result.review_mistakes':'📝 Hatalarımı gözden geçir',
  'result.retry':'🔄 Başka bir test seç',
  'result.home_link':'← Ana sayfa',

  // ===== Hata gözden geçirme =====
  'review.prev':'→ Önceki',
  'review.next':'Sonraki ←',
  'review.end':'Gözden geçirmeyi bitir',

  // ===== İpucu (zor seviye) =====
  'hint.btn':'💡 İpucu (ilk 3 kelime)',
  'voice.record_btn':'🎤 Sesli kayıt',
  'voice.text_btn':'⌨️ Yazarak',
  'voice.press_to_record':'🎤 Kayıt için dokun',
  'voice.recording':'⏸ Kaydı durdur',
  'voice.paused':'▶️ Kayda devam et',
  'voice.clear_btn':'🗑️ Tümünü sil ve baştan başla',
  'voice.not_supported':'⚠️ Bu tarayıcı kaydı desteklemiyor',
  'voice.https_only':'🔒 Yalnızca resmî sitede çalışır',

  // ===== Geri bildirim (doğru/yanlış) =====
  'feedback.correct_full':'✓ Aferin! Tamamen doğru 🌟',
  'feedback.correct_mcq':'✓ Aferin! 🌟',
  'feedback.wrong_full_prefix':'✗ Doğru cevap:',
  'feedback.wrong_mcq_prefix':'✗ Doğru cevap: ',
  'feedback.skip_prefix':'⬅ Doğru cevap:',
  'feedback.words_correct_count':'{correct} / {total} kelime doğru',
  'feedback.words_extra':' — ayrıca {extra} fazladan kelime',
  'feedback.accuracy_line':'Bu cevabın doğruluğu: %{pct} ({total} kelimeden {matched} tanesi)',
  'feedback.accuracy_total_line':'Genel toplam: %{pct} ({total} kelimeden {correct} tanesi)',

  // ===== Gözden geçirme / sıralama — ek metinler =====
  'review.number_label':'Gözden geçirme {cur} / {total}',
  'order.dot_active_title':'Şu anda etkin hücre',
  'order.dot_jump_title':'Buradan devam etmek için dokun',
  'order.result_line':'{correct} / {total} doğru sırada',
  'order.result_review_label':'Gözden geçirmek için doğru sıra:',
  'oh.step1_act':'Sıraya bir ayet yerleştir',
  'oh.step1_why':'Aşağıdaki herhangi bir ayete dokunarak onu etkin hücreye (yeşil daire) yerleştir.',
  'oh.step2_act':'Bir hücre seç, sonra doldur',
  'oh.step2_why':'Kesikli daireler boş hücrelerdir. Birini etkinleştirmek için dokun, sonra bir ayete dokunarak onu oraya yerleştir — bir sonrakine değil.',
  'oh.step3_act':'Değiştirmek için bir ayet seç',
  'oh.step3_why':'Ayetin metnine değil, numarasına dokun — etrafında altın rengi bir çerçeve belirir.',
  'oh.step4_act':'İki ayeti birbiriyle değiştir',
  'oh.step4_why':'Yerlerini değiştirmek için başka bir ayetin numarasına dokun. Seçimi kaldırmak için aynı numaraya yeniden dokun.',
  'oh.step5_act':'Bir ayeti sıradan çıkar',
  'oh.step5_why':'Kutusunun içindeki ayet metnine dokunarak onu aşağıya geri gönder ve hücresini boşalt.',
  'oh.seg1':'İlk ayet',
  'oh.seg2':'İkinci ayet',
  'oh.seg3':'Üçüncü ayet'
}
,

de: {
  // ===== Allgemein / Navigation =====
  'nav.tools_title':'Werkzeuge',
  'nav.lang_label':'Sprache',
  'nav.feedback':'Feedback',
  'nav.share':'Seite teilen',
  'nav.qr':'QR-Code',
  'nav.about':'📖 Über das Projekt',
  'nav.progress':'📊 Mein Fortschritt',
  'nav.back':'← Zurück',

  // ===== Startseite =====
  'home.title':'Quran Darbi — Auswendiglernen',
  'home.subtitle':'Teste dein Auswendiglernen Seite für Seite — interaktive Quizze zur Wiederholung und Festigung',
  'home.recite_btn':'🎤 Teste deine Rezitation',
  'home.progress_btn':'📊 Mein Fortschritt',
  'home.progress_btn_sub':'Alle Fortschrittsdetails ◀',
  'home.stat_tests':'verfügbare Quizze',
  'home.stat_parts':'Teile',
  'home.stat_surahs':'Suren',
  'home.beta_tag':'✦ Beta-Start',
  'home.beta_text_prefix':'Wir freuen uns über dein ',
  'home.beta_link':'Feedback und deine Vorschläge',
  'home.search_placeholder':'Suche nach einer Sure oder Seite...',
  'home.filter_all':'Alle Teile',
  'home.filter_built':'Jetzt verfügbar',
  'home.filter_soon':'Demnächst',
  'home.filter_empty':'Kein Teil entspricht diesem Filter.',
  'home.juz_prefix':'Juz’',
  'home.juz_soon':'Demnächst',
  'home.juz_surahs_count':'{n} Suren',
  'home.juz_available_count':'{n} verfügbar',
  'home.juz_completed_count':'{done} / {total} abgeschlossen',
  'home.card_soon_badge':'Bald',
  'home.card_complete_badge':'✓ Fertig',
  'home.lvl_easy_title':'Leicht',
  'home.lvl_medium_title':'Mittel',
  'home.lvl_hard_title':'Schwer',
  'home.hero_progress_line':'Du hast {done} von {total} Seiten abgeschlossen ({pct}%)',
  'home.hero_last_visited':'Zuletzt wiederholt: {name}',
  'home.about_title':'Über das Projekt',
  'home.about_p1':'"Darbi" ist eine interaktive Plattform, die jedem hilft, das Buch Gottes auswendig zu lernen und durch vielfältige Quizze zu wiederholen.',
  'home.about_p2':'Sorgfältig gestaltet, um das Auswendiglernen zu festigen und die Beherrschung zu schärfen, mit besonderem Fokus auf die einander ähnlichen/wiederkehrenden Verse des Korans (mutaschabihat).',
  'home.footer_copy':'Darbi — Koran-Auswendiglernen. Alle Rechte vorbehalten',

  // ===== Feedback-Modal =====
  'fdbk.title':'💬 Teile dein Feedback',
  'fdbk.type_label':'Art des Feedbacks',
  'fdbk.type_quran':'Fehler im Korantext',
  'fdbk.type_question':'Fehler in einer Frage oder Antwort',
  'fdbk.type_voice':'Problem mit der Sprachaufnahme',
  'fdbk.type_design':'Design- oder Anzeigeproblem',
  'fdbk.type_suggestion':'Verbesserungsvorschlag',
  'fdbk.type_other':'Sonstiges',
  'fdbk.note_label':'Details (optional)',
  'fdbk.note_placeholder':'Schreibe hier deine Notiz...',
  'fdbk.send':'Über WhatsApp senden',
  'fdbk.cancel':'Abbrechen',

  // ===== QR-Modal =====
  'qr.title':'🔲 Scannen, um diese Seite zu öffnen',
  'qr.caption':'Scanne den Code, um die Seite auf deinem Handy zu öffnen',
  'qr.copy_btn':'📋 Link kopieren',
  'qr.copied':'✅ Kopiert',
  'qr.copy_failed':'Kopieren fehlgeschlagen',
  'qr.close_btn':'Schließen',
  'qr.img_alt':'QR-Code zum Öffnen dieser Seite auf deinem Handy',

  // ===== Quiz-Kopfzeile/Infos =====
  'quiz.stat_question':'Frage',
  'quiz.stat_wrong':'Falsch',
  'quiz.stat_correct':'Richtig',
  'quiz.resume_text':'📌 Du hast ein unvollendetes Quiz. Dort weitermachen oder von vorne beginnen?',
  'quiz.resume_continue':'Weiter',
  'quiz.resume_restart':'Von vorne beginnen',
  'quiz.recite_test_link':'🎤 Teste deine Rezitation',

  // ===== Level-Auswahl =====
  'level.choose_title':'Wähle ein Quiz-Level',
  'level.choose_sub':'Jedes Level testet dich auf andere Weise',
  'level.easy_name':'Leicht',
  'level.easy_desc':'Wähle die richtige Antwort',
  'level.medium_name':'Mittel',
  'level.medium_desc':'Fülle die Lücke aus',
  'level.hard_name':'Schwer',
  'level.hard_desc':'Schreibe die vollständige Ayah',
  'level.order_name':'Reihenfolge',
  'level.order_desc':'Bringe die Ayat in die richtige Reihenfolge',
  'level.start_btn':'Quiz starten ←',
  'level.prev_page':'⏮️ Vorherige Seite',
  'level.next_page':'Nächste Seite ⏭️',

  // ===== Während des Quiz =====
  'quiz.q_number':'Frage {cur} von {total}',
  'quiz.q_number_short':'Frage {cur} /',
  'quiz.prev_q':'→ Vorherige Frage',
  'quiz.skip_q':'⏭ Überspringen',
  'quiz.next_q':'Nächste Frage ←',
  'quiz.return_to_levels':'🔄 Anderes Quiz wählen',
  'quiz.medium_placeholder':'Gib das fehlende Wort ein...',
  'quiz.hard_placeholder':'Gib die vollständige Ayah ein...',
  'quiz.hard_placeholder_plural':'Gib die vollständigen Ayat ein...',
  'quiz.submit_check':'Prüfen ✓',
  'quiz.ayah_label':'Ayah {n}',

  // ===== Reihenfolge =====
  'order.instruction':'Bringe die Ayat in die richtige Reihenfolge — tippe eine Ayah an, um sie einzusetzen. Möchtest du einen Platz überspringen? Tippe den Platz an, ab dem du fortfahren möchtest.',
  'order.help_btn':'? Wie die Reihenfolge funktioniert',
  'order.help_title':'Wie die Reihenfolge funktioniert',
  'order.help_prev':'← Zurück',
  'order.help_stop':'⏸ Stopp',
  'order.help_play':'▶ Abspielen',
  'order.help_next':'Weiter →',
  'order.help_start_btn':'Reihenfolge starten',
  'order.reveal_btn':'💡 Richtige Reihenfolge zeigen',
  'order.check_btn':'Prüfen ✓',
  'order.selected_label':'Ausgewählt: ',
  'order.selected_suffix':' — tippe einen Ersatz an',
  'order.delete_btn':'✕ Entfernen',
  'order.select_title':'Antippen zum Auswählen, dann einen Ersatz antippen',
  'order.deselect_title':'Antippen zum Abwählen',
  'order.final_step_caption':'✓ Das sind alle Schritte',
  'order.final_step_why':'Sobald jeder Platz gefüllt ist, erscheint die Schaltfläche „Prüfen ✓“, um deine Reihenfolge zu bewerten.',

  // ===== Ergebnis =====
  'result.perfect_title':'Ausgezeichnet! Perfektes Auswendiglernen',
  'result.perfect_msg':'Maschallah! Du beherrschst die ganze Seite',
  'result.great_title':'Gut gemacht!',
  'result.great_msg':'Großartiges Ergebnis — mach mit der Wiederholung weiter',
  'result.good_title':'Gut',
  'result.good_msg':'Wiederhole die Sure erneut und mach das Quiz noch einmal',
  'result.weak_title':'Braucht mehr Wiederholung',
  'result.weak_msg':'Keine Sorge — regelmäßige Wiederholung ist der Schlüssel',
  'result.score_line':'{wc} / {wt} Wörter — {pct}%  |  {cc} / {qt} Fragen',
  'result.review_mistakes':'📝 Meine Fehler überprüfen',
  'result.retry':'🔄 Anderes Quiz wählen',
  'result.home_link':'← Startseite',

  // ===== Fehlerüberprüfung =====
  'review.prev':'→ Zurück',
  'review.next':'Weiter ←',
  'review.end':'Wiederholung beenden',

  // ===== Hinweis (schweres Level) =====
  'hint.btn':'💡 Hinweis (erste 3 Wörter)',
  'voice.record_btn':'🎤 Sprachaufnahme',
  'voice.text_btn':'⌨️ Tippen',
  'voice.press_to_record':'🎤 Zum Aufnehmen antippen',
  'voice.recording':'⏸ Aufnahme stoppen',
  'voice.paused':'▶️ Aufnahme fortsetzen',
  'voice.clear_btn':'🗑️ Alles löschen und neu beginnen',
  'voice.not_supported':'⚠️ Dieser Browser unterstützt keine Aufnahme',
  'voice.https_only':'🔒 Funktioniert nur auf der offiziellen Seite',

  // ===== Feedback (richtig/falsch) =====
  'feedback.correct_full':'✓ Gut gemacht! Vollständig richtig 🌟',
  'feedback.correct_mcq':'✓ Gut gemacht! 🌟',
  'feedback.wrong_full_prefix':'✗ Die richtige Antwort:',
  'feedback.wrong_mcq_prefix':'✗ Die richtige Antwort: ',
  'feedback.skip_prefix':'⬅ Die richtige Antwort:',
  'feedback.words_correct_count':'{correct} / {total} Wörter richtig',
  'feedback.words_extra':' — plus {extra} zusätzliche(s) Wort(e)',
  'feedback.accuracy_line':'Genauigkeit dieser Antwort: {pct}% ({matched} von {total} Wörtern)',
  'feedback.accuracy_total_line':'Gesamt: {pct}% ({correct} von {total} Wörtern)',

  // ===== Überprüfung / Reihenfolge — zusätzliche Texte =====
  'review.number_label':'Überprüfung {cur} von {total}',
  'order.dot_active_title':'Aktuell aktiver Platz',
  'order.dot_jump_title':'Antippen, um von hier fortzufahren',
  'order.result_line':'{correct} / {total} in der richtigen Reihenfolge',
  'order.result_review_label':'Richtige Reihenfolge zur Überprüfung:',
  'oh.step1_act':'Eine Ayah in die Sequenz einsetzen',
  'oh.step1_why':'Tippe unten eine beliebige Ayah an, um sie in den aktiven Platz (den grünen Kreis) zu setzen.',
  'oh.step2_act':'Einen Platz auswählen und dann füllen',
  'oh.step2_why':'Die gestrichelten Kreise sind die leeren Plätze. Tippe einen an, um ihn zu aktivieren, und tippe dann eine Ayah an, um sie dort einzusetzen — nicht in den nächsten.',
  'oh.step3_act':'Eine Ayah zum Tauschen auswählen',
  'oh.step3_why':'Tippe auf die Nummer der Ayah — nicht auf ihren Text — und ein goldener Rahmen erscheint um sie.',
  'oh.step4_act':'Die beiden Ayat tauschen',
  'oh.step4_why':'Tippe auf die Nummer einer anderen Ayah, um die Plätze zu tauschen. Tippe erneut auf dieselbe Nummer, um die Auswahl aufzuheben.',
  'oh.step5_act':'Eine Ayah aus der Sequenz entfernen',
  'oh.step5_why':'Tippe auf den Text der Ayah in ihrem Kästchen, um sie zurückzuschicken und ihren Platz zu leeren.',
  'oh.seg1':'Die erste Ayah',
  'oh.seg2':'Die zweite Ayah',
  'oh.seg3':'Die dritte Ayah'
},

es: {
  // ===== General / navegación =====
  'nav.tools_title':'Herramientas',
  'nav.lang_label':'Idioma',
  'nav.feedback':'Comentarios',
  'nav.share':'Compartir página',
  'nav.qr':'Código QR',
  'nav.about':'📖 Acerca del proyecto',
  'nav.progress':'📊 Mi progreso',
  'nav.back':'← Volver',

  // ===== Página de inicio =====
  'home.title':'Quran Darbi — Memorización',
  'home.subtitle':'Pon a prueba tu memorización página por página — cuestionarios interactivos para repasar y reforzar',
  'home.recite_btn':'🎤 Pon a prueba tu recitación',
  'home.progress_btn':'📊 Mi progreso',
  'home.progress_btn_sub':'Ver todos los detalles del progreso ◀',
  'home.stat_tests':'cuestionarios disponibles',
  'home.stat_parts':'partes',
  'home.stat_surahs':'suras',
  'home.beta_tag':'✦ Lanzamiento beta',
  'home.beta_text_prefix':'Agradecemos tus ',
  'home.beta_link':'comentarios y sugerencias',
  'home.search_placeholder':'Buscar una sura o página...',
  'home.filter_all':'Todas las partes',
  'home.filter_built':'Disponible ahora',
  'home.filter_soon':'Próximamente',
  'home.filter_empty':'Ninguna parte coincide con este filtro por ahora.',
  'home.juz_prefix':'Juz’',
  'home.juz_soon':'Próximamente',
  'home.juz_surahs_count':'{n} suras',
  'home.juz_available_count':'{n} disponibles',
  'home.juz_completed_count':'{done} / {total} completadas',
  'home.card_soon_badge':'Pronto',
  'home.card_complete_badge':'✓ Hecho',
  'home.lvl_easy_title':'Fácil',
  'home.lvl_medium_title':'Medio',
  'home.lvl_hard_title':'Difícil',
  'home.hero_progress_line':'Has completado {done} de {total} páginas ({pct}%)',
  'home.hero_last_visited':'Última revisión: {name}',
  'home.about_title':'Acerca del proyecto',
  'home.about_p1':'"Darbi" es una plataforma interactiva que ayuda a todos a memorizar y repasar el Libro de Dios mediante una variedad de cuestionarios.',
  'home.about_p2':'Diseñada cuidadosamente para consolidar la memorización y afinar el dominio, con especial atención a los versículos similares/recurrentes del Corán (mutashabihat).',
  'home.footer_copy':'Darbi — Memorización del Corán. Todos los derechos reservados',

  // ===== Modal de comentarios =====
  'fdbk.title':'💬 Comparte tu opinión',
  'fdbk.type_label':'Tipo de comentario',
  'fdbk.type_quran':'Error en el texto coránico',
  'fdbk.type_question':'Error en una pregunta o respuesta',
  'fdbk.type_voice':'Problema con la grabación de voz',
  'fdbk.type_design':'Problema de diseño o visualización',
  'fdbk.type_suggestion':'Sugerencia de mejora',
  'fdbk.type_other':'Otro',
  'fdbk.note_label':'Detalles (opcional)',
  'fdbk.note_placeholder':'Escribe tu nota aquí...',
  'fdbk.send':'Enviar por WhatsApp',
  'fdbk.cancel':'Cancelar',

  // ===== Modal de código QR =====
  'qr.title':'🔲 Escanea para abrir esta página',
  'qr.caption':'Escanea el código para abrir el sitio en tu teléfono',
  'qr.copy_btn':'📋 Copiar enlace',
  'qr.copied':'✅ Copiado',
  'qr.copy_failed':'Error al copiar',
  'qr.close_btn':'Cerrar',
  'qr.img_alt':'Código QR para abrir esta página en tu teléfono',

  // ===== Encabezado/información del cuestionario =====
  'quiz.stat_question':'Pregunta',
  'quiz.stat_wrong':'Incorrectas',
  'quiz.stat_correct':'Correctas',
  'quiz.resume_text':'📌 Tienes un cuestionario sin terminar. ¿Continuar donde lo dejaste o empezar de nuevo?',
  'quiz.resume_continue':'Continuar',
  'quiz.resume_restart':'Empezar de nuevo',
  'quiz.recite_test_link':'🎤 Pon a prueba tu recitación',

  // ===== Selección de nivel =====
  'level.choose_title':'Elige un nivel de cuestionario',
  'level.choose_sub':'Cada nivel te evalúa de una manera diferente',
  'level.easy_name':'Fácil',
  'level.easy_desc':'Elige la respuesta correcta',
  'level.medium_name':'Medio',
  'level.medium_desc':'Completa el espacio en blanco',
  'level.hard_name':'Difícil',
  'level.hard_desc':'Escribe la aleya completa',
  'level.order_name':'Orden',
  'level.order_desc':'Ordena las aleyas',
  'level.start_btn':'Comenzar el cuestionario ←',
  'level.prev_page':'⏮️ Página anterior',
  'level.next_page':'Página siguiente ⏭️',

  // ===== Durante el cuestionario =====
  'quiz.q_number':'Pregunta {cur} de {total}',
  'quiz.q_number_short':'Pregunta {cur} /',
  'quiz.prev_q':'→ Pregunta anterior',
  'quiz.skip_q':'⏭ Omitir',
  'quiz.next_q':'Pregunta siguiente ←',
  'quiz.return_to_levels':'🔄 Elegir otro cuestionario',
  'quiz.medium_placeholder':'Escribe la palabra que falta...',
  'quiz.hard_placeholder':'Escribe la aleya completa...',
  'quiz.hard_placeholder_plural':'Escribe las aleyas completas...',
  'quiz.submit_check':'Comprobar ✓',
  'quiz.ayah_label':'Aleya {n}',

  // ===== Ordenar =====
  'order.instruction':'Ordena las aleyas — toca una aleya para colocarla en la secuencia. ¿Quieres saltar una casilla? Toca la casilla desde la que quieres continuar.',
  'order.help_btn':'? Cómo funciona el orden',
  'order.help_title':'Cómo funciona el orden',
  'order.help_prev':'← Anterior',
  'order.help_stop':'⏸ Detener',
  'order.help_play':'▶ Reproducir',
  'order.help_next':'Siguiente →',
  'order.help_start_btn':'Empezar a ordenar',
  'order.reveal_btn':'💡 Mostrar el orden correcto',
  'order.check_btn':'Comprobar ✓',
  'order.selected_label':'Seleccionado: ',
  'order.selected_suffix':' — toca un reemplazo',
  'order.delete_btn':'✕ Quitar',
  'order.select_title':'Toca para seleccionarla, luego toca un reemplazo',
  'order.deselect_title':'Toca para deseleccionar',
  'order.final_step_caption':'✓ Eso es todo',
  'order.final_step_why':'Cuando todas las casillas estén llenas, aparecerá el botón "Comprobar ✓" para calificar tu orden.',

  // ===== Resultado =====
  'result.perfect_title':'¡Excelente! Memorización perfecta',
  'result.perfect_msg':'¡Mashallah! Dominas la página entera',
  'result.great_title':'¡Bien hecho!',
  'result.great_msg':'Gran resultado — sigue repasando',
  'result.good_title':'Bien',
  'result.good_msg':'Repasa la sura de nuevo y vuelve a hacer el cuestionario',
  'result.weak_title':'Necesita más repaso',
  'result.weak_msg':'No te preocupes — el repaso constante es la clave',
  'result.score_line':'{wc} / {wt} palabras — {pct}%  |  {cc} / {qt} preguntas',
  'result.review_mistakes':'📝 Revisar mis errores',
  'result.retry':'🔄 Elegir otro cuestionario',
  'result.home_link':'← Inicio',

  // ===== Repaso de errores =====
  'review.prev':'→ Anterior',
  'review.next':'Siguiente ←',
  'review.end':'Terminar repaso',

  // ===== Pista (nivel difícil) =====
  'hint.btn':'💡 Pista (primeras 3 palabras)',
  'voice.record_btn':'🎤 Grabación de voz',
  'voice.text_btn':'⌨️ Escribir',
  'voice.press_to_record':'🎤 Toca para grabar',
  'voice.recording':'⏸ Detener grabación',
  'voice.paused':'▶️ Reanudar grabación',
  'voice.clear_btn':'🗑️ Borrar todo y empezar de nuevo',
  'voice.not_supported':'⚠️ Este navegador no admite grabación',
  'voice.https_only':'🔒 Funciona solo en el sitio oficial',

  // ===== Comentario (correcto/incorrecto) =====
  'feedback.correct_full':'✓ ¡Bien hecho! Totalmente correcto 🌟',
  'feedback.correct_mcq':'✓ ¡Bien hecho! 🌟',
  'feedback.wrong_full_prefix':'✗ La respuesta correcta:',
  'feedback.wrong_mcq_prefix':'✗ La respuesta correcta: ',
  'feedback.skip_prefix':'⬅ La respuesta correcta:',
  'feedback.words_correct_count':'{correct} / {total} palabras correctas',
  'feedback.words_extra':' — más {extra} palabra(s) extra',
  'feedback.accuracy_line':'Precisión de esta respuesta: {pct}% ({matched} de {total} palabras)',
  'feedback.accuracy_total_line':'Total: {pct}% ({correct} de {total} palabras)',

  // ===== Repaso / orden — cadenas adicionales =====
  'review.number_label':'Repaso {cur} de {total}',
  'order.dot_active_title':'Casilla activa actual',
  'order.dot_jump_title':'Toca para continuar desde aquí',
  'order.result_line':'{correct} / {total} en el orden correcto',
  'order.result_review_label':'Orden correcto para repasar:',
  'oh.step1_act':'Colocar una aleya en la secuencia',
  'oh.step1_why':'Toca cualquier aleya de abajo para colocarla en la casilla activa (el círculo verde).',
  'oh.step2_act':'Elige una casilla y luego llénala',
  'oh.step2_why':'Los círculos discontinuos son las casillas vacías. Toca una para activarla y luego toca una aleya para colocarla ahí — no en la siguiente.',
  'oh.step3_act':'Selecciona una aleya para intercambiar',
  'oh.step3_why':'Toca el número de la aleya — no su texto — y aparecerá un contorno dorado alrededor.',
  'oh.step4_act':'Intercambia las dos aleyas',
  'oh.step4_why':'Toca el número de otra aleya para intercambiar sus lugares. Toca el mismo número de nuevo para deseleccionar.',
  'oh.step5_act':'Saca una aleya de la secuencia',
  'oh.step5_why':'Toca el texto de la aleya dentro de su casilla para devolverla y vaciar su lugar.',
  'oh.seg1':'La primera aleya',
  'oh.seg2':'La segunda aleya',
  'oh.seg3':'La tercera aleya'
},

fa: {
  // ===== عمومی / پیمایش =====
  'nav.tools_title':'ابزارها',
  'nav.lang_label':'زبان',
  'nav.feedback':'بازخورد',
  'nav.share':'اشتراک‌گذاری صفحه',
  'nav.qr':'کد QR',
  'nav.about':'📖 درباره‌ی پروژه',
  'nav.progress':'📊 پیشرفت من',
  'nav.back':'← بازگشت',

  // ===== صفحه اصلی =====
  'home.title':'قرآن دربی — حفظ قرآن',
  'home.subtitle':'حفظ خود را صفحه به صفحه بیازمایید — آزمون‌های تعاملی برای مرور و تثبیت',
  'home.recite_btn':'🎤 تلاوت خود را بیازمایید',
  'home.progress_btn':'📊 پیشرفت من',
  'home.progress_btn_sub':'جزئیات کامل پیشرفت ◀',
  'home.stat_tests':'آزمون موجود',
  'home.stat_parts':'جزء',
  'home.stat_surahs':'سوره',
  'home.beta_tag':'✦ راه‌اندازی نسخه آزمایشی',
  'home.beta_text_prefix':'از ',
  'home.beta_link':'بازخورد و پیشنهادهای شما استقبال می‌کنیم',
  'home.search_placeholder':'جستجوی سوره یا صفحه...',
  'home.filter_all':'همه‌ی جزءها',
  'home.filter_built':'اکنون در دسترس',
  'home.filter_soon':'به‌زودی',
  'home.filter_empty':'در حال حاضر هیچ جزئی با این فیلتر مطابقت ندارد.',
  'home.juz_prefix':'جزء',
  'home.juz_soon':'به‌زودی',
  'home.juz_surahs_count':'{n} سوره',
  'home.juz_available_count':'{n} در دسترس',
  'home.juz_completed_count':'{done} / {total} تکمیل‌شده',
  'home.card_soon_badge':'به‌زودی',
  'home.card_complete_badge':'✓ انجام‌شده',
  'home.lvl_easy_title':'آسان',
  'home.lvl_medium_title':'متوسط',
  'home.lvl_hard_title':'دشوار',
  'home.hero_progress_line':'شما {done} از {total} صفحه را تکمیل کرده‌اید ({pct}%)',
  'home.hero_last_visited':'آخرین مرور: {name}',
  'home.about_title':'درباره‌ی پروژه',
  'home.about_p1':'"دربی" یک پلتفرم تعاملی است که به همه کمک می‌کند کتاب خدا را از طریق آزمون‌های گوناگون حفظ و مرور کنند.',
  'home.about_p2':'با دقت طراحی‌شده برای تثبیت حفظ و تقویت تسلط، با تمرکز بر آیات متشابه/تکرارشونده‌ی قرآن.',
  'home.footer_copy':'دربی — حفظ قرآن. تمامی حقوق محفوظ است',

  // ===== پنجره بازخورد =====
  'fdbk.title':'💬 بازخورد خود را به اشتراک بگذارید',
  'fdbk.type_label':'نوع بازخورد',
  'fdbk.type_quran':'خطا در متن قرآن',
  'fdbk.type_question':'خطا در یک سؤال یا پاسخ',
  'fdbk.type_voice':'مشکل ضبط صدا',
  'fdbk.type_design':'مشکل طراحی یا نمایش',
  'fdbk.type_suggestion':'پیشنهاد بهبود',
  'fdbk.type_other':'سایر',
  'fdbk.note_label':'جزئیات (اختیاری)',
  'fdbk.note_placeholder':'یادداشت خود را اینجا بنویسید...',
  'fdbk.send':'ارسال از طریق واتساپ',
  'fdbk.cancel':'انصراف',

  // ===== پنجره کد QR =====
  'qr.title':'🔲 برای باز کردن این صفحه اسکن کنید',
  'qr.caption':'کد را اسکن کنید تا سایت روی گوشی شما باز شود',
  'qr.copy_btn':'📋 کپی پیوند',
  'qr.copied':'✅ کپی شد',
  'qr.copy_failed':'کپی ناموفق بود',
  'qr.close_btn':'بستن',
  'qr.img_alt':'کد QR برای باز کردن این صفحه روی گوشی شما',

  // ===== سربرگ/اطلاعات صفحه آزمون =====
  'quiz.stat_question':'سؤال',
  'quiz.stat_wrong':'غلط',
  'quiz.stat_correct':'درست',
  'quiz.resume_text':'📌 یک آزمون ناتمام دارید. از همان‌جا ادامه دهید یا از نو شروع کنید؟',
  'quiz.resume_continue':'ادامه',
  'quiz.resume_restart':'شروع دوباره',
  'quiz.recite_test_link':'🎤 تلاوت خود را بیازمایید',

  // ===== انتخاب سطح =====
  'level.choose_title':'سطح آزمون را انتخاب کنید',
  'level.choose_sub':'هر سطح شما را به شیوه‌ای متفاوت می‌آزماید',
  'level.easy_name':'آسان',
  'level.easy_desc':'پاسخ درست را انتخاب کنید',
  'level.medium_name':'متوسط',
  'level.medium_desc':'جای خالی را پر کنید',
  'level.hard_name':'دشوار',
  'level.hard_desc':'آیه کامل را بنویسید',
  'level.order_name':'ترتیب',
  'level.order_desc':'آیات را به ترتیب بچینید',
  'level.start_btn':'شروع آزمون ←',
  'level.prev_page':'⏮️ صفحه قبل',
  'level.next_page':'صفحه بعد ⏭️',

  // ===== در حین آزمون =====
  'quiz.q_number':'سؤال {cur} از {total}',
  'quiz.q_number_short':'سؤال {cur} /',
  'quiz.prev_q':'→ سؤال قبلی',
  'quiz.skip_q':'⏭ رد کردن',
  'quiz.next_q':'سؤال بعدی ←',
  'quiz.return_to_levels':'🔄 انتخاب آزمون دیگر',
  'quiz.medium_placeholder':'کلمه‌ی جاافتاده را بنویسید...',
  'quiz.hard_placeholder':'آیه کامل را بنویسید...',
  'quiz.hard_placeholder_plural':'آیات کامل را بنویسید...',
  'quiz.submit_check':'بررسی ✓',
  'quiz.ayah_label':'آیه {n}',

  // ===== ترتیب =====
  'order.instruction':'آیات را به ترتیب بچینید — برای قرار دادن یک آیه در توالی، روی آن ضربه بزنید. می‌خواهید از یک جایگاه رد شوید؟ روی جایگاهی که می‌خواهید از آن ادامه دهید ضربه بزنید.',
  'order.help_btn':'؟ چیدن ترتیب چگونه کار می‌کند',
  'order.help_title':'چیدن ترتیب چگونه کار می‌کند',
  'order.help_prev':'← قبلی',
  'order.help_stop':'⏸ توقف',
  'order.help_play':'▶ پخش',
  'order.help_next':'بعدی →',
  'order.help_start_btn':'شروع چیدمان',
  'order.reveal_btn':'💡 نمایش ترتیب درست',
  'order.check_btn':'بررسی ✓',
  'order.selected_label':'انتخاب‌شده: ',
  'order.selected_suffix':' — جایگزین را ضربه بزنید',
  'order.delete_btn':'✕ حذف',
  'order.select_title':'برای انتخاب ضربه بزنید، سپس جایگزین را ضربه بزنید',
  'order.deselect_title':'برای لغو انتخاب ضربه بزنید',
  'order.final_step_caption':'✓ همه‌ی حرکت‌ها همین‌هاست',
  'order.final_step_why':'وقتی همه‌ی جایگاه‌ها پر شوند، دکمه‌ی «بررسی ✓» برای نمره‌دهی به ترتیب شما ظاهر می‌شود.',

  // ===== نتیجه =====
  'result.perfect_title':'عالی! حفظ کامل و بی‌نقص',
  'result.perfect_msg':'ماشاءالله! کل صفحه را کاملاً مسلط شده‌اید',
  'result.great_title':'آفرین!',
  'result.great_msg':'نتیجه‌ی عالی — به مرور ادامه دهید',
  'result.good_title':'خوب',
  'result.good_msg':'سوره را دوباره مرور کنید و آزمون را از نو بزنید',
  'result.weak_title':'نیاز به مرور بیشتر',
  'result.weak_msg':'نگران نباشید — مرور مداوم کلید موفقیت است',
  'result.score_line':'{wc} / {wt} کلمه — {pct}%  |  {cc} / {qt} سؤال',
  'result.review_mistakes':'📝 مرور اشتباهاتم',
  'result.retry':'🔄 انتخاب آزمون دیگر',
  'result.home_link':'← خانه',

  // ===== مرور اشتباهات =====
  'review.prev':'→ قبلی',
  'review.next':'بعدی ←',
  'review.end':'پایان مرور',

  // ===== راهنمایی (سطح دشوار) =====
  'hint.btn':'💡 راهنمایی (۳ کلمه‌ی اول)',
  'voice.record_btn':'🎤 ضبط صدا',
  'voice.text_btn':'⌨️ تایپ',
  'voice.press_to_record':'🎤 برای ضبط ضربه بزنید',
  'voice.recording':'⏸ توقف ضبط',
  'voice.paused':'▶️ ادامه‌ی ضبط',
  'voice.clear_btn':'🗑️ پاک کردن همه و شروع دوباره',
  'voice.not_supported':'⚠️ این مرورگر از ضبط پشتیبانی نمی‌کند',
  'voice.https_only':'🔒 فقط روی سایت رسمی کار می‌کند',

  // ===== بازخورد (درست/غلط) =====
  'feedback.correct_full':'✓ آفرین! کاملاً درست 🌟',
  'feedback.correct_mcq':'✓ آفرین! 🌟',
  'feedback.wrong_full_prefix':'✗ پاسخ درست:',
  'feedback.wrong_mcq_prefix':'✗ پاسخ درست: ',
  'feedback.skip_prefix':'⬅ پاسخ درست:',
  'feedback.words_correct_count':'{correct} / {total} کلمه درست',
  'feedback.words_extra':' — به‌علاوه {extra} کلمه‌ی اضافه',
  'feedback.accuracy_line':'دقت این پاسخ: {pct}% ({matched} از {total} کلمه)',
  'feedback.accuracy_total_line':'کل: {pct}% ({correct} از {total} کلمه)',

  // ===== مرور / ترتیب — رشته‌های اضافی =====
  'review.number_label':'مرور {cur} از {total}',
  'order.dot_active_title':'جایگاه فعال کنونی',
  'order.dot_jump_title':'برای ادامه از اینجا ضربه بزنید',
  'order.result_line':'{correct} / {total} به ترتیب درست',
  'order.result_review_label':'ترتیب درست برای مرور:',
  'oh.step1_act':'قرار دادن یک آیه در توالی',
  'oh.step1_why':'روی هر آیه در پایین ضربه بزنید تا در جایگاه فعال (دایره‌ی سبز) قرار گیرد.',
  'oh.step2_act':'یک جایگاه را انتخاب کنید، سپس آن را پر کنید',
  'oh.step2_why':'دایره‌های نقطه‌چین جایگاه‌های خالی هستند. روی یکی ضربه بزنید تا فعال شود، سپس روی یک آیه ضربه بزنید تا در آنجا قرار گیرد — نه در جایگاه بعدی.',
  'oh.step3_act':'یک آیه را برای جابه‌جایی انتخاب کنید',
  'oh.step3_why':'روی شماره‌ی آیه ضربه بزنید — نه متن آن — و یک قاب طلایی دور آن ظاهر می‌شود.',
  'oh.step4_act':'دو آیه را جابه‌جا کنید',
  'oh.step4_why':'روی شماره‌ی آیه‌ی دیگری ضربه بزنید تا جای آن‌ها عوض شود. برای لغو انتخاب، دوباره روی همان شماره ضربه بزنید.',
  'oh.step5_act':'یک آیه را از توالی بیرون بکشید',
  'oh.step5_why':'روی متن آیه داخل جعبه‌اش ضربه بزنید تا به پایین بازگردد و جایگاهش خالی شود.',
  'oh.seg1':'آیه‌ی اول',
  'oh.seg2':'آیه‌ی دوم',
  'oh.seg3':'آیه‌ی سوم'
}

};

var SUPPORTED = ['ar','en','fr','tr','de','es','fa'];
var LANG_LABELS = {ar:'العربية', en:'🇬🇧 English', fr:'🇫🇷 Français', tr:'🇹🇷 Türkçe', de:'🇩🇪 Deutsch', es:'🇪🇸 Español', fa:'🇮🇷 فارسی'};

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
  document.documentElement.setAttribute('dir', (code==='ar'||code==='fa') ? 'rtl' : 'ltr');
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
