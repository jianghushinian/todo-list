"""
测试模型类
"""
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from todo.models.todo import Todo


def test_todo():
    """测试 Todo 模型类"""
    content = uuid.uuid4().hex
    t = Todo(content=content)
    t.save()
    ts = Todo.all()
    find_todo = Todo.get(t.id)
    t.delete()

    assert t.content == content
    assert t.id in [t.id for t in ts]
    assert t.id == find_todo.id


def main():
    test_todo()


if __name__ == '__main__':
    main()
