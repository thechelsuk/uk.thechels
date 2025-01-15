'use strict';

const CACHE_VERSION = {{ site.github.build_revision }};
let CURRENT_CACHES = {
  offline: 'offline-v' + CACHE_VERSION
};
const OFFLINE_URL = 'about.html';

function createCacheBustedRequest(url) {
  let request = new Request(url, {cache: 'reload'});
  if ('cache' in request) {
    return request;
  }

  // If {cache: 'reload'} didn't have any effect, append a cache-busting URL parameter instead.
  let bustedUrl = new URL(url, self.location.href);
  bustedUrl.search += (bustedUrl.search ? '&' : '') + 'cachebust=' + Date.now();
  return new Request(bustedUrl);
}

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CURRENT_CACHES).then(function(cache) {
      return cache.addAll(
        [
          '/style.css',
          '/index.html',
          '/images/gh-header-image-cropped.jpg',
          '/images/logo.png',
          '/images/me72.png',
          '/about.html',
          '/books.html',
          '/cv.html',
          '/manual.html',
          '/podcasts.html',
        ]
      );
    })
  );
});

self.addEventListener('activate', event => {
  let expectedCacheNames = Object.keys(CURRENT_CACHES).map(function(key) {
    return CURRENT_CACHES[key];
  });

  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (expectedCacheNames.indexOf(cacheName) === -1) {
            console.log('Deleting out of date cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate' ||
      (event.request.method === 'GET' &&
       event.request.headers.get('accept').includes('text/html'))) {
    console.log('Handling fetch event for', event.request.url);
    event.respondWith(
      fetch(event.request).catch(error => {
        console.log('Fetch failed; returning offline page instead.', error);
        return caches.match(OFFLINE_URL);
      })
    );
  }
});
