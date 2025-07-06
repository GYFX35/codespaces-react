const CACHE_NAME = 'openpage-v1';
const urlsToCache = [
    '/', // Corresponds to post_list_view
    '/post/create/', // Corresponds to create_post_view
    // We should ideally cache specific, versioned static assets like CSS and JS.
    // For now, let's add the JS file we know.
    // The manifest file is also good to cache.
    '/static/openpage/js/create_post.js',
    '/static/openpage/manifest.json',
    // Add placeholder paths for main site CSS if/when created, e.g., '/static/css/main.css'
    // Add placeholder paths for any specific app CSS, e.g., '/static/openpage/css/style.css'
    '/offline/' // Our offline fallback page URL
];

// Install event: Cache core assets
self.addEventListener('install', event => {
    console.log('[Service Worker] Install event');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[Service Worker] Caching app shell');
                // AddAll can fail if any of the resources fail to fetch.
                // Consider adding them individually with error handling if some are non-critical.
                return cache.addAll(urlsToCache.map(url => new Request(url, { cache: 'reload' })));
            })
            .catch(error => {
                console.error('[Service Worker] Failed to cache app shell:', error);
            })
    );
});

// Activate event: Clean up old caches
self.addEventListener('activate', event => {
    console.log('[Service Worker] Activate event');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== CACHE_NAME) {
                        console.log('[Service Worker] Clearing old cache:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    return self.clients.claim(); // Ensure new service worker takes control immediately
});

// Fetch event: Serve cached content when offline, or fetch from network
self.addEventListener('fetch', event => {
    console.log('[Service Worker] Fetch event for:', event.request.url);
    // We only want to handle GET requests for caching strategy
    if (event.request.method !== 'GET') {
        return;
    }

    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    console.log('[Service Worker] Found in cache:', event.request.url);
                    return response; // Serve from cache
                }
                console.log('[Service Worker] Not found in cache, fetching from network:', event.request.url);
                return fetch(event.request)
                    .then(networkResponse => {
                        // Optional: Cache new requests dynamically if needed
                        // Be careful with what you cache dynamically, especially for non-static assets
                        // if (networkResponse && networkResponse.status === 200 && event.request.url.startsWith(self.location.origin)) {
                        //     const responseToCache = networkResponse.clone();
                        //     caches.open(CACHE_NAME)
                        //         .then(cache => {
                        //             cache.put(event.request, responseToCache);
                        //         });
                        // }
                        return networkResponse;
                    })
                    .catch(error => {
                        console.error('[Service Worker] Fetch failed for:', event.request.url, error);
                        // If fetching fails (e.g., user is offline) and it's a navigation request,
                        // try to return the offline fallback page.
                        if (event.request.mode === 'navigate') {
                            console.log('[Service Worker] Serving offline page.');
                            return caches.match('/offline/');
                        }
                        // For non-navigation requests (like images, scripts),
                        // we don't return the offline page, just let the fetch fail.
                        // A more robust solution might return placeholder images/data.
                        return Promise.reject(error); // Ensure the promise chain rejects
                    });
            })
    );
});
