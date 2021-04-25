from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

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
    my_form = UserForm()
    return render(request, "register.html", {"forms": my_form})


def get_valid_code(request):
    img_data = gen_valid_code(request)

    return HttpResponse(img_data)
