import requests

class ProcessHttp:

    def __init__(self):
        self.res = None

    def sendHttp(self,url,method,data,header=None):
        method = method.upper()
        if method == "GET":
            self.res = requests.get(url, params=data,headers=header)
        elif method == "POST":
            self.res = requests.post(url, params=data,headers=header)
        if self.res.status_code == 200:
            self.res.encoding='gbk'
            return self.res.json()
        else:
            msg = "HTTP request error,the status code is:%s"%(str(self.res.status_code))
            raise msg

if __name__ == '__main__':
    # oms请求测试
    url="http://172.19.80.213:9001/"
    method="GET"
    data={
    "Funcid":620001,
    "FID_CXBZ":0,
    "FID_LY":1,
    "FID_DDLX":200,
    "FID_KHH":"5LC05004",
    "FID_GDH":"5LC05004",
    "FID_ZJZH":"5LC05004",
    "FID_TXMM":8888888,
    "FID_JYMM":123456,
    "FID_WTLB":1001,
    "FID_JYS":"NY",
    "FID_ZQDM":"F",
    "FID_WTSL":20,
    "FID_WTJG":14,
    "FID_GGLB":1
    }
    pro_http=ProcessHttp()
    res=pro_http.sendHttp(url,method,data)
    print(res)
    # midoffice
    # url="http://127.0.0.1:6060/midoffice/singleUser/feed/insert"
    # method="POST"
    # data={
    #     "feedbackType":"1",
    #     "feedbackContent":"3",
    #     "thsUserId":"111",
    #     "thsAccount":"222",
    #     "platform":"gphone",
    #     "version":"1.1.0",
    #     "buildVersion":"LHSG037.08.472.1.32",
    #     "phoneModel":"Mi 10 Pro",
    #     "business":"System",
    #     "modular":"System",
    #     "function":"System Settings",
    #     "opinionSources":"System Settings",
    #     "memo":""
    # }
    # header={"token":"MTM2MTc6MTYyMzA0NzY3MDo1YTY5ZmQ0ODg0MWI4ODJmNDQ1OWFkZGFmMzFhMWE5Yw=="}
    # pro_http=ProcessHttp()
    # res=pro_http.sendHttp(url,method,data,header)
    # print(res)