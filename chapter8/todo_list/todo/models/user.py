"""
用户模型
"""
import hashlib

from . import Model
from todo.config import SECRET


class User(Model):
    """
    User 模型类
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.username = kwargs.get('username', '')
        self.password = kwargs.get('password', '')

    @classmethod
    def generate_password(cls, raw_password):
        """生成密码

        Args:
            raw_password: 未加密的原始密码

        Returns:
            加密后的密码
        """
        md5 = hashlib.md5()
        md5.update(SECRET.encode('utf-8'))
        md5.update(raw_password.encode('utf-8'))
        return md5.hexdigest()

    @classmethod
    def validate_password(cls, raw_password, password):
        """验证密码

        Args:
            raw_password: 未加密的原始密码
            password: 加密后的密码

        Returns:
            验证结果 True / False
        """
        md5 = hashlib.md5()
        md5.update(SECRET.encode('utf-8'))
        md5.update(raw_password.encode('utf-8'))
        return md5.hexdigest() == password
