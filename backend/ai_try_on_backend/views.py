import os

from django.http import HttpResponse, JsonResponse
from django.views import View
from .utils import session_check
from .token import tokenForRtc, Role_Publisher, Role_Attendee
import time
from .screenShot import http_authenticate, acquire, start, stop
import json
import datetime
from users.models import User
import requests
import oss2
from aip import AipBodyAnalysis
from PIL import Image
import io
from backend.settings import BASE_DIR
from imageMask .u2net_test import U2Net
from imageParse .exp .inference .inference import Graphonomy
from imagePose .keypoints_from_images import openPose
from virtualTryOn .test import virtualTryOn
import cv2


class ClothShot(View):
    def post(self, request):
        response = HttpResponse()
        return_model = {"msg_code": 100, "message": None, "cloth_object_name": ''}
        try:
            sessionId = request.COOKIES['sessionid']
            meeting = request.POST.get("meeting")
            meeting = json.loads(meeting)
            session_data = request.session.load()
            sessionCheck = session_check(request, sessionId)
            if sessionCheck == "login":
                appID = meeting["appID"]
                certification = meeting["certification"]
                channel = meeting["channel"]
                uid = 9  # Record Account uid is 9
                role = Role_Attendee
                privilegeExpiredTs = 24*60*60+int(time.time())
                token = tokenForRtc(appID, certification, channel, uid, role, privilegeExpiredTs)
                if http_authenticate():
                    resourceid = acquire(appID, channel)
                    if "Error" not in resourceid:
                        sid = start(appID, channel, resourceid, token)
                        clothObjectTime = str(datetime.datetime.utcnow()).replace("-", "").replace(" ", "").replace(".", "").replace(":", "")
                        clothObjectTime = clothObjectTime[:16]
                        if "Error" not in sid:
                            time.sleep(2)
                            stop_result = stop(appID, channel, resourceid, sid)
                            if stop_result:
                                host = User.objects.filter(room_num=channel)
                                host_uid = ''
                                if len(host):
                                    host_uid = str(host[0].id)
                                else:
                                    raise RuntimeError("Error, Meeting Host Not Found!")
                                clothImgName = sid + "_" + channel + "__uid_s_" + host_uid + "__uid_e_video_" + clothObjectTime
                                print(clothImgName)
                                return_model["msg_code"] = 100
                                return_model["message"] = "截图成功!"
                                return_model["cloth_object_name"] = clothImgName
                            else:
                                return_model["msg_code"] = 1001
                                return_model["message"] = "截图失败，请联系管理员!"
                        else:
                            return_model["msg_code"] = 1001
                            return_model["message"] = sid
                    else:
                        return_model["msg_code"] = 1001
                        return_model["message"] = resourceid

                else:
                    return_model["msg_code"] = 1001
                    return_model["message"] = "HTTP基本认证未通过，截图失败！"
            elif sessionCheck == "expired":
                return_model["msg_code"] = 1001
                return_model["message"] = "sessionid失效，登录过期请重新登录！"
            elif sessionCheck == "notExist":
                return_model["msg_code"] = 1001
                return_model["message"] = "请先登录后再操作！"
        except Exception as e:
            return_model["msg_code"] = 1001
            return_model["message"] = "截图失败," + str(e)

        response.content = json.dumps(return_model, ensure_ascii=False)
        return response


class GetCutCloth(View):
    # def post(self, request):
    #     response = HttpResponse()
    #     return_model = {"msg_code": 100, "message": None}
    #
    #     cloth_object_key = request.POST.get("clothObjectKey")
    #     print(type(cloth_object_key))
    #     cloth_object_key = json.loads(cloth_object_key)
    #     print(type(cloth_object_key))
    #
    #     # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    #     auth = oss2.Auth('*******', '******')
    #     # Endpoint以杭州为例，其它Region请按实际情况填写。
    #     bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'ai-try-on')
    #
    #     # bucket.get_object的返回值是一个类文件对象（File-Like Object），同时也是一个可迭代对象（Iterable）。
    #     object_stream = bucket.get_object(cloth_object_key)
    #     image = object_stream.read()
    #     print(image)
    #
    #     # 由于get_object接口返回的是一个stream流，需要执行read()后才能计算出返回Object数据的CRC checksum，因此需要在调用该接口后做CRC校验。
    #     if object_stream.client_crc != object_stream.server_crc:
    #         print("The CRC checksum between client and server is inconsistent!")
    #
    #     APP_ID = '*******'
    #     API_KEY = '*******'
    #     SECRET_KEY = '******'
    #
    #     client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
    #
    #     """ 调用人体检测与属性识别 """
    #     bodyInfo = client.bodyAttr(image)
    #     print("1")
    #     person_num, position = 0, {}
    #     if bodyInfo:
    #         for key, value in bodyInfo.items():
    #             if key == 'person_num':
    #                 person_num = value
    #             if key == 'person_info':
    #                 obj = value[-1]
    #                 for k, v in obj.items():
    #                     if k == 'location':
    #                         for kk, vv in v.items():
    #                             position[kk] = vv
    #
    #     left, upper, right, lower, width, height = 0, 0, 0, 0, 0, 0
    #     for key, value in position.items():
    #         if key == 'top':
    #             upper = value
    #         if key == 'left':
    #             left = value
    #         if key == 'width':
    #             width = value
    #         if key == 'height':
    #             height = value
    #
    #     right = left + width
    #     lower = upper + height
    #
    #     img = Image.open(io.BytesIO(image))
    #     print(type(img))
    #
    #     print(img.size)
    #     cutCloth = io.BytesIO()
    #     cropped = img.crop((left, upper, right, lower))
    #     print(type(cropped))
    #     cropped.save(cutCloth, "JPEG")
    #     print(type(str(BASE_DIR)))
    #     cropped.save(os.path.join(str(BASE_DIR)+'/static/images/cloth/', cloth_object_key[-21:]).replace('/', '\\'))
    #     cutClothBytes = cutCloth.getvalue()
    #
    #     response.content = cutClothBytes
    #     return response
    def post(self, request):
        response = HttpResponse()
        print(BASE_DIR)
        dir_path = os.path.join(BASE_DIR, "static\\images\\cloth\\cloth.png")
        with open(dir_path, 'rb') as f:
            im = f.read()
        img = Image.open(io.BytesIO(im))
        print(type(img))

        print(img.size)
        cutCloth = io.BytesIO()
        img.save(cutCloth, "JPEG")
        cutClothBytes = cutCloth.getvalue()

        response.content = cutClothBytes
        return response


class GetCloth(View):
    def post(self, request):
        response = HttpResponse()
        cloth_object_key = request.POST.get("clothObjectKey")
        cloth_object_key = json.loads(cloth_object_key)
        print(type(cloth_object_key))

        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        auth = oss2.Auth('*******', '*******')
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'ai-try-on')

        # bucket.get_object的返回值是一个类文件对象（File-Like Object），同时也是一个可迭代对象（Iterable）。
        object_stream = bucket.get_object(cloth_object_key)
        cloth_bytes = object_stream.read()
        print(type(cloth_bytes))

        # 由于get_object接口返回的是一个stream流，需要执行read()后才能计算出返回Object数据的CRC checksum，因此需要在调用该接口后做CRC校验。
        if object_stream.client_crc != object_stream.server_crc:
            print("The CRC checksum between client and server is inconsistent!")

        response.content = cloth_bytes
        return response


class GetTryOnCloth(View):
    def post(self, request):
        response = HttpResponse()
        humanImageKey = request.POST.get("humanImageName")
        clothObjectKey = request.POST.get("clothObjectKey")
        humanImageKey = json.loads(humanImageKey)
        clothObjectKey = json.loads(clothObjectKey)

        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        auth = oss2.Auth('******', '*******')
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'ai-try-on')

        # bucket.get_object的返回值是一个类文件对象（File-Like Object），同时也是一个可迭代对象（Iterable）。
        object_stream = bucket.get_object(humanImageKey)
        image = object_stream.read()
        print(type(image))


        imgStream = io.BytesIO(image)
        imgPIL = Image.open(imgStream)
        imgPIL.save(os.path.join(str(BASE_DIR)+'/static/images/image/', humanImageKey).replace('/', '\\'))

        # 由于get_object接口返回的是一个stream流，需要执行read()后才能计算出返回Object数据的CRC checksum，因此需要在调用该接口后做CRC校验。
        if object_stream.client_crc != object_stream.server_crc:
            print("The CRC checksum between client and server is inconsistent!")

        images_dir = os.path.join(str(BASE_DIR) + '/static/', 'images').replace('/', '\\')

        # reshape && get cloth mask
        cloth_dir = os.path.join(images_dir, 'cloth', clothObjectKey[-21:])
        print(cloth_dir)
        clothImage = cv2.imread(cloth_dir)
        print(clothImage.shape)
        b, g, r = cv2.split(clothImage)
        clothImage = cv2.merge([r, g, b])
        clothImage = cv2.resize(clothImage, (192, 256), interpolation=cv2.INTER_AREA)
        print(clothImage.shape)
        img2 = Image.fromarray(clothImage)
        img2.save(cloth_dir)

        U2Net(os.path.join(str(BASE_DIR)+'/static/images/', 'cloth').replace('/', '\\'))

        # reshape && get human image mask
        humanImage_dir = os.path.join(images_dir, 'image', humanImageKey)
        print(humanImage_dir)
        humanImage = cv2.imread(humanImage_dir)
        print(humanImage.shape)
        b, g, r = cv2.split(humanImage)
        humanImage = cv2.merge([r, g, b])
        humanImage = cv2.resize(humanImage, (192, 256), interpolation=cv2.INTER_AREA)
        print(humanImage.shape)
        img2 = Image.fromarray(humanImage)
        img2.save(humanImage_dir)

        # get humanKeyPoints
        openPose(humanImageKey)

        U2Net(os.path.join(str(BASE_DIR)+'/static/images/', 'image').replace('/', '\\'))

        # get parse images
        Graphonomy(humanImageKey)

        # get GMM image
        # prepare .txt
        txt_dir = os.path.join(str(BASE_DIR), "static\\images\\test_pairs.txt")
        print(txt_dir)
        print(humanImageKey + ' ' + clothObjectKey)
        with open(txt_dir, 'w') as f:
            f.write(humanImageKey + ' ' + clothObjectKey[-21:])
        virtualTryOn('GMM', 'GMM')

        # get TOM image
        virtualTryOn("TOM", 'TOM')

        tryOnImage = Image.open(cloth_dir)
        tryOnImageStream = io.BytesIO()
        tryOnImage.save(tryOnImageStream, "JPEG")
        tryOnImageBytes = tryOnImageStream.getvalue()
        response.content = tryOnImageBytes

        return response


class GetAICloth(View):
    def get(self, request):
        response = HttpResponse()
        print(BASE_DIR)
        dir_path = os.path.join(BASE_DIR, "static\\images\\result_dir\\model.jpg")
        with open(dir_path, 'rb') as f:
            im = f.read()
        img = Image.open(io.BytesIO(im))
        print(type(img))

        print(img.size)
        Cloth = io.BytesIO()
        img.save(Cloth, "JPEG")
        clothBytes = Cloth.getvalue()

        time.sleep(10)
        response.content = clothBytes
        return response