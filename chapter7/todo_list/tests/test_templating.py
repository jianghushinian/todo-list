"""
测试模板引擎
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from todo.utils.templating import Template


def test_template():
    """测试模板引擎"""
    from collections import namedtuple

    html = """
    <h1>{{ title }}</h1>
    <div>
        {% for todo in todo_list %}
            <p>{{ todo.content }}</p>
        {% endfor %}
    </div>
    """

    render_result = """
    <h1>Todo List</h1>
    <div>
        
            <p>one</p>
        
            <p>two</p>
        
    </div>
    """

    Todo = namedtuple('Todo', 'content')
    ctx = {
        'title': 'Todo List',
        'todo_list': [Todo('one'), Todo('two')]
    }
    t = Template(html, ctx)
    assert t.render() == render_result


def main():
    test_template()


if __name__ == '__main__':
    main()
