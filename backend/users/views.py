from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.sessions import *
from django.core import serializers
from django.db import models
from .models import User, Meeting
import datetime
import pytz
import json
import time
from .utils import session_check
from .token import tokenForRtc, Role_Publisher, Role_Attendee


class Login(View):
    def post(self, request):
        response = HttpResponse(content_type='application/json; charset=utf-8')
        return_model = {"msg_code": 100, "message": None}
        try:
            username = request.POST.get("username")
            pwd = request.POST.get("password")
            # 验证数据库中的用户名密码
            obj = User.objects.filter(username=username)
            if len(obj):
                if obj[0].password == pwd:
                    return_model["message"] = "登录成功！"
                    # 将用户信息存入session
                    if not request.session.session_key:
                        request.session.create()
                    request.session['user'] = model_to_dict(obj[0])
                    request.session.save()
                    # request.set_session_key = request.session.get_new_session_key
                    session_key = request.session.session_key
                    response.set_signed_cookie('sessionid', session_key, salt="ai_try_on_backend", httponly=True, max_age=1000)
                    request.session.set_expiry(0)
                    print('key')
                    print(session_key)
                else:
                    return_model["msg_code"] = 1001
                    return_model["message"] = "密码不正确"
            else:
                return_model["msg_code"] = 1001
                return_model["message"] = "用户不存在"
        except Exception as e:
            return_model["msg_code"] = 1001
            return_model["message"] = "登录失败！" + str(e)

        response["Access-Control-Allow-Origin"] = "http://localhost:8081"
        response["Access-Control-Allow-Credentials"] = True
        response.content = json.dumps(return_model, ensure_ascii=False)
        return response


class Register(View):
    def post(self, request):
        response = HttpResponse()
        return_model = {"msg_code": 100, "message": None}
        try:
            username = request.POST.get("username")
            pwd = request.POST.get("password")
            pwd_confirm = request.POST.get("passwordConf")
            obj = User.objects.filter(username=username)
            if obj:
                return_model["msg_code"] = 1001
                return_model["message"] = "该用户名已被占用！"
            else:
                if pwd == pwd_confirm:
                    user = User(username=username, password=pwd)
                    user.save()
                    return_model["message"] = "注册成功！"
                else:
                    return_model["msg_code"] = 1001
                    return_model["message"] = "两次密码不一致！"
        except Exception as e:
            return_model["msg_code"] = 1001
            return_model["message"] = "注册失败" + str(e)

        response.content = json.dumps(return_model, ensure_ascii=False)
        return response


class Logout(View):
    def get(self, request):
        response = HttpResponse(content_type='application/json; charset=utf-8')
        return_model = {"msg_code": 100, "message": None}
        try:
            sessionId = request.COOKIES['sessionid']
            if request.session.exists(sessionId):
                request.session.flush()
                return_model["message"] = "注销成功！"
            else:
                raise RuntimeError("注销失败！")
        except Exception as e:
            return_model["msg_code"] = 1001
            return_model["message"] = "注销失败！" + str(e)

        response.content = json.dumps(return_model, ensure_ascii=False)
        return response


class SignAnchor(View):
    def post(self, request):
        response = HttpResponse()
        return_model = {"msg_code": 100, "message": None}
        try:
            sessionId = request.COOKIES['sessionid']
            loginCheck = session_check(request, sessionId)
            if loginCheck == "login":
                session_data = request.session.load()
                username = session_data['user']['username']
                room_num = request.POST.get("roomNum")
                user_query_set = User.objects.filter(username=username)
                if len(user_query_set):
                    user = user_query_set[0]
                    if user.room_num:
                        return_model["msg_code"] = 1001
                        return_model["message"] = "你已注册成为主播，可直接开启直播！"
                    else:
                        room_query_set = User.objects.filter(room_num=room_num)
                        if len(room_query_set):
                            return_model["msg_code"] = 1001
                            return_model["message"] = "该房间号已被注册！"
                        else:
                            user.room_num = room_num
                            user.save()
                            return_model["message"] = "注册成功，可开启直播！"
                else:
                    return_model["msg_code"] = 1001
                    return_model["message"] = "注册主播失败！"
            elif loginCheck == "expired":
                raise RuntimeError("sessionid已过期！")
            elif loginCheck == "notExist":
                raise RuntimeError("sessionid不存在！")

        except Exception as e:
            return_model["msg_code"] = 1001
            print(e)
            return_model["message"] = "注册失败！" + str(e)

        response.content = json.dumps(return_model, ensure_ascii=False)
        return response


class StartLive(View):
    def post(self, request):
        response = HttpResponse()
        return_model = {"msg_code": 100, "message": None, "meeting": []}
        try:
            sessionId = request.COOKIES['sessionid']
            room_num = request.POST.get("roomNum")
            session_data = request.session.load()
            sessionCheck = session_check(request, sessionId)
            if sessionCheck == "login":
                meeting = Meeting(channel=room_num, host=session_data["user"]["username"])
                return_model['message'] = "直播开启成功！"

                json_meeting = model_to_dict(meeting)
                appID = json_meeting["appID"]
                certification = json_meeting["certification"]
                channel = json_meeting["channel"]
                uid = session_data["user"]["id"]
                role = Role_Publisher
                privilegeExpiredTs = 24*60*60+int(time.time())
                token = tokenForRtc(appID, certification, channel, uid, role, privilegeExpiredTs)
                json_meeting["token"] = token
                json_meeting["uid"] = uid
                return_model["meeting"] = json_meeting
                meeting.save()
            elif sessionCheck == "expired":
                return_model["msg_code"] = 1001
                return_model["message"] = "sessionid失效，登录过期请重新登录！"
            elif sessionCheck == "notExist":
                return_model["msg_code"] = 1001
                return_model["message"] = "请先登录后再操作！"
        except Exception as e:
            return_model["msg_code"] = 1001
            return_model["message"] = "开启直播失败," + str(e)

        response.content = json.dumps(return_model, ensure_ascii=False)
        return response


class StopLive(View):
    def get(self, request):
        response = HttpResponse()
        return_model = {"msg_code": 100, "message": None}
        try:
            sessionId = request.COOKIES['sessionid']
            session_data = request.session.load()
            sessionCheck = session_check(request, sessionId)
            if sessionCheck == "login":
                user = User.objects.get(username=session_data["user"]["username"])
                user.meeting_token = ""
                user.save()
                Meeting.objects.filter(host=user.username).delete()
            elif sessionCheck == "expired":
                return_model["msg_code"] = 1001
                return_model["message"] = "sessionid失效，登录过期请重新登录！"
            elif sessionCheck == "notExist":
                return_model["msg_code"] = 1001
                return_model["message"] = "请先登录后再操作！"
        except Exception as e:
            return_model["msg_code"] = 1001
            return_model["message"] = "关闭直播失败," + str(e)

        response.content = json.dumps(return_model, ensure_ascii=False)
        return response


class WatchLive(View):
    def post(self, request):
        response = HttpResponse()
        return_model = {"msg_code": 100, "message": None, "meeting": []}
        try:
            sessionId = request.COOKIES['sessionid']
            room_num = request.POST.get("roomNum")
            session_data = request.session.load()
            sessionCheck = session_check(request, sessionId)
            if sessionCheck == "login":
                host = User.objects.get(room_num=room_num)
                meeting = Meeting.objects.get(host=host.username)
                json_meeting = model_to_dict(meeting)
                appID = json_meeting["appID"]
                certification = json_meeting["certification"]
                channel = json_meeting["channel"]
                uid = session_data["user"]["id"]
                role = Role_Attendee
                privilegeExpiredTs = 24 * 60 * 60 + int(time.time())
                token = tokenForRtc(appID, certification, channel, uid, role, privilegeExpiredTs)
                json_meeting["token"] = token
                json_meeting["uid"] = uid
                return_model["meeting"] = json_meeting
            elif sessionCheck == "expired":
                return_model["msg_code"] = 1001
                return_model["message"] = "sessionid失效，登录过期请重新登录！"

            elif sessionCheck == "notExist":
                return_model["msg_code"] = 1001
                return_model["message"] = "请先登录后再操作！"
        except Exception as e:
            return_model["msg_code"] = 1001
            return_model["message"] = "开启直播失败," + str(e)

        response.content = json.dumps(return_model, ensure_ascii=False)
        return response


class GetUser(View):
    def get(self, request):
        try:
            sessionId = ''
            if request.COOKIES['sessionid']:
                sessionId = request.COOKIES['sessionid']
            session_data = {}
            sessionCheck = session_check(request, sessionId)
            if sessionCheck == "login":
                session_data = request.session.load()
            elif sessionCheck == "expired":
                raise RuntimeError("sessionid已过期！")
            elif sessionCheck == "notExist":
                raise RuntimeError("sessionid不存在！")
            return JsonResponse({"username": session_data['user']['username']}, json_dumps_params={"ensure_ascii": False})
        except Exception as e:
            return JsonResponse(str(e), json_dumps_params={"ensure_ascii": False}, safe=False)


