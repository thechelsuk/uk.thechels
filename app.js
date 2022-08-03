// check see if your browser supports service workers
if ('serviceWorker' in navigator) {
    navigator.serviceWorker
        .register('sw.js')
        .then(reg => {console.info('Service Worker registration successful: ', reg)})
        .catch(err => {console.warn('Service Worker setup failed: ', err)});
}
