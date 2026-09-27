/*!
 * darbi-progress-plus.js
 * ---------------------------------------------------------------
 * إضافات فوق نظام التتبع الموجود فعليًا في دربي (darbi_progress +
 * saveDarbiProgress في كل صفحة اختبار) — الملف ده مايلمسش ولا يبدّل
 * أي حاجة في النظام القديم، بس بيضيف جنبه:
 *   • قائمة مراجعة ذكية (أسئلة بتتكرر فيها الأخطاء عبر الأيام)
 *   • عداد مواظبة (كام يوم متتالي فاتحة فيه اختبار)
 *   • نسخة احتياطية شاملة (تصدير/استيراد) لكل بيانات التقدم — قرار
 *     مقصود إننا نفضل من غير حسابات/سيرفر: موقع دربي مجاني بدون تسجيل
 *     دخول، وإضافة حسابات حقيقية معناها مسؤولية قانونية حقيقية عن
 *     بيانات شخصية (GDPR) مش مبررة لمشروع بالحجم ده. الملف ده بيتابع
 *     كمان امتى آخر نسخة احتياطية اتاخدت عشان نقترح على الزائرة تاخد
 *     نسخة جديدة كل ١٤ يوم لو عندها تقدم حقيقي (DarbiExtra.shouldSuggestBackup)
 *   • شريط تذكير الورد اليومي
 *
 * التركيب: سطر واحد قبل </body> في أي صفحة اختبار (بعد باقي السكربتات):
 *   <script src="darbi-progress-plus.js"></script>
 *
 * وربط قائمة المراجعة الذكية محتاج سطر إضافي واحد بس في ٣ أماكن
 * (كلهم عندهم نفس الجملة بالظبط: wrongIndices.push(qIndex);) —
 * تتضاف بعدها مباشرة في كل صفحة اختبار:
 *   if(window.DarbiExtra)DarbiExtra.recordMiss(currentLevel,qIndex,questions[qIndex]);
 *
 * ده كل التعديل المطلوب في صفحات الاختبار نفسها. باقي المنطق (الحفظ،
 * القراءة، العرض) كله هنا في الملف ده.
 * ---------------------------------------------------------------
 */
(function (window) {
  'use strict';

  var PROGRESS_KEY = 'darbi_progress'; // النظام الحالي — قراءة فقط من هنا، الكتابة تفضل زي ما هي
  var MISSED_KEY = 'darbi_missed_v1';  // جديد، إضافي
  var STREAK_KEY = 'darbi_streak_v1';  // جديد، إضافي
  var HISTORY_KEY = 'darbi_daily_log_v1'; // جديد، إضافي — تاريخ الأيام التي فيها نشاط (لعرض تتبع الأسبوع)
  var HISTORY_MAX_DAYS = 35; // نحتفظ بآخر ٣٥ يوم بس (كفاية لعرض آخر أسبوع + هامش)
  var BACKUP_META_KEY = 'darbi_backup_meta_v1'; // جديد — آخر مرة اتصدّرت فيها نسخة احتياطية
  var BACKUP_REMIND_DAYS = 14; // كل كام يوم نقترح نسخة احتياطية جديدة

  function todayStr() {
    var d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }

  function safeGetJSON(key, fallback) {
    try {
      var raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function safeSetJSON(key, val) {
    try {
      window.localStorage.setItem(key, JSON.stringify(val));
      return true;
    } catch (e) {
      return false;
    }
  }

  // نفس طريقة استخراج مفتاح الصفحة المستخدمة في saveDarbiProgress الحالية
  // ملحوظة مهمة (اكتُشفت 2026-09-27): RESUME_KEY مُعرَّفة في كل صفحة اختبار
  // بـ`const RESUME_KEY=...` — وأي `const`/`let` في أعلى مستوى سكربت عادي
  // (غير module) بيتحط في السكوب المشترك بين كل وسوم <script> بالصفحة، لكن
  // مايتحطّش كخاصية على window. يعني `window.RESUME_KEY` بترجع undefined
  // دايمًا حتى لو RESUME_KEY نفسها موجودة ومعرَّفة — وده كان بيخلّي
  // currentPageKey() ترجع null دايمًا، وبالتالي recordMiss() كانت بترجع
  // من غير ما تسجّل أي غلطة أبدًا، مهما كان الربط في صفحات الاختبار صحيح.
  // الحل: نجرّب المتغيّر العاري RESUME_KEY الأول (لأنه بيتلاقى في نفس
  // السكوب المشترك)، وwindow.RESUME_KEY كخيار احتياطي فقط.
  function currentPageKey() {
    try {
      if (typeof RESUME_KEY !== 'undefined' && RESUME_KEY) return String(RESUME_KEY).replace('quranResume_', '');
    } catch (e) {}
    try {
      if (window.RESUME_KEY) return String(window.RESUME_KEY).replace('quranResume_', '');
    } catch (e) {}
    return null;
  }

  // ---------- المواظبة ----------
  function touchStreak() {
    var s = safeGetJSON(STREAK_KEY, { lastActiveDate: null, currentStreak: 0, longestStreak: 0 });
    var today = todayStr();
    if (s.lastActiveDate === today) return s;
    if (s.lastActiveDate) {
      var diffDays = Math.round((new Date(today) - new Date(s.lastActiveDate)) / 86400000);
      s.currentStreak = diffDays === 1 ? s.currentStreak + 1 : 1;
    } else {
      s.currentStreak = 1;
    }
    s.longestStreak = Math.max(s.longestStreak || 0, s.currentStreak);
    s.lastActiveDate = today;
    safeSetJSON(STREAK_KEY, s);
    return s;
  }

  function getStreak() {
    return safeGetJSON(STREAK_KEY, { lastActiveDate: null, currentStreak: 0, longestStreak: 0 });
  }

  // ---------- سجل الأيام (لتتبّع الأسبوع في "تقدّمي") ----------
  // بيسجّل اليوم في السجل لو فيه نشاط فعلي النهاردة (نفس شرط hasDoneToday)
  function recordTodayInHistory() {
    if (!hasDoneToday()) return;
    var today = todayStr();
    var hist = safeGetJSON(HISTORY_KEY, []);
    if (hist.indexOf(today) === -1) {
      hist.push(today);
      if (hist.length > HISTORY_MAX_DAYS) hist = hist.slice(hist.length - HISTORY_MAX_DAYS);
      safeSetJSON(HISTORY_KEY, hist);
    }
  }

  // بيرجّع آخر ٧ أيام (من ٦ أيام فاتوا لحد النهاردة) لعرضها كنقاط أسبوع
  function getWeekTracker() {
    var hist = safeGetJSON(HISTORY_KEY, []);
    var shortLabels = ['ح', 'ن', 'ث', 'ر', 'خ', 'ج', 'س']; // فهرسها Date.getDay(): 0=أحد .. 6=سبت
    var days = [];
    var base = new Date();
    for (var i = 6; i >= 0; i--) {
      var d = new Date(base.getFullYear(), base.getMonth(), base.getDate() - i);
      var ds = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
      days.push({
        date: ds,
        done: hist.indexOf(ds) !== -1,
        label: shortLabels[d.getDay()],
        isToday: i === 0
      });
    }
    return days;
  }

  // هل تم إنهاء أي مستوى في أي صفحة النهاردة؟ (مبني على lastVisited
  // الموجودة فعليًا في darbi_progress، تتحدث من saveDarbiProgress الحالية)
  function hasDoneToday() {
    var all = safeGetJSON(PROGRESS_KEY, {});
    var today = todayStr();
    return Object.keys(all).some(function (k) {
      var e = all[k];
      return e && e.lastVisited && String(e.lastVisited).slice(0, 10) === today;
    });
  }

  // ---------- قائمة المراجعة الذكية ----------
  function recordMiss(level, qIndex, question) {
    var pageKey = currentPageKey();
    if (!pageKey || !question) return;
    var answerText = (question.choices && question.choices[question.answer] !== undefined)
      ? question.choices[question.answer]
      : question.answer;
    var all = safeGetJSON(MISSED_KEY, {});
    var k = pageKey + '|' + level + '|' + qIndex;
    var m = all[k] || { pageKey: pageKey, level: level, qIndex: qIndex, missCount: 0 };
    m.qIndex = qIndex; // مضافة 2026-09-27 — تلزم لبناء رابط "أعد المحاولة" المباشر للسؤال نفسه
    m.missCount += 1;
    m.verseText = answerText || m.verseText || '';
    m.lastMissed = todayStr();
    all[k] = m;
    safeSetJSON(MISSED_KEY, all);
  }

  function getReviewQueue(limit) {
    var all = safeGetJSON(MISSED_KEY, {});
    var list = Object.keys(all).map(function (k) { return all[k]; });
    list.sort(function (a, b) { return b.missCount - a.missCount; });
    return list.slice(0, limit || 10);
  }

  // ---------- قراءة ملخصة لصفحة "تقدّمي" (تُبنى لاحقًا فوق دي) ----------
  function getOverallFromProgress(totalPages) {
    var all = safeGetJSON(PROGRESS_KEY, {});
    var done = 0, started = 0;
    Object.keys(all).forEach(function (k) {
      var e = all[k];
      if (!e) return;
      var levels = ['easy', 'medium', 'hard'];
      var allDone = levels.every(function (lvl) { return e[lvl] && e[lvl].done; });
      var anyAttempt = levels.some(function (lvl) { return e[lvl]; });
      if (allDone) done++;
      else if (anyAttempt) started++;
    });
    return { pagesDone: done, pagesStarted: started, totalPages: totalPages || 604 };
  }

  // ---------- نسخة احتياطية شاملة ----------
  function exportBackup() {
    var bundle = {
      version: 1,
      exportedAt: new Date().toISOString(),
      darbi_progress: safeGetJSON(PROGRESS_KEY, {}),
      darbi_missed_v1: safeGetJSON(MISSED_KEY, {}),
      darbi_streak_v1: safeGetJSON(STREAK_KEY, {})
    };
    var blob = new Blob([JSON.stringify(bundle, null, 2)], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'darbi-backup-' + todayStr() + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    safeSetJSON(BACKUP_META_KEY, { lastBackupDate: todayStr() });
  }

  function getLastBackupDate() {
    var meta = safeGetJSON(BACKUP_META_KEY, {});
    return meta.lastBackupDate || null;
  }

  // هل نقترح على الزائرة تاخد نسخة احتياطية جديدة؟ (تُستخدم في صفحة
  // "تقدّمي" — مش شريط منفصل جوه كل صفحة، عشان ميتكررش مع تذكير الورد)
  function shouldSuggestBackup() {
    var hasProgress = Object.keys(safeGetJSON(PROGRESS_KEY, {})).length > 0;
    if (!hasProgress) return false;
    var last = getLastBackupDate();
    if (!last) return true;
    var days = Math.round((new Date(todayStr()) - new Date(last)) / 86400000);
    return days >= BACKUP_REMIND_DAYS;
  }

  function importBackup(file, callback) {
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function (e) {
      try {
        var data = JSON.parse(e.target.result);
        if (data && data.version === 1) {
          if (data.darbi_progress) safeSetJSON(PROGRESS_KEY, data.darbi_progress);
          if (data.darbi_missed_v1) safeSetJSON(MISSED_KEY, data.darbi_missed_v1);
          if (data.darbi_streak_v1) safeSetJSON(STREAK_KEY, data.darbi_streak_v1);
          if (callback) callback(true);
        } else if (callback) callback(false, 'ملف غير متوافق');
      } catch (err) {
        if (callback) callback(false, 'تعذّر قراءة الملف');
      }
    };
    reader.readAsText(file);
  }

  // ---------- شريط تذكير الورد اليومي (داخل الموقع فقط) ----------
  function maybeShowReminderBanner() {
    try {
      if (window.DARBI_NO_REMINDER) return; // صفحات مخصّصة (زي تقدّمي) بتعرض تذكيرها بنفسها
      if (localStorage.getItem('darbiReminderOff') === '1') return;
      var today = todayStr();
      if (sessionStorage.getItem('darbiReminderDismissed') === today) return;
      if (hasDoneToday()) return;

      var bar = document.createElement('div');
      bar.setAttribute('dir', 'rtl');
      bar.style.cssText = [
        'display:flex', 'align-items:center', 'justify-content:center', 'gap:10px', 'flex-wrap:wrap',
        'padding:9px 14px', 'background:var(--green,#2E6B3E)', 'color:#fff',
        'font-family:"Amiri",Tahoma,sans-serif', 'font-size:.82rem', 'position:relative', 'z-index:300'
      ].join(';');
      bar.innerHTML =
        '<span>🌙 لم تبدأ وردك اليوم بعد — أكمل حفظك الآن</span>' +
        '<button type="button" data-darbi-dismiss style="background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.4);color:#fff;border-radius:8px;padding:4px 10px;font-size:.76rem;cursor:pointer;">ذكّرني غدًا</button>' +
        '<button type="button" data-darbi-off style="background:transparent;border:0;color:#e7f0e2;font-size:.72rem;text-decoration:underline;cursor:pointer;">إيقاف نهائي</button>';

      document.body.insertBefore(bar, document.body.firstChild);
      bar.querySelector('[data-darbi-dismiss]').addEventListener('click', function () {
        sessionStorage.setItem('darbiReminderDismissed', today);
        bar.remove();
      });
      bar.querySelector('[data-darbi-off]').addEventListener('click', function () {
        try { localStorage.setItem('darbiReminderOff', '1'); } catch (e) {}
        bar.remove();
      });
    } catch (e) {
      // أي خطأ هنا مايأثرش على باقي الصفحة
    }
  }

  // ---------- القفز المباشر لسؤال معيّن من قائمة المراجعة الذكية ----------
  // لو الصفحة اتفتحت برابط فيه ?review=easy:7 مثلًا، بنحاول نبدأ نفس
  // المستوى وننده showQuestion() على نفس رقم السؤال (qIndex) اللي
  // المستخدم غلط فيه، بدل ما تفضل تبدأ من شاشة اختيار المستوى. بيعتمد
  // على المتغيرات/الدوال المشتركة الموجودة فعليًا في كل صفحة اختبار
  // (selectLevel/startQuiz/showQuestion/qIndex/questions) — بنفس فكرة
  // currentPageKey() فوق (سكوب مشترك بين وسوم <script> في نفس الصفحة).
  // أي خطأ هنا (صفحة قديمة شكلها مختلف مثلًا) بيرجع بصمت لشاشة اختيار
  // المستوى العادية، من غير ما يكسر تحميل الصفحة.
  function jumpToReviewQuestion() {
    try {
      var params = new URLSearchParams(window.location.search);
      var rev = params.get('review');
      if (!rev) return;
      var parts = rev.split(':');
      var level = parts[0];
      var idx = parseInt(parts[1], 10);
      if (['easy', 'medium', 'hard'].indexOf(level) === -1 || isNaN(idx) || idx < 0) return;
      if (typeof selectLevel !== 'function' || typeof startQuiz !== 'function' || typeof showQuestion !== 'function') return;
      selectLevel(level);
      startQuiz();
      if (typeof questions !== 'undefined' && questions && idx < questions.length) {
        qIndex = idx;
        showQuestion();
      }
    } catch (e) {
      // فشل القفز التلقائي مايمنعش الصفحة من الفتح عادي على شاشة اختيار المستوى
    }
  }

  window.DarbiExtra = {
    recordMiss: recordMiss,
    getReviewQueue: getReviewQueue,
    getStreak: getStreak,
    getWeekTracker: getWeekTracker,
    hasDoneToday: hasDoneToday,
    getOverallFromProgress: getOverallFromProgress,
    exportBackup: exportBackup,
    importBackup: importBackup,
    getLastBackupDate: getLastBackupDate,
    shouldSuggestBackup: shouldSuggestBackup
  };

  // تشغيل تلقائي بمجرد تحميل السكربت في أي صفحة
  touchStreak();
  recordTodayInHistory();
  maybeShowReminderBanner();
  jumpToReviewQuestion();

})(window);
