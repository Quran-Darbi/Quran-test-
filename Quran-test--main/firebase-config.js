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
  apiKey: "AIzaSyCdmE5x5kU7YWQsonpo11OVvvEljBm7Enw",
  authDomain: "quran-darbi.firebaseapp.com",
  projectId: "quran-darbi",
  storageBucket: "quran-darbi.firebasestorage.app",
  messagingSenderId: "539368696486",
  appId: "1:539368696486:web:0665adbf273ea62b5d2267"
};

self.DARBI_FIREBASE_VAPID_KEY = "BKhu87w46C5LVD_46YU_BwVR1XJDoTeszXpZoznOhyZSx5yL_o7jg9FBQeE5vmptTrwJ4mPRPpFliwdhZmNQUPM";
