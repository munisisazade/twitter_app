// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function () {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#post_add_form").submit(function (e) {
        e.preventDefault();
        var data = new FormData();
        data.append("context", $(".post-content").val());
        data.append("picture", $(".post-image")[0].files[0]);
        $.ajax({
            url: $(this).data("action"),
            method: "POST",
            processData: false,
            contentType: false,
            data: data,
            success: function (data) {
                $("input, textarea").val("");
                $(".all_posts").html(data);
            },
        });
        return false;
    });

    $(document).on("click", ".like", function (e) {
        var data = new FormData();
        var count = $(this).find("ins");
        data.append("post_id", $(this).attr("data-post-id"));
        $.ajax({
            url: $(this).data("action"),
            method: "POST",
            processData: false,
            contentType: false,
            data: data,
            success: function (data) {
                count.text(data.like_count);
            },
        });
    });

    // follow user
    $(".follow").click(function (e) {
        e.preventDefault();
        console.log("yess");
        var form = new FormData();
        var url = $(this).attr("data-follow-url");
        var profile_id = $(this).attr("data-follow-id");
        var text = $(this);
        form.append("pk", profile_id);
        $.ajax({
            url: url,
            data: form,
            method: "POST",
            processData: false,
            contentType: false,
            success: function (data) {
                $(".total_count").html(data.follow_count);
                if (data.status) {
                    text.text("Followed");
                }
                else {
                    text.text("Follow");
                }
            }
        })
    });
});