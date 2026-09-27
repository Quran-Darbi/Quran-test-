/*!
 * firebase-messaging-sw.js
 * ---------------------------------------------------------------
 * Service Worker مخصَّص لاستقبال إشعارات Firebase Cloud Messaging
 * في الخلفية (حتى لو المتصفح أو الموقع مقفول). منفصل تمامًا عن
 * service-worker.js الأصلي (بتاع التخزين المؤقّت/PWA)، ومسجَّل
 * بنطاق (scope) مختلف من darbi-push.js حتى ما يتعارضوش.
 * ---------------------------------------------------------------
 */
importScripts('https://www.gstatic.com/firebasejs/10.13.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.13.0/firebase-messaging-compat.js');
importScripts('./firebase-config.js');

firebase.initializeApp(self.DARBI_FIREBASE_CONFIG || {});
const messaging = firebase.messaging();

messaging.onBackgroundMessage(function (payload) {
  const title = (payload.notification && payload.notification.title) || 'دربي لحفظ القرآن';
  const options = {
    body: (payload.notification && payload.notification.body) || '🌙 لم تبدأ وردك اليوم بعد',
    icon: './icons/icon-192x192.png',
    badge: './icons/icon-192x192.png',
    dir: 'rtl',
    lang: 'ar',
    data: payload.data || {}
  };
  self.registration.showNotification(title, options);
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  event.waitUntil(clients.openWindow('./progress.html'));
});
