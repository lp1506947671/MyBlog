from django.urls import path, re_path

from blog import views

app_name = "blog_app"
urlpatterns = [
    # 验证码
    path("get_validate_code/", views.get_valid_code),
    # 个人站点
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)/$', views.home_site),
    re_path(r"^(?P<username>\w+)/$", views.home_site),
]
