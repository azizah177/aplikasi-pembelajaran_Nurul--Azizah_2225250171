// Service worker sederhana: membuat aplikasi bisa di-"Install" / "Tambahkan ke layar utama" di Android.
const CACHE = "aritma-v1";
const ASET = ["/", "/css/style.css", "/js/app.js", "/js/scene3d.js", "/manifest.json", "/icon.svg"];

self.addEventListener("install", (e) => e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASET))));
self.addEventListener("activate", (e) =>
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))));

// Network dulu, kalau offline pakai cache. API tidak di-cache.
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.pathname.startsWith("/api/")) return;
  e.respondWith(
    fetch(e.request)
      .then((r) => { const cp = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, cp)); return r; })
      .catch(() => caches.match(e.request))
  );
});
