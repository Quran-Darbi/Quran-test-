/*!
 * firebase-config.js
 * ---------------------------------------------------------------
 * إعدادات Firebase العامة لموقع دربي — هذه القيم ليست سرّية أصلًا
 * (مصمَّمة لتُستخدم من المتصفح مباشرة)، لكن لازم تُستبدَل بقيم
 * مشروعك الحقيقي في Firebase حتى تعمل ميزة التذكير الحقيقي.
 *
 * من وين تجيبيها:
 *   Firebase Console → ⚙️ إعدادات المشروع → عام → تطبيقاتك (Web app)
 *   → SDK setup and configuration → Config
 *
 * مفتاح VAPID من:
 *   Firebase Console → Project settings → Cloud Messaging
 *   → Web configuration → Web Push certificates → Generate key pair
 *
 * لاحظي: نكتب على self بدل window عمدًا، عشان الملف ده بيتحمّل
 * جوّه Service Worker (firebase-messaging-sw.js) كمان، ومفيش window هناك.
 * ---------------------------------------------------------------
 */
self.DARBI_FIREBASE_CONFIG = {
  apiKey: "ضعي القيمة هنا",
  authDomain: "ضعي القيمة هنا",
  projectId: "ضعي القيمة هنا",
  storageBucket: "ضعي القيمة هنا",
  messagingSenderId: "ضعي القيمة هنا",
  appId: "ضعي القيمة هنا"
};

self.DARBI_FIREBASE_VAPID_KEY = "ضعي القيمة هنا";
