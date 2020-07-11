if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/static/js/sw.js').then(function (registration) {
        }, function (err) {
        });
    });
}