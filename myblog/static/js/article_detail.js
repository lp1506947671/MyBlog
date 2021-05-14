//对文章进行点赞
function likeArticles() {
    $("#div_digg .action ").click(function () {
        console.log("触发点击事件");
        let is_up = $(this).hasClass("diggit");
        let operateCount = $(this).children("span");
        $.ajax({
            url: "/blog/toggle_like/",
            method: "post",
            data: {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                is_up: is_up,
                article_id: $(".article_info")[0].getAttribute("id")
            },
            success: function (data) {
                console.log(data);
                if (data.state) {
                    let count = parseInt(operateCount.text());
                    operateCount.text(count + 1)
                } else {
                    let tip = is_up ? "已经点赞过" : "已经吐槽过";
                    let myFloat = is_up ? "left" : "right";
                    $("#digg_tips").html(tip);
                    $("#digg_tips").css({float: myFloat});
                    setTimeout(function () {
                        $("#digg_tips").html('')
                    }, 1000)
                }
            }
        })

    })
}

//评论树
function getCommentTree() {

}

//评论请求
function sendComment() {

}

//回复按钮
function answerBtn() {

}


//主函数
getCommentTree();
sendComment();
answerBtn();
likeArticles();