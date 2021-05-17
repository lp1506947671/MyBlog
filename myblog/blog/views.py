import json
import threading

from django.contrib import auth
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Count, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from blog import models
from blog.models import UserInfo
from blog.utils.my_forms import UserForm
from blog.utils.validate_code import gen_valid_code


# Create your views here.
def index(request):
    article_list = models.Article.objects.all()
    return render(request, "index.html", {"article_list": article_list})


def login(request):
    if request.method == "POST":
        response = {"user": None, "msg": None}
        user = request.POST.get("user")

        pwd = request.POST.get("pwd")
        validate = request.POST.get("validate")
        if validate.upper() == request.session.get("valid_code_str").upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)
                response["user"] = user.username
            else:
                response["msg"] = "账号或密码错误"
        else:
            response["msg"] = "验证码错误"
        return JsonResponse(response)
    return render(request, "login.html")


def logout(request):
    # request.session.flush()
    auth.logout(request)
    return redirect("/login/")


def register(request):
    """
    1.判断是否是post的请求
    2.将form组件中提交的数据传递给UserForm,并新建{"user":None,"msg":None}
    3.判断校验是否通过
        通过:
            从校验通过的数据中获取user,pwd,email,avatar(从FILES中获取)
            将user存储到response
            如果avatar_obj存在,则将其存在关键字字典中
            通过UserInfo表创建用户
        不通过:
             日志输出通过校验的字段
             日志输出错误信息
             将错误信息存储到msg中
    """

    if request.method == "POST":
        print(request.POST)
        response = {"user": None, "msg": None}
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar = request.FILES.get("avatar")
            response["user"] = user
            extra_dict = {"avatar": avatar} if avatar else {}
            UserInfo.objects.create_user(username=user, password=pwd, email=email, **extra_dict)
        else:
            print(form.errors)
            print(form.cleaned_data)
            response["msg"] = form.errors
        return JsonResponse(response)

    my_form = UserForm()
    return render(request, "register.html", {"forms": my_form})


def home_site(request, username, **kwargs):
    """
        1.获取当前用户,及用户博客
        2.查询当前用户的所有文章列表
        3.判断kwargs是否有参数:category,tag,archive
    """
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, "not_found.html")
    blog = user.blog
    article_list = models.Article.objects.filter(user=user)
    result = {"username": username, "blog": blog, "article_list": article_list}
    if kwargs:
        condition = kwargs.get("condition")
        param = kwargs.get("param")
        if condition == 'category':
            article_list = article_list.filter(category__title=param)
        elif condition == 'tag':
            article_list = article_list.filter(tags__title=param)
        else:
            year, month = param.split("/")
            article_list = article_list.filter(create_time__year=year, create_time__month=month)
        result["article_list"] = article_list
    return render(request, "home_site.html", result)


def article_detail(request, username, article_id):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    article_obj = models.Article.objects.filter(pk=article_id).first()
    comment_list = models.Comment.objects.filter(article_id=article_id)
    result = {"username": user, "blog": blog, "article_obj": article_obj, "comment_list": comment_list}
    return render(request, "article_detail.html", result)


def get_valid_code(request):
    img_data = gen_valid_code(request)

    return HttpResponse(img_data)


def article_like(request):
    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))
    user_id = request.user.pk
    response = {"state": True}
    like = models.ArticlesUpDown.objects.filter(user_id=user_id, article_id=article_id).first()
    if like:
        response["state"] = False
        response['handle'] = like.is_up
        return JsonResponse(response)
    models.ArticlesUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
    article_obj = models.Article.objects.filter(nid=article_id)
    if is_up:
        article_obj.update(up_count=F("up_count") + 1)
    else:
        article_obj.update(down_count=F("down_count") + 1)

    return JsonResponse(response)


def comment(request):
    # 获取article_id,content,pid,user_id
    # 获取当前文章id: article_id
    article_id = request.POST.get("article_id")
    # 获取当前的评论: content
    pid = request.POST.get("pid")
    # 获取当前的评论的父类id: pid
    content = request.POST.get("content")
    # 获取当前登录用户
    user_id = request.user.pk
    # 获取文章对象
    article_obj = models.Article.objects.filter(nid=article_id).first()
    # 事务操作
    with transaction.atomic():
        # 创建评论:user_id,article_id,parent_comment_id
        comment_obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, parent_comment_id=pid,
                                                    content=content)
        # 文章的评论数加1
        models.Article.objects.filter(nid=article_id).update(comment_count=F("comment_count") + 1)
    # 创建response: create_time, username, content
    response = {"create_time": comment_obj.create_time.strftime("%Y-%m-%d %X"),
                "username": request.user.username,
                "content": content,
                "comment_id": comment_obj.pk
                }

    return JsonResponse(response)


def get_comment_tree(request):
    article_id = request.GET.get("article_id")
    response = list(models.Comment.objects.filter(article_id=article_id).order_by("pk").values("pk", "content",
                                                                                               "parent_comment_id"))
    return JsonResponse(response, safe=False)
