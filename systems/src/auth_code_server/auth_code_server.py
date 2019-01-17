# 外接平台需设置账号密码
import sys
from auth_code_server.pop_up_window import ManualGetCode
from auth_code_server.auth_code_conf import AUTHCODE



class ImgAuthCodeServer(object):
    """验证码服务"""
    #     接入打码平台
    def auto_verificate(self, auth_type, img):
        for k,v in AUTHCODE.items():
            if auth_type == k:
                code=v['verificate_method'](k,v['username'],v['password'],v['soft_id'],v['soft_key'],img)
                return code
    # 手动打码
    def manual(self,img,verificate_url):
            # 如果在win上运行
            if sys.platform.startswith('win'):
                code = ManualGetCode().get_code(img)
            #     如果运行环境是linux
            else:
                # linux
                print(verificate_url)
                code = input("请复制上面网址到浏览器，并输入网址中的验证码：")
            return code


class OtherAuthVerificate(object):
    """其他验证方式"""
    pass
if __name__ == '__main__':
    ImgAuthCodeServer().auto_verificate('chaojiying','')