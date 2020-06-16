"""
基础模型
"""
import os
import json

from todo.config import BASE_DIR


class Model(object):
    """
    基础模型类
    """

    @classmethod
    def _db_path(cls):
        """获取存储模型对象数据的文件的绝对路径"""
        class_name = cls.__name__
        file_name = f'{class_name.lower()}.json'
        path = os.path.join(BASE_DIR, 'db', file_name)
        return path

    @classmethod
    def _load_db(cls):
        """加载 JSON 文件中所有模型对象数据"""
        with open(cls._db_path(), 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def _save_db(cls, data):
        """将模型对象数据保存到 JSON 文件

        Args:
            data: 模型数据集

        Returns:
            None
        """
        with open(cls._db_path(), 'w', encoding='utf-8') as f:
            return json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def all(cls, sort=False, reverse=False):
        """查询全部模型对象

        Args:
            sort: 查询结果集是否根据模型对象的 id 进行排序
            reverse: 排序顺序

        Returns:
            模型对象组成的结果集列表
        """
        models = [cls(**model) for model in cls._load_db()]
        if sort:
            models = sorted(models, key=lambda x: x.id, reverse=reverse)
        return models

    @classmethod
    def find_by(cls, limit=-1, ensure_one=False, sort=False, reverse=False, **kwargs):
        """根据传入条件查询模型对象

        Args:
            limit: 限制查询条数
            ensure_one: 是否限制只查询一条数据
            sort: 查询结果集是否根据模型对象的 id 进行排序
            reverse: 排序顺序
            **kwargs: 模型对象属性的任意关键字参数

        Returns:
            模型对象组成的结果集列表
        """
        result = []
        models = [model.__dict__ for model in cls.all(sort=sort, reverse=reverse)]
        for model in models:
            for k, v in kwargs.items():
                if model.get(k) != v:
                    break
            else:
                result.append(cls(**model))

        if 0 < limit < len(result):
            result = result[:limit]
        if ensure_one:
            result = result[0] if len(result) > 0 else None

        return result

    @classmethod
    def get(cls, id):
        """通过 id 查询模型对象

        Args:
            id: 模型对象 id

        Returns:
            模型对象 / None
        """
        result = cls.find_by(id=id, ensure_one=True)
        return result

    def save(self):
        """保存模型对象"""
        # 查找出除 self 以外所有 model
        # model.__dict__ 是保存了所有实例属性的字典
        models = [model.__dict__ for model in self.all(sort=True) if model.id != self.id]

        # 自增 id
        if self.id is None:
            # 如果 model_list 大于 0 说明不是第一条 model，取最后一条 model 的 id 加 1
            if len(models) > 0:
                self.id = models[-1]['id'] + 1
            # 否则说明是第一条 model，id 为 1
            else:
                self.id = 1

        # 将当前 model 追加到 model_list
        models.append(self.__dict__)
        # 将所有 model 保存到文件
        self._save_db(models)

    def delete(self):
        """删除模型对象"""
        model_list = [model.__dict__ for model in self.all() if model.id != self.id]
        self._save_db(model_list)
