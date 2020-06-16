"""
测试模型类
"""
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from todo.models.todo import Todo
from todo.models.user import User
from todo.models.session import Session


def test_user():
    """测试 User 模型类"""
    username = uuid.uuid4().hex
    raw_password = 'password'
    password = User.generate_password(raw_password)
    u = User(username=username, password=password)
    u.save()
    us = User.all(sort=True)
    find_user = User.find_by(username=username, ensure_one=True)
    u.delete()

    assert u.username == username
    assert u.password == password
    assert u.validate_password(raw_password, u.password) is True
    assert u.id in [u.id for u in us]
    assert u.id == find_user.id


def test_session():
    """测试 Session 模型类"""
    username = uuid.uuid4().hex
    raw_password = 'password'
    password = User.generate_password(raw_password)
    u = User(username=username, password=password)
    u.save()
    expire_in = '2099-12-31 00:00:00'
    s = Session(user_id=u.id, expire_in=expire_in)
    s.save()
    ss = Session.all()
    find_sessions = Session.find_by(user_id=u.id, expire_in=expire_in)
    u.delete()
    s.delete()

    assert s.user_id == u.id
    assert s.expire_in == expire_in
    assert s.id in [s.id for s in ss]
    assert s.id == find_sessions[0].id
    assert len(find_sessions) == 1


def test_todo():
    """测试 Todo 模型类"""
    username = uuid.uuid4().hex
    raw_password = 'password'
    password = User.generate_password(raw_password)
    u = User(username=username, password=password)
    u.save()
    content = uuid.uuid4().hex
    t = Todo(user_id=u.id, content=content)
    t.save()
    ts = Todo.all()
    find_todo = Todo.get(t.id)
    u.delete()
    t.delete()

    assert t.user_id == u.id
    assert t.content == content
    assert t.id in [t.id for t in ts]
    assert t.id == find_todo.id


def main():
    test_user()
    test_session()
    test_todo()


if __name__ == '__main__':
    main()
