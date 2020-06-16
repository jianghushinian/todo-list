"""
日志处理
"""
import os
import datetime

from todo.config import BASE_DIR

path = os.path.join(BASE_DIR, 'logs/todo.log')


def logger(*args, **kwargs):
    """记录日志"""
    now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    with open(path, 'a') as f:
        # 将日志输出到屏幕，方便调试，上线时可关掉
        # print(now, '-', *args, **kwargs)
        # 将日志输出到文件
        print(now, '-', *args, **kwargs, file=f)
