"""
用户认证相关工具
"""
import functools

from todo.models.user import User
from todo.models.session import Session
from todo.utils.http import redirect
from todo.utils.logging import logger


def current_user(request):
    """获取当前登录用户

    Args:
        request: 请求对象

    Returns:
        如果已登录，返回当前登录用户对象，否则返回 None
    """
    # 从 Cookie 中获取 session_id
    cookies = request.cookies
    logger(f'cookies: {cookies}')
    session_id = cookies.get('session_id')

    # 查找 Session 并验证其是否过期
    session = Session.get(session_id)
    if not session:
        return None
    if session.is_expired():
        session.delete()
        return None

    # 查找当前登录用户
    user = User.get(session.user_id)
    if not user:
        return None
    return user


def login_required(func):
    """验证登录

    此函数是一个装饰器，可以装饰在控制器函数上，用于验证用户是否登录
    如果用户未登录，则重定向到登录页面

    Args:
        func: 需要验证登录的控制器函数

    Returns:
        wrapper: 可以验证是否登录的函数
    """

    @functools.wraps(func)
    def wrapper(request):
        user = current_user(request)
        if not user:
            return redirect('/login')
        result = func(request)
        return result

    return wrapper
