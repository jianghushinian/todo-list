"""
控制器
"""
from todo.utils import render_template


def index():
    """首页视图函数"""
    return render_template('index.html')


routes = {
    '/': (index, ['GET']),
    '/index': (index, ['GET']),
}
