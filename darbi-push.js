/*!
 * darbi-push.js
 * ---------------------------------------------------------------
 * تسجيل/إلغاء تذكير الورد اليومي عبر إشعارات حقيقية (Firebase Cloud
 * Messaging). يعمل فقط في progress.html، ولا يلمس darbi_progress
 * ولا أي نظام موجود فعليًا. إضافي بالكامل.
 *
 * التخزين: وثيقة واحدة في Firestore لكل جهاز، مفتاحها = رمز الجهاز
 * (FCM token) نفسه — بدون أي حساب أو بيانات شخصية. الحقول المحفوظة:
 *   utcTime      وقت التذكير المطلوب بتوقيت UTC ("HH:MM")
 *   localTime    نفس الوقت بالتوقيت المحلي وقت الحفظ (لعرضه فقط)
 *   timezone     المنطقة الزمنية للجهاز (معلوماتية)
 *   lastSentDate آخر يوم اتبعت فيه رسالة (يمنع التكرار في نفس اليوم)
 *   updatedAt    وقت آخر تحديث
 *
 * الإرسال الفعلي يتم من خارج المتصفح تمامًا: GitHub Action مجدولة
 * (راجعي .github/workflows/daily-reminder.yml) بتقرأ Firestore
 * وتبعت عبر Firebase Admin SDK.
 * ---------------------------------------------------------------
 */
(function (window) {
  'use strict';

  var TOKEN_KEY = 'darbi_push_token_v1';
  var SW_PATH = 'firebase-messaging-sw.js';
  var SW_SCOPE = '/firebase-cloud-messaging-push-scope';
  var COLLECTION = 'darbi_reminders';

  var app = null, messaging = null, db = null;

  function configReady() {
    var c = window.DARBI_FIREBASE_CONFIG;
    return !!(c && c.apiKey && String(c.apiKey).indexOf('ضعي') === -1);
  }

  function browserSupported() {
    return !!(window.firebase && 'Notification' in window && 'serviceWorker' in navigator);
  }

  function supported() {
    return browserSupported() && configReady();
  }

  function status() {
    if (!browserSupported()) return 'unsupported';
    if (!configReady()) return 'not-configured';
    if (Notification.permission === 'denied') return 'denied';
    if (Notification.permission !== 'granted') return 'default';
    return localStorage.getItem(TOKEN_KEY) ? 'active' : 'granted-inactive';
  }

  function ensureApp() {
    if (app) return app;
    app = firebase.initializeApp(window.DARBI_FIREBASE_CONFIG);
    messaging = firebase.messaging();
    db = firebase.firestore();
    return app;
  }

  // بتحوّل "20:00" (محلي، وقت الحفظ) إلى مكافئها بتوقيت UTC، اعتمادًا
  // على فارق التوقيت الحالي للجهاز (لا يُعاد حسابه تلقائيًا لاحقًا —
  // إعادة حفظ الوقت بعد تغيّر التوقيت الصيفي/الشتوي يصحّحه من جديد)
  function utcHHMMFromLocal(hhmm) {
    var parts = String(hhmm).split(':');
    var h = parseInt(parts[0], 10) || 0;
    var m = parseInt(parts[1], 10) || 0;
    var now = new Date();
    var local = new Date(now.getFullYear(), now.getMonth(), now.getDate(), h, m, 0);
    return String(local.getUTCHours()).padStart(2, '0') + ':' + String(local.getUTCMinutes()).padStart(2, '0');
  }

  function enable(localTime, cb) {
    if (!supported()) { cb && cb(false, 'غير مدعوم على هذا المتصفح/الجهاز'); return; }
    ensureApp();
    Notification.requestPermission().then(function (perm) {
      if (perm !== 'granted') { cb && cb(false, 'تم رفض إذن الإشعارات'); return; }
      navigator.serviceWorker.register(SW_PATH, { scope: SW_SCOPE })
        .then(function (reg) {
          return messaging.getToken({ vapidKey: window.DARBI_FIREBASE_VAPID_KEY, serviceWorkerRegistration: reg });
        })
        .then(function (token) {
          if (!token) { cb && cb(false, 'تعذّر الحصول على رمز الجهاز'); return; }
          var tz = 'UTC';
          try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC'; } catch (e) {}
          var utcTime = utcHHMMFromLocal(localTime);
          db.collection(COLLECTION).doc(token).set({
            utcTime: utcTime,
            localTime: localTime,
            timezone: tz,
            lastSentDate: null,
            updatedAt: new Date().toISOString()
          }).then(function () {
            localStorage.setItem(TOKEN_KEY, token);
            cb && cb(true);
          }).catch(function (err) {
            cb && cb(false, 'تعذّر الحفظ: ' + (err && err.message));
          });
        })
        .catch(function (err) {
          cb && cb(false, 'تعذّر تفعيل الإشعارات: ' + (err && err.message));
        });
    }).catch(function (err) {
      cb && cb(false, 'تعذّر طلب الإذن: ' + (err && err.message));
    });
  }

  function disable(cb) {
    var token = localStorage.getItem(TOKEN_KEY);
    if (!token) { cb && cb(true); return; }
    try {
      ensureApp();
      db.collection(COLLECTION).doc(token).delete()
        .then(function () { localStorage.removeItem(TOKEN_KEY); cb && cb(true); })
        .catch(function () { localStorage.removeItem(TOKEN_KEY); cb && cb(true); });
    } catch (e) {
      localStorage.removeItem(TOKEN_KEY);
      cb && cb(true);
    }
  }

  window.DarbiPush = {
    supported: supported,
    status: status,
    enable: enable,
    disable: disable
  };
})(window);
