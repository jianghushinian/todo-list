"""
Todo 模型
"""
from . import Model


class Todo(Model):
    """
    Todo 模型类
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.content = kwargs.get('content', '')
