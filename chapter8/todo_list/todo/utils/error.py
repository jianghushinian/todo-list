"""
异常处理
"""
from todo.utils.templating import render_template
from todo.utils.http import Response


def page_not_found():
    """处理 400 异常"""
    body = render_template('error/404.html')
    return Response(body, status=400)


def internal_server_error():
    """处理 500 异常"""
    body = render_template('error/500.html')
    return Response(body, status=500)


errors = {
    404: page_not_found,
    500: internal_server_error,
}
