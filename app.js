// check see if your browser supports service workers
if ('serviceWorker' in navigator) {
    navigator.serviceWorker
        // register the service worker script
        .register('sw.js')
        // using promises tell us if successful or there was an error
        .then(reg => {console.info('Service Worker registration successful: ', reg)})
        .catch(err => {console.warn('Service Worker setup failed: ', err)});
}
