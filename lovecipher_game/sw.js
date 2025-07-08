const CACHE_NAME = 'lovecipher-cache-v1';
const CORE_ASSETS = [
  '.', // Alias for index.html
  'index.html',
  'style.css',
  'script.js',
  'manifest.json', // Good to cache the manifest too
  'icons/icon-192x192.png',
  'icons/icon-512x512.png'
];

// Install event: Cache core assets
self.addEventListener('install', event => {
  console.log('SW: Install event');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('SW: Caching core assets');
        return cache.addAll(CORE_ASSETS);
      })
      .then(() => self.skipWaiting()) // Activate worker immediately
      .catch(error => {
        console.error('SW: Failed to cache core assets:', error);
      })
  );
});

// Activate event: Clean up old caches if any
self.addEventListener('activate', event => {
  console.log('SW: Activate event');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('SW: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim()) // Claim clients immediately
  );
});

// Fetch event: Serve from cache first, then network
self.addEventListener('fetch', event => {
  // console.log('SW: Fetch event for:', event.request.url);
  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          // console.log('SW: Serving from cache:', event.request.url);
          return cachedResponse;
        }
        // console.log('SW: Fetching from network:', event.request.url);
        return fetch(event.request).then(networkResponse => {
          // Optionally, cache new requests dynamically if needed
          // For this basic setup, we only cache core assets on install.
          // If you want to cache other things (e.g., images loaded by CSS/JS, API calls):
          /*
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
          }
          */
          return networkResponse;
        }).catch(error => {
          console.error('SW: Fetch failed; returning offline page or error for:', event.request.url, error);
          // Optionally, return a fallback offline page if appropriate
          // For a single-page app like this, if index.html is cached, it should mostly work.
        });
      })
  );
});
