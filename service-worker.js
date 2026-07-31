/* دربي لحفظ القرآن — Service Worker
   الاستراتيجية: Network First with Cache Fallback
   الشبكة أولًا حتى تصل التعديلات الجديدة فورًا، والكاش احتياطي عند انقطاع الاتصال. */

const CACHE = 'darbi-v1';

/* المسارات نسبية عمدًا: تعمل على الدومين المخصص وعلى github.io بلا تعديل */
const BASE = new URL('./', self.registration.scope).pathname;
const PRECACHE = [
  BASE,
  BASE + 'index.html',
  BASE + 'manifest.json',
  BASE + 'icons/icon-192x192.png'
];

/* ---------- التثبيت: تخزين مبدئي متسامح (فشل ملف لا يُسقط التثبيت) ---------- */
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await Promise.all(PRECACHE.map(url =>
      cache.add(new Request(url, { cache: 'reload' })).catch(() => null)
    ));
    await self.skipWaiting();
  })());
});

/* ---------- التفعيل: حذف النسخ القديمة ---------- */
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

/* ---------- الجلب: الشبكة أولًا ثم الكاش ---------- */
self.addEventListener('fetch', event => {
  const req = event.request;

  /* لا نعترض إلا طلبات GET من نفس النطاق (نترك Analytics وQR والخطوط تمر مباشرة) */
  if (req.method !== 'GET') return;
  if (new URL(req.url).origin !== self.location.origin) return;

  event.respondWith((async () => {
    try {
      const fresh = await fetch(req);
      if (fresh && fresh.ok) {
        const cache = await caches.open(CACHE);
        cache.put(req, fresh.clone());
      }
      return fresh;
    } catch (err) {
      const cached = await caches.match(req);
      if (cached) return cached;

      /* صفحة غير مخزّنة والاتصال مقطوع → نرجع الصفحة الرئيسية */
      if (req.mode === 'navigate') {
        const home = await caches.match(BASE + 'index.html');
        if (home) return home;
      }
      throw err;
    }
  })());
});
