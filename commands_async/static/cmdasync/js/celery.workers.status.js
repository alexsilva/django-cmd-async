var workers_check_status = function() {
    var csrftoken = cmdasyncform.getCookie("csrftoken");
    var $toast = $('#popup-msg');
    $.ajax({
        type: "GET",
        dataType: 'json',
        url: "workers/status/",
        beforeSend: function(xhr, settings) {
            if (!cmdasyncform.csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }).done(function(data) {
        var $body = $toast.find(".toast-body").empty();
        if (data.status) {
            $toast.find('.online').html(data.workers.length);
            $.each(data.workers, function (i, name) {
                $body.append('<p class="text-muted">' + name + '</p>')
            })
        } else {
            $body.html('<p class="text-muted">' + data.message + '</p>');
            setTimeout(workers_check_status, 5000);
        }
        $toast.toast("show");
    }).fail(function(){
        setTimeout(workers_check_status, 5000);
    })
};