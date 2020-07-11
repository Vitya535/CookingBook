const CACHE_NAME = 'offline-cooking-book';
const urlsToCache = [
    '/',
    '/about',
    '/dishes/salads_and_appetizers',
    '/dishes/sandwiches',
    '/dishes/meat_dishes',
    '/dishes/fish_and_seafood',
    '/dishes/sauces_and_marinades',
    '/dishes/vegetable_dishes',
    '/dishes/milk_dishes',
    '/dishes/cereals_and_pasta',
    '/dishes/cakes_and_pastries',
    '/dishes/fruit_dishes',
    '/dishes/lean_dishes',
    '/dishes/sweet_food_and_drinks',
    '/static/robots.txt',
    'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.0/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.4/jquery-confirm.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.1/css/solid.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.4.2/umd/popper.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.0/js/bootstrap.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.4/jquery-confirm.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.1/js/fontawesome.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.1/js/solid.min.js',
    '/static/css/common.css',
    '/static/js/sw_register.js',
    '/static/gen/jquery-confirm_fontawesome_custom.css',
    '/static/gen/popper_bootstrap_jquery-confirm.js',
    '/static/img/background_first_page.webp',
    '/static/img/keks_rojdestvenskii_s_mandarinami.webp',
    '/static/img/kurica_s_sirom_v_duhovke.webp',
    '/static/img/pechenie_mordashki.webp',
    '/static/img/pie.webp',
    '/static/img/favicon.ico',
    '/static/webfonts/fa-solid-900.woff2'
];

self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function (cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function (event) {
    if (!navigator.onLine) {
        event.respondWith(
            caches.match(event.request)
                .then(function (response) {
                        if (response) {
                            return response;
                        }
                        return fetch(event.request);
                    }
                )
        );
    }
});