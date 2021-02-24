$(document).ready(function () {
    var page = 1;
    $(window).scroll(function () {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            page += 1;
            load_data(page);
        }
    });

    function load_data(page) {
        $.ajax({
            url: "/msg/more",
            type: "POST",
            dataType: "json",
            data: { "page": page },
            success: function (data) {
                alert(data["id"]);
                alert(data["name"]);
                alert(data["msg"]);
            },
            error: function () {
                alert("OOPS!");
            }
        })
    }

});
