后台
  1.url:/blog/comment/
  2.method:post
      获取当前文章id:article_id
      获取当前的评论:content
      获取当前的评论的父类id: pid
      获取当前登录用户

      获取文章对象
      创建事务:
              创建评论:user_id,article_id,parent_comment_id
              文章的评论数加1
      创建response: create_time,username,content
      创建线程:threading,send_mail,参数(标题,评论内容,邮件主机,[邮箱])
      JasonResponse

  3.获取评论树
             获取文章的id
             根据文章id,按照主健排序,获取"pk","content","parent_comment_id"
前台:
    1.html
      {# 评论树 #}
      div class comments list-group
          p:tree_btn
          div:comment_tree
      {# 评论列表 #}
      ul class list-group comment-list
          li :list-group-item
              div:
                  a 楼层
                  span 日期
                  a span 用户名
                  a  回复按钮 class:pull-right reply_btn  username:
              div:是否有父评论:pid_info well
                  p:父评论的用户名:父评论的内容
              div:comment_con
                  p:评论内容

    2.Js
      //评论请求
                定义父类id
                绑定点击按钮
                          获取用户输入的内容
                          如果父类id存在
                              1.获取@用户名\n后面的\n索引,并切取后面的内容
                              2.发起ajax请求
                                  csrftoken值
                                  article_id值
                                  content
                                  父评论id
                          成功: 获取创建时间,用户名,内容
                                创建评论内容html
                                li
                                  div span a
                                  div p
                                将创建的html内容插入到评论数列表后面
                                最后清空评论框里输入的内容

     //评论树(当前用户的评论树)
        url:blog/get_comment_tree
        data:文章id
        成功:获取到文章数据
             遍历文章数据
             获取评论对象的id
             获取评论的内容
             获取评论的父对象
             拼接成评论的内容
             判断是否有父评论
                没有则直接将comment加到评论树的后面
                有的话追加到到相应评论的后面

      //回复按钮
                回复按钮绑定点击事件
                当点击评论按钮的时候,聚焦到评论框
                评论框自动输入@被评论用户名
                并且获取被评论用户的id

      //评论树