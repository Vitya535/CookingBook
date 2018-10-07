$(document).ready(function()
{
    var green_td;
    $('#apply').click(function()
    {
        var textarea_value = $('textarea.update').val();
        $(green_td).text(textarea_value);
    });

    $('#delete').click(function()
    {
        alert($('row_for_items:first-child').text())
    });

    $('table.content').click(function(e)
    {
        var rows = $(this).find('td');
        $.each(rows, function(index, value)
        {
            rows.eq(index).css("background","");
        });
        if (e.target.className == 'item')
        {
            $(e.target).css("background","green");
            green_td = e.target;
            $('textarea.update').text($(e.target).html());
        }
        else if (e.target.tagName == 'TH')
        {
            $('textarea.update').empty();
            // можно отсортировать еще по тому атрибуту, который подсвечен
        }
    });

    $('#what_show').change(function()
    {
        var selected = $('#what_show option:selected').text();
        $.ajax
        ({
            type: "GET",
            url: "/" + selected,
            success: function()
            {
                window.location.href = "/" + selected;
            }
        })
    });
});