const CACHE='ngwama-v2';
const FILES=['/Soc-kinshasa/','/Soc-kinshasa/index.html','/Soc-kinshasa/manifest.json','/Soc-kinshasa/icon-192.png','/Soc-kinshasa/icon-512.png'];
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)))}); 
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.map(k=>{if(k!==CACHE) return caches.delete(k)}))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(fetch(e.request).then(r=>{let c=r.clone();caches.open(CACHE).then(cache=>cache.put(e.request,c));return r}).catch(()=>caches.match(e.request).then(m=>m||caches.match('/Soc-kinshasa/index.html'))))});
