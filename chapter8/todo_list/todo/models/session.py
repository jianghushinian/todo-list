"""
Session 模型
"""
import uuid
import datetime

from . import Model


class Session(Model):
    """
    Session 模型类
    """

    def __init__(self, **kwargs):
        # 为了安全起见，Session id 不使用自增数字，而使用 uuid
        self.id = kwargs.get('id')
        if self.id is None:
            self.id = uuid.uuid4().hex

        self.user_id = kwargs.get('user_id', -1)
        self.expire_in = kwargs.get('expire_in')

        if self.expire_in is None:
            now = datetime.datetime.now()
            expire_in = now + datetime.timedelta(days=1)
            self.expire_in = expire_in.strftime('%Y-%m-%d %H:%M:%S')

    def is_expired(self):
        """判断 Session 是否过期"""
        now = datetime.datetime.now()
        return datetime.datetime.strptime(self.expire_in, '%Y-%m-%d %H:%M:%S') <= now

    def save(self):
        """覆写父类的 save 方法，保存时过滤掉已经过期的 Session"""
        models = [model.__dict__ for model in self.all()
                  if model.id != self.id and not model.is_expired()]
        if not self.is_expired():
            models.append(self.__dict__)
        self._save_db(models)
