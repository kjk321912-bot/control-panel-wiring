// 앱을 고친 뒤에는 VERSION을 올려야 태블릿에 새 버전이 내려갑니다.
const VERSION='v5';
const CORE=[
  './','index.html','manifest.webmanifest',
  'icons/icon-192.png','icons/icon-512.png','icons/maskable-512.png','icons/apple-touch-icon.png',
  'img/b01.png','img/b02.png','img/b03.png','img/b04.png','img/b05.png','img/b06.png','img/b07.png','img/b08.png','img/b09.png','img/b10.png','img/b11.png','img/b12.png','img/b13.png','img/b14.png','img/b15.png','img/b16.png','img/b17.png','img/b18.png','img/c01.png','img/c02.png','img/c03.png','img/c04.png','img/c05.png','img/c06.png','img/c07.png','img/c08.png','img/c09.png','img/c10.png','img/c11.png','img/c12.png','img/c13.png','img/c14.png','img/c15.png','img/c16.png','img/c17.png','img/c18.png','img/pin01.png','img/pin10.png'
];
const APP='cpw-app-'+VERSION, FONT='cpw-font';

self.addEventListener('install',e=>{
  e.waitUntil(caches.open(APP).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',e=>{
  e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==APP&&k!==FONT).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener('fetch',e=>{
  const req=e.request;if(req.method!=='GET')return;
  const url=new URL(req.url);
  // 글꼴: 한 번 받은 뒤에는 캐시에서 (오프라인이면 기본 글꼴로 표시)
  if(url.hostname==='fonts.googleapis.com'||url.hostname==='fonts.gstatic.com'){
    e.respondWith(caches.open(FONT).then(async c=>{
      const hit=await c.match(req);if(hit)return hit;
      try{const res=await fetch(req);if(res.ok||res.type==='opaque')c.put(req,res.clone());return res;}catch(_){return new Response('',{status:503});}
    }));
    return;
  }
  if(url.origin!==location.origin)return;
  // 앱 화면: 인터넷이 되면 새 버전을 받고, 안 되면 캐시로
  if(req.mode==='navigate'){
    e.respondWith(fetch(req,{cache:'no-store'}).then(res=>{const cp=res.clone();caches.open(APP).then(c=>c.put('index.html',cp));return res;}).catch(()=>caches.match('index.html')));
    return;
  }
  e.respondWith(caches.match(req,{ignoreSearch:true}).then(hit=>hit||fetch(req).then(res=>{if(res.ok){const cp=res.clone();caches.open(APP).then(c=>c.put(req,cp));}return res;})));
});
