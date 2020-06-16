"""
测试视图函数
"""
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from todo.controllers import routes
from todo.utils.http import Request
from todo.models.todo import Todo
from todo.models.user import User
from todo.models.session import Session


def test_register():
    """测试注册"""
    # 测试 GET 请求
    request_message = 'GET /register HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\n'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    assert 'Register' in r

    # 测试 POST 请求
    username = uuid.uuid4().hex
    raw_password = 'password'
    password = User.generate_password(raw_password)
    request_message = f'POST /register HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\n' \
                      f'username={username}&password={password}'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    u = User.find_by(username=username, ensure_one=True)
    u.delete()
    assert b'302 FOUND' in bytes(r)
    assert b'/login' in bytes(r)


def test_login():
    """测试登录"""
    # 测试 GET 请求
    request_message = 'GET /login HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\n'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    assert 'Login' in r

    # 测试 POST 请求
    username = uuid.uuid4().hex
    raw_password = 'password'
    password = User.generate_password(raw_password)
    u = User(username=username, password=password)
    u.save()
    request_message = f'POST /login HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\n' \
                      f'username={username}&password={raw_password}'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    u.delete()
    s = Session.get(r.cookies.get('session_id'))
    s.delete()
    assert b'302 FOUND' in bytes(r)
    assert b'/index' in bytes(r)
    assert b'session_id' in bytes(r)

    r = route(request)
    assert r.decode('utf-8') == '用户名或密码不正确'


def test_index():
    """测试首页"""
    username = uuid.uuid4().hex
    raw_password = 'password'
    password = User.generate_password(raw_password)
    u = User(username=username, password=password)
    u.save()
    s = Session(user_id=u.id, expire_in='2099-12-31 00:00:00')
    s.save()
    request_message = f'GET / HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n' \
                      f'Cookie: session_id={s.id}\r\n\r\n'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    u.delete()
    s.delete()
    assert b'Todo List' in bytes(r, encoding='utf-8')
    assert b'/new' in bytes(r, encoding='utf-8')

    r = route(request)
    assert b'302 FOUND' in bytes(r)
    assert b'/login' in bytes(r)


def test_new():
    """测试新增 todo"""
    username = uuid.uuid4().hex
    raw_password = 'password'
    password = User.generate_password(raw_password)
    u = User(username=username, password=password)
    u.save()
    s = Session(user_id=u.id, expire_in='2099-12-31 00:00:00')
    s.save()
    content = uuid.uuid4().hex
    request_message = f'POST /new HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n' \
                      f'Cookie: session_id={s.id}\r\n\r\ncontent={content}'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    t = Todo.find_by(user_id=u.id, ensure_one=True)
    u.delete()
    s.delete()
    t.delete()

    assert b'302 FOUND' in bytes(r)
    assert b'/index' in bytes(r)
    assert t.content == content


def test_edit():
    """测试编辑 todo"""
    username = uuid.uuid4().hex
    raw_password = 'password'
    password = User.generate_password(raw_password)
    u = User(username=username, password=password)
    u.save()
    s = Session(user_id=u.id, expire_in='2099-12-31 00:00:00')
    s.save()
    content = uuid.uuid4().hex
    t = Todo(user_id=u.id, content=content)
    t.save()
    edit_content = 'Edit: ' + content
    request_message = f'POST /edit HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n' \
                      f'Cookie: session_id={s.id}\r\n\r\nid={t.id}&content={edit_content}'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    t = Todo.find_by(user_id=u.id, content=edit_content, ensure_one=True)
    u.delete()
    s.delete()
    t.delete()
    assert b'302 FOUND' in bytes(r)
    assert b'/index' in bytes(r)
    assert t.content == edit_content

    r = route(request)
    assert b'302 FOUND' in bytes(r)
    assert b'/login' in bytes(r)


def test_delete():
    """测试删除 todo"""
    username = uuid.uuid4().hex
    raw_password = 'password'
    password = User.generate_password(raw_password)
    u = User(username=username, password=password)
    u.save()
    s = Session(user_id=u.id, expire_in='2099-12-31 00:00:00')
    s.save()
    content = uuid.uuid4().hex
    t = Todo(user_id=u.id, content=content)
    t.save()
    request_message = f'POST /delete HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n' \
                      f'Cookie: session_id={s.id}\r\n\r\nid={t.id}'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    t = Todo.find_by(user_id=u.id, content=content, ensure_one=True)
    u.delete()
    s.delete()
    assert b'302 FOUND' in bytes(r)
    assert b'/index' in bytes(r)
    assert t is None

    r = route(request)
    assert b'302 FOUND' in bytes(r)
    assert b'/login' in bytes(r)


def main():
    test_register()
    test_login()
    test_index()
    test_new()
    test_edit()
    test_delete()


if __name__ == '__main__':
    main()
