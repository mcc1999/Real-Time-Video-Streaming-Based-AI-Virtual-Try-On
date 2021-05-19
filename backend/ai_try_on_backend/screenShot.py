import base64
import http.client
import json


def http_authenticate():
    # 客户ID、密钥
    customer_key = "*******"
    customer_secret = "*******"
    credentials = customer_key + ":" + customer_secret
    # 使用 base64 进行编码
    base64_credentials = base64.b64encode(credentials.encode("utf8"))
    credential = base64_credentials.decode("utf8")

    # 通过基本 URL 创建连接对象
    conn = http.client.HTTPSConnection("api.agora.io")

    # 创建 Header 对象
    headers = {'Authorization': 'basic ' + credential, 'Content-Type': 'application/json'}

    # 发送请求
    payload = ""
    conn.request("GET", "/dev/v1/projects", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    print("Test:")
    print(data)
    return data["success"]


# step1 acquire
def acquire(appID: str, channel: str) -> str:
    # 客户ID、密钥
    customer_key = "******"
    customer_secret = "******"
    credentials = customer_key + ":" + customer_secret
    # 使用 base64 进行编码
    base64_credentials = base64.b64encode(credentials.encode("utf8"))
    credential = base64_credentials.decode("utf8")

    # 通过基本 URL 创建连接对象
    conn = http.client.HTTPSConnection("api.agora.io")

    # 创建 Header 对象
    headers = {'Authorization': 'basic ' + credential, 'Content-Type': 'application/json'}

    # Agora APP参数
    uid = "9"
    url = "/v1/apps/" + appID + "/cloud_recording/"

    acquire_url = url + "acquire"
    acquire_body = json.dumps({
        'cname': channel,
        'uid': uid,
        'clientRequest': {
            "resourceExpiredHour": 24,
            "scene": 0
        }
    })
    conn.request("POST", acquire_url, acquire_body, headers)
    acquire_res = conn.getresponse()
    acquire_data = acquire_res.read().decode("utf-8")
    print("Acquire:")
    print(acquire_data)
    if acquire_res.status == 200:
        return json.loads(acquire_data)["resourceId"]
    else:
        return "Acquire Error" + acquire_res.status


# step2 start
def start(appID: str, channel: str, resourceid: str, token: str) -> str:
    # 客户ID、密钥
    customer_key = "******"
    customer_secret = "********"
    credentials = customer_key + ":" + customer_secret
    # 使用 base64 进行编码
    base64_credentials = base64.b64encode(credentials.encode("utf8"))
    credential = base64_credentials.decode("utf8")

    # 通过基本 URL 创建连接对象
    conn = http.client.HTTPSConnection("api.agora.io")

    # 创建 Header 对象
    headers = {'Authorization': 'basic ' + credential, 'Content-Type': 'application/json'}

    # Agora APP参数
    uid = "9"
    url = "/v1/apps/" + appID + "/cloud_recording/"

    start_url = url + "resourceid/" + resourceid + "/mode/individual/start"
    start_body = json.dumps({
        "cname": channel,
        "uid": uid,
        "clientRequest": {
            "token": token,
            "recordingConfig": {
                "channelType": 1,
                "subscribeUidGroup": 0
            },
            "snapshotConfig": {
                "captureInterval": 10,
                "fileType": ["jpg"]
            },
            "storageConfig": {
                "vendor": 2,
                "region": 1,
                "bucket": "ai-try-on",
                "accessKey": "*******",
                "secretKey": "******",
            }
        }
    })
    conn.request("POST", start_url ,start_body, headers)
    start_res = conn.getresponse()
    start_data = start_res.read().decode("utf-8")
    print("Start:")
    print(start_res.status)
    print(start_data)
    if start_res.status == 200:
        return json.loads(start_data)["sid"]
    else:
        return "Error" + start_res.status


def stop(appID: str, channel: str, resourceid: str, sid: str):
    # 客户ID、密钥
    customer_key = "*******"
    customer_secret = "******"
    credentials = customer_key + ":" + customer_secret
    # 使用 base64 进行编码
    base64_credentials = base64.b64encode(credentials.encode("utf8"))
    credential = base64_credentials.decode("utf8")

    # 通过基本 URL 创建连接对象
    conn = http.client.HTTPSConnection("api.agora.io")

    # 创建 Header 对象
    headers = {'Authorization': 'basic ' + credential, 'Content-Type': 'application/json'}

    # Agora APP参数
    uid = "9"
    url = "/v1/apps/" + appID + "/cloud_recording/"

    stop_url = url + "resourceid/" + resourceid + "/sid/"+ sid + "/mode/individual/stop"
    stop_body = json.dumps({
        'cname': channel,
        'uid': uid,
        'clientRequest': {
        }
    })
    conn.request("POST", stop_url, stop_body, headers)
    stop_res = conn.getresponse()
    stop_data = stop_res.read().decode("utf-8")
    print("Stop:")
    print(stop_res.status)
    print(stop_data)
    if stop_res.status == 200:
        return True
    else:
        return False