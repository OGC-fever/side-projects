$(document).ready(function () {
    $('img').click(function () {
        var src = $(this).attr('src');
        var id = src.split("/")[2];
        $('#photo_modal').attr('src', "/image/" + id);
        // $('#author_modal').text(test);
        // '{{ url_for(msg,id=' + id + ') }}');
        // $('#author_modal').text('{{ url_for(author,id=' + id + ') }}');
        // document.getElementById("author_modal").innerHTML =
        //     '{{ url_for(author,id=' + id + ') }}';

        // alert(id);
        $('#cardModal').modal('show');
    })

    $('.modal-dialog').click(function (event) {
        $("#cardModal").modal("hide");
    })

});

