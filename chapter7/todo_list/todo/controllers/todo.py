"""
Todo 控制器
"""
from todo.utils.http import redirect
from todo.utils.templating import render_template
from todo.utils.logging import logger
from todo.models.todo import Todo


def index(request):
    """首页视图函数"""
    # 倒序排序，最近添加的 todo 排在前面
    todo_list = Todo.all(sort=True, reverse=True)
    context = {
        'todo_list': todo_list,
    }
    return render_template('todo/index.html', **context)


def new(request):
    """新建 todo 视图函数"""
    form = request.form
    logger(f'form: {form}')

    content = form.get('content')
    if content:
        todo = Todo(content=content)
        todo.save()
    return redirect('/index')


def edit(request):
    """编辑 todo 视图函数"""
    # 处理 POST 请求
    if request.method == 'POST':
        form = request.form
        logger(f'form: {form}')

        id = int(form.get('id', -1))
        content = form.get('content')

        if id != -1 and content:
            todo = Todo.get(id=id)
            if todo:
                todo.content = content
                todo.save()
        return redirect('/index')

    # 处理 GET 请求
    args = request.args
    logger(f'args: {args}')

    id = int(args.get('id', -1))
    if id == -1:
        return redirect('/index')

    todo = Todo.get(id=id)
    if not todo:
        return redirect('/index')

    context = {
        'todo': todo,
    }
    return render_template('todo/edit.html', **context)


def delete(request):
    """删除 todo 视图函数"""
    form = request.form
    logger(f'form: {form}')

    id = int(form.get('id', -1))
    if id != -1:
        todo = Todo.get(id=id)
        if todo:
            todo.delete()
    return redirect('/index')


routes = {
    '/': (index, ['GET']),
    '/index': (index, ['GET']),
    '/new': (new, ['POST']),
    '/edit': (edit, ['GET', 'POST']),
    '/delete': (delete, ['POST']),
}
