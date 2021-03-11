var page = 1;

ajax_load(page);

function ajax_board(json) {
    $('#ajax_board').html("");
    for (value in json) {
        if (value != "count") {
            $('#ajax_board').append(`
            <tr>
                <td>${value}</td>
                <td>${json[value]["name"]}</td>
                <td>${json[value]["title"]}</td>
            </tr>`
            );
        }
    }
}

function ajax_pagination(json) {
    $('#ajax_pagination').html("");
    for (i = 0; i < json["count"] / 10; i++) {
        $('#ajax_pagination').append(`
        <li class="page-item">
            <a class="page-link" href="#" onclick="ajax_load(${i + 1});">${i + 1}</a>
        </li>`
        );
    }
}

function ajax_load(page) {
    $('#ajax_list').show();
    $.ajax({
        url: "/ptt/list/" + page,
        type: "GET",
        dataType: "json",
        data: { "page": page },
        success: function (json) {
            ajax_board(json)
            ajax_pagination(json)
        },
    })
}
