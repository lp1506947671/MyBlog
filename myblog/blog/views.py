from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from blog.models import UserInfo
from blog.utils.my_forms import UserForm
from blog.utils.validate_code import gen_valid_code


# Create your views here.


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


def get_valid_code(request):
    img_data = gen_valid_code(request)

    return HttpResponse(img_data)
