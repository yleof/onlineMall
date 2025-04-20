from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.users.models import User
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django_redis import get_redis_connection
from django.http import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.views import LoginRequiredJSONMixin

import re
import json

class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})

class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})
    
class RegisterView(View):
    """用户注册"""

    def post(self, request):
        # 1.接收参数：请求体中的JSON数据 request.body
        json_bytes = request.body  # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode()  # 将bytes类型的JSON数据，转成JSON字符串
        json_dict = json.loads(json_str)  # 将JSON字符串，转成python的标准字典

        # 2. extract data
        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        sms_code = json_dict.get('sms_code')
        allow = json_dict.get('allow')

        # 3. validate
        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code':400, 'errmsg':'缺少必传参数!'})
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        # 判断两次密码是否一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        # 判断是否勾选用户协议
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})
        
        # verify sms code
        redis_conn = get_redis_connection('code')
        redis_sms_code = redis_conn.get(mobile)
        if not redis_sms_code:
            return JsonResponse({'code':400, 'errmsg':'短信验证码失效'})
        if sms_code != redis_sms_code.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})
        
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册失败!'})    

        
        login(request, user)

        return JsonResponse({'code': 0, 'errmsg': '注册成功!'})


class LoginView(View):
    def post(self, request: HttpRequest):
        # 1. get params
        json_dict = json.loads(request.body.decode())
        username = json_dict.get('username')
        password = json_dict.get('password')
        remembered = json_dict.get('remembered')

        # 2. validate
        if not all([username, password]):
            return JsonResponse({'code':400, 'errmsg':'login params incomplete'})
        
        if re.match('^1[3-9]\d{9}$', username):
            # 手机号
            User.USERNAME_FIELD = 'mobile'
        else:
            # account 是用户名
            # 根据用户名从数据库获取 user 对象返回.
            User.USERNAME_FIELD = 'username'
        
        # 3. verify with DB
        # method 2
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code':400, 'errmsg':'Account or Password is incorrect'})
        
        # 4. session
        login(request, user)

        # 5. if remember
        if remembered != True:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)

        # 6. return response
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})

        # 7. set cookie
        response.set_cookie('username', username)

        return response


class LogoutView(View):

    def delete(self, request):

        # clear session
        logout(request)

        # logout, return response and redirect
        response = JsonResponse({'code':0,
                                 'errmsg':'ok'})
        
        # clear cookie
        response.delete_cookie('username')

        return response

## no hand appeared when I move cursor to quit


class CenterView(LoginRequiredJSONMixin, View):
    
    def get(self, request):
        """提供个人信息界面"""
        return JsonResponse({
            'code': 0, 
            'errmsg': '个人中心',
             "info_data":{
                    "username":"itcast",
                    "mobile": "18310820688",
                    "email": "",
                    "email_active": 'true'
                }
            })