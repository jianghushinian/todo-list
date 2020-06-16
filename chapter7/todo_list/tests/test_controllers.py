"""
测试视图函数
"""
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from todo.utils.http import Request
from todo.controllers import routes
from todo.models.todo import Todo


def test_index():
    """测试首页"""
    request_message = 'GET / HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\n'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)

    assert b'Todo List' in bytes(r, encoding='utf-8')
    assert b'/new' in bytes(r, encoding='utf-8')


def test_new():
    """测试新增 todo"""
    content = uuid.uuid4().hex
    request_message = f'POST /new HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\ncontent={content}'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    t = Todo.find_by(content=content, ensure_one=True)
    t.delete()

    assert b'302 FOUND' in bytes(r)
    assert b'/index' in bytes(r)
    assert t.content == content


def test_edit():
    """测试编辑 todo"""
    content = uuid.uuid4().hex
    t = Todo(content=content)
    t.save()
    edit_content = 'Edit: ' + content
    request_message = f'POST /edit HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\n' \
                      f'id={t.id}&content={edit_content}'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    t = Todo.find_by(content=edit_content, ensure_one=True)
    t.delete()

    assert b'302 FOUND' in bytes(r)
    assert b'/index' in bytes(r)
    assert t.content == edit_content


def test_delete():
    """测试删除 todo"""
    content = uuid.uuid4().hex
    t = Todo(content=content)
    t.save()
    request_message = f'POST /delete HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\nid={t.id}'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    t = Todo.find_by(content=content, ensure_one=True)

    assert b'302 FOUND' in bytes(r)
    assert b'/index' in bytes(r)
    assert t is None


def main():
    test_index()
    test_new()
    test_edit()
    test_delete()


if __name__ == '__main__':
    main()
