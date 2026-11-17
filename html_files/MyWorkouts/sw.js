// App assets only. Workout/account data stays in the existing account-scoped stores.
const BUILD='36d87dacd84d41d3';
const base=new URL('./',self.location.href);
const CACHE_PREFIX='myworkouts-assets-'+encodeURIComponent(base.pathname)+'-';
const CACHE=CACHE_PREFIX+BUILD;
self.addEventListener('install',event=>event.waitUntil((async()=>{
 const cache=await caches.open(CACHE);const response=await fetch(new Request(base.href,{cache:'no-cache'}));
 if(!response.ok||!response.headers.get('content-type')?.includes('text/html'))throw new Error('App shell unavailable');
 await cache.put(base.href,response);await self.skipWaiting();
})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{
 for(const name of await caches.keys())if(name.startsWith(CACHE_PREFIX)&&name!==CACHE)await caches.delete(name);
 await self.clients.claim();
})()));
self.addEventListener('fetch',event=>{
 const request=event.request;if(request.method!=='GET')return;const url=new URL(request.url);
 const navigation=request.mode==='navigate'&&url.origin===base.origin&&(url.pathname===base.pathname||url.pathname===base.pathname+'index.html');
 const localMedia=url.origin===base.origin&&url.pathname.startsWith(base.pathname+'exercises/')&&/\.(gif|png|jpe?g|webp|svg)$/.test(url.pathname);
 const staticAsset=localMedia||(url.origin==='https://www.gstatic.com'&&url.pathname.startsWith('/firebasejs/'))||url.origin==='https://fonts.googleapis.com'||url.origin==='https://fonts.gstatic.com';
 if(!navigation&&!staticAsset)return;
 event.respondWith((async()=>{
  const cache=await caches.open(CACHE),key=navigation?base.href:request;
  const cached=await cache.match(key);if(cached)return cached;
  const response=await fetch(request);if(response.ok)try{await cache.put(key,response.clone());}catch{}return response;
 })());
});
self.addEventListener('notificationclick',event=>{
 event.notification.close();const candidate=new URL(event.notification.data?.url||base.href,base);
 const target=candidate.origin===base.origin&&candidate.pathname.startsWith(base.pathname)?candidate.href:base.href;
 event.waitUntil((async()=>{const windows=await self.clients.matchAll({type:'window',includeUncontrolled:true});const existing=windows.find(client=>new URL(client.url).pathname.startsWith(base.pathname));if(existing)await existing.focus();else await self.clients.openWindow(target);})());
});
