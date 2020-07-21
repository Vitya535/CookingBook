$(document).ready(function () {
    const csrf_token = $('meta[name=csrf-token]').attr('content');
    const buttons_for_delete = $('.bi-trash').parent();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        }
    });

    $("#back-top")
        .hide()
        .on('click', function () {
            $('html').animate({
                scrollTop: 0
            }, 800);
            return false;
        });

    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 200) {
            $('#back-top').fadeIn();
        } else {
            $('#back-top').fadeOut();
        }
    });

    $(buttons_for_delete).on('click', function () {
        const self = this;
        $.confirm({
            title: 'Удаление блюда',
            content: 'Вы действительно хотите удалить это блюдо?',
            buttons: {
                Yes: function () {
                    const dish_name = $(self).siblings('p:first').text();
                    $.post('/delete', {'dish_name': dish_name})
                        .done(function () {
                            $(self).closest('.row').remove();
                        })
                        .fail(function (xhr, status, error) {
                            console.log(xhr.statusText);
                            console.log(status);
                            console.log(error);
                        });
                },
                No: function () {
                }
            }
        });
    });
});