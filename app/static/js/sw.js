const CACHE_NAME = 'offline-cooking-book';
const urlsToCache = [
    '/',
    '/about',
    '/salads_and_appetizers',
    '/sandwiches',
    '/meat_dishes',
    '/fish_and_seafood',
    '/sauces_and_marinades',
    '/vegetable_dishes',
    '/milk_dishes',
    '/cereals_and_pasta',
    '/cakes_and_pastries',
    '/fruit_dishes',
    '/lean_dishes',
    '/sweet_food_and_drinks',
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

const postUrl = '/delete';

self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function (cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

// self.addEventListener('install', function (event) {
//     event.waitUntil(
//         caches.open(CACHE_NAME)
//             .then(function (cache) {
//                 response = new HttpResponse(JSON.stringify({'dish_name': 'Печенье Мордашки'}));
//                 return cache.put(postUrl, response);
//             })
//     );
// });

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        // if (event.request.url === postUrl) {
        //     return fetch(postUrl, new Response(JSON.stringify({'dish_name': 'Печенье Мордашки'})));
        // } else {
            return fetch(event.request);
        // }
      }
    )
  );
});