$(document).ready(function () {
    $('.popup').click(function () {
        var id = $(this).attr('id');
        if ($(this).find('img').attr("src")) {
            var check_img = true
        }
        $.ajax({
            url: "/card_info",
            type: "POST",
            dataType: "json",
            data: { "id": id },
            success: function (data) {
                if (check_img) {
                    $('#image_modal').attr('src', "/image/" + id);
                } else {
                    $('#image_modal').attr('src', " ");
                }
                $('#msg_modal').html(data["msg"].split("\n").join("<br>"));
                $('#author_modal').html(data["name"]);
            },
            error: function (error) {
                alert("OOPS!");
            }
        })

        $('#cardModal').modal('show');
    })

    // $('#image_modal').click(function () {
    //     $("#cardModal").modal("hide");
    // })

    // $('.form-button').click(function () {
    //     $("#formModal").modal("hide");
    // })
});
