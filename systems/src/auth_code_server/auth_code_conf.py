import requests
from hashlib import md5

class Chaojiying_Client(object):
    """超级鹰"""

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

class RClient(object):
    """若快"""

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode("utf-8")).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()

class GetAgencyCode(object):
    """验证平台汇总"""
    def get_agency(self,auth_name,username,password,soft_id,soft_key, img):
        if auth_name=='chaojiying':
            return Chaojiying_Client(username=username,password=password,soft_id=soft_id).PostPic(img,1902)['pic_str']
        elif auth_name=='ruokuai':
            return RClient(username=username, password=password, soft_id=soft_id,soft_key=soft_key).rk_create(img, 3040)['Result']

AUTHCODE = {
    'chaojiying': {
        'to': Chaojiying_Client,
        'username': 'ssl834',
        'password': 's6370sl',
        'soft_id': '1',
        'soft_key': 'b40ffbee5c1cf4e38028c197eb2fc751',
        'verificate_method': GetAgencyCode().get_agency

    },
    'ruokuai': {
        'to': RClient,
        'username': 'ssl834',
        'password': 's6370sl',
        'soft_id': '1',
        'soft_key': 'b40ffbee5c1cf4e38028c197eb2fc751',
        'verificate_method': GetAgencyCode().get_agency
    }
}