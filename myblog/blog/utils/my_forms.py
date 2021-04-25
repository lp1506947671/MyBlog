#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets


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
