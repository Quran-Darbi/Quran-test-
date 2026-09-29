/*!
 * darbi-auth-sync.js
 * ---------------------------------------------------------------
 * تسجيل دخول اختياري بحساب جوجل (بدون كلمة سر، بدون سيرفر خاص بنا)
 * لمزامنة تقدّم الحفظ بين الأجهزة، حتى لا يُفقد عند مسح بيانات
 * المتصفح أو فتح الموقع من جهاز جديد.
 *
 * يعمل فقط في progress.html (المرحلة الأولى)، ولا يلمس darbi_progress
 * ولا أي نظام موجود فعليًا — إضافي بالكامل ومَبنيّ على نفس مشروع
 * Firebase المستخدم أصلًا في darbi-push.js (quran-darbi).
 *
 * مهم: هذا اختياري تمامًا. الزائر الذي لا يسجّل الدخول يستمر بنفس
 * تجربة اليوم (تخزين محلي فقط عبر localStorage).
 *
 * التخزين السحابي: وثيقة واحدة لكل مستخدم في مجموعة Firestore
 * "darbi_users"، مفتاحها = uid الحساب. الحقول: progress / missed /
 * streak / history (نسخة من نفس بيانات localStorage) + email/
 * displayName (لعرض اسم الحساب المسجَّل فقط) + updatedAt.
 *
 * استراتيجية الدمج (merge)، مهمة عشان محدش يفقد تقدّمه:
 * عند كل تسجيل دخول أو ضغطة "مزامنة الآن"، تُدمَج نسخة الجهاز الحالي
 * مع نسخة السحابة بأخذ "الأفضل" من كل جانب لكل صفحة/مستوى (وليس
 * استبدال جانب بالكامل بالآخر) — فلا يمكن لعملية مزامنة أن تمحو
 * تقدّمًا محرَزًا فعلاً على أي من الجهازين.
 *
 * التركيب في progress.html (بعد باقي سكربتات Firebase):
 *   <script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-auth-compat.js"></script>
 *   ... (باقي سكربتات firebase + firebase-config.js كما هي) ...
 *   <script src="darbi-auth-sync.js"></script>
 * ---------------------------------------------------------------
 */
(function (window) {
  'use strict';

  var PROGRESS_KEY = 'darbi_progress';
  var MISSED_KEY = 'darbi_missed_v1';
  var STREAK_KEY = 'darbi_streak_v1';
  var HISTORY_KEY = 'darbi_daily_log_v1';
  var COLLECTION = 'darbi_users';
  var LAST_UID_KEY = 'darbi_auth_last_uid_v1'; // معلوماتي فقط (لعرض حالة "كان مسجّلاً" بسرعة قبل رد Firebase)

  var app = null, auth = null, db = null, provider = null;
  var currentUser = null;
  var onChangeCb = null;

  function safeGetJSON(key, fallback) {
    try {
      var raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) { return fallback; }
  }
  function safeSetJSON(key, val) {
    try { window.localStorage.setItem(key, JSON.stringify(val)); return true; }
    catch (e) { return false; }
  }

  function configReady() {
    var c = window.DARBI_FIREBASE_CONFIG;
    return !!(c && c.apiKey && String(c.apiKey).indexOf('ضعي') === -1);
  }

  function supported() {
    return !!(window.firebase && window.firebase.auth && configReady());
  }

  function ensureApp() {
    if (app) return app;
    app = (window.firebase.apps && window.firebase.apps.length) ? window.firebase.apps[0] : window.firebase.initializeApp(window.DARBI_FIREBASE_CONFIG);
    auth = window.firebase.auth();
    db = window.firebase.firestore();
    provider = new window.firebase.auth.GoogleAuthProvider();
    return app;
  }

  // ---------- دمج البيانات (لا يمحو تقدّمًا من أي جانب) ----------
  function laterDate(a, b) {
    if (!a) return b || null;
    if (!b) return a || null;
    return (new Date(a) > new Date(b)) ? a : b;
  }

  function mergeProgress(local, cloud) {
    local = local || {}; cloud = cloud || {};
    var keys = {};
    Object.keys(local).forEach(function (k) { keys[k] = true; });
    Object.keys(cloud).forEach(function (k) { keys[k] = true; });
    var out = {};
    Object.keys(keys).forEach(function (pageKey) {
      var l = local[pageKey] || {};
      var c = cloud[pageKey] || {};
      var merged = {};
      ['easy', 'medium', 'hard'].forEach(function (level) {
        var ml = l[level], mc = c[level];
        if (!ml && !mc) return;
        merged[level] = {
          done: !!(ml && ml.done) || !!(mc && mc.done),
          score: Math.max((ml && ml.score) || 0, (mc && mc.score) || 0)
        };
      });
      merged.lastVisited = laterDate(l.lastVisited, c.lastVisited);
      out[pageKey] = merged;
    });
    return out;
  }

  function mergeMissed(local, cloud) {
    local = local || {}; cloud = cloud || {};
    var out = {};
    Object.keys(local).forEach(function (k) { out[k] = local[k]; });
    Object.keys(cloud).forEach(function (k) {
      var c = cloud[k], l = out[k];
      if (!l) { out[k] = c; return; }
      out[k] = {
        pageKey: l.pageKey || c.pageKey,
        level: l.level || c.level,
        qIndex: (l.qIndex != null) ? l.qIndex : c.qIndex,
        missCount: Math.max(l.missCount || 0, c.missCount || 0),
        verseText: l.verseText || c.verseText || '',
        lastMissed: laterDate(l.lastMissed, c.lastMissed)
      };
    });
    return out;
  }

  function mergeStreak(local, cloud) {
    var l = local || { lastActiveDate: null, currentStreak: 0, longestStreak: 0 };
    var c = cloud || { lastActiveDate: null, currentStreak: 0, longestStreak: 0 };
    var newer = laterDate(l.lastActiveDate, c.lastActiveDate);
    var base = (newer === c.lastActiveDate && c.lastActiveDate) ? c : l;
    return {
      lastActiveDate: newer,
      currentStreak: Math.max(base.currentStreak || 0, (newer === l.lastActiveDate ? (l.currentStreak || 0) : 0), (newer === c.lastActiveDate ? (c.currentStreak || 0) : 0)),
      longestStreak: Math.max(l.longestStreak || 0, c.longestStreak || 0, l.currentStreak || 0, c.currentStreak || 0)
    };
  }

  function mergeHistory(local, cloud) {
    var set = {};
    (local || []).forEach(function (d) { set[d] = true; });
    (cloud || []).forEach(function (d) { set[d] = true; });
    var out = Object.keys(set).sort();
    return out.slice(Math.max(0, out.length - 35));
  }

  function readLocalBundle() {
    return {
      progress: safeGetJSON(PROGRESS_KEY, {}),
      missed: safeGetJSON(MISSED_KEY, {}),
      streak: safeGetJSON(STREAK_KEY, { lastActiveDate: null, currentStreak: 0, longestStreak: 0 }),
      history: safeGetJSON(HISTORY_KEY, [])
    };
  }

  function writeLocalBundle(b) {
    safeSetJSON(PROGRESS_KEY, b.progress);
    safeSetJSON(MISSED_KEY, b.missed);
    safeSetJSON(STREAK_KEY, b.streak);
    safeSetJSON(HISTORY_KEY, b.history);
  }

  // ---------- المزامنة الفعلية ----------
  function syncNow(cb) {
    if (!currentUser) { cb && cb(false, 'لم يتم تسجيل الدخول'); return; }
    ensureApp();
    var uid = currentUser.uid;
    var ref = db.collection(COLLECTION).doc(uid);
    ref.get().then(function (snap) {
      var cloud = snap.exists ? (snap.data() || {}) : {};
      var local = readLocalBundle();
      var merged = {
        progress: mergeProgress(local.progress, cloud.progress),
        missed: mergeMissed(local.missed, cloud.missed),
        streak: mergeStreak(local.streak, cloud.streak),
        history: mergeHistory(local.history, cloud.history)
      };
      writeLocalBundle(merged);
      return ref.set({
        progress: merged.progress,
        missed: merged.missed,
        streak: merged.streak,
        history: merged.history,
        email: currentUser.email || null,
        displayName: currentUser.displayName || null,
        updatedAt: new Date().toISOString()
      });
    }).then(function () {
      cb && cb(true);
    }).catch(function (err) {
      cb && cb(false, (err && err.message) || 'خطأ غير معروف');
    });
  }

  // ---------- تسجيل الدخول / الخروج ----------
  function signIn(cb) {
    if (!supported()) { cb && cb(false, 'المزامنة غير متاحة على هذا المتصفح'); return; }
    ensureApp();
    auth.signInWithPopup(provider).then(function () {
      cb && cb(true);
    }).catch(function (err) {
      // بعض المتصفحات (متصفح داخل تطبيق آخر، أو حظر النوافذ المنبثقة) تمنع signInWithPopup
      var code = err && err.code;
      if (code === 'auth/popup-blocked' || code === 'auth/operation-not-supported-in-this-environment' || code === 'auth/cancelled-popup-request') {
        try {
          auth.signInWithRedirect(provider);
          cb && cb(true); // سيُستكمل بعد إعادة التحميل عبر getRedirectResult في init()
        } catch (e) {
          cb && cb(false, (e && e.message) || 'تعذّر تسجيل الدخول');
        }
        return;
      }
      cb && cb(false, (err && err.message) || 'تعذّر تسجيل الدخول');
    });
  }

  function signOutUser(cb) {
    if (!supported()) { cb && cb(true); return; }
    ensureApp();
    auth.signOut().then(function () {
      try { localStorage.removeItem(LAST_UID_KEY); } catch (e) {}
      cb && cb(true);
    }).catch(function (err) {
      cb && cb(false, (err && err.message) || 'خطأ غير معروف');
    });
  }

  // ---------- التهيئة ----------
  function init(onChange) {
    onChangeCb = onChange;
    if (!supported()) { onChange && onChange({ status: 'unsupported' }); return; }
    ensureApp();
    // نلتقط نتيجة signInWithRedirect لو حصلت
    auth.getRedirectResult().catch(function () {});
    auth.onAuthStateChanged(function (user) {
      currentUser = user || null;
      if (user) {
        try { localStorage.setItem(LAST_UID_KEY, user.uid); } catch (e) {}
        onChangeCb && onChangeCb({ status: 'syncing', user: user });
        syncNow(function (ok, err) {
          onChangeCb && onChangeCb({ status: ok ? 'signed-in' : 'sync-error', user: user, error: err });
        });
      } else {
        onChangeCb && onChangeCb({ status: 'signed-out' });
      }
    });
  }

  window.DarbiAuth = {
    supported: supported,
    init: init,
    signIn: signIn,
    signOut: signOutUser,
    syncNow: syncNow,
    getUser: function () { return currentUser; },
    isSignedIn: function () { return !!currentUser; }
  };

})(window);
