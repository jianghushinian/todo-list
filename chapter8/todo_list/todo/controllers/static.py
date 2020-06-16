"""
静态资源控制器
"""
import os

from todo.config import BASE_DIR
from todo.utils.http import Response


def static(request):
    """读取静态资源视图函数

    Args:
        request: 请求对象

    Returns:
        静态资源响应对象
    """
    # 能够处理的静态资源类型
    content_type = {
        'css': 'text/css',
        '.js': 'text/javascript',
        'png': 'image/png',  # 文件需要返回二进制
        'jpg': 'image/jpeg',
    }

    # 请求路径格式：/static/css/style.css
    # 根据请求路径中的文件名后缀判断静态文件类型，指定响应首部字段 Content-Type
    headers = {
        'Content-Type': content_type.get(request.path[-3:], 'text/plain'),
    }

    # 获取静态资源绝对路径
    path = request.path.lstrip('/')
    file_path = os.path.join(BASE_DIR, path)

    # 读取静态资源内容，构造响应对象并返回
    with open(file_path, 'r') as f:
        body = f.read()
    return Response(body, headers=headers)


def favicon(request):
    """读取网页 ICO 图标

    Args:
        request: 请求对象

    Returns:
        ICO 图标响应对象
    """
    headers = {
        'Content-Type': 'image/x-icon',
    }
    path = f'static/{request.path.lstrip("/")}'
    file_path = os.path.join(BASE_DIR, path)
    # ICO 图标文件需要读取为二进制
    with open(file_path, 'rb') as f:
        body = f.read()
    return Response(body, headers=headers)


routes = {
    '/static': (static, ['GET']),
    '/favicon.ico': (favicon, ['GET']),
}
