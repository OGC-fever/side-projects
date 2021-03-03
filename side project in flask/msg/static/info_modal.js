$(document).ready(function () {
    var modal = document.getElementById('replyModal')
    modal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget
        var name = button.getAttribute('name')
        var title = modal.querySelector('.modal-title')
        var msg = modal.querySelector('.modal-body textarea')
        if (name) {
            title.textContent = 'Reply to : ' + name
            msg.value = "@" + name + "\n"
        }
    })
})