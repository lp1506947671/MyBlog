//刷新验证码
$("#validate_code_img").click(function () {
    $(this)[0].src += '?';
});
//发起登录请求
$("#login").click(function () {
    $.ajax({
        type: "post",
        url: "",
        data: {
            user: $("#user").val(),
            pwd: $("#pwd").val(),
            validate: $("#validate").val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        },
        success: function (data) {
            console.log(data);
            if (data.user) {
                if (location.search){
                   location.href=location.search.slice(6)
                }
                else{
                   console.log("跳转");
                   location.href="/index/"
                }

                    } else {
                $(".error").text(data.msg).css({
                    "color": "red", "margin-left": "10px"
                });
               setTimeout(function () {
                  $(".error").text()
               },1000)
            }
        }

    })
});
