$(document).ready(function () {
    $('img').click(function (event) {
        var img_src = $(this).attr('image');
        var card_id = img_src.split("/")[2];
        var text_modal = $(this).closest('.card').find('#card_text_' + card_id).text();
        var author_modal = $(this).closest('.card').find('#card_author_' + card_id).text();

        $('#photo_modal').attr('src', img_src);
        $('#text_modal').text(text_modal);
        $('#author_modal').text(author_modal);
        $('#cardModal').modal('show');
    })

    var $container = $('#grid');
    $container.imagesLoaded(function () { $container.masonry(); })

    window.onclick = function (event) {
        if (event.target.id = "photo_modal") {
            $("#cardModal").modal("hide");
        }
    }
});

function formSubmit(token) {
    document.getElementById("validation").submit();
}
