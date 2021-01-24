$(document).ready(function () {
    $('img').click(function () {
        var src = $(this).attr('src');
        var id = src.split("/")[2];
        $.ajax({
            url: "/card_info",
            type: "POST",
            dataType: "json",
            data: { "id": id },
            success: function (data) {
                $('#image_modal').attr('src', "/image/" + id);
                $('#msg_modal').html(data["msg"].replace("\n","<br>"));
                $('#author_modal').html(data["name"]);
            },
            error: function () {
                alert("OOPS!");
            }
        })
        $('#cardModal').modal('show');
    })

    $('.modal-dialog').click(function () {
        $("#cardModal").modal("hide");
    })
});
