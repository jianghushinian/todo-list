"""
Todo 控制器
"""
from todo.utils.http import redirect
from todo.utils.logging import logger
from todo.utils.templating import render_template
from todo.models.todo import Todo
from todo.utils.auth import login_required, current_user


@login_required
def index(request):
    """首页视图函数

    Args:
        request: 请求对象

    Returns:
        返回首页（即列表页）
    """
    user = current_user(request)
    todo_list = Todo.find_by(user_id=user.id, sort=True, reverse=True)
    context = {
        'todo_list': todo_list,
    }
    return render_template('todo/index.html', **context)


@login_required
def new(request):
    """新建 todo 视图函数

    Args:
        request: 请求对象

    Returns:
        重定向到首页
    """
    form = request.form
    logger(f'form: {form}')

    content = form.get('content')
    if content:
        user = current_user(request)
        if user:
            todo = Todo(content=content, user_id=user.id)
            todo.save()
    return redirect('/index')


@login_required
def edit(request):
    """编辑 todo 视图函数

    Args:
        request: 请求对象

    Returns:
        GET 请求:
            返回编辑页面
        POST 请求:
            更新当前编辑项，重定向到首页
    """
    if request.method == 'POST':
        form = request.form
        logger(f'form: {form}')

        id = int(form.get('id', -1))
        content = form.get('content')

        if id != -1 and content:
            user = current_user(request)
            if user:
                todo = Todo.find_by(id=id, user_id=user.id, ensure_one=True)
                if todo:
                    todo.content = content
                    todo.save()
        return redirect('/index')

    args = request.args
    logger(f'args: {args}')

    id = int(args.get('id', -1))
    if id == -1:
        return redirect('/index')

    user = current_user(request)
    if not user:
        return redirect('/index')

    todo = Todo.find_by(id=id, user_id=user.id, ensure_one=True)
    if not todo:
        return redirect('/index')

    context = {
        'todo': todo,
    }
    return render_template('todo/edit.html', **context)


@login_required
def delete(request):
    """删除 todo 视图函数

    Args:
        request: 请求对象

    Returns:
        删除当前项，重定向到首页
    """
    form = request.form
    logger(f'form: {form}')

    id = int(form.get('id', -1))
    if id != -1:
        user = current_user(request)
        if user:
            todo = Todo.find_by(id=id, user_id=user.id, ensure_one=True)
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
