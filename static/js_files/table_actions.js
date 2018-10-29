$(document).ready(function()
{
    var green_td;
    $('table.content').tablesorter({widgets: ['zebra']});

    $('#what_show').change(function()
    {
        var selected = $('#what_show option:selected').text();
        $.ajax
        ({
            url: '/' + selected,
            method: 'POST'
        })
        .done(function(attributes)
        {
            var trs = $('thead tr');
            $(trs).empty();
            $(attributes[0]).each(function()
            {
                $(trs[0]).append('<th>' + this[1]);
                $(trs[1]).append('<td><input placeholder="фильтр">');
            });
            $('tbody').empty();
            for (var i = 0; i < attributes[1].length; i++)
            {
                $('tbody').append('<tr class="data">');
                $(attributes[1][i]).each(function()
                {
                    $('tr:last').append('<td class="item">' + this);
                });
            }
            $('table.content').tablesorter({widgets: ['zebra']});
        });
    });

    $('#apply').click(function()
    {
        if ($(green_td).text() == $('textarea.update').val())
            return;
        else
        {
            var textarea_value = $('textarea.update').val();
            var green_td_index = $(green_td).index();
            var attr_title = $($('thead th')[green_td_index]).text();
            var tr_for_update = $(green_td).parent().find('td')[0];
            var arg_id = $(tr_for_update).text();
            $.ajax
            ({
                url: '/update_from_db',
                method: "POST",
                contentType: 'application/json;charset=UTF-8',
                data : JSON.stringify({'value' : textarea_value, 'update_id' : arg_id, 'attr_title' : attr_title}),
                success: function()
                {
                    $(green_td).text(textarea_value);
                    $('table.content').trigger('update');
                    $('#apply').prop('disabled', true);
                },
                error: function(request, status, message)
                {
                    alert(request.responseJSON.message);
                }
            });
        }
    });

    $('#delete').click(function()
    {
        if (!green_td)
            alert('Сначала выберите запись!');
        else
        {
            var tr_for_update = $(green_td).parent().find('td')[0];
            var arg_id = $(tr_for_update).text();
            $.ajax
            ({
                url: '/del_from_db',
                method: "POST",
                contentType: 'application/json;charset=UTF-8',
                data : JSON.stringify({'delete_id': arg_id}),
                success : function()
                {
                    $(green_td).parent().detach();
                    $('table.content').trigger('update');
                },
                error : function(request, status, message)
                {
                    alert(request.responseJSON.message);
                }
            });
        }
    });

    $('#add').click(function()
    {
        $.ajax
        ({
            url: '/add_to_db',
            method: "POST",
            success : function()
            {
                $('tbody').append('<tr>');
                var tr = $('tbody tr:last');
                var last_id = $(tr).index() + 1;
                var attr_count = $('thead th').length;
                for (var i = 0; i < attr_count; i++)
                    $(tr).append('<td class="item">');
                $(tr).children('td:first').append(last_id);
                $('table.content').trigger('update');
            },
            error : function(request, status, message)
            {
                alert(request.responseJSON.message);
            }
        });
    });

    $('table.content').click(function(e)
    {
        $(green_td).css("background", "");
        if (e.target.className == 'item')
        {
            $(e.target).css("background","green");
            green_td = e.target;
            $('textarea.update').text($(e.target).html());
        }
        else if (e.target.tagName == 'TH')
            $('textarea.update').empty();
    });

    function filterTable(table)
    {
        var filters = $(table).find('.filters td');
        var rows = $(table).find('.data');
        $(rows).each(function(rowIndex)
        {
            var valid = true;
            $(this).find('td').each(function(colIndex)
            {
                if ($(filters).eq(colIndex).find('input').val())
                    if ($(this).html().toLowerCase().indexOf($(filters).eq(colIndex).find('input').val().toLowerCase()) == -1)
                        valid = valid && false;
            });
            if (valid === true)
                $(this).css('display', '');
            else
                $(this).css('display', 'none');
        });
    }

    $(this).on('input', '.filters input', function()
    {
        filterTable($(this).parents('table.content'));
        $('table.content').trigger('update');
    });

    $(this).on('input', 'textarea.update', function()
    {
        $('#apply').prop('disabled', false);
    });

    $('table.content').dblclick(function(e)
    {
        $('textarea.update').prop('readonly', false);
        if (e.target.className == 'item')
            $('textarea.update').focus();
    });
});