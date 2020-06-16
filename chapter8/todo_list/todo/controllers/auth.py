"""
用户认证控制器
"""
from todo.utils.auth import current_user
from todo.utils.http import redirect
from todo.utils.templating import render_template
from todo.utils.logging import logger
from todo.models.user import User
from todo.models.session import Session


def register(request):
    """注册

    Args:
        request: 请求对象

    Returns:
        GET 请求:
            返回注册页面
        POST 请求:
            注册成功将重定向到登录页
            注册失败返回失败原因提示短语
    """
    if request.method == 'POST':
        # 获取表单中的用户名和密码
        form = request.form
        logger(f'form: {form}')
        username = form.get('username')
        raw_password = form.get('password')

        # 验证用户名和密码是否合法
        if not username or not raw_password:
            return '无效的用户名或密码'.encode('utf-8')
        user = User.find_by(username=username, ensure_one=True)
        if user:
            return '用户名已存在'.encode('utf-8')

        # 对密码进行散列计算，创建并保存用户信息
        password = User.generate_password(raw_password)
        user = User(username=username, password=password)
        user.save()
        # 注册成功后重定向到登录页面
        return redirect('/login')

    return render_template('auth/register.html')


def login(request):
    """登录

    Args:
        request: 请求对象

    Returns:
        GET 请求:
            返回登录页面
        POST 请求:
            登录成功将重定向到首页
            登录失败返回失败原因提示短语
    """
    # 如果用户已经登录，直接重定向到首页
    if current_user(request):
        return redirect('/index')

    if request.method == 'POST':
        message = '用户名或密码不正确'.encode('utf-8')

        # 获取表单中的用户名和密码
        form = request.form
        logger(f'form: {form}')
        username = form.get('username')
        raw_password = form.get('password')

        # 验证用户名和密码是否正确
        if not username or not raw_password:
            return message
        user = User.find_by(username=username, ensure_one=True)
        if not user:
            return message
        password = user.password
        if not User.validate_password(raw_password, password):
            return message

        # 创建 Session 并将 session_id 写入 Cookie 实现登录
        session = Session(user_id=user.id)
        session.save()
        cookies = {
            'session_id': session.id,
        }
        return redirect('/index', cookies=cookies)

    return render_template('auth/login.html')


routes = {
    '/register': (register, ['GET', 'POST']),
    '/login': (login, ['GET', 'POST']),
}
