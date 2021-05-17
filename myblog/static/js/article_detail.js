let article_id = $(".article_info")[0].getAttribute("id");
// 定义父类id
let pid = '';

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
    $.ajax({
        url: "/blog/get_comment_tree/",
        type: "get",
        data: {article_id: article_id},
        success: function (data) {
            console.log(data);
            // 遍历文章数据
            $.each(data, function (index, comment_objects) {
                // 获取评论对象的id
                let pk = comment_objects.pk;
                // 获取评论的内容
                let content = comment_objects.content;
                // 获取评论的父对象
                let parent_comment_id = comment_objects.parent_comment_id;
                // 拼接成评论的内容
                let s = '<div class="comment_item" comment_id=' + pk + '><span>' + content + '</span></div>';
                //判断是否有父评论
                if (!parent_comment_id) {
                    // 没有则直接将comment加到评论树的后面
                    $(".comment_tree").append(s);
                } else {
                    //有的话追加到到相应评论的后面
                    $("[comment_id=" + parent_comment_id + "]").append(s);
                }
            })
        }
    })
}

//评论请求
function sendComment() {
    // 绑定点击按钮
    $(".comment_btn").click(function () {
        console.log("begin send");
        // 获取用户输入的内容
        let content = $("#comment_content").val();
        // 如果父类id存在
        if (pid) {
            // 1.获取@用户名\n后面的\n索引,并切取后面的内容
            let index = content.indexOf("\n");
            content = content.slice(index + 1);
        }
        // 2.发起ajax请求
        $.ajax({
            url: "/blog/comment/",
            type: "post",
            data: {
                //  csrftoken值
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
                // article_id值
                "article_id": $(".article_info")[0].getAttribute("id"),
                // content
                "content": content,
                //  父评论id
                "pid": pid
            },
            success: function (data) {
                // 获取创建时间,用户名,内容
                let create_time = data.create_time;
                let username = data.username;
                let content = data.content;
                let comment_id = data.comment_id;
                // 创建评论内容html
                let s = `<li class="list-group-item">
                            <div>
                            <span>${create_time}</span>&nbsp;&nbsp;
                            <a href=""><span>${username}</span></a>
                            <a class="pull-right reply_btn" username="${username}"
                               comment_pk="${comment_id}">回复</a>
                            </div>   
                            <div class="comment_con"><p>${content}</p></div>
                            
                        </li>`;
                // 最后清空评论框里输入的内容
                $("ul.comment_list").append(s);
                // 最后清空评论框里输入的内容
                $("#comment_content").val('');

            }

        })
    })

}

//回复按钮
function answerBtn() {
// 回复按钮绑定点击事件
    $(".comment_list").on("click", ".reply_btn", function () {
        alert("段落被点击了。");
        // 当点击评论按钮的时候,聚焦到评论框
        $("#comment_content").focus();
        // 评论框自动输入@被评论用户名
        let val = "@" + $(this).attr("username") + "\n";
        $("#comment_content").val(val);
        // 并且获取被评论用户的id
        pid = $(this).attr("comment_pk")
    });
}


//主函数
getCommentTree();
sendComment();
answerBtn();
likeArticles();