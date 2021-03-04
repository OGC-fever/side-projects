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
                for (i = 0; i < data["id"].length; i++) {
                    $('#ajax-insert').append(`
                        <div class="col px-2 my-2">
                            <div class="card h-100 bg-secondary info">
                                <div class="cropped">
                                    <img src="/msg/timg/${id = data["id"][i]}" loading="lazy" class="card-img img-fluid">
                                </div>
                                <a href="info/${id = data["id"][i]}">
                                    <div class="card-img-overlay bg-dark px-2 py-2">
                                        <div class="text-light px-1 pt-1 text-start">
                                        ${data["msg"][i].replace("\n", "<br>")}
                                        </div>
                                        <div class="card-footer px-1 py-1 text-end">
                                            <small class="blockquote-footer text-muted">
                                            ${data["name"][i]}
                                            </small>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>`
                    );
                }
            },
            error: function () {
                alert("OOPS!");
            }
        })
    }
});
