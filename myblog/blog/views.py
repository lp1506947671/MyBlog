from django.http import HttpResponse
from django.shortcuts import render
from blog.utils.validate_code import gen_valid_code


# Create your views here.


def login(request):
    return render(request, "login.html")


def get_valid_code(request):
    img_data = gen_valid_code()

    return HttpResponse(img_data)
