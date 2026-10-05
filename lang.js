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
  // ===== تحسينات صفحة تقدّمي (أكتوبر 2026) =====
  'progress.continue_title':'▶️ تابع من حيث توقفت',
  'progress.continue_btn':'تابع',
  'progress.goal_set_label':'اختر هدفك اليومي (عدد الصفحات):',
  'progress.goal_progress':'صفحات اليوم: {c} من {n}',
  'progress.review_today_title':'🔁 راجع اليوم',
  'progress.show_all':'عرض الكل ({n})',
  'progress.show_less':'عرض أقل',
  'progress.not_started':'سور لم تبدأ بعد ({n})',
  'progress.juz_label':'الجزء {n}',
  // ===== عام / التنقل =====
  'nav.tools_title':'الأدوات',
  'nav.lang_label':'اللغة',
  'nav.feedback':'الاقتراحات',
  'nav.share':'مشاركة الصفحة',
  'nav.qr':'كود QR',
  'nav.about':'📖 عن المشروع',
  'about.dua':'نسأل الله أن يجعل القرآن ربيع قلوبنا، ونور صدورنا، وأن يرزقنا حفظه وإتقانه والعمل به.',
  'nav.progress':'📊 تقدّمي',
  'nav.sync_signin':'☁️ تسجيل الدخول',
  'nav.font_size':'🔠 حجم الخط',
  'nav.sync_on':"☁️ تقدّمك محفوظ ✅",
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
  'about.role_title':'ما دور هذا الموقع؟',
  'about.role_p1':'هذا الموقع أداة مساعدة لتثبيت حفظ القرآن ومتشابهاته، ولا يُغني عن التلقي من شيخ مُتقِن؛ فالتشكيل وأحكام التجويد تُؤخذ بالسماع والمشافهة.',
  'about.role_p2':'فليكن مُعِينًا لك على الإتقان، لا بديلًا عن القراءة على أهل الإتقان.',
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
  'reminder.banner':'🌙 لم تبدأ وردك اليوم بعد — أكمل حفظك الآن',
  'reminder.tomorrow':'ذكّرني غدًا',
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
,


  // ===== اختبر تلاوتك (recitation.html) =====
  'recite.page_sub':'اختر السورة — اقرأ من أي آية تريد — الموقع يصحح كل كلمة',
  'recite.select_label':'اختر السورة أو الصفحة',
  'recite.search_placeholder':'🔍 ابحث باسم السورة أو رقم الصفحة',
  'recite.no_results':'لا توجد نتائج مطابقة',
  'recite.select_default_option':'— اختر —',
  'recite.placeholder_text':'سيظهر النص هنا...',
  'recite.prev_btn':'⏮️ السابق',
  'recite.next_btn':'التالي ⏭️',
  'recite.rec_desc_html':'اضغط 🎤 وابدأ التلاوة من أي آية<br>توقف متى شئت — سنحدد موضعك تلقائياً<br>🟢 صح &nbsp;|&nbsp; 🔴 غلط &nbsp;|&nbsp; ➖ محذوف',
  'recite.choose_surah_first':'اختر سورة أولاً',
  'recite.show_text_btn':'📖 اعرض نص السورة',
  'recite.hide_text_btn':'🙈 إخفاء النص',
  'recite.hint_used':'💡 اتستخدمت',
  'recite.clear_btn':'🗑️ مسح والبدء من جديد',
  'recite.check_btn':'✓ تحقق من التلاوة',
  'recite.result_label':'النتيجة',
  'recite.scope_note':'ℹ️ هذا الاختبار يتحقق من الكلمات وترتيبها في حفظك، ولا يتحقق حالياً من دقة الحركات (التشكيل) أو أحكام التجويد والمدود — هذا الجزء قيد البحث والتطوير.',
  'recite.legend_correct':'صحيحة',
  'recite.legend_wrong':'خاطئة',
  'recite.legend_missing':'محذوفة',
  'recite.retry_btn':'🔄 إعادة التسجيل',
  'recite.selected_info':'✓ {name} — {count} كلمة',
  'recite.btn_start':'🎤 اضغط وابدأ التلاوة',
  'recite.btn_pause':'⏸ إيقاف مؤقت',
  'recite.btn_resume':'▶️ استمر في التلاوة',
  'recite.said_prefix':'قلت: ',
  'recite.where_start':'بدأت من أول السورة',
  'recite.where_approx':'📍 بدأت من الكلمة {n} تقريباً',
  'recite.pct_label':'٪ {pct}',
  'recite.result_perfect':'🌟 ممتاز! حفظك مطابق للنص',
  'recite.result_great':'✨ أحسنت! حفظك قوي',
  'recite.result_good':'📖 جيد — راجع الكلمات الحمراء',
  'recite.result_weak':'💪 تحتاج مراجعة',
  'recite.err_inapp_browser':'⚠️ التسجيل الصوتي لا يعمل داخل متصفح التطبيق هذا (ماسنجر / إنستغرام / إلخ).\n\nافتح الموقع من متصفح Chrome مباشرة:\n1) اضغط على النقاط الثلاث (⋮) أعلى الصفحة\n2) اختر "افتح في المتصفح" أو "Open in Browser"\n\nأو انسخ رابط الموقع والصقه في تطبيق Chrome.',
  'recite.err_needs_chrome':'⚠️ التسجيل الصوتي يحتاج إلى متصفح Chrome ليعمل.\n\nإذا كنت على آيفون: حمّل تطبيق Chrome من App Store وافتح الموقع منه (وليس من Safari).\nوإذا كنت على أندرويد: افتح الموقع من تطبيق Chrome.',
  'recite.err_speech_blocked':'⚠️ تعذّر بدء التسجيل الصوتي.\n\nعلى آيباد أو آيفون: فعّل «الإملاء» من الإعدادات ← عام ← لوحة المفاتيح، واسمح للموقع باستخدام الميكروفون. وإن استمر العطل فافتح الموقع من تطبيق Chrome.',

  // ===== تقدّمي (progress.html) =====
  'progress.home_btn':'🏠 الرئيسية',
  'progress.subtitle':'تابع رحلتك في حفظ القرآن',
  'progress.subtitle_empty':'هذه بدايتك — ابدأ أول اختبار',
  'progress.subtitle_progress':'أنجزت {done} من {total} صفحة — استمر 🌿',
  'progress.streak_label':'يوم متتالٍ',
  'progress.streak_best_label':'أطول سلسلة',
  'progress.empty_text':'لم تبدأ رحلة الحفظ هنا بعد — ابدأ أول اختبار وسيظهر تقدّمك في هذه الصفحة أولًا بأول',
  'progress.empty_cta':'ابدأ الآن',
  'progress.goal_title':'🎯 هدفي اليومي',
  'progress.goal_not_done':'لم تنجز هدف اليوم بعد',
  'progress.goal_done_headline':'أنجزت هدف اليوم!',
  'progress.goal_desc':'الهدف: نشاط حفظ واحد يوميًا على الأقل',
  'progress.goal_done_msg':'أنجزت هدف اليوم — أحسنت!',
  'progress.badges_title':'🏅 الأوسمة',
  'progress.rec_stat_pages':'صفحات جرى اختبارها',
  'progress.rec_stat_best':'أفضل نسبة',
  'progress.rec_stat_tries':'محاولات',
  'progress.rec_last_title':'آخر المحاولات',
  'progress.rec_reached':'وصلت إلى الآية {a} — {c}٪ من الصفحة',
  'progress.rec_reached_noayah':'وصلت إلى {c}٪ من الصفحة',
  'progress.rec_empty':'لم تجرِ هذا الاختبار بعد. ابدأ الآن ليُسجَّل تقدمك هنا.',
  'progress.rec_go':'ابدأ الاختبار',
  'progress.rec_note':'النسبة تخص الكلمات وترتيبها، ولا تشمل الحركات وأحكام التجويد.',
  'progress.badge_rec_first':'أول اختبار صوتي',
  'progress.badge_rec_90':'دقة ٩٠٪ صوتيًا',
  'progress.badge_rec_surah':'سورة كاملة صوتيًا',
  'progress.badge_week':'أسبوع كامل',
  'progress.badge_first_juz':'أول جزء مكتمل',
  'progress.badge_30days':'٣٠ يوم متتالٍ',
  'progress.badge_100pages':'١٠٠ صفحة',
  'progress.badge_amma':'جزء عمّ كاملًا',
  'progress.badge_60days':'٦٠ يوم متتالٍ',
  'progress.badge_3surahs':'٣ سور كاملة',
  'progress.badge_300pages':'٣٠٠ صفحة',
  'progress.surah_progress_title':'📚 تقدّمك في كل سورة',
  'progress.filter_all_surahs':'كل السور',
  'progress.filter_complete':'مكتمل',
  'progress.filter_incomplete':'لم يكتمل بعد',
  'progress.filter_empty':'لا توجد سور مطابقة لهذا الفلتر حاليًا.',
  'progress.review_title':'🔁 قائمة المراجعة الذكية',
  'progress.review_empty':'لا توجد أسئلة بحاجة إلى مراجعة حاليًا — واصل هكذا 👏',
  'progress.review_remove':'حذف من قائمة المراجعة',
  'progress.question_label':'سؤال {n}',
  'progress.reminder_title':'🔔 التذكير اليومي',
  'progress.reminder_enable_label':'تفعيل إشعارات التذكير',
  'progress.reminder_enable_sub':'تصل حتى لو الموقع مغلق',
  'progress.reminder_time_label':'الوقت:',
  'progress.reminder_note':'الإشعار مبني على الوقت فقط، ولا يعرف هل أنجزتِ ورد اليوم أم لا (لأن الموقع بلا حسابات، وبياناتك محفوظة في متصفحك فقط). قد ينحرف التوقيت بضع دقائق أحيانًا.',
  'progress.reminder_coming_soon':'ميزة التذكير عبر الإشعارات قيد التفعيل حاليًا على هذا الموقع.',
  'progress.reminder_denied':'تم حظر إذن الإشعارات من إعدادات المتصفح لهذا الموقع — لتفعيله لاحقًا افتحي إعدادات الموقع في المتصفح واسمحي بالإشعارات',
  'progress.activating':'جارٍ التفعيل…',
  'progress.reminder_enabled':'تم تفعيل التذكير ✅',
  'progress.reminder_enable_fail':'تعذّر التفعيل: ',
  'progress.saving':'جارٍ الحفظ…',
  'progress.time_updated':'تم تحديث الوقت ✅',
  'progress.save_fail':'تعذّر الحفظ: ',
  'progress.backup_title':'💾 نسخة احتياطية',
  'progress.backup_none':'لم تُؤخذ أي نسخة احتياطية بعد',
  'progress.last_backup':'آخر نسخة احتياطية: ',
  'progress.backup_suggest':'⏰ مرّت فترة طويلة — يُستحسن أخذ نسخة احتياطية جديدة، لأن بياناتك محفوظة في هذا المتصفح فقط',
  'progress.backup_export_btn':'⬇️ تنزيل نسخة احتياطية',
  'progress.backup_import_btn':'⬆️ استيراد نسخة',
  'progress.backup_export_ok':'تم تنزيل النسخة الاحتياطية ✅',
  'progress.backup_import_ok':'تم استيراد النسخة الاحتياطية بنجاح ✅',
  'progress.backup_import_fail':'تعذّر الاستيراد: ',
  'progress.unknown_error':'خطأ غير معروف',
  'progress.sync_title':"☁️ احفظ تقدّمك على حسابك",
  'progress.sync_desc':"سجّل الدخول بحساب جوجل ليُحفظ تقدّمك ويظهر تلقائيًا على كل أجهزتك، حتى لو غيّرت الهاتف أو مسحت بيانات المتصفح.",
  'progress.sync_signin_btn':"🔵 المتابعة بحساب جوجل",
  'progress.sync_signout_btn':'تسجيل الخروج',
  'progress.sync_now_btn':"🔄 تحديث تقدّمي الآن",
  'progress.sync_signed_in_as':'تم تسجيل الدخول: ',
  'progress.sync_syncing':"جارٍ حفظ تقدّمك…",
  'progress.sync_ok':"تم حفظ تقدّمك ✅",
  'progress.sync_fail':"تعذّر حفظ تقدّمك: ",
  'progress.sync_unsupported':"ميزة حفظ التقدّم على الحساب غير متاحة على هذا المتصفح"
},

en: {
  // ===== تحسينات صفحة تقدّمي (أكتوبر 2026) =====
  'progress.continue_title':'▶️ Continue where you left off',
  'progress.continue_btn':'Continue',
  'progress.goal_set_label':'Choose your daily goal (pages):',
  'progress.goal_progress':'Today: {c} of {n} pages',
  'progress.review_today_title':'🔁 Review today',
  'progress.show_all':'Show all ({n})',
  'progress.show_less':'Show less',
  'progress.not_started':'Surahs not started yet ({n})',
  'progress.juz_label':'Juz’ {n}',
  // ===== General / navigation =====
  'nav.tools_title':'Tools',
  'nav.lang_label':'Language',
  'nav.feedback':'Feedback',
  'nav.share':'Share page',
  'nav.qr':'QR code',
  'nav.about':'📖 About',
  'about.dua':'We ask Allah to make the Qur’an the spring of our hearts and the light of our chests, and to grant us its memorization, mastery and practice.',
  'nav.progress':'📊 My Progress',
  'nav.sync_signin':'☁️ Sign in',
  'nav.font_size':'🔠 Text size',
  'nav.sync_on':"☁️ Progress saved ✅",
  'nav.back':'← Back',

  // ===== Home page =====
  'home.title':'Quran Darbi',
  'home.subtitle':'Test your memorization page by page — interactive quizzes to review and reinforce it',
  'home.recite_btn':'🎤 Recitation Test',
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
  'about.role_title':'What is the role of this site?',
  'about.role_p1':'This site is a helping tool for consolidating your memorization of the Quran and its similar verses (mutashabihat). It is not a substitute for learning from a qualified teacher (shaykh): vocalization and the rules of tajweed are taken through listening and direct oral transmission.',
  'about.role_p2':'Let it be an aid toward mastery, not a replacement for reciting to those who have mastered it.',
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
  'reminder.banner':'🌙 You haven’t started today’s portion yet — continue your memorization now',
  'reminder.tomorrow':'Remind me tomorrow',
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
,
  'recite.page_sub':'Choose a surah — recite from any ayah you like — the site corrects every word',
  'recite.select_label':'Choose the surah or page',
  'recite.search_placeholder':'🔍 Search by surah name or page number',
  'recite.no_results':'No matching results',
  'recite.select_default_option':'— Choose —',
  'recite.placeholder_text':'The text will appear here...',
  'recite.prev_btn':'⏮️ Previous',
  'recite.next_btn':'Next ⏭️',
  'recite.rec_desc_html':'Tap 🎤 and start reciting from any ayah<br>Stop whenever you like — we’ll detect your position automatically<br>🟢 Correct &nbsp;|&nbsp; 🔴 Wrong &nbsp;|&nbsp; ➖ Missing',
  'recite.choose_surah_first':'Choose a surah first',
  'recite.show_text_btn':'📖 Show the surah text',
  'recite.hide_text_btn':'🙈 Hide the text',
  'recite.hint_used':'💡 Used',
  'recite.clear_btn':'🗑️ Clear and start over',
  'recite.check_btn':'✓ Check the recitation',
  'recite.result_label':'Result',
  'recite.scope_note':'ℹ️ This test checks the words and their order in your memorization, and does not yet check the accuracy of diacritics or tajweed and madd rules — this part is still under research and development.',
  'recite.legend_correct':'Correct',
  'recite.legend_wrong':'Wrong',
  'recite.legend_missing':'Missing',
  'recite.retry_btn':'🔄 Record again',
  'recite.selected_info':'✓ {name} — {count} words',
  'recite.btn_start':'🎤 Tap to start reciting',
  'recite.btn_pause':'⏸ Pause',
  'recite.btn_resume':'▶️ Continue reciting',
  'recite.said_prefix':'You said: ',
  'recite.where_start':'You started from the beginning of the surah',
  'recite.where_approx':'📍 You started from around word {n}',
  'recite.pct_label':'{pct}%',
  'recite.result_perfect':'🌟 Excellent! Your memorization matches the text exactly',
  'recite.result_great':'✨ Well done! Your memorization is strong',
  'recite.result_good':'📖 Good — review the words in red',
  'recite.result_weak':'💪 Needs more review',
  'recite.err_inapp_browser':'⚠️ Voice recording does not work inside this app’s browser (Messenger / Instagram / etc.).\n\nOpen the site directly in Chrome:\n1) Tap the three dots (⋮) at the top of the page\n2) Choose "Open in Browser"\n\nOr copy the site link and paste it into the Chrome app.',
  'recite.err_needs_chrome':'⚠️ Voice recording needs the Chrome browser to work.\n\nIf you’re on iPhone: download the Chrome app from the App Store and open the site from it (not from Safari).\nIf you’re on Android: open the site from the Chrome app.',
  'recite.err_speech_blocked':'⚠️ Voice recording could not start.\n\nOn iPad or iPhone: turn on Dictation in Settings → General → Keyboard, and allow this site to use the microphone. If it still fails, open the site from the Chrome app.',
  'progress.home_btn':'🏠 Home',
  'progress.subtitle':'Track your Qur’an memorization journey',
  'progress.subtitle_empty':'This is your beginning — start your first test',
  'progress.subtitle_progress':'You’ve completed {done} of {total} pages — keep going 🌿',
  'progress.streak_label':'day streak',
  'progress.streak_best_label':'longest streak',
  'progress.empty_text':'You haven’t started your memorization journey here yet — start your first test and your progress will appear on this page as you go',
  'progress.empty_cta':'Start now',
  'progress.goal_title':'🎯 My daily goal',
  'progress.goal_not_done':'You haven’t completed today’s goal yet',
  'progress.goal_done_headline':'You’ve completed today’s goal!',
  'progress.goal_desc':'Goal: at least one memorization activity per day',
  'progress.goal_done_msg':'You’ve completed today’s goal — well done!',
  'progress.badges_title':'🏅 Badges',
  'progress.rec_stat_pages':'Pages tested',
  'progress.rec_stat_best':'Best score',
  'progress.rec_stat_tries':'Attempts',
  'progress.rec_last_title':'Latest attempts',
  'progress.rec_reached':'Reached ayah {a} — {c}% of the page',
  'progress.rec_reached_noayah':'Reached {c}% of the page',
  'progress.rec_empty':'You have not taken this test yet. Start now and your progress will appear here.',
  'progress.rec_go':'Start the test',
  'progress.rec_note':'The score covers words and their order only, not vowel marks or tajweed rules.',
  'progress.badge_rec_first':'First voice test',
  'progress.badge_rec_90':'90% by voice',
  'progress.badge_rec_surah':'Full surah by voice',
  'progress.badge_week':'Full week',
  'progress.badge_first_juz':'First juz’ completed',
  'progress.badge_30days':'30-day streak',
  'progress.badge_100pages':'100 pages',
  'progress.badge_amma':'Juz’ Amma completed',
  'progress.badge_60days':'60-day streak',
  'progress.badge_3surahs':'3 complete surahs',
  'progress.badge_300pages':'300 pages',
  'progress.surah_progress_title':'📚 Your progress in each surah',
  'progress.filter_all_surahs':'All surahs',
  'progress.filter_complete':'Completed',
  'progress.filter_incomplete':'Not completed yet',
  'progress.filter_empty':'No surahs match this filter right now.',
  'progress.review_title':'🔁 Smart review list',
  'progress.review_empty':'No questions need review right now — keep it up 👏',
  'progress.review_remove':'Remove from review list',
  'progress.question_label':'Question {n}',
  'progress.reminder_title':'🔔 Daily reminder',
  'progress.reminder_enable_label':'Enable reminder notifications',
  'progress.reminder_enable_sub':'Arrives even if the site is closed',
  'progress.reminder_time_label':'Time:',
  'progress.reminder_note':'The notification is based on time only, and doesn’t know whether you’ve completed today’s portion or not (since the site has no accounts, and your data is stored only in your browser). The timing may drift by a few minutes sometimes.',
  'progress.reminder_coming_soon':'The reminder notification feature is currently being rolled out on this site.',
  'progress.reminder_denied':'Notification permission has been blocked in the browser settings for this site — to enable it later, open the site settings in your browser and allow notifications',
  'progress.activating':'Enabling…',
  'progress.reminder_enabled':'Reminder enabled ✅',
  'progress.reminder_enable_fail':'Could not enable: ',
  'progress.saving':'Saving…',
  'progress.time_updated':'Time updated ✅',
  'progress.save_fail':'Could not save: ',
  'progress.backup_title':'💾 Backup',
  'progress.backup_none':'No backup has been taken yet',
  'progress.last_backup':'Last backup: ',
  'progress.backup_suggest':'⏰ It’s been a while — it’s best to take a new backup, since your data is stored only in this browser',
  'progress.backup_export_btn':'⬇️ Download backup',
  'progress.backup_import_btn':'⬆️ Import a backup',
  'progress.backup_export_ok':'Backup downloaded ✅',
  'progress.backup_import_ok':'Backup imported successfully ✅',
  'progress.backup_import_fail':'Could not import: ',
  'progress.unknown_error':'Unknown error',
  'progress.sync_title':"☁️ Save your progress to your account",
  'progress.sync_desc':"Continue with your Google account so your progress is saved and appears automatically on all your devices, even if you switch phones or clear your browser data.",
  'progress.sync_signin_btn':"🔵 Continue with Google",
  'progress.sync_signout_btn':'Sign out',
  'progress.sync_now_btn':"🔄 Update my progress now",
  'progress.sync_signed_in_as':'Signed in as: ',
  'progress.sync_syncing':"Saving your progress…",
  'progress.sync_ok':"Your progress is saved ✅",
  'progress.sync_fail':"Couldn’t save your progress: ",
  'progress.sync_unsupported':"Saving progress to an account isn’t available on this browser"
},

fr: {
  // ===== تحسينات صفحة تقدّمي (أكتوبر 2026) =====
  'progress.continue_title':'▶️ Reprenez où vous vous êtes arrêté',
  'progress.continue_btn':'Continuer',
  'progress.goal_set_label':'Choisissez votre objectif quotidien (pages) :',
  'progress.goal_progress':'Aujourd’hui : {c} sur {n} pages',
  'progress.review_today_title':'🔁 À réviser aujourd’hui',
  'progress.show_all':'Tout afficher ({n})',
  'progress.show_less':'Afficher moins',
  'progress.not_started':'Sourates pas encore commencées ({n})',
  'progress.juz_label':'Juz’ {n}',
  // ===== Général / navigation =====
  'nav.tools_title':'Outils',
  'nav.lang_label':'Langue',
  'nav.feedback':'Suggestions',
  'nav.share':'Partager la page',
  'nav.qr':'Code QR',
  'nav.about':'📖 À propos',
  'about.dua':'Nous demandons à Allah de faire du Coran le printemps de nos cœurs et la lumière de nos poitrines, et de nous accorder de le mémoriser, de le maîtriser et de le mettre en pratique.',
  'nav.progress':'📊 Mes progrès',
  'nav.sync_signin':'☁️ Connexion',
  'nav.font_size':'🔠 Taille du texte',
  'nav.sync_on':"☁️ Progression enregistrée ✅",
  'nav.back':'← Retour',

  // ===== Page d’accueil =====
  'home.title':'Quran Darbi',
  'home.subtitle':'Testez votre mémorisation page par page — des quiz interactifs pour réviser et consolider',
  'home.recite_btn':'🎤 Test de récitation',
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
  'about.role_title':'Quel est le rôle de ce site ?',
  'about.role_p1':'Ce site est un outil d’aide pour consolider la mémorisation du Coran et de ses versets similaires (mutashabihat). Il ne remplace pas l’apprentissage auprès d’un maître qualifié (cheikh) : la vocalisation et les règles du tajwid s’acquièrent par l’écoute et la transmission orale.',
  'about.role_p2':'Qu’il soit pour vous un soutien vers la maîtrise, et non un substitut à la récitation auprès de ceux qui la maîtrisent.',
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
  'voice.text_btn':'⌨️ Écrire',
  'reminder.banner':'🌙 Vous n’avez pas encore commencé votre révision du jour — poursuivez votre mémorisation maintenant',
  'reminder.tomorrow':'Me le rappeler demain',
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
,
  'recite.page_sub':'Choisissez une sourate — récitez à partir de n’importe quel verset — le site corrige chaque mot',
  'recite.select_label':'Choisissez la sourate ou la page',
  'recite.search_placeholder':'🔍 Rechercher par nom de sourate ou numéro de page',
  'recite.no_results':'Aucun résultat correspondant',
  'recite.select_default_option':'— Choisir —',
  'recite.placeholder_text':'Le texte apparaîtra ici...',
  'recite.prev_btn':'⏮️ Précédent',
  'recite.next_btn':'Suivant ⏭️',
  'recite.rec_desc_html':'Appuyez sur 🎤 et récitez à partir de n’importe quel verset<br>Arrêtez-vous quand vous voulez — nous détecterons votre position automatiquement<br>🟢 Correct &nbsp;|&nbsp; 🔴 Faux &nbsp;|&nbsp; ➖ Manquant',
  'recite.choose_surah_first':'Choisissez d’abord une sourate',
  'recite.show_text_btn':'📖 Afficher le texte de la sourate',
  'recite.hide_text_btn':'🙈 Masquer le texte',
  'recite.hint_used':'💡 Utilisé',
  'recite.clear_btn':'🗑️ Effacer et recommencer',
  'recite.check_btn':'✓ Vérifier la récitation',
  'recite.result_label':'Résultat',
  'recite.scope_note':'ℹ️ Ce test vérifie les mots et leur ordre dans votre mémorisation, mais ne vérifie pas encore l’exactitude des voyelles (tachkil) ni les règles de tajwid et de madd — cette partie est encore en recherche et développement.',
  'recite.legend_correct':'Correct',
  'recite.legend_wrong':'Faux',
  'recite.legend_missing':'Manquant',
  'recite.retry_btn':'🔄 Recommencer l’enregistrement',
  'recite.selected_info':'✓ {name} — {count} mots',
  'recite.btn_start':'🎤 Appuyez pour commencer à réciter',
  'recite.btn_pause':'⏸ Pause',
  'recite.btn_resume':'▶️ Continuer à réciter',
  'recite.said_prefix':'Vous avez dit : ',
  'recite.where_start':'Vous avez commencé au début de la sourate',
  'recite.where_approx':'📍 Vous avez commencé environ au mot {n}',
  'recite.pct_label':'{pct} %',
  'recite.result_perfect':'🌟 Excellent ! Votre mémorisation correspond exactement au texte',
  'recite.result_great':'✨ Bravo ! Votre mémorisation est solide',
  'recite.result_good':'📖 Bien — révisez les mots en rouge',
  'recite.result_weak':'💪 Nécessite une révision',
  'recite.err_inapp_browser':'⚠️ L’enregistrement vocal ne fonctionne pas dans le navigateur de cette application (Messenger / Instagram / etc.).\n\nOuvrez le site directement dans Chrome :\n1) Appuyez sur les trois points (⋮) en haut de la page\n2) Choisissez « Ouvrir dans le navigateur »\n\nOu copiez le lien du site et collez-le dans l’application Chrome.',
  'recite.err_needs_chrome':'⚠️ L’enregistrement vocal nécessite le navigateur Chrome pour fonctionner.\n\nSi vous êtes sur iPhone : téléchargez l’application Chrome depuis l’App Store et ouvrez le site depuis celle-ci (pas depuis Safari).\nSi vous êtes sur Android : ouvrez le site depuis l’application Chrome.',
  'recite.err_speech_blocked':'⚠️ L’enregistrement vocal n’a pas pu démarrer.\n\nSur iPad ou iPhone : activez la dictée dans Réglages → Général → Clavier, et autorisez le site à utiliser le microphone. Si cela ne fonctionne toujours pas, ouvrez le site depuis l’application Chrome.',
  'progress.home_btn':'🏠 Accueil',
  'progress.subtitle':'Suivez votre parcours de mémorisation du Coran',
  'progress.subtitle_empty':'C’est votre début — commencez votre premier test',
  'progress.subtitle_progress':'Vous avez terminé {done} pages sur {total} — continuez 🌿',
  'progress.streak_label':'jours consécutifs',
  'progress.streak_best_label':'plus longue série',
  'progress.empty_text':'Vous n’avez pas encore commencé votre parcours de mémorisation ici — commencez votre premier test et votre progression apparaîtra sur cette page au fur et à mesure',
  'progress.empty_cta':'Commencer maintenant',
  'progress.goal_title':'🎯 Mon objectif quotidien',
  'progress.goal_not_done':'Vous n’avez pas encore atteint l’objectif du jour',
  'progress.goal_done_headline':'Vous avez atteint l’objectif du jour !',
  'progress.goal_desc':'Objectif : au moins une activité de mémorisation par jour',
  'progress.goal_done_msg':'Vous avez atteint l’objectif du jour — bravo !',
  'progress.badges_title':'🏅 Badges',
  'progress.rec_stat_pages':'Pages testées',
  'progress.rec_stat_best':'Meilleur score',
  'progress.rec_stat_tries':'Tentatives',
  'progress.rec_last_title':'Dernières tentatives',
  'progress.rec_reached':'Arrivé à l’aya {a} — {c} % de la page',
  'progress.rec_reached_noayah':'Arrivé à {c} % de la page',
  'progress.rec_empty':'Vous n’avez pas encore passé ce test. Commencez maintenant : votre progression s’affichera ici.',
  'progress.rec_go':'Commencer le test',
  'progress.rec_note':'Le score porte sur les mots et leur ordre, pas sur les voyelles ni les règles du tajwid.',
  'progress.badge_rec_first':'Premier test vocal',
  'progress.badge_rec_90':'90 % à l’oral',
  'progress.badge_rec_surah':'Sourate complète à l’oral',
  'progress.badge_week':'Semaine complète',
  'progress.badge_first_juz':'Premier juz’ terminé',
  'progress.badge_30days':'30 jours consécutifs',
  'progress.badge_100pages':'100 pages',
  'progress.badge_amma':'Juz’ Amma complet',
  'progress.badge_60days':'60 jours consécutifs',
  'progress.badge_3surahs':'3 sourates complètes',
  'progress.badge_300pages':'300 pages',
  'progress.surah_progress_title':'📚 Votre progression dans chaque sourate',
  'progress.filter_all_surahs':'Toutes les sourates',
  'progress.filter_complete':'Terminé',
  'progress.filter_incomplete':'Pas encore terminé',
  'progress.filter_empty':'Aucune sourate ne correspond à ce filtre pour le moment.',
  'progress.review_title':'🔁 Liste de révision intelligente',
  'progress.review_empty':'Aucune question n’a besoin d’être révisée pour le moment — continuez ainsi 👏',
  'progress.review_remove':'Retirer de la liste de révision',
  'progress.question_label':'Question {n}',
  'progress.reminder_title':'🔔 Rappel quotidien',
  'progress.reminder_enable_label':'Activer les notifications de rappel',
  'progress.reminder_enable_sub':'Arrive même si le site est fermé',
  'progress.reminder_time_label':'Heure :',
  'progress.reminder_note':'La notification est basée uniquement sur l’heure et ne sait pas si vous avez terminé votre portion du jour (le site n’a pas de comptes et vos données sont stockées uniquement dans votre navigateur). L’heure peut parfois varier de quelques minutes.',
  'progress.reminder_coming_soon':'La fonctionnalité de rappel par notification est en cours de déploiement sur ce site.',
  'progress.reminder_denied':'L’autorisation de notification a été bloquée dans les paramètres du navigateur pour ce site — pour l’activer plus tard, ouvrez les paramètres du site dans votre navigateur et autorisez les notifications',
  'progress.activating':'Activation en cours…',
  'progress.reminder_enabled':'Rappel activé ✅',
  'progress.reminder_enable_fail':'Impossible d’activer : ',
  'progress.saving':'Enregistrement…',
  'progress.time_updated':'Heure mise à jour ✅',
  'progress.save_fail':'Impossible d’enregistrer : ',
  'progress.backup_title':'💾 Sauvegarde',
  'progress.backup_none':'Aucune sauvegarde n’a encore été effectuée',
  'progress.last_backup':'Dernière sauvegarde : ',
  'progress.backup_suggest':'⏰ Cela fait longtemps — il est préférable de faire une nouvelle sauvegarde, car vos données ne sont stockées que dans ce navigateur',
  'progress.backup_export_btn':'⬇️ Télécharger la sauvegarde',
  'progress.backup_import_btn':'⬆️ Importer une sauvegarde',
  'progress.backup_export_ok':'Sauvegarde téléchargée ✅',
  'progress.backup_import_ok':'Sauvegarde importée avec succès ✅',
  'progress.backup_import_fail':'Impossible d’importer : ',
  'progress.unknown_error':'Erreur inconnue',
  'progress.sync_title':"☁️ Enregistrez votre progression sur votre compte",
  'progress.sync_desc':"Continuez avec votre compte Google pour que votre progression soit enregistrée et apparaisse automatiquement sur tous vos appareils, même en cas de changement de téléphone ou d’effacement des données du navigateur.",
  'progress.sync_signin_btn':"🔵 Continuer avec Google",
  'progress.sync_signout_btn':'Se déconnecter',
  'progress.sync_now_btn':"🔄 Mettre à jour ma progression",
  'progress.sync_signed_in_as':'Connecté en tant que : ',
  'progress.sync_syncing':"Enregistrement de votre progression…",
  'progress.sync_ok':"Votre progression est enregistrée ✅",
  'progress.sync_fail':"Échec de l’enregistrement de votre progression : ",
  'progress.sync_unsupported':"L’enregistrement sur un compte n’est pas disponible sur ce navigateur"
},

tr: {
  // ===== تحسينات صفحة تقدّمي (أكتوبر 2026) =====
  'progress.continue_title':'▶️ Kaldığın yerden devam et',
  'progress.continue_btn':'Devam et',
  'progress.goal_set_label':'Günlük hedefini seç (sayfa):',
  'progress.goal_progress':'Bugün: {n} sayfadan {c}',
  'progress.review_today_title':'🔁 Bugün tekrar et',
  'progress.show_all':'Tümünü göster ({n})',
  'progress.show_less':'Daha az göster',
  'progress.not_started':'Henüz başlanmamış sureler ({n})',
  'progress.juz_label':'Cüz {n}',
  // ===== Genel / gezinme =====
  'nav.tools_title':'Araçlar',
  'nav.lang_label':'Dil',
  'nav.feedback':'Öneriler',
  'nav.share':'Sayfayı paylaş',
  'nav.qr':'QR kodu',
  'nav.about':'📖 Proje hakkında',
  'about.dua':'Allah’tan, Kur’ân’ı kalplerimizin baharı ve göğüslerimizin nûru kılmasını; onu ezberlemeyi, iyi öğrenmeyi ve ona göre amel etmeyi bize nasip etmesini niyaz ederiz.',
  'nav.progress':'📊 İlerlemem',
  'nav.sync_signin':'☁️ Giriş yap',
  'nav.font_size':'🔠 Yazı boyutu',
  'nav.sync_on':"☁️ İlerleme kaydedildi ✅",
  'nav.back':'← Geri',

  // ===== Ana sayfa =====
  'home.title':'Quran Darbi',
  'home.subtitle':'Ezberini sayfa sayfa test et — tekrar etmek ve pekiştirmek için etkileşimli testler',
  'home.recite_btn':'🎤 Ezber Testi',
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
  'about.role_title':'Bu sitenin rolü nedir?',
  'about.role_p1':'Bu site, Kur’an’ın ve müteşabih ayetlerinin ezberini pekiştirmeye yardımcı bir araçtır. Ehil bir hocanın (şeyhin) yanında öğrenmenin yerini tutmaz; harekeler ve tecvid kuralları dinleyerek ve yüz yüze aktarımla öğrenilir.',
  'about.role_p2':'Bu site ustalığa ulaşmanızda size yardımcı olsun; ehil kişilere okumanın yerine geçmesin.',
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
  'reminder.banner':'🌙 Bugünkü çalışmanıza henüz başlamadınız — ezberinize şimdi devam edin',
  'reminder.tomorrow':'Yarın hatırlat',
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
,
  'recite.page_sub':'Bir sure seçin — istediğiniz ayetten başlayın — site her kelimeyi düzeltir',
  'recite.select_label':'Sure veya sayfa seçin',
  'recite.search_placeholder':'🔍 Sure adı veya sayfa numarasıyla ara',
  'recite.no_results':'Eşleşen sonuç yok',
  'recite.select_default_option':'— Seçin —',
  'recite.placeholder_text':'Metin burada görünecek...',
  'recite.prev_btn':'⏮️ Önceki',
  'recite.next_btn':'Sonraki ⏭️',
  'recite.rec_desc_html':'🎤’a dokunun ve istediğiniz ayetten okumaya başlayın<br>İstediğiniz zaman durun — konumunuzu otomatik algılarız<br>🟢 Doğru &nbsp;|&nbsp; 🔴 Yanlış &nbsp;|&nbsp; ➖ Eksik',
  'recite.choose_surah_first':'Önce bir sure seçin',
  'recite.show_text_btn':'📖 Sure metnini göster',
  'recite.hide_text_btn':'🙈 Metni gizle',
  'recite.hint_used':'💡 Kullanıldı',
  'recite.clear_btn':'🗑️ Temizle ve yeniden başla',
  'recite.check_btn':'✓ Okumayı kontrol et',
  'recite.result_label':'Sonuç',
  'recite.scope_note':'ℹ️ Bu test, ezberinizdeki kelimeleri ve sıralarını kontrol eder; harekelerin doğruluğunu veya tecvid ve med kurallarını henüz kontrol etmez — bu kısım hâlâ araştırma ve geliştirme aşamasındadır.',
  'recite.legend_correct':'Doğru',
  'recite.legend_wrong':'Yanlış',
  'recite.legend_missing':'Eksik',
  'recite.retry_btn':'🔄 Kaydı tekrarla',
  'recite.selected_info':'✓ {name} — {count} kelime',
  'recite.btn_start':'🎤 Okumaya başlamak için dokunun',
  'recite.btn_pause':'⏸ Duraklat',
  'recite.btn_resume':'▶️ Okumaya devam et',
  'recite.said_prefix':'Söylediğiniz: ',
  'recite.where_start':'Sureye baştan başladınız',
  'recite.where_approx':'📍 Yaklaşık {n}. kelimeden başladınız',
  'recite.pct_label':'%{pct}',
  'recite.result_perfect':'🌟 Mükemmel! Ezberiniz metinle birebir uyuşuyor',
  'recite.result_great':'✨ Aferin! Ezberiniz güçlü',
  'recite.result_good':'📖 İyi — kırmızı kelimeleri gözden geçirin',
  'recite.result_weak':'💪 Daha fazla tekrar gerekiyor',
  'recite.err_inapp_browser':'⚠️ Sesli kayıt bu uygulama tarayıcısında (Messenger / Instagram vb.) çalışmaz.\n\nSiteyi doğrudan Chrome’da açın:\n1) Sayfanın üstündeki üç noktaya (⋮) dokunun\n2) "Tarayıcıda Aç" seçeneğini seçin\n\nYa da site bağlantısını kopyalayıp Chrome uygulamasına yapıştırın.',
  'recite.err_needs_chrome':'⚠️ Sesli kaydın çalışması için Chrome tarayıcısı gerekir.\n\niPhone kullanıyorsanız: App Store’dan Chrome uygulamasını indirip siteyi ondan açın (Safari’den değil).\nAndroid kullanıyorsanız: siteyi Chrome uygulamasından açın.',
  'recite.err_speech_blocked':'⚠️ Sesli kayıt başlatılamadı.\n\niPad veya iPhone’da: Ayarlar → Genel → Klavye bölümünden Dikte’yi açın ve siteye mikrofon izni verin. Yine olmazsa siteyi Chrome uygulamasından açın.',
  'progress.home_btn':'🏠 Ana Sayfa',
  'progress.subtitle':'Kur’an ezberleme yolculuğunuzu takip edin',
  'progress.subtitle_empty':'Bu sizin başlangıcınız — ilk testinize başlayın',
  'progress.subtitle_progress':'{total} sayfadan {done} tanesini tamamladınız — devam edin 🌿',
  'progress.streak_label':'gün seri',
  'progress.streak_best_label':'en uzun seri',
  'progress.empty_text':'Burada henüz ezber yolculuğunuza başlamadınız — ilk testinize başlayın, ilerlemeniz bu sayfada adım adım görünecek',
  'progress.empty_cta':'Şimdi başla',
  'progress.goal_title':'🎯 Günlük hedefim',
  'progress.goal_not_done':'Bugünkü hedefinizi henüz tamamlamadınız',
  'progress.goal_done_headline':'Bugünkü hedefinizi tamamladınız!',
  'progress.goal_desc':'Hedef: günde en az bir ezber etkinliği',
  'progress.goal_done_msg':'Bugünkü hedefinizi tamamladınız — tebrikler!',
  'progress.badges_title':'🏅 Rozetler',
  'progress.rec_stat_pages':'Test edilen sayfalar',
  'progress.rec_stat_best':'En iyi oran',
  'progress.rec_stat_tries':'Deneme',
  'progress.rec_last_title':'Son denemeler',
  'progress.rec_reached':'{a}. ayete kadar geldiniz — sayfanın %{c}’i',
  'progress.rec_reached_noayah':'Sayfanın %{c}’ine ulaştınız',
  'progress.rec_empty':'Bu testi henüz yapmadınız. Şimdi başlayın; ilerlemeniz burada görünecek.',
  'progress.rec_go':'Testi başlat',
  'progress.rec_note':'Oran yalnızca kelimeleri ve sıralarını kapsar; harekeleri ve tecvid kurallarını kapsamaz.',
  'progress.badge_rec_first':'İlk sesli test',
  'progress.badge_rec_90':'Sesle %90',
  'progress.badge_rec_surah':'Sesle tam sure',
  'progress.badge_week':'Tam bir hafta',
  'progress.badge_first_juz':'İlk tamamlanan cüz',
  'progress.badge_30days':'30 gün seri',
  'progress.badge_100pages':'100 sayfa',
  'progress.badge_amma':'Amme Cüzü tamamlandı',
  'progress.badge_60days':'60 gün seri',
  'progress.badge_3surahs':'3 tam sure',
  'progress.badge_300pages':'300 sayfa',
  'progress.surah_progress_title':'📚 Her suredeki ilerlemeniz',
  'progress.filter_all_surahs':'Tüm sureler',
  'progress.filter_complete':'Tamamlanan',
  'progress.filter_incomplete':'Henüz tamamlanmadı',
  'progress.filter_empty':'Şu anda bu filtreyle eşleşen sure yok.',
  'progress.review_title':'🔁 Akıllı tekrar listesi',
  'progress.review_empty':'Şu anda tekrar gerektiren soru yok — böyle devam edin 👏',
  'progress.review_remove':'Tekrar listesinden kaldır',
  'progress.question_label':'Soru {n}',
  'progress.reminder_title':'🔔 Günlük hatırlatma',
  'progress.reminder_enable_label':'Hatırlatma bildirimlerini etkinleştir',
  'progress.reminder_enable_sub':'Site kapalı olsa bile gelir',
  'progress.reminder_time_label':'Saat:',
  'progress.reminder_note':'Bildirim yalnızca saate dayanır ve bugünkü virdinizi tamamlayıp tamamlamadığınızı bilmez (site hesapsız çalışır, verileriniz yalnızca tarayıcınızda saklanır). Zamanlama bazen birkaç dakika kayabilir.',
  'progress.reminder_coming_soon':'Bildirimli hatırlatma özelliği bu sitede şu anda etkinleştiriliyor.',
  'progress.reminder_denied':'Bu site için bildirim izni tarayıcı ayarlarından engellendi — daha sonra etkinleştirmek için tarayıcınızdaki site ayarlarını açıp bildirimlere izin verin',
  'progress.activating':'Etkinleştiriliyor…',
  'progress.reminder_enabled':'Hatırlatma etkinleştirildi ✅',
  'progress.reminder_enable_fail':'Etkinleştirilemedi: ',
  'progress.saving':'Kaydediliyor…',
  'progress.time_updated':'Saat güncellendi ✅',
  'progress.save_fail':'Kaydedilemedi: ',
  'progress.backup_title':'💾 Yedekleme',
  'progress.backup_none':'Henüz yedek alınmadı',
  'progress.last_backup':'Son yedekleme: ',
  'progress.backup_suggest':'⏰ Uzun zaman geçti — verileriniz yalnızca bu tarayıcıda saklandığından yeni bir yedek almanız önerilir',
  'progress.backup_export_btn':'⬇️ Yedeği indir',
  'progress.backup_import_btn':'⬆️ Yedek içe aktar',
  'progress.backup_export_ok':'Yedek indirildi ✅',
  'progress.backup_import_ok':'Yedek başarıyla içe aktarıldı ✅',
  'progress.backup_import_fail':'İçe aktarılamadı: ',
  'progress.unknown_error':'Bilinmeyen hata',
  'progress.sync_title':"☁️ İlerlemeni hesabına kaydet",
  'progress.sync_desc':"Google hesabınla devam et; ilerlemen kaydedilsin ve telefonunu değiştirsen ya da tarayıcı verilerini silsen bile tüm cihazlarında otomatik olarak görünsün.",
  'progress.sync_signin_btn':"🔵 Google ile devam et",
  'progress.sync_signout_btn':'Çıkış yap',
  'progress.sync_now_btn':"🔄 İlerlemeni şimdi güncelle",
  'progress.sync_signed_in_as':'Giriş yapıldı: ',
  'progress.sync_syncing':"İlerlemen kaydediliyor…",
  'progress.sync_ok':"İlerlemen kaydedildi ✅",
  'progress.sync_fail':"İlerlemen kaydedilemedi: ",
  'progress.sync_unsupported':"İlerlemeyi hesaba kaydetme bu tarayıcıda kullanılamıyor"
}
,

de: {
  // ===== تحسينات صفحة تقدّمي (أكتوبر 2026) =====
  'progress.continue_title':'▶️ Mach dort weiter, wo du aufgehört hast',
  'progress.continue_btn':'Weiter',
  'progress.goal_set_label':'Wähle dein Tagesziel (Seiten):',
  'progress.goal_progress':'Heute: {c} von {n} Seiten',
  'progress.review_today_title':'🔁 Heute wiederholen',
  'progress.show_all':'Alle anzeigen ({n})',
  'progress.show_less':'Weniger anzeigen',
  'progress.not_started':'Noch nicht begonnene Suren ({n})',
  'progress.juz_label':'Dschuz’ {n}',
  // ===== Allgemein / Navigation =====
  'nav.tools_title':'Werkzeuge',
  'nav.lang_label':'Sprache',
  'nav.feedback':'Feedback',
  'nav.share':'Seite teilen',
  'nav.qr':'QR-Code',
  'nav.about':'📖 Über das Projekt',
  'about.dua':'Wir bitten Allah, den Koran zum Frühling unserer Herzen und zum Licht unserer Brüste zu machen und uns zu schenken, ihn auswendig zu lernen, zu beherrschen und danach zu handeln.',
  'nav.progress':'📊 Mein Fortschritt',
  'nav.sync_signin':'☁️ Anmelden',
  'nav.font_size':'🔠 Schriftgröße',
  'nav.sync_on':"☁️ Fortschritt gespeichert ✅",
  'nav.back':'← Zurück',

  // ===== Startseite =====
  'home.title':'Quran Darbi',
  'home.subtitle':'Teste dein Auswendiglernen Seite für Seite — interaktive Quizze zur Wiederholung und Festigung',
  'home.recite_btn':'🎤 Rezitationstest',
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
  'about.role_title':'Welche Rolle hat diese Website?',
  'about.role_p1':'Diese Website ist ein Hilfsmittel, um das Auswendiglernen des Korans und seiner ähnlichen Verse (Mutaschabihat) zu festigen. Sie ersetzt nicht das Lernen bei einem qualifizierten Lehrer (Scheich): Vokalisierung und Tadschwid-Regeln werden durch Zuhören und mündliche Überlieferung erlernt.',
  'about.role_p2':'Sie soll eine Hilfe auf dem Weg zur Meisterschaft sein, kein Ersatz für das Rezitieren bei Kundigen.',
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
  'reminder.banner':'🌙 Du hast heute noch nicht angefangen — mach jetzt mit deinem Auswendiglernen weiter',
  'reminder.tomorrow':'Morgen erinnern',
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
,
  'recite.page_sub':'Wähle eine Sure — rezitiere ab einem beliebigen Vers — die Seite korrigiert jedes Wort',
  'recite.select_label':'Wähle die Sure oder Seite',
  'recite.search_placeholder':'🔍 Suche nach Surennamen oder Seitenzahl',
  'recite.no_results':'Keine passenden Ergebnisse',
  'recite.select_default_option':'— Wählen —',
  'recite.placeholder_text':'Der Text erscheint hier...',
  'recite.prev_btn':'⏮️ Zurück',
  'recite.next_btn':'Weiter ⏭️',
  'recite.rec_desc_html':'Tippe auf 🎤 und rezitiere ab einem beliebigen Vers<br>Höre jederzeit auf — wir erkennen deine Position automatisch<br>🟢 Richtig &nbsp;|&nbsp; 🔴 Falsch &nbsp;|&nbsp; ➖ Fehlt',
  'recite.choose_surah_first':'Wähle zuerst eine Sure',
  'recite.show_text_btn':'📖 Surentext anzeigen',
  'recite.hide_text_btn':'🙈 Text ausblenden',
  'recite.hint_used':'💡 Verwendet',
  'recite.clear_btn':'🗑️ Löschen und neu beginnen',
  'recite.check_btn':'✓ Rezitation prüfen',
  'recite.result_label':'Ergebnis',
  'recite.scope_note':'ℹ️ Dieser Test prüft die Wörter und ihre Reihenfolge in deinem Auswendiggelernten, prüft aber noch nicht die Genauigkeit der Vokalzeichen oder die Tadschwid- und Madd-Regeln — dieser Teil befindet sich noch in Forschung und Entwicklung.',
  'recite.legend_correct':'Richtig',
  'recite.legend_wrong':'Falsch',
  'recite.legend_missing':'Fehlt',
  'recite.retry_btn':'🔄 Aufnahme wiederholen',
  'recite.selected_info':'✓ {name} — {count} Wörter',
  'recite.btn_start':'🎤 Tippen, um mit der Rezitation zu beginnen',
  'recite.btn_pause':'⏸ Pause',
  'recite.btn_resume':'▶️ Rezitation fortsetzen',
  'recite.said_prefix':'Du hast gesagt: ',
  'recite.where_start':'Du hast am Anfang der Sure begonnen',
  'recite.where_approx':'📍 Du hast etwa bei Wort {n} begonnen',
  'recite.pct_label':'{pct} %',
  'recite.result_perfect':'🌟 Ausgezeichnet! Dein Auswendiggelerntes stimmt genau mit dem Text überein',
  'recite.result_great':'✨ Gut gemacht! Dein Auswendiggelerntes ist stark',
  'recite.result_good':'📖 Gut — überprüfe die rot markierten Wörter',
  'recite.result_weak':'💪 Braucht mehr Wiederholung',
  'recite.err_inapp_browser':'⚠️ Die Sprachaufnahme funktioniert nicht im Browser dieser App (Messenger / Instagram usw.).\n\nÖffne die Website direkt in Chrome:\n1) Tippe oben auf die drei Punkte (⋮)\n2) Wähle „Im Browser öffnen“\n\nOder kopiere den Link der Website und füge ihn in die Chrome-App ein.',
  'recite.err_needs_chrome':'⚠️ Die Sprachaufnahme benötigt den Chrome-Browser, um zu funktionieren.\n\nWenn du ein iPhone hast: Lade die Chrome-App aus dem App Store herunter und öffne die Website darüber (nicht über Safari).\nWenn du Android hast: Öffne die Website über die Chrome-App.',
  'recite.err_speech_blocked':'⚠️ Die Sprachaufnahme konnte nicht gestartet werden.\n\nAuf iPad oder iPhone: Aktiviere das Diktieren unter Einstellungen → Allgemein → Tastatur und erlaube der Website den Zugriff auf das Mikrofon. Falls es weiterhin nicht klappt, öffne die Website in der Chrome-App.',
  'progress.home_btn':'🏠 Startseite',
  'progress.subtitle':'Verfolge deine Reise beim Auswendiglernen des Korans',
  'progress.subtitle_empty':'Das ist dein Anfang — starte deinen ersten Test',
  'progress.subtitle_progress':'Du hast {done} von {total} Seiten abgeschlossen — mach weiter 🌿',
  'progress.streak_label':'Tage in Folge',
  'progress.streak_best_label':'längste Serie',
  'progress.empty_text':'Du hast deine Auswendiglern-Reise hier noch nicht begonnen — starte deinen ersten Test, und dein Fortschritt erscheint nach und nach auf dieser Seite',
  'progress.empty_cta':'Jetzt starten',
  'progress.goal_title':'🎯 Mein Tagesziel',
  'progress.goal_not_done':'Du hast das heutige Ziel noch nicht erreicht',
  'progress.goal_done_headline':'Du hast das heutige Ziel erreicht!',
  'progress.goal_desc':'Ziel: mindestens eine Auswendiglern-Aktivität pro Tag',
  'progress.goal_done_msg':'Du hast das heutige Ziel erreicht — gut gemacht!',
  'progress.badges_title':'🏅 Abzeichen',
  'progress.rec_stat_pages':'Getestete Seiten',
  'progress.rec_stat_best':'Beste Quote',
  'progress.rec_stat_tries':'Versuche',
  'progress.rec_last_title':'Letzte Versuche',
  'progress.rec_reached':'Bis Aya {a} gelesen — {c} % der Seite',
  'progress.rec_reached_noayah':'{c} % der Seite gelesen',
  'progress.rec_empty':'Sie haben diesen Test noch nicht gemacht. Starten Sie jetzt, Ihr Fortschritt erscheint hier.',
  'progress.rec_go':'Test starten',
  'progress.rec_note':'Die Quote bezieht sich nur auf Wörter und deren Reihenfolge, nicht auf Vokalzeichen oder Tadschwid-Regeln.',
  'progress.badge_rec_first':'Erster Sprachtest',
  'progress.badge_rec_90':'90 % per Stimme',
  'progress.badge_rec_surah':'Ganze Sure per Stimme',
  'progress.badge_week':'Ganze Woche',
  'progress.badge_first_juz':'Erster abgeschlossener Juz',
  'progress.badge_30days':'30 Tage in Folge',
  'progress.badge_100pages':'100 Seiten',
  'progress.badge_amma':'Juz Amma vollständig',
  'progress.badge_60days':'60 Tage in Folge',
  'progress.badge_3surahs':'3 vollständige Suren',
  'progress.badge_300pages':'300 Seiten',
  'progress.surah_progress_title':'📚 Dein Fortschritt in jeder Sure',
  'progress.filter_all_surahs':'Alle Suren',
  'progress.filter_complete':'Abgeschlossen',
  'progress.filter_incomplete':'Noch nicht abgeschlossen',
  'progress.filter_empty':'Derzeit gibt es keine Suren, die zu diesem Filter passen.',
  'progress.review_title':'🔁 Intelligente Wiederholungsliste',
  'progress.review_empty':'Derzeit müssen keine Fragen wiederholt werden — mach weiter so 👏',
  'progress.review_remove':'Aus der Wiederholungsliste entfernen',
  'progress.question_label':'Frage {n}',
  'progress.reminder_title':'🔔 Tägliche Erinnerung',
  'progress.reminder_enable_label':'Erinnerungsbenachrichtigungen aktivieren',
  'progress.reminder_enable_sub':'Kommt auch, wenn die Website geschlossen ist',
  'progress.reminder_time_label':'Uhrzeit:',
  'progress.reminder_note':'Die Benachrichtigung basiert nur auf der Uhrzeit und weiß nicht, ob du dein heutiges Pensum erledigt hast (die Website hat keine Konten, deine Daten werden nur in deinem Browser gespeichert). Die Zeit kann manchmal um ein paar Minuten abweichen.',
  'progress.reminder_coming_soon':'Die Erinnerungsbenachrichtigung wird derzeit auf dieser Website eingeführt.',
  'progress.reminder_denied':'Die Benachrichtigungsberechtigung wurde in den Browsereinstellungen für diese Website blockiert — um sie später zu aktivieren, öffne die Website-Einstellungen in deinem Browser und erlaube Benachrichtigungen',
  'progress.activating':'Wird aktiviert…',
  'progress.reminder_enabled':'Erinnerung aktiviert ✅',
  'progress.reminder_enable_fail':'Aktivierung fehlgeschlagen: ',
  'progress.saving':'Wird gespeichert…',
  'progress.time_updated':'Uhrzeit aktualisiert ✅',
  'progress.save_fail':'Speichern fehlgeschlagen: ',
  'progress.backup_title':'💾 Sicherung',
  'progress.backup_none':'Es wurde noch keine Sicherung erstellt',
  'progress.last_backup':'Letzte Sicherung: ',
  'progress.backup_suggest':'⏰ Es ist eine Weile her — am besten erstellst du eine neue Sicherung, da deine Daten nur in diesem Browser gespeichert sind',
  'progress.backup_export_btn':'⬇️ Sicherung herunterladen',
  'progress.backup_import_btn':'⬆️ Sicherung importieren',
  'progress.backup_export_ok':'Sicherung heruntergeladen ✅',
  'progress.backup_import_ok':'Sicherung erfolgreich importiert ✅',
  'progress.backup_import_fail':'Import fehlgeschlagen: ',
  'progress.unknown_error':'Unbekannter Fehler',
  'progress.sync_title':"☁️ Speichere deinen Fortschritt in deinem Konto",
  'progress.sync_desc':"Fahre mit deinem Google-Konto fort, damit dein Fortschritt gespeichert wird und automatisch auf all deinen Geräten erscheint – auch wenn du das Handy wechselst oder die Browserdaten löschst.",
  'progress.sync_signin_btn':"🔵 Weiter mit Google",
  'progress.sync_signout_btn':'Abmelden',
  'progress.sync_now_btn':"🔄 Meinen Fortschritt jetzt aktualisieren",
  'progress.sync_signed_in_as':'Angemeldet als: ',
  'progress.sync_syncing':"Dein Fortschritt wird gespeichert…",
  'progress.sync_ok':"Dein Fortschritt wurde gespeichert ✅",
  'progress.sync_fail':"Fortschritt konnte nicht gespeichert werden: ",
  'progress.sync_unsupported':"Das Speichern des Fortschritts im Konto ist in diesem Browser nicht verfügbar"
},

es: {
  // ===== تحسينات صفحة تقدّمي (أكتوبر 2026) =====
  'progress.continue_title':'▶️ Continúa donde lo dejaste',
  'progress.continue_btn':'Continuar',
  'progress.goal_set_label':'Elige tu meta diaria (páginas):',
  'progress.goal_progress':'Hoy: {c} de {n} páginas',
  'progress.review_today_title':'🔁 Repasa hoy',
  'progress.show_all':'Ver todo ({n})',
  'progress.show_less':'Ver menos',
  'progress.not_started':'Suras aún sin empezar ({n})',
  'progress.juz_label':'Yuz’ {n}',
  // ===== General / navegación =====
  'nav.tools_title':'Herramientas',
  'nav.lang_label':'Idioma',
  'nav.feedback':'Comentarios',
  'nav.share':'Compartir página',
  'nav.qr':'Código QR',
  'nav.about':'📖 Acerca del proyecto',
  'about.dua':'Pedimos a Allah que haga del Corán la primavera de nuestros corazones y la luz de nuestros pechos, y que nos conceda memorizarlo, dominarlo y ponerlo en práctica.',
  'nav.progress':'📊 Mi progreso',
  'nav.sync_signin':'☁️ Iniciar sesión',
  'nav.font_size':'🔠 Tamaño del texto',
  'nav.sync_on':"☁️ Progreso guardado ✅",
  'nav.back':'← Volver',

  // ===== Página de inicio =====
  'home.title':'Quran Darbi',
  'home.subtitle':'Pon a prueba tu memorización página por página — cuestionarios interactivos para repasar y reforzar',
  'home.recite_btn':'🎤 Prueba de recitación',
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
  'about.role_title':'¿Cuál es el papel de este sitio?',
  'about.role_p1':'Este sitio es una herramienta de apoyo para consolidar la memorización del Corán y de sus versículos similares (mutashabihat). No sustituye el aprendizaje con un maestro cualificado (sheij): la vocalización y las reglas del tayuid se adquieren escuchando y por transmisión oral.',
  'about.role_p2':'Que sea una ayuda hacia la maestría, y no un sustituto de recitar ante quienes la dominan.',
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
  'reminder.banner':'🌙 Aún no has empezado tu repaso de hoy — continúa tu memorización ahora',
  'reminder.tomorrow':'Recuérdamelo mañana',
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
,
  'recite.page_sub':'Elige una sura — recita desde cualquier aleya — el sitio corrige cada palabra',
  'recite.select_label':'Elige la sura o la página',
  'recite.search_placeholder':'🔍 Busca por nombre de sura o número de página',
  'recite.no_results':'No hay resultados coincidentes',
  'recite.select_default_option':'— Elegir —',
  'recite.placeholder_text':'El texto aparecerá aquí...',
  'recite.prev_btn':'⏮️ Anterior',
  'recite.next_btn':'Siguiente ⏭️',
  'recite.rec_desc_html':'Toca 🎤 y comienza a recitar desde cualquier aleya<br>Detente cuando quieras — detectaremos tu posición automáticamente<br>🟢 Correcto &nbsp;|&nbsp; 🔴 Incorrecto &nbsp;|&nbsp; ➖ Falta',
  'recite.choose_surah_first':'Elige primero una sura',
  'recite.show_text_btn':'📖 Mostrar el texto de la sura',
  'recite.hide_text_btn':'🙈 Ocultar el texto',
  'recite.hint_used':'💡 Usado',
  'recite.clear_btn':'🗑️ Borrar y empezar de nuevo',
  'recite.check_btn':'✓ Comprobar la recitación',
  'recite.result_label':'Resultado',
  'recite.scope_note':'ℹ️ Esta prueba comprueba las palabras y su orden en tu memorización, y aún no comprueba la precisión de las vocales (tachkil) ni las reglas de tayuid y madd — esta parte sigue en investigación y desarrollo.',
  'recite.legend_correct':'Correcto',
  'recite.legend_wrong':'Incorrecto',
  'recite.legend_missing':'Falta',
  'recite.retry_btn':'🔄 Grabar de nuevo',
  'recite.selected_info':'✓ {name} — {count} palabras',
  'recite.btn_start':'🎤 Toca para empezar a recitar',
  'recite.btn_pause':'⏸ Pausar',
  'recite.btn_resume':'▶️ Continuar recitando',
  'recite.said_prefix':'Dijiste: ',
  'recite.where_start':'Empezaste desde el principio de la sura',
  'recite.where_approx':'📍 Empezaste aproximadamente en la palabra {n}',
  'recite.pct_label':'{pct} %',
  'recite.result_perfect':'🌟 ¡Excelente! Tu memorización coincide exactamente con el texto',
  'recite.result_great':'✨ ¡Bien hecho! Tu memorización es sólida',
  'recite.result_good':'📖 Bien — repasa las palabras en rojo',
  'recite.result_weak':'💪 Necesita más repaso',
  'recite.err_inapp_browser':'⚠️ La grabación de voz no funciona dentro del navegador de esta app (Messenger / Instagram / etc.).\n\nAbre el sitio directamente en Chrome:\n1) Toca los tres puntos (⋮) en la parte superior de la página\n2) Elige "Abrir en el navegador"\n\nO copia el enlace del sitio y pégalo en la app de Chrome.',
  'recite.err_needs_chrome':'⚠️ La grabación de voz necesita el navegador Chrome para funcionar.\n\nSi usas iPhone: descarga la app de Chrome desde App Store y abre el sitio desde ella (no desde Safari).\nSi usas Android: abre el sitio desde la app de Chrome.',
  'recite.err_speech_blocked':'⚠️ No se pudo iniciar la grabación de voz.\n\nEn iPad o iPhone: activa el dictado en Ajustes → General → Teclado y permite que el sitio use el micrófono. Si sigue sin funcionar, abre el sitio desde la app de Chrome.',
  'progress.home_btn':'🏠 Inicio',
  'progress.subtitle':'Sigue tu recorrido de memorización del Corán',
  'progress.subtitle_empty':'Este es tu comienzo — empieza tu primera prueba',
  'progress.subtitle_progress':'Has completado {done} de {total} páginas — sigue así 🌿',
  'progress.streak_label':'días seguidos',
  'progress.streak_best_label':'racha más larga',
  'progress.empty_text':'Aún no has comenzado tu recorrido de memorización aquí — empieza tu primera prueba y tu progreso irá apareciendo en esta página',
  'progress.empty_cta':'Empezar ahora',
  'progress.goal_title':'🎯 Mi meta diaria',
  'progress.goal_not_done':'Aún no has completado la meta de hoy',
  'progress.goal_done_headline':'¡Has completado la meta de hoy!',
  'progress.goal_desc':'Meta: al menos una actividad de memorización al día',
  'progress.goal_done_msg':'¡Has completado la meta de hoy — bien hecho!',
  'progress.badges_title':'🏅 Insignias',
  'progress.rec_stat_pages':'Páginas evaluadas',
  'progress.rec_stat_best':'Mejor resultado',
  'progress.rec_stat_tries':'Intentos',
  'progress.rec_last_title':'Últimos intentos',
  'progress.rec_reached':'Llegaste a la aleya {a} — {c} % de la página',
  'progress.rec_reached_noayah':'Llegaste al {c} % de la página',
  'progress.rec_empty':'Aún no has hecho esta prueba. Empieza ahora y tu progreso aparecerá aquí.',
  'progress.rec_go':'Empezar la prueba',
  'progress.rec_note':'El resultado se refiere solo a las palabras y su orden, no a las vocales ni a las reglas del tayuid.',
  'progress.badge_rec_first':'Primera prueba de voz',
  'progress.badge_rec_90':'90 % por voz',
  'progress.badge_rec_surah':'Sura completa por voz',
  'progress.badge_week':'Semana completa',
  'progress.badge_first_juz':'Primer yuz completado',
  'progress.badge_30days':'Racha de 30 días',
  'progress.badge_100pages':'100 páginas',
  'progress.badge_amma':'Yuz Amma completo',
  'progress.badge_60days':'Racha de 60 días',
  'progress.badge_3surahs':'3 suras completas',
  'progress.badge_300pages':'300 páginas',
  'progress.surah_progress_title':'📚 Tu progreso en cada sura',
  'progress.filter_all_surahs':'Todas las suras',
  'progress.filter_complete':'Completado',
  'progress.filter_incomplete':'Aún no completado',
  'progress.filter_empty':'Ninguna sura coincide con este filtro por ahora.',
  'progress.review_title':'🔁 Lista de repaso inteligente',
  'progress.review_empty':'Ninguna pregunta necesita repaso ahora mismo — sigue así 👏',
  'progress.review_remove':'Quitar de la lista de repaso',
  'progress.question_label':'Pregunta {n}',
  'progress.reminder_title':'🔔 Recordatorio diario',
  'progress.reminder_enable_label':'Activar las notificaciones de recordatorio',
  'progress.reminder_enable_sub':'Llega incluso si el sitio está cerrado',
  'progress.reminder_time_label':'Hora:',
  'progress.reminder_note':'La notificación se basa solo en la hora y no sabe si has completado tu lectura de hoy o no (el sitio no tiene cuentas, y tus datos se guardan solo en tu navegador). La hora puede desviarse unos minutos a veces.',
  'progress.reminder_coming_soon':'La función de recordatorio mediante notificaciones se está habilitando actualmente en este sitio.',
  'progress.reminder_denied':'El permiso de notificaciones ha sido bloqueado en la configuración del navegador para este sitio — para activarlo más tarde, abre la configuración del sitio en tu navegador y permite las notificaciones',
  'progress.activating':'Activando…',
  'progress.reminder_enabled':'Recordatorio activado ✅',
  'progress.reminder_enable_fail':'No se pudo activar: ',
  'progress.saving':'Guardando…',
  'progress.time_updated':'Hora actualizada ✅',
  'progress.save_fail':'No se pudo guardar: ',
  'progress.backup_title':'💾 Copia de seguridad',
  'progress.backup_none':'Aún no se ha realizado ninguna copia de seguridad',
  'progress.last_backup':'Última copia de seguridad: ',
  'progress.backup_suggest':'⏰ Ha pasado tiempo — es recomendable hacer una nueva copia de seguridad, ya que tus datos solo se guardan en este navegador',
  'progress.backup_export_btn':'⬇️ Descargar copia de seguridad',
  'progress.backup_import_btn':'⬆️ Importar una copia',
  'progress.backup_export_ok':'Copia de seguridad descargada ✅',
  'progress.backup_import_ok':'Copia de seguridad importada correctamente ✅',
  'progress.backup_import_fail':'No se pudo importar: ',
  'progress.unknown_error':'Error desconocido',
  'progress.sync_title':"☁️ Guarda tu progreso en tu cuenta",
  'progress.sync_desc':"Continúa con tu cuenta de Google para que tu progreso se guarde y aparezca automáticamente en todos tus dispositivos, incluso si cambias de teléfono o borras los datos del navegador.",
  'progress.sync_signin_btn':"🔵 Continuar con Google",
  'progress.sync_signout_btn':'Cerrar sesión',
  'progress.sync_now_btn':"🔄 Actualizar mi progreso ahora",
  'progress.sync_signed_in_as':'Sesión iniciada como: ',
  'progress.sync_syncing':"Guardando tu progreso…",
  'progress.sync_ok':"Tu progreso se ha guardado ✅",
  'progress.sync_fail':"No se pudo guardar tu progreso: ",
  'progress.sync_unsupported':"Guardar el progreso en una cuenta no está disponible en este navegador"
},

fa: {
  // ===== تحسينات صفحة تقدّمي (أكتوبر 2026) =====
  'progress.continue_title':'▶️ از همان‌جا که ماندی ادامه بده',
  'progress.continue_btn':'ادامه',
  'progress.goal_set_label':'هدف روزانه‌ات را انتخاب کن (تعداد صفحه):',
  'progress.goal_progress':'امروز: {c} از {n} صفحه',
  'progress.review_today_title':'🔁 مرور امروز',
  'progress.show_all':'نمایش همه ({n})',
  'progress.show_less':'نمایش کمتر',
  'progress.not_started':'سوره‌های شروع‌نشده ({n})',
  'progress.juz_label':'جزء {n}',
  // ===== عمومی / پیمایش =====
  'nav.tools_title':'ابزارها',
  'nav.lang_label':'زبان',
  'nav.feedback':'بازخورد',
  'nav.share':'اشتراک‌گذاری صفحه',
  'nav.qr':'کد QR',
  'nav.about':'📖 درباره‌ی پروژه',
  'about.dua':'از خداوند می‌خواهیم که قرآن را بهار دل‌هایمان و نور سینه‌هایمان قرار دهد و حفظ، اتقان و عمل به آن را روزی ما کند.',
  'nav.progress':'📊 پیشرفت من',
  'nav.sync_signin':'☁️ ورود',
  'nav.font_size':'🔠 اندازه متن',
  'nav.sync_on':"☁️ پیشرفت ذخیره شد ✅",
  'nav.back':'← بازگشت',

  // ===== صفحه اصلی =====
  'home.title':'قرآن دربی',
  'home.subtitle':'حفظ خود را صفحه به صفحه بیازمایید — آزمون‌های تعاملی برای مرور و تثبیت',
  'home.recite_btn':'🎤 آزمون تلاوت',
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
  'about.role_title':'نقش این سایت چیست؟',
  'about.role_p1':'این سایت ابزاری کمکی برای تثبیت حفظ قرآن و آیات متشابه آن است و جای آموختن از استاد ماهر (شیخ) را نمی‌گیرد؛ حرکات و احکام تجوید با شنیدن و مشافهه آموخته می‌شود.',
  'about.role_p2':'باشد که یاری‌رسان شما در اتقان باشد، نه جایگزین قرائت نزد اهل اتقان.',
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
  'reminder.banner':'🌙 هنوز ورد امروز را شروع نکرده‌اید — همین حالا حفظ خود را ادامه دهید',
  'reminder.tomorrow':'فردا یادآوری کن',
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
,
  'recite.page_sub':'سوره‌ای را انتخاب کنید — از هر آیه‌ای که می‌خواهید بخوانید — سایت هر کلمه را تصحیح می‌کند',
  'recite.select_label':'سوره یا صفحه را انتخاب کنید',
  'recite.search_placeholder':'🔍 با نام سوره یا شماره صفحه جستجو کنید',
  'recite.no_results':'نتیجه‌ای یافت نشد',
  'recite.select_default_option':'— انتخاب کنید —',
  'recite.placeholder_text':'متن اینجا ظاهر می‌شود...',
  'recite.prev_btn':'⏮️ قبلی',
  'recite.next_btn':'بعدی ⏭️',
  'recite.rec_desc_html':'روی 🎤 بزنید و از هر آیه‌ای که می‌خواهید بخوانید<br>هر وقت خواستید توقف کنید — موقعیت شما را خودکار تشخیص می‌دهیم<br>🟢 درست &nbsp;|&nbsp; 🔴 غلط &nbsp;|&nbsp; ➖ حذف‌شده',
  'recite.choose_surah_first':'ابتدا سوره را انتخاب کنید',
  'recite.show_text_btn':'📖 نمایش متن سوره',
  'recite.hide_text_btn':'🙈 پنهان کردن متن',
  'recite.hint_used':'💡 استفاده شد',
  'recite.clear_btn':'🗑️ پاک کردن و شروع دوباره',
  'recite.check_btn':'✓ بررسی تلاوت',
  'recite.result_label':'نتیجه',
  'recite.scope_note':'ℹ️ این آزمون کلمات و ترتیب آن‌ها را در حفظ شما بررسی می‌کند، و هنوز دقت اعراب یا احکام تجوید و مدود را بررسی نمی‌کند — این بخش هنوز در حال پژوهش و توسعه است.',
  'recite.legend_correct':'درست',
  'recite.legend_wrong':'غلط',
  'recite.legend_missing':'حذف‌شده',
  'recite.retry_btn':'🔄 تکرار ضبط',
  'recite.selected_info':'✓ {name} — {count} کلمه',
  'recite.btn_start':'🎤 برای شروع تلاوت بزنید',
  'recite.btn_pause':'⏸ توقف موقت',
  'recite.btn_resume':'▶️ ادامه تلاوت',
  'recite.said_prefix':'شما گفتید: ',
  'recite.where_start':'از ابتدای سوره شروع کردید',
  'recite.where_approx':'📍 تقریباً از کلمه {n} شروع کردید',
  'recite.pct_label':'٪ {pct}',
  'recite.result_perfect':'🌟 عالی! حفظ شما دقیقاً با متن مطابقت دارد',
  'recite.result_great':'✨ آفرین! حفظ شما قوی است',
  'recite.result_good':'📖 خوب — کلمات قرمز را مرور کنید',
  'recite.result_weak':'💪 نیاز به مرور بیشتر دارد',
  'recite.err_inapp_browser':'⚠️ ضبط صدا در مرورگر داخل این برنامه (مسنجر / اینستاگرام و غیره) کار نمی‌کند.\n\nسایت را مستقیماً در Chrome باز کنید:\n۱) روی سه نقطه (⋮) بالای صفحه بزنید\n۲) گزینه «باز کردن در مرورگر» را انتخاب کنید\n\nیا پیوند سایت را کپی کرده و در برنامه Chrome جای‌گذاری کنید.',
  'recite.err_needs_chrome':'⚠️ ضبط صدا برای کار کردن به مرورگر Chrome نیاز دارد.\n\nاگر آیفون دارید: برنامه Chrome را از App Store دانلود کرده و سایت را از آن باز کنید (نه از Safari).\nاگر اندروید دارید: سایت را از برنامه Chrome باز کنید.',
  'recite.err_speech_blocked':'⚠️ شروع ضبط صدا ممکن نشد.\n\nدر آیپد یا آیفون: «دیکته» را در تنظیمات ← عمومی ← صفحه‌کلید فعال کنید و به سایت اجازهٔ استفاده از میکروفون بدهید. اگر باز هم کار نکرد، سایت را از برنامهٔ Chrome باز کنید.',
  'progress.home_btn':'🏠 خانه',
  'progress.subtitle':'سفر حفظ قرآن خود را دنبال کنید',
  'progress.subtitle_empty':'این آغاز شماست — اولین آزمون خود را شروع کنید',
  'progress.subtitle_progress':'{done} از {total} صفحه را کامل کرده‌اید — ادامه دهید 🌿',
  'progress.streak_label':'روز متوالی',
  'progress.streak_best_label':'طولانی‌ترین سلسله',
  'progress.empty_text':'شما هنوز سفر حفظ خود را در اینجا آغاز نکرده‌اید — اولین آزمون را شروع کنید تا پیشرفت شما در این صفحه نمایش داده شود',
  'progress.empty_cta':'اکنون شروع کنید',
  'progress.goal_title':'🎯 هدف روزانه من',
  'progress.goal_not_done':'هنوز هدف امروز را کامل نکرده‌اید',
  'progress.goal_done_headline':'هدف امروز را کامل کردید!',
  'progress.goal_desc':'هدف: حداقل یک فعالیت حفظ در روز',
  'progress.goal_done_msg':'هدف امروز را کامل کردید — آفرین!',
  'progress.badges_title':'🏅 نشان‌ها',
  'progress.rec_stat_pages':'صفحه‌های آزمون‌شده',
  'progress.rec_stat_best':'بهترین درصد',
  'progress.rec_stat_tries':'تلاش‌ها',
  'progress.rec_last_title':'آخرین تلاش‌ها',
  'progress.rec_reached':'تا آیه {a} رسیدید — {c}٪ از صفحه',
  'progress.rec_reached_noayah':'به {c}٪ از صفحه رسیدید',
  'progress.rec_empty':'هنوز این آزمون را انجام نداده‌اید. اکنون شروع کنید تا پیشرفت شما اینجا نمایش داده شود.',
  'progress.rec_go':'شروع آزمون',
  'progress.rec_note':'درصد فقط به کلمات و ترتیب آن‌ها مربوط است، نه حرکات و احکام تجوید.',
  'progress.badge_rec_first':'نخستین آزمون صوتی',
  'progress.badge_rec_90':'۹۰٪ صوتی',
  'progress.badge_rec_surah':'سوره کامل صوتی',
  'progress.badge_week':'یک هفته کامل',
  'progress.badge_first_juz':'اولین جزء کامل‌شده',
  'progress.badge_30days':'۳۰ روز متوالی',
  'progress.badge_100pages':'۱۰۰ صفحه',
  'progress.badge_amma':'جزء عمّ به‌طور کامل',
  'progress.badge_60days':'۶۰ روز متوالی',
  'progress.badge_3surahs':'۳ سوره کامل',
  'progress.badge_300pages':'۳۰۰ صفحه',
  'progress.surah_progress_title':'📚 پیشرفت شما در هر سوره',
  'progress.filter_all_surahs':'همه سوره‌ها',
  'progress.filter_complete':'کامل‌شده',
  'progress.filter_incomplete':'هنوز کامل نشده',
  'progress.filter_empty':'در حال حاضر سوره‌ای با این فیلتر مطابقت ندارد.',
  'progress.review_title':'🔁 فهرست مرور هوشمند',
  'progress.review_empty':'در حال حاضر سؤالی نیاز به مرور ندارد — همین‌طور ادامه دهید 👏',
  'progress.review_remove':'حذف از فهرست مرور',
  'progress.question_label':'سؤال {n}',
  'progress.reminder_title':'🔔 یادآوری روزانه',
  'progress.reminder_enable_label':'فعال‌سازی اعلان‌های یادآوری',
  'progress.reminder_enable_sub':'حتی اگر سایت بسته باشد می‌رسد',
  'progress.reminder_time_label':'زمان:',
  'progress.reminder_note':'اعلان فقط بر اساس زمان است و نمی‌داند وِرد امروز را انجام داده‌اید یا نه (چون سایت حساب کاربری ندارد و داده‌های شما فقط در مرورگرتان ذخیره می‌شود). گاهی زمان‌بندی ممکن است چند دقیقه جابه‌جا شود.',
  'progress.reminder_coming_soon':'ویژگی یادآوری از طریق اعلان در حال حاضر در این سایت در حال فعال‌سازی است.',
  'progress.reminder_denied':'اجازه اعلان برای این سایت در تنظیمات مرورگر مسدود شده است — برای فعال‌سازی بعداً، تنظیمات سایت را در مرورگر باز کرده و اعلان‌ها را مجاز کنید',
  'progress.activating':'در حال فعال‌سازی…',
  'progress.reminder_enabled':'یادآوری فعال شد ✅',
  'progress.reminder_enable_fail':'فعال‌سازی ممکن نشد: ',
  'progress.saving':'در حال ذخیره…',
  'progress.time_updated':'زمان به‌روزرسانی شد ✅',
  'progress.save_fail':'ذخیره ممکن نشد: ',
  'progress.backup_title':'💾 نسخه پشتیبان',
  'progress.backup_none':'هنوز نسخه پشتیبانی گرفته نشده است',
  'progress.last_backup':'آخرین نسخه پشتیبان: ',
  'progress.backup_suggest':'⏰ مدت زیادی گذشته است — بهتر است نسخه پشتیبان جدیدی بگیرید، زیرا داده‌های شما فقط در این مرورگر ذخیره شده است',
  'progress.backup_export_btn':'⬇️ دانلود نسخه پشتیبان',
  'progress.backup_import_btn':'⬆️ وارد کردن نسخه',
  'progress.backup_export_ok':'نسخه پشتیبان دانلود شد ✅',
  'progress.backup_import_ok':'نسخه پشتیبان با موفقیت وارد شد ✅',
  'progress.backup_import_fail':'وارد کردن ممکن نشد: ',
  'progress.unknown_error':'خطای ناشناخته',
  'progress.sync_title':"☁️ پیشرفتت را در حسابت ذخیره کن",
  'progress.sync_desc':"با حساب گوگل ادامه بده تا پیشرفتت ذخیره شود و به‌طور خودکار روی همه دستگاه‌هایت نمایش داده شود، حتی اگر گوشی‌ات را عوض کنی یا داده‌های مرورگر را پاک کنی.",
  'progress.sync_signin_btn':"🔵 ادامه با گوگل",
  'progress.sync_signout_btn':'خروج',
  'progress.sync_now_btn':"🔄 به‌روزرسانی پیشرفتم",
  'progress.sync_signed_in_as':'وارد شده به‌عنوان: ',
  'progress.sync_syncing':"در حال ذخیره پیشرفتت…",
  'progress.sync_ok':"پیشرفتت ذخیره شد ✅",
  'progress.sync_fail':"ذخیره پیشرفتت ناموفق بود: ",
  'progress.sync_unsupported':"ذخیره پیشرفت در حساب در این مرورگر در دسترس نیست"
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
    // متغيرات العدّاد ({cur} / {total}) لسه ما اتحدّدتش قبل بدء الاختبار — نعرض "-" بدل النص الخام
    el.textContent = t(el.getAttribute('data-i18n')).replace(/\{(?:cur|total)\}/g, '-');
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
  scope.querySelectorAll('[data-i18n-aria]').forEach(function(el){
    // تسمية وصولية (aria-label) بلا رموز تعبيرية في أولها
    el.setAttribute('aria-label', t(el.getAttribute('data-i18n-aria')).replace(/^[^A-Za-z\u00C0-\u024F\u0400-\u04FF\u0600-\u06FF\u0750-\u077F]+/, ''));
  });
}

function updateLangMenuUI(code){
  var cur=document.getElementById('tools-lang-cur');
  if(cur) cur.textContent = LANG_LABELS[code] || LANG_LABELS.ar;
  document.querySelectorAll('#tools-lang-list button[data-code]').forEach(function(b){
    b.classList.toggle('lang-active', b.getAttribute('data-code')===code);
  });
}

// علامة صغيرة (✅) جنب "تقدّمي" في قائمة الأدوات لو الزائر مسجّل دخول
// بجوجل من قبل على هذا الجهاز — مجرد مؤشّر بصري خفيف مبني على قراءة
// localStorage (المفتاح اللي بيحفظه darbi-auth-sync.js عند تسجيل
// الدخول/الخروج في progress.html)، من غير ما نحمّل Firebase في أي
// صفحة تانية. بيتنفّذ على كل الصفحات (لأن lang.js محمّل في كلها)،
// وبيتعاد تطبيقه بعد كل applyStaticText() عشان تبديل اللغة ميمسحوش.
function applyProgressSignedBadge(){
  try{
    var signedIn = !!localStorage.getItem('darbi_auth_last_uid_v1');
    document.querySelectorAll('[data-i18n="nav.progress"]').forEach(function(el){
      var mark = el.querySelector('.progress-signed-mark');
      if(signedIn){
        if(!mark){
          mark = document.createElement('span');
          mark.className = 'progress-signed-mark';
          mark.textContent = ' ✅';
          mark.style.cssText = 'font-size:0.75em;';
          el.appendChild(mark);
        }
      } else if(mark){
        mark.remove();
      }
    });
  }catch(e){}
}

// سطر "تسجيل الدخول والمزامنة" في قائمة الأدوات (☰) في كل الصفحات — يفتح
// كارت المزامنة في "تقدّمي". لو الزائر مسجّل دخول من قبل يظهر "المزامنة مفعّلة ✅".
function ensureSyncMenuItem(){
  try{
    var signedIn = !!localStorage.getItem('darbi_auth_last_uid_v1');
    document.querySelectorAll('.tools-menu').forEach(function(menu){
      var item = menu.querySelector('.tools-sync-item');
      if(!item){
        var anchor = null, shareBtn = null, progBtn = null;
        menu.querySelectorAll('.tools-item').forEach(function(b){
          var oc = b.getAttribute('onclick')||'';
          if(oc.indexOf('shareApp')!==-1) shareBtn=b;
          else if(oc.indexOf('progress.html')!==-1) progBtn=b;
        });
        anchor = shareBtn || progBtn;
        item = document.createElement('button');
        item.className = 'tools-item tools-sync-item';
        item.setAttribute('onclick', "toolsClose();location.href='progress.html#sync-card';");
        var span = document.createElement('span');
        item.appendChild(span);
        if(anchor) anchor.after(item); else menu.insertBefore(item, menu.firstChild);
      }
      var sp = item.querySelector('span');
      sp.setAttribute('data-i18n', signedIn ? 'nav.sync_on' : 'nav.sync_signin');
    });
  }catch(e){}
}


// ===== حجم الخط لكل الموقع (تكبير الصفحة كلها: ١٠٠٪ / ١١٥٪ / ١٣٠٪) =====
var FONT_KEY='darbi_fontscale_v1', FONT_STEPS=[1,1.15,1.3];
function getFontStep(){try{var v=parseInt(localStorage.getItem(FONT_KEY),10);return (v>=0&&v<FONT_STEPS.length)?v:0;}catch(e){return 0;}}
function applyFontStep(i){
  try{document.documentElement.style.zoom=(i===0?'':String(FONT_STEPS[i]));}catch(e){}
  try{document.querySelectorAll('.tools-font-item .fs-btn').forEach(function(b){b.classList.toggle('on',+b.getAttribute('data-step')===i);});}catch(e){}
}
function ensureFontItem(){
  try{
    if(!document.getElementById('darbi-fs-style')){
      var st=document.createElement('style');st.id='darbi-fs-style';
      st.textContent='.tools-font-item{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:10px 14px;font-size:0.88rem;color:var(--text,#1A1A1A);}'
        +'.tools-font-item .fs-btns{margin-inline-start:auto;display:flex;gap:5px;}'
        +'.tools-font-item .fs-btn{font-family:inherit;border:1.5px solid var(--border,#E4EAE4);background:var(--card,#fff);color:var(--text,#1A1A1A);border-radius:8px;min-width:34px;height:32px;cursor:pointer;line-height:1;}'
        +'.tools-font-item .fs-btn.on{background:var(--green,#2E6B42);border-color:var(--green,#2E6B42);color:#fff;}';
      document.head.appendChild(st);
    }
    document.querySelectorAll('.tools-menu').forEach(function(menu){
      if(menu.querySelector('.tools-font-item'))return;
      var row=document.createElement('div');row.className='tools-font-item';
      var lab=document.createElement('span');lab.setAttribute('data-i18n','nav.font_size');row.appendChild(lab);
      var box=document.createElement('span');box.className='fs-btns';
      [['A\u2212',0,-1],['A',0,0],['A+',0,1]].forEach(function(d,idx){
        var b=document.createElement('button');b.type='button';b.className='fs-btn';b.textContent=d[0];
        b.setAttribute('data-step',String(idx));
        b.setAttribute('aria-label',['-','=','+'][idx]);
        b.style.fontSize=[0.8,1,1.2][idx]+'rem';
        b.addEventListener('click',function(ev){ev.stopPropagation();try{localStorage.setItem(FONT_KEY,String(idx));}catch(e){}applyFontStep(idx);});
        box.appendChild(b);
      });
      row.appendChild(box);
      row.addEventListener('click',function(ev){ev.stopPropagation();});
      menu.appendChild(row); // في آخر القائمة
    });
    applyFontStep(getFontStep());
  }catch(e){}
}
applyFontStep(getFontStep());

function applyLang(code){
  if(SUPPORTED.indexOf(code)===-1) code='ar';
  setLangPref(code);
  document.documentElement.setAttribute('lang', code);
  document.documentElement.setAttribute('dir', (code==='ar'||code==='fa') ? 'rtl' : 'ltr');
  ensureSyncMenuItem();
  ensureFontItem();
  applyStaticText();
  applyProgressSignedBadge();
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

/* ===== ترجمة عناوين السور وصيغ الآيات (النص القرآني نفسه لا يُترجم أبدًا) =====
   تعمل على نصوص بصيغ محددة فقط (سورة X، الآيات N–N، اكتب الآية… إلخ)، فلا تمسّ أي آية.
   العربية والفارسية تبقيان كما هما. */
(function(){
'use strict';
var SN = [ // [عربي, إنجليزي (يُستعمل للألمانية والإسبانية، والفرنسية بتحويل بسيط), تركي]
['الفاتحة','Al-Fatihah','Fâtiha'],['البقرة','Al-Baqarah','Bakara'],['آل عمران','Ali ‘Imran','Âl-i İmrân'],['النساء','An-Nisa','Nisâ'],['المائدة','Al-Ma’idah','Mâide'],['الأنعام','Al-An’am','En’âm'],['الأعراف','Al-A’raf','A’râf'],['الأنفال','Al-Anfal','Enfâl'],['التوبة','At-Tawbah','Tevbe'],['يونس','Yunus','Yûnus'],
['هود','Hud','Hûd'],['يوسف','Yusuf','Yûsuf'],['الرعد','Ar-Ra’d','Ra’d'],['إبراهيم','Ibrahim','İbrâhîm'],['الحجر','Al-Hijr','Hicr'],['النحل','An-Nahl','Nahl'],['الإسراء','Al-Isra','İsrâ'],['الكهف','Al-Kahf','Kehf'],['مريم','Maryam','Meryem'],['طه','Ta-Ha','Tâhâ'],
['الأنبياء','Al-Anbiya','Enbiyâ'],['الحج','Al-Hajj','Hac'],['المؤمنون','Al-Mu’minun','Mü’minûn'],['النور','An-Nur','Nûr'],['الفرقان','Al-Furqan','Furkân'],['الشعراء','Ash-Shu’ara','Şuarâ'],['النمل','An-Naml','Neml'],['القصص','Al-Qasas','Kasas'],['العنكبوت','Al-‘Ankabut','Ankebût'],['الروم','Ar-Rum','Rûm'],
['لقمان','Luqman','Lokmân'],['السجدة','As-Sajdah','Secde'],['الأحزاب','Al-Ahzab','Ahzâb'],['سبأ','Saba','Sebe’'],['فاطر','Fatir','Fâtır'],['يس','Ya-Sin','Yâsîn'],['الصافات','As-Saffat','Sâffât'],['ص','Sad','Sâd'],['الزمر','Az-Zumar','Zümer'],['غافر','Ghafir','Mü’min'],
['فصلت','Fussilat','Fussilet'],['الشورى','Ash-Shura','Şûrâ'],['الزخرف','Az-Zukhruf','Zuhruf'],['الدخان','Ad-Dukhan','Duhân'],['الجاثية','Al-Jathiyah','Câsiye'],['الأحقاف','Al-Ahqaf','Ahkâf'],['محمد','Muhammad','Muhammed'],['الفتح','Al-Fath','Fetih'],['الحجرات','Al-Hujurat','Hucurât'],['ق','Qaf','Kâf'],
['الذاريات','Adh-Dhariyat','Zâriyât'],['الطور','At-Tur','Tûr'],['النجم','An-Najm','Necm'],['القمر','Al-Qamar','Kamer'],['الرحمن','Ar-Rahman','Rahmân'],['الواقعة','Al-Waqi’ah','Vâkıa'],['الحديد','Al-Hadid','Hadîd'],['المجادلة','Al-Mujadilah','Mücâdele'],['الحشر','Al-Hashr','Haşr'],['الممتحنة','Al-Mumtahanah','Mümtehine'],
['الصف','As-Saff','Saf'],['الجمعة','Al-Jumu’ah','Cuma'],['المنافقون','Al-Munafiqun','Münâfikûn'],['التغابن','At-Taghabun','Teğâbün'],['الطلاق','At-Talaq','Talâk'],['التحريم','At-Tahrim','Tahrîm'],['الملك','Al-Mulk','Mülk'],['القلم','Al-Qalam','Kalem'],['الحاقة','Al-Haqqah','Hâkka'],['المعارج','Al-Ma’arij','Meâric'],
['نوح','Nuh','Nûh'],['الجن','Al-Jinn','Cin'],['المزمل','Al-Muzzammil','Müzzemmil'],['المدثر','Al-Muddaththir','Müddessir'],['القيامة','Al-Qiyamah','Kıyâme'],['الإنسان','Al-Insan','İnsân'],['المرسلات','Al-Mursalat','Mürselât'],['النبأ','An-Naba','Nebe’'],['النازعات','An-Nazi’at','Nâziât'],['عبس','‘Abasa','Abese'],
['التكوير','At-Takwir','Tekvîr'],['الانفطار','Al-Infitar','İnfitâr'],['المطففين','Al-Mutaffifin','Mutaffifîn'],['الانشقاق','Al-Inshiqaq','İnşikâk'],['البروج','Al-Buruj','Bürûc'],['الطارق','At-Tariq','Târık'],['الأعلى','Al-A’la','A’lâ'],['الغاشية','Al-Ghashiyah','Gâşiye'],['الفجر','Al-Fajr','Fecr'],['البلد','Al-Balad','Beled'],
['الشمس','Ash-Shams','Şems'],['الليل','Al-Layl','Leyl'],['الضحى','Ad-Duha','Duhâ'],['الشرح','Ash-Sharh','İnşirâh'],['التين','At-Tin','Tîn'],['العلق','Al-‘Alaq','Alak'],['القدر','Al-Qadr','Kadir'],['البينة','Al-Bayyinah','Beyyine'],['الزلزلة','Az-Zalzalah','Zilzâl'],['العاديات','Al-‘Adiyat','Âdiyât'],
['القارعة','Al-Qari’ah','Kâria'],['التكاثر','At-Takathur','Tekâsür'],['العصر','Al-‘Asr','Asr'],['الهمزة','Al-Humazah','Hümeze'],['الفيل','Al-Fil','Fîl'],['قريش','Quraysh','Kureyş'],['الماعون','Al-Ma’un','Mâûn'],['الكوثر','Al-Kawthar','Kevser'],['الكافرون','Al-Kafirun','Kâfirûn'],['النصر','An-Nasr','Nasr'],
['المسد','Al-Masad','Mesed'],['الإخلاص','Al-Ikhlas','İhlâs'],['الفلق','Al-Falaq','Felâk'],['الناس','An-Nas','Nâs']];
function nrm(s){return String(s).replace(/[ً-ٰٟـۖ-ۭ]/g,'').replace(/[أإآٱ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه').replace(/\s+/g,' ').trim();}
var IDX={};SN.forEach(function(r){IDX[nrm(r[0])]=r;});
IDX[nrm('المنافقين')]=IDX[nrm('المنافقون')];
function surahName(ar,lg){var r=IDX[nrm(ar)];if(!r)return null;if(lg==='tr')return r[2];
  var en=r[1];return lg==='fr'?en.replace(/ah$/,'a'):en;}

var PAR={ // ملاحظات بين قوسين
 'خاتمه السوره':{en:'end of the surah',fr:'fin de la sourate',de:'Ende der Sure',es:'final de la sura',tr:'sûrenin sonu'},
 'ايه الدين':{en:'the verse of debt',fr:'le verset de la dette',de:'der Schuldvers',es:'el versículo de la deuda',tr:'borç ayeti'},
 'ايه الكرسي':{en:'Ayat al-Kursi',fr:'Ayat al-Kursi',de:'Ayat al-Kursi',es:'Ayat al-Kursi',tr:'Âyetü’l-Kürsî'},
 'ختام البقره':{en:'end of Al-Baqarah',fr:'fin d’Al-Baqara',de:'Ende von Al-Baqara',es:'final de Al-Baqara',tr:'Bakara’nın sonu'}
};
var T={
 en:{cnt:function(n){return n+(n==1?' verse':' verses');},sur:function(n){return 'Surah '+n;},vs:function(a,b){return 'Verses '+a+'–'+b;},v:function(a){return 'Verse '+a;},vto:function(a,b){return 'Verses '+a+' to '+b;},ft:function(a,b){return 'From verse '+a+' to verse '+b;},cmp:' (complete)',wvs:function(a,b){return 'Write verses '+a+'–'+b;},wv:function(a){return 'Write verse '+a;},wvo:function(n,s){return 'Write verse '+n+' of Surah '+s+' in full';},test:'Memorization test',juz:'Juz’ Amma',pg:'Page',face:'Side',mp:function(n){return 'Page '+n+' of the Mushaf';},full:function(s,n){return 'Surah '+s+' — complete ('+n+(n==1?' verse)':' verses)');},p:'p.'},
 fr:{cnt:function(n){return n+(n==1?' verset':' versets');},sur:function(n){return 'Sourate '+n;},vs:function(a,b){return 'Versets '+a+'–'+b;},v:function(a){return 'Verset '+a;},vto:function(a,b){return 'Versets '+a+' à '+b;},ft:function(a,b){return 'Du verset '+a+' au verset '+b;},cmp:' (complet)',wvs:function(a,b){return 'Écrivez les versets '+a+'–'+b;},wv:function(a){return 'Écrivez le verset '+a;},wvo:function(n,s){return 'Écrivez le verset '+n+' de la sourate '+s+' en entier';},test:'Test de mémorisation',juz:'Juz’ Amma',pg:'Page',face:'Face',mp:function(n){return 'Page '+n+' du Mushaf';},full:function(s,n){return 'Sourate '+s+' — complète ('+n+(n==1?' verset)':' versets)');},p:'p.'},
 de:{cnt:function(n){return n+(n==1?' Vers':' Verse');},sur:function(n){return 'Sure '+n;},vs:function(a,b){return 'Verse '+a+'–'+b;},v:function(a){return 'Vers '+a;},vto:function(a,b){return 'Verse '+a+' bis '+b;},ft:function(a,b){return 'Von Vers '+a+' bis Vers '+b;},cmp:' (vollständig)',wvs:function(a,b){return 'Schreibe die Verse '+a+'–'+b;},wv:function(a){return 'Schreibe Vers '+a;},wvo:function(n,s){return 'Schreibe Vers '+n+' der Sure '+s+' vollständig';},test:'Auswendig-Test',juz:'Dschuz’ Amma',pg:'Seite',face:'Hälfte',mp:function(n){return 'Seite '+n+' des Mushaf';},full:function(s,n){return 'Sure '+s+' — vollständig ('+n+(n==1?' Vers)':' Verse)');},p:'S.'},
 es:{cnt:function(n){return n+(n==1?' versículo':' versículos');},sur:function(n){return 'Sura '+n;},vs:function(a,b){return 'Versículos '+a+'–'+b;},v:function(a){return 'Versículo '+a;},vto:function(a,b){return 'Versículos '+a+' a '+b;},ft:function(a,b){return 'Del versículo '+a+' al versículo '+b;},cmp:' (completo)',wvs:function(a,b){return 'Escribe los versículos '+a+'–'+b;},wv:function(a){return 'Escribe el versículo '+a;},wvo:function(n,s){return 'Escribe el versículo '+n+' de la sura '+s+' completo';},test:'Prueba de memorización',juz:'Yuz’ Amma',pg:'Página',face:'Cara',mp:function(n){return 'Página '+n+' del Mushaf';},full:function(s,n){return 'Sura '+s+' — completa ('+n+(n==1?' versículo)':' versículos)');},p:'p.'},
 tr:{cnt:function(n){return n+' ayet';},sur:function(n){return n+' Suresi';},vs:function(a,b){return a+'–'+b+'. ayetler';},v:function(a){return a+'. ayet';},vto:function(a,b){return a+'. ayetten '+b+'. ayete kadar';},ft:function(a,b){return a+'. ayetten '+b+'. ayete kadar';},cmp:' (tamamı)',wvs:function(a,b){return a+'–'+b+'. ayetleri yazın';},wv:function(a){return a+'. ayeti yazın';},wvo:function(n,s){return s+' Suresi’nin '+n+'. ayetini eksiksiz yazın';},test:'Ezber testi',juz:'Amme Cüzü',pg:'Sayfa',face:'Yüz',mp:function(n){return 'Mushaf’ın '+n+'. sayfası';},full:function(s,n){return s+' Suresi — tamamı ('+n+' ayet)';},p:'s.'}
};
function dg(s){return String(s).replace(/[٠-٩]/g,function(c){return String(c.charCodeAt(0)-1632);}).replace(/[۰-۹]/g,function(c){return String(c.charCodeAt(0)-1776);});}
var DASH='\\s*[\\u2013\\u2014-]\\s*';
function par(p,lg){if(!p)return '';var r=PAR[nrm(p)];return ' ('+(r&&r[lg]?r[lg]:p)+')';}
function loc(src,lg){
  var L=T[lg];if(!L)return null;
  var s=dg(src).replace(/\s+/g,' ').trim(),m,n;
  var o2=loc2(src,lg);if(o2!==null)return o2;
  if((m=s.match(/^اكتب الآية رقم (\d+) من سورة (.+?) كاملة$/))){n=surahName(m[2],lg);return n?L.wvo(m[1],n):null;}
  if((m=s.match(/^اكتب (?:الآيات|الآيتين) (\d+)\s*[–-]\s*(\d+)$/)))return L.wvs(m[1],m[2]);
  if((m=s.match(/^اكتب الآية (?:رقم )?(\d+)$/)))return L.wv(m[1]);
  if((m=s.match(/^سورة (.+?) كاملة \((\d+) (?:آية|آيات)\)$/))){n=surahName(m[1],lg);return n?L.full(n,+m[2]):null;}
  if((m=s.match(/^سورة (.+?) \((\d+) (?:آية|آيات)\)$/))){n=surahName(m[1],lg);return n?L.sur(n)+' ('+L.cnt(+m[2])+')':null;}
  if((m=s.match(/^(?:(سورة) )?(.+?) ص ?(\d+) — (آيات|آية) (\d+)(?:\s*[–-]\s*(\d+))?(?: \((.+)\))?$/))){n=surahName(m[2],lg);if(!n)return null;
    return (m[1]?L.sur(n):n)+' '+L.p+m[3]+' \u2014 '+(m[6]?L.vs(m[5],m[6]):L.v(m[5]))+par(m[7],lg);}
  if((m=s.match(/^سورة (.+?) — آية (\d+)$/))){n=surahName(m[1],lg);return n?L.sur(n)+' \u2014 '+L.v(m[2]):null;}
  if((m=s.match(/^سورة (.+)$/))){n=surahName(m[1],lg);return n?L.sur(n):null;}
  if((m=s.match(/^(?:الآيتين|الآيتان) (\d+)\s*[–-]\s*(\d+)$/)))return L.vs(m[1],m[2]);
  if((m=s.match(/^من الآية (\d+) إلى الآية (\d+)$/)))return L.ft(m[1],m[2]);
  if((m=s.match(/^الآيات (\d+) إلى (\d+)$/)))return L.vto(m[1],m[2]);
  if((m=s.match(/^الآيات (\d+)\s*[–-]\s*(\d+)( كاملة)?$/)))return L.vs(m[1],m[2])+(m[3]?L.cmp:'');
  if((m=s.match(/^الآية (\d+)(?: \((.+)\))?$/)))return L.v(m[1])+par(m[2],lg);
  if(nrm(s)==='جزء عم')return L.juz;
  if((m=s.match(/^الصفحة (\d+)$/)))return L.pg+' '+m[1];
  if((m=s.match(/^اختبار الحفظ \| (.+)$/))){var parts=m[1].split(' | '),outp=[],x;
    for(var pi=0;pi<parts.length;pi++){var r=parts[pi];
      if(nrm(r)==='جزء عم')outp.push(L.juz);
      else if(nrm(r)==='ام الكتاب')outp.push(lg==='tr'?'Ümmü\u2019l-Kitâb':'Umm al-Kitab');
      else if((x=r.match(/^صفحة (\d+)$/)))outp.push(L.pg+' '+x[1]);
      else if((x=r.match(/^ص ?(\d+)\s*[–-]\s*(\d+)$/)))outp.push(L.p+' '+x[1]+'\u2013'+x[2]);
      else if((x=r.match(/^وجه (\d+) — صفحة (\d+)$/)))outp.push(L.face+' '+x[1]+' \u2014 '+L.pg+' '+x[2]);
      else return null;}
    return L.test+' | '+outp.join(' | ');}
  if((m=s.match(/^صفحة (\d+) من المصحف(?: — (.+))?$/)))return L.mp(m[1]);
  if((m=s.match(/^ص ?(\d+) — (آيات|آية) (\d+)(?:\s*[–-]\s*(\d+))?(?: \((.+)\))?$/)))
    return L.p+m[1]+' — '+(m[4]?L.vs(m[3],m[4]):L.v(m[3]))+par(m[5],lg);
  return null;
}
var X={"en": {"wvf": "Write verse {n} in full", "w2": "Write verses {a} and {b} of Surah {S} in full", "wl": "Write verses {l} of Surah {S} in full", "wr": "Write verses {a}–{b} of Surah {S}", "wrf": "Write verses {a}–{b} of Surah {S} in full", "wsur": "Write the whole surah ({n} verses)", "wk": "Write Ayat al-Kursi (verse {n}) in full", "first": "Write the first part of verse {n}, up to {q}", "last": "Write the last part of verse {n}, from {q} to its end", "begin": "Write the beginning of verse {n}, from {q} to {r}", "end": "Write the end of verse {n}, from {q} to its end", "mid": "Write the middle part of verse {n}, from {q} to {r}", "rg": "Write from {q} to {r}", "rgn": "Write from {q} to {r} (verse {n})", "rge": "Write from {q} to the end of verse {n}", "dayn": "Write the beginning of the verse of debt ({n}), from {q} to {r}", "wvoq": "Write verse {n} of Surah {S}, from {q} to its end", "two1": "Write verses {a} and {b} of Surah {S} (the first sentence of each)", "ident": "Write verses {a}–{b} (two identical verses)", "all": " (with all its parts)", "and_": "and"}, "fr": {"wvf": "Écrivez le verset {n} en entier", "w2": "Écrivez en entier les versets {a} et {b} de la sourate {S}", "wl": "Écrivez en entier les versets {l} de la sourate {S}", "wr": "Écrivez les versets {a}–{b} de la sourate {S}", "wrf": "Écrivez en entier les versets {a}–{b} de la sourate {S}", "wsur": "Écrivez la sourate entière ({n} versets)", "wk": "Écrivez Ayat al-Kursi (verset {n}) en entier", "first": "Écrivez le début du verset {n}, jusqu’à {q}", "last": "Écrivez la fin du verset {n}, à partir de {q}", "begin": "Écrivez le début du verset {n}, de {q} à {r}", "end": "Écrivez la fin du verset {n}, à partir de {q}", "mid": "Écrivez la partie centrale du verset {n}, de {q} à {r}", "rg": "Écrivez de {q} à {r}", "rgn": "Écrivez de {q} à {r} (verset {n})", "rge": "Écrivez de {q} jusqu’à la fin du verset {n}", "dayn": "Écrivez le début du verset de la dette ({n}), de {q} à {r}", "wvoq": "Écrivez le verset {n} de la sourate {S}, à partir de {q} jusqu’à la fin", "two1": "Écrivez les versets {a} et {b} de la sourate {S} (la première phrase de chacun)", "ident": "Écrivez les versets {a}–{b} (deux versets au texte identique)", "all": " (avec toutes ses parties)", "and_": "et"}, "de": {"wvf": "Schreibe Vers {n} vollständig", "w2": "Schreibe die Verse {a} und {b} der Sure {S} vollständig", "wl": "Schreibe die Verse {l} der Sure {S} vollständig", "wr": "Schreibe die Verse {a}–{b} der Sure {S}", "wrf": "Schreibe die Verse {a}–{b} der Sure {S} vollständig", "wsur": "Schreibe die ganze Sure ({n} Verse)", "wk": "Schreibe Ayat al-Kursi (Vers {n}) vollständig", "first": "Schreibe den Anfang von Vers {n} bis {q}", "last": "Schreibe das Ende von Vers {n}, ab {q}", "begin": "Schreibe den Anfang von Vers {n}, von {q} bis {r}", "end": "Schreibe das Ende von Vers {n}, ab {q}", "mid": "Schreibe den mittleren Teil von Vers {n}, von {q} bis {r}", "rg": "Schreibe von {q} bis {r}", "rgn": "Schreibe von {q} bis {r} (Vers {n})", "rge": "Schreibe von {q} bis zum Ende von Vers {n}", "dayn": "Schreibe den Anfang des Schuldverses ({n}), von {q} bis {r}", "wvoq": "Schreibe Vers {n} der Sure {S}, ab {q} bis zum Ende", "two1": "Schreibe die Verse {a} und {b} der Sure {S} (jeweils den ersten Satz)", "ident": "Schreibe die Verse {a}–{b} (zwei Verse mit identischem Text)", "all": " (mit allen Teilen)", "and_": "und"}, "es": {"wvf": "Escribe el versículo {n} completo", "w2": "Escribe completos los versículos {a} y {b} de la sura {S}", "wl": "Escribe completos los versículos {l} de la sura {S}", "wr": "Escribe los versículos {a}–{b} de la sura {S}", "wrf": "Escribe completos los versículos {a}–{b} de la sura {S}", "wsur": "Escribe la sura completa ({n} versículos)", "wk": "Escribe Ayat al-Kursi (versículo {n}) completo", "first": "Escribe el comienzo del versículo {n}, hasta {q}", "last": "Escribe el final del versículo {n}, desde {q}", "begin": "Escribe el comienzo del versículo {n}, de {q} a {r}", "end": "Escribe el final del versículo {n}, desde {q}", "mid": "Escribe la parte central del versículo {n}, de {q} a {r}", "rg": "Escribe de {q} a {r}", "rgn": "Escribe de {q} a {r} (versículo {n})", "rge": "Escribe desde {q} hasta el final del versículo {n}", "dayn": "Escribe el comienzo del versículo de la deuda ({n}), de {q} a {r}", "wvoq": "Escribe el versículo {n} de la sura {S}, desde {q} hasta el final", "two1": "Escribe los versículos {a} y {b} de la sura {S} (la primera frase de cada uno)", "ident": "Escribe los versículos {a}–{b} (dos versículos de texto idéntico)", "all": " (con todas sus partes)", "and_": "y"}, "tr": {"wvf": "{n}. ayeti eksiksiz yazın", "w2": "{S} Suresi’nin {a}. ve {b}. ayetlerini eksiksiz yazın", "wl": "{S} Suresi’nin {l}. ayetlerini eksiksiz yazın", "wr": "{S} Suresi’nin {a}–{b}. ayetlerini yazın", "wrf": "{S} Suresi’nin {a}–{b}. ayetlerini eksiksiz yazın", "wsur": "Sûrenin tamamını yazın ({n} ayet)", "wk": "Âyetü’l-Kürsî’yi ({n}. ayet) eksiksiz yazın", "first": "{n}. ayetin başından {q} ifadesine kadar yazın", "last": "{n}. ayetin {q} ifadesinden sonuna kadar olan kısmını yazın", "begin": "{n}. ayetin başlangıcını, {q} ifadesinden {r} ifadesine kadar yazın", "end": "{n}. ayetin sonunu, {q} ifadesinden itibaren yazın", "mid": "{n}. ayetin orta kısmını, {q} ifadesinden {r} ifadesine kadar yazın", "rg": "{q} ifadesinden {r} ifadesine kadar yazın", "rgn": "{q} ifadesinden {r} ifadesine kadar yazın ({n}. ayet)", "rge": "{q} ifadesinden {n}. ayetin sonuna kadar yazın", "dayn": "Borç ayetinin ({n}) başlangıcını, {q} ifadesinden {r} ifadesine kadar yazın", "wvoq": "{S} Suresi’nin {n}. ayetini {q} ifadesinden sonuna kadar yazın", "two1": "{S} Suresi’nin {a}. ve {b}. ayetlerini yazın (her birinin ilk cümlesi)", "ident": "{a}–{b}. ayetleri yazın (metni aynı olan iki ayet)", "all": " (tüm kısımlarıyla)", "and_": "ve"}};

var ORD1={'الاولي':1,'الثانيه':2,'الثالثه':3,'الرابعه':4,'الخامسه':5,'السادسه':6,'السابعه':7,'الثامنه':8,'التاسعه':9};
var ORDT={'العشرين':20,'الثلاثين':30,'الاربعين':40,'الخمسين':50,'الستين':60,'السبعين':70,'الثمانين':80,'التسعين':90};
function ordNum(w){w=nrm(w);var m,a,b;
  if(ORD1[w])return ORD1[w];if(w==='العاشره')return 10;if(ORDT[w])return ORDT[w];
  if((m=w.match(/^(\S+) عشره$/))){a=m[1]==='الحاديه'?1:ORD1[m[1]];return a&&a>0?10+a:null;}
  if((m=w.match(/^(\S+) و(ال\S+)$/))){a=m[1]==='الحاديه'?1:ORD1[m[1]];b=ORDT[m[2]];return a&&b?a+b:null;}
  return null;}
function fill(t,o){return t.replace(/\{(\w)\}/g,function(_,k){return o[k]===undefined?'':o[k];});}
function qq(x){return '⁧«'+x+'»⁩';}
function joinL(arr,and){return arr.length<2?arr.join(''):arr.slice(0,-1).join(', ')+' '+and+' '+arr[arr.length-1];}
function loc2(src,lg){
  var X2=X[lg];if(!X2)return null;
  var qs=[];var z=dg(src).replace(/«([^»]*)»/g,function(_,x){qs.push(x);return '«Q»';});
  z=nrm(z.replace(/[ً-ٰٟࣔ-ࣿۖ-ۭـ]/g,''));
  var m,n,o;
  function S(x){return surahName(x,lg);}
  if(z.indexOf('اكتب')!==0)return null;
  if((m=z.match(/^اكتب الايه رقم (\d+) من سوره (.+?) كامله( \(بجميع اجزائها\))?$/))){n=S(m[2]);return n?fill(L_(lg).wvo(m[1],n),{})+(m[3]?X2.all:''):null;}
  if((m=z.match(/^اكتب الايه (.+?) من سوره (.+?) كامله( \(بجميع اجزائها\))?$/))){var k=ordNum(m[1]);n=S(m[2]);return (k&&n)?L_(lg).wvo(k,n)+(m[3]?X2.all:''):null;}
  if((m=z.match(/^اكتب الايه رقم (\d+) من سوره (.+?) من «Q» حتي اخرها$/))){n=S(m[2]);return n?fill(X2.wvoq,{n:m[1],S:n,q:qq(qs[0])}):null;}
  if((m=z.match(/^اكتب الايه (\d+) من سوره (.+)$/))){n=S(m[2]);return n?L_(lg).wvo(m[1],n):null;}
  if((m=z.match(/^اكتب الايه (\d+) كامله$/)))return fill(X2.wvf,{n:m[1]});
  if((m=z.match(/^اكتب الايتين (\d+) و(\d+) كاملتين من سوره (.+)$/))){n=S(m[3]);return n?fill(X2.w2,{a:m[1],b:m[2],S:n}):null;}
  if((m=z.match(/^اكتب الايات ([\d و]+) كامله من سوره (.+)$/))){n=S(m[2]);return n?fill(X2.wl,{l:joinL(m[1].match(/\d+/g),X2.and_),S:n}):null;}
  if((m=z.match(/^اكتب الايات (\d+)\s*(?:الي|[–-])\s*(\d+) (كامله )?من سوره (.+)$/))){n=S(m[4]);return n?fill(m[3]?X2.wrf:X2.wr,{a:m[1],b:m[2],S:n}):null;}
  if((m=z.match(/^اكتب السوره كامله \((\d+) ايات\)$/)))return fill(X2.wsur,{n:m[1]});
  if((m=z.match(/^اكتب ايه الكرسي \(الايه (\d+)\) كامله$/)))return fill(X2.wk,{n:m[1]});
  if((m=z.match(/^اكتب الايتين (\d+) و(\d+) من سوره (.+?) \(اول جمله من كل منهما\)$/))){n=S(m[3]);return n?fill(X2.two1,{a:m[1],b:m[2],S:n}):null;}
  if((m=z.match(/^اكتب الايات (\d+)\s*[–-]\s*(\d+) \(ايتان متطابقتان نصا\)$/)))return fill(X2.ident,{a:m[1],b:m[2]});
  if((m=z.match(/^اكتب اول جزء من الايه (\d+) حتي «Q»$/)))return fill(X2.first,{n:m[1],q:qq(qs[0])});
  if((m=z.match(/^اكتب اخر جزء من الايه (\d+) من «Q» حتي اخرها$/)))return fill(X2.last,{n:m[1],q:qq(qs[0])});
  if((m=z.match(/^اكتب بدايه الايه (\d+) من «Q» حتي «Q»$/)))return fill(X2.begin,{n:m[1],q:qq(qs[0]),r:qq(qs[1])});
  if((m=z.match(/^اكتب نهايه الايه (\d+) من «Q» حتي اخرها$/)))return fill(X2.end,{n:m[1],q:qq(qs[0])});
  if((m=z.match(/^اكتب الجزء الاوسط من الايه (\d+) من «Q» حتي «Q»$/)))return fill(X2.mid,{n:m[1],q:qq(qs[0]),r:qq(qs[1])});
  if((m=z.match(/^اكتب من «Q» حتي «Q» من الايه (\d+)$/)))return fill(X2.rgn,{n:m[1],q:qq(qs[0]),r:qq(qs[1])});
  if((m=z.match(/^اكتب من «Q» حتي نهايه الايه (\d+)$/)))return fill(X2.rge,{n:m[1],q:qq(qs[0])});
  if((m=z.match(/^اكتب من «Q» حتي «Q»$/)))return fill(X2.rg,{q:qq(qs[0]),r:qq(qs[1])});
  if((m=z.match(/^اكتب بدايه ايه الدين \((\d+)\) من «Q» حتي «Q»$/)))return fill(X2.dayn,{n:m[1],q:qq(qs[0]),r:qq(qs[1])});
  return null;
}
function L_(lg){return T[lg];}

/* ===== الصفحة الرئيسية: أسماء السور والملاحظات (بطاقات، عناوين الأجزاء، الأزرار) ===== */
var NOTE={
 'البدايه':{en:'beginning',fr:'début',de:'Anfang',es:'inicio',tr:'başlangıç'},
 'ختام الجزء':{en:'end of the juz’',fr:'fin du juz’',de:'Ende des Juz’',es:'final del juz’',tr:'cüzün sonu'},
 'يتبع':{en:'continued below',fr:'suite',de:'wird fortgesetzt',es:'continúa',tr:'devam ediyor'},
 'تابع':{en:'cont.',fr:'suite',de:'Forts.',es:'cont.',tr:'devamı'},
 'تتمه':{en:'continued',fr:'suite',de:'Fortsetzung',es:'continuación',tr:'devamı'}
};
var NOTEBTN={
 en:{c:function(S,j){return S+' continues in Juz’ '+j+' →';},b:function(S,j){return '← '+S+' began in Juz’ '+j;}},
 fr:{c:function(S,j){return S+' continue dans le Juz’ '+j+' →';},b:function(S,j){return '← '+S+' a commencé dans le Juz’ '+j;}},
 de:{c:function(S,j){return S+' wird in Juz’ '+j+' fortgesetzt →';},b:function(S,j){return '← '+S+' begann in Juz’ '+j;}},
 es:{c:function(S,j){return S+' continúa en el Juz’ '+j+' →';},b:function(S,j){return '← '+S+' comenzó en el Juz’ '+j;}},
 tr:{c:function(S,j){return S+', '+j+'. cüzde devam ediyor →';},b:function(S,j){return '← '+S+' '+j+'. cüzde başlamıştı';}}
};
function idxName(x,lg){x=String(x).trim();if(nrm(x)==='جزء عم')return T[lg].juz;
  var o=surahName(x,lg);if(o)return o;
  var m=x.match(/^(.+?) \((.+)\)$/);
  if(m){var a=surahName(m[1],lg);if(!a)return null;var inner=m[2].trim(),nt;
    if(/^[\d\s–-]+$/.test(inner))return a+' ('+dg(inner)+')';
    if((nt=inner.match(/^(تتمة)\s+([\d\s–-]+)$/)))return a+' ('+(NOTE[nrm(nt[1])][lg])+' '+dg(nt[2])+')';
    var r=NOTE[nrm(inner)];return r&&r[lg]?a+' ('+r[lg]+')':null;}
  return null;}
function idxLoc(src,lg){
  var L=T[lg];if(!L)return null;var s=dg(src).replace(/\s+/g,' ').trim(),m,n;
  if((m=s.match(/^ص ?(\d+)$/)))return L.p+' '+m[1];
  if((m=s.match(/^(\d+) (?:آية|آيات)$/)))return L.cnt(+m[1]);
  if((m=s.match(/^(\d+) \+ (.+?) (\d+)\s*[–-]\s*(\d+)$/))){n=surahName(m[2],lg);return n?m[1]+' + '+n+' '+m[3]+'–'+m[4]:null;}
  if(nrm(s)==='قريبا'||s==='قريباً'){return window.darbiT?window.darbiT('home.card_soon_badge'):null;}
  if(nrm(s)==='ايه الكرسي'){var pk=PAR[nrm(s)];return pk&&pk[lg]?pk[lg]:null;}
  var nb=NOTEBTN[lg];
  if(nb){ if((m=s.match(/^سورة (.+?) تكمل في الجزء (\d+) ←$/))){n=surahName(m[1],lg);return n?nb.c(L.sur(n),m[2]):null;}
          if((m=s.match(/^◄ سورة (.+?) بدأت في الجزء (\d+)$/))){n=surahName(m[1],lg);return n?nb.b(L.sur(n),m[2]):null;} }
  if((m=s.match(/^سورة (.+?) \((.+)\)$/))){var q=idxName(m[1]+' ('+m[2]+')',lg);return q?L.sur(q):null;}
  var parts=s.split(/\s*(?: — |،)\s*/),out=[],seps=s.match(/ — |،/g)||[],i;
  for(i=0;i<parts.length;i++){var pn=idxName(parts[i],lg);if(pn===null)return null;out.push(pn);}
  var res=out[0];for(i=1;i<out.length;i++)res+=(seps[i-1]==='،'?', ':' — ')+out[i];
  return res;}
var IDXSEL='.card-name,.surah-name,.surah-panel-title,.juz-title,.card-meta,.note-btn';
var PRE=/^(سورة|الآية|الآيات|الآيتين|الآيتان|من الآية|اكتب|اختبار الحفظ|صفحة|الصفحة|ص ?\d|[^\d]{2,25} ص ?\d+ — )/;

/* عنوان التبويب (document.title): يُترجم بنفس القواعد، والأصل العربي محفوظ للعودة */
function stripLead(x){return String(x).replace(/^[^A-Za-zÀ-ɏ؀-ۿ]+/,'');}
function titleLoc(ar,lg){
  var L=T[lg];if(!L)return null;var s=dg(ar).replace(/\s+/g,' ').trim(),m,T_=window.darbiT;
  var brand=T_?T_('home.title'):null;
  if(s==='دربي لحفظ القرآن')return brand;
  if((m=s.match(/^عن المشروع — دربي لحفظ القرآن$/)))return stripLead(T_('nav.about'))+' — '+brand;
  if((m=s.match(/^تقدّمي — دربي لحفظ القرآن$/)))return stripLead(T_('nav.progress'))+' — '+brand;
  if((m=s.match(/^اختبر حفظك — دربي لحفظ القرآن$/)))return stripLead(T_('home.recite_btn'))+' — '+brand;
  if((m=s.match(/^اختبار حفظ (?:القرآن - )?سورة (.+?)(?:\s*[—-]\s*الآيات [\d–-]+)?(?:\s*[—-]\s*(?:الصفحة|صفحة) (\d+))?(?:\s*\|\s*(.+))?$/))){
    var n=surahName(m[1].trim(),lg);if(!n)return null;
    var out=L.test+' — '+L.sur(n);if(m[2])out+=' — '+L.pg+' '+m[2];
    if(m[3]){var tv=null,tx;if(nrm(m[3])==='جزء عم')tv=L.juz;else if((tx=m[3].match(/^الآيات (\d+)\s*[–-]\s*(\d+)( كاملة)?$/)))tv=L.vs(tx[1],tx[2])+(tx[3]?L.cmp:'');if(tv)out+=' | '+tv;}
    return out;}
  return null;}
var titleAr=null;
function fixTitle(lg){
  try{if(titleAr===null)titleAr=document.title;
    var o=T[lg]?titleLoc(titleAr,lg):null;var want=o===null?titleAr:o;if(document.title!==want)document.title=want;}catch(e){}}
var tracked=[];
function curLang(){return (window.darbiLang&&window.darbiLang())||document.documentElement.lang||'ar';}
function setTxt(el,v){if(el.__dOut===undefined)tracked.push(el);el.textContent=v;el.__dOut=v;}
function doEl(el,lg){
  var t=el.textContent;
  if(el.__dAr!==undefined&&t===el.__dOut){ // أنا من كتب هذا النص؛ المصدر محفوظ
    var o=(T[lg]?loc(el.__dAr,lg):null);
    if(o===null&&T[lg]&&el.matches&&el.matches(IDXSEL))o=idxLoc(el.__dAr,lg);
    var want=o===null?el.__dAr:o;
    if(want!==t){el.__dOut=want;el.textContent=want;}
    return;}
  if(el.closest&&el.closest('[data-no-loc]'))return;
  var isIdx=!!(el.matches&&el.matches(IDXSEL));
  if(!isIdx&&(!PRE.test(t.trim())||t.length>140))return;
  var o2=T[lg]?loc(t,lg):null;
  if(o2===null&&isIdx&&T[lg])o2=idxLoc(t,lg);
  if(o2===null)return;
  el.__dAr=t;if(tracked.indexOf(el)===-1)tracked.push(el);
  el.__dOut=o2;el.textContent=o2;
}
function doLabel(g,lg){
  var t=g.getAttribute('label');if(g.__dArL===undefined){if(!t||!PRE.test(t))return;g.__dArL=t;}
  var o=T[lg]?loc(g.__dArL,lg):null;g.setAttribute('label',o===null?g.__dArL:o);
}
var busy=false,pending=false;
function scan(root){
  var lg=curLang();busy=true;
  try{
    var base=root||document;
    var list=base.querySelectorAll?base.querySelectorAll('div,span,button,option,p,h1,h2,h3,a,label,li'):[];
    for(var i=0;i<list.length;i++){var e=list[i];if(e.children.length===0)doEl(e,lg);}
    if(base.nodeType===1&&base.children.length===0)doEl(base,lg);
    (base.querySelectorAll?base.querySelectorAll('optgroup[label]'):[]).forEach(function(g){doLabel(g,lg);});
    if(!root){ fixTitle(lg); // مرور كامل: أعد ضبط العناصر المتتبَّعة (تغيّر اللغة)
      tracked.forEach(function(el){if(el.isConnected)doEl(el,lg);});
    }
  }catch(e){}
  busy=false;
}
window.darbiIdxLoc=function(ar){try{var lg=curLang();return T[lg]?idxLoc(ar,lg):null;}catch(e){return null;}};
window.darbiLocText=function(s){try{var o=loc(s,curLang());return o===null?s:o;}catch(e){return s;}};
window.darbiDisplayName=function(ar){ // اسم منقول بحروف لاتينية (أو null إن كانت اللغة عربية/فارسية أو الاسم غير معروف)
  try{var lg=curLang();if(!T[lg])return null;var o=loc(ar,lg);if(o!==null)return o;
    var n=surahName(String(ar).replace(/^سورة /,''),lg);return n||null;}catch(e){return null;}};
window.darbiSurahName=function(ar){try{var lg=curLang();return surahName(ar,lg)||ar;}catch(e){return ar;}};
var q=[],sched=false;
function flush(){sched=false;var nodes=q;q=[];nodes.forEach(function(n){if(n.isConnected)scan(n.nodeType===1?n:n.parentElement);});}
function start(){
  scan();
  var mo=new MutationObserver(function(ms){
    if(busy)return;
    var lgChanged=false;
    ms.forEach(function(m){
      if(m.type==='attributes'&&m.target===document.documentElement){lgChanged=true;return;}
      if(m.type==='characterData'){if(m.target.parentElement)q.push(m.target.parentElement);}
      else m.addedNodes.forEach(function(n){if(n.nodeType===1)q.push(n);else if(n.nodeType===3&&n.parentElement)q.push(n.parentElement);});
    });
    if(lgChanged){scan();}
    if(q.length&&!sched){sched=true;(window.requestAnimationFrame||setTimeout)(flush);}
  });
  mo.observe(document.documentElement,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['lang']});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
