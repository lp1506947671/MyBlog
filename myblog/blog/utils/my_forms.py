#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from blog.models import UserInfo


class UserForm(forms.Form):
    """
    max_length,label,widget ,error_messages
    user,pwd,re_pwd,email
    """
    user = forms.CharField(max_length=32, label="用户名", error_messages={'required': "该字段不能为空"},
                           widget=widgets.TextInput(attrs={"class": "form-control"}))
    pwd = forms.CharField(max_length=32, label="密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    re_pwd = forms.CharField(max_length=32, label="确认密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=32, label="邮箱", widget=widgets.EmailInput(attrs={"class": "form-control"}))

    def clean_user(self):
        """
        获取表单中传过来的user
            用户不存在直接换回
            用户存在则直接抛出异常用户已经被注册
        """
        val = self.cleaned_data.get("user")
        user = UserInfo.objects.filter(username=val).first()
        if not user:
            return val
        else:
            raise ValidationError("该用户已经注册")

    def clean(self):
        """
        校验两次输入的密码是否一致
        判断两次输入的密码是否都存在
        都存在:
            相等:返回self.clean_data
            不相等:抛出validationError的错误
        不都存在:
            返回通过校验的数据
        """
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("密码不一致")
        else:
            return self.cleaned_data
