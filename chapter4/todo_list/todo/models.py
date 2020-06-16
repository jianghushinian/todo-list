"""
模型
"""
import os
import json

from todo.config import BASE_DIR


class Todo(object):
    """
    Todo 模型类
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.content = kwargs.get('content', '')

    @classmethod
    def _db_path(cls):
        """获取存储 todo 数据文件的绝对路径"""
        # 返回 'todo_list/todo/db/todo.json' 文件的绝对路径
        path = os.path.join(BASE_DIR, 'db/todo.json')
        return path

    @classmethod
    def _load_db(cls):
        """加载 JSON 文件中所有 todo 数据"""
        path = cls._db_path()
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def all(cls, sort=False, reverse=False):
        """获取全部 todo"""
        # 这一步用来将所有从 JSON 文件中读取的 todo 数据转换为 Todo 实例化对象，方便后续操作
        todo_list = [cls(**todo_dict) for todo_dict in cls._load_db()]
        # 对数据按照 id 进行排序
        if sort:
            todo_list = sorted(todo_list, key=lambda x: x.id, reverse=reverse)
        return todo_list
