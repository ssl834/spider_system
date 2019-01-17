import urllib.request,urllib.parse
import http.cookiejar
import requests

class GetCookie(object):
    """获取cookie对象"""
    def __init__(self):
        user_agent = r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.16 Safari/537.36'
        self.headers= {'User-Agent': user_agent}
    def get_cookie(self,url,data=None):
        if data:
            # 获取登录cookie
            cookie = http.cookiejar.CookieJar()
            handler = urllib.request.HTTPCookieProcessor(cookie)
            opener = urllib.request.build_opener(handler)
            postdata=urllib.parse.urlencode(data).encode()
            request=urllib.request.Request(url,postdata,self.headers)
            response = opener.open(request)

        else:
            # 获取正常cookie
            r=requests.get(url,self.headers)
            cookie=r.cookies

        return cookie

