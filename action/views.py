# from django.shortcuts import render
from django.middleware.csrf import get_token
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User

from utils.response import rest_resp

# Create your views here.
def get_csrf_token(request):
    get_token(request)
    return rest_resp()

def user_login(request):
    if request.method != 'POST':
        return rest_resp(405, "Method Not Allowed")
    
    name = request.POST.get('name', '')
    passwd = request.POST.get('passwd', '')

    if not name or not passwd:
        return rest_resp(400, "用户名及密码不能为空！")

    if User.objects.filter(username=name).exists():
        user = authenticate(username=name, password=passwd)
        if user is not None:
            login(request, user)
            return rest_resp(200, "登陆成功！")
        else:
            return rest_resp(406, "用户名或密码错误！")
    else:
        return rest_resp(404, "该用户不存在！")


def user_logout(request):
    if request.method != 'POST':
        return rest_resp(405, "Method Not Allowed")
    logout(request)
    return rest_resp(200, "登出成功！")
    