#coding:utf-8
# zstd 压缩与解压

import zstd
import base64


class ZstdUtils:
    '''
    zstd压缩算法
    '''

    def __init__(self, level=1):
        self.level = level

    def to_bytes(self, data):
        """
        转换为bytes
        """
        return data.encode('utf-8')

    def to_str(self, data):
        """
        转换为string
        """
        return data.decode('utf-8')

    def b64_encode(self, data):
        """
        转换为base64
        """
        return base64.b64encode(data)

    def b64_decode(self, data):
        """
        base64解压缩
        """
        return base64.b64decode(data)

    def compress(self, data):
        bytes_data = self.to_bytes(data)
        return self.to_str(self.b64_encode(zstd.compress(bytes_data, self.level)))

    def decompress(self, data):
        decompress_data = zstd.decompress(self.b64_decode(data))
        if decompress_data:
            return self.to_str(decompress_data)
