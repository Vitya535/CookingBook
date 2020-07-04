$(document).ready(function () {
    const csrf_token = "{{ csrf_token() }}";
    const buttons_for_delete = $('.fa-trash').parent();
    const buttons_for_update = $('.fa-pencil').parent();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("#back-top")
        .hide()
        .on('click', function () {
            $('body, html').animate({
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

    $(buttons_for_update).on('click', function () {
        $.confirm({
            title: 'Редактирование блюда',
            content: 'Вы действительно хотите отредактировать данные об этом блюде?',
            buttons: {
                Yes: function () {
                    $.alert('Confirmed!');
                },
                No: function () {
                    $.alert('Canceled!');
                }
            }
        });
    });
});