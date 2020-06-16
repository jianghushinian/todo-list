"""
工具集
"""
import os
import re

from todo.config import BASE_DIR


class Request(object):
    """请求类"""

    def __init__(self, request_message):
        method, path, headers = self.parse_data(request_message)
        self.method = method  # 请求方法 GET、POST
        self.path = path  # 请求路径 /index
        self.headers = headers  # 请求头 {'Host': '127.0.0.1:8000'}

    def parse_data(self, data):
        """解析请求数据"""
        # 用请求报文中的第一个 '\r\n\r\n' 做分割，将得到请求头和请求体
        # 请求体暂时用不到先不处理
        header, body = data.split('\r\n\r\n', 1)
        method, path, headers = self._parse_header(header)
        return method, path, headers

    def _parse_header(self, data):
        """解析请求头"""
        # 拆分请求行和请求首部
        request_line, request_header = data.split('\r\n', 1)

        # 请求行拆包 'GET /index HTTP/1.1' -> ['GET', '/index', 'HTTP/1.1']
        # 因为 HTTP 版本号没什么用，所以用一个下划线 _ 变量来接收
        method, path, _ = request_line.split()

        # 解析请求首部所有的键值对，组装成字典
        headers = {}
        for header in request_header.split('\r\n'):
            k, v = header.split(': ', 1)
            headers[k] = v

        return method, path, headers


class Response(object):
    """响应类"""

    # 根据状态码获取原因短语
    reason_phrase = {
        200: 'OK',
        405: 'METHOD NOT ALLOWED',
    }

    def __init__(self, body, headers=None, status=200):
        # 默认响应首部字段，指定响应内容的类型为 HTML
        _headers = {
            'Content-Type': 'text/html; charset=utf-8',
        }

        if headers is not None:
            _headers.update(headers)
        self.headers = _headers  # 响应头
        self.body = body  # 响应体
        self.status = status  # 状态码

    def __bytes__(self):
        """构造响应报文"""
        # 状态行 'HTTP/1.1 200 OK\r\n'
        header = f'HTTP/1.1 {self.status} {self.reason_phrase.get(self.status, "")}\r\n'
        # 响应首部
        header += ''.join(f'{k}: {v}\r\n' for k, v in self.headers.items())
        # 空行
        blank_line = '\r\n'
        # 响应体
        body = self.body

        # body 支持 str 或 bytes 类型
        if isinstance(body, str):
            body = body.encode('utf-8')
        response_message = (header + blank_line).encode('utf-8') + body
        return response_message


class Template(object):
    """模板引擎"""

    def __init__(self, text, context):
        # 保存最终结果
        self.result = []
        # 保存从 HTML 中解析出来的 for 语句代码片段
        self.for_snippet = []
        # 上下文变量
        self.context = context
        # 使用正则匹配出所有的 for 语句、模板变量
        self.snippets = re.split('({{.*?}}|{%.*?%})', text, flags=re.DOTALL)
        # 标记是否为 for 语句代码段
        is_for_snippet = False

        # 遍历所有匹配出来的代码片段
        for snippet in self.snippets:
            # 解析模板变量
            if snippet.startswith('{{'):
                if is_for_snippet is False:
                    # 去掉花括号和空格，获取变量名
                    var = snippet[2:-2].strip()
                    # 获取变量的值
                    snippet = self._get_var_value(var)
            # 解析 for 语句
            elif snippet.startswith('{%'):
                # for 语句开始代码片段 -> {% for todo in todo_list %}
                if 'in' in snippet:
                    is_for_snippet = True
                    self.result.append('{}')
                # for 语句结束代码片段 -> {% endfor %}
                else:
                    is_for_snippet = False
                    snippet = ''

            if is_for_snippet:
                # 如果是 for 语句代码段，需要进行二次处理，暂时保存到 for 语句片段列表中
                self.for_snippet.append(snippet)
            else:
                # 如果是模板变量，直接将变量值追加到结果列表中
                self.result.append(snippet)

    def _get_var_value(self, var):
        """根据变量名获取变量的值"""
        # 如果 '.' 不在变量名中，直接在上下文变量中获取变量的值
        if '.' not in var:
            value = self.context.get(var)
        # '.' 在变量名中（对象.属性），说明是要获取对象的属性
        else:
            obj, attr = var.split('.')
            value = getattr(self.context.get(obj), attr)

        # 保证返回的变量值为字符串
        if not isinstance(value, str):
            value = str(value)
        return value

    def _parse_for_snippet(self):
        """解析 for 语句片段代码"""
        # 保存 for 语句片段解析结果
        result = []
        if self.for_snippet:
            # 解析 for 语句开始代码片段
            # '{% for todo in todo_list %}' -> ['for', 'todo', 'in', 'todo_list']
            words = self.for_snippet[0][2:-2].strip().split()
            # 从上下文变量中获取 for 语句中的可迭代对象
            iter_obj = self.context.get(words[-1])
            # 遍历可迭代对象
            for i in iter_obj:
                # 遍历 for 语句片段的代码块
                for snippet in self.for_snippet[1:]:
                    # 解析模板变量
                    if snippet.startswith('{{'):
                        # 去掉花括号和空格，获取变量名
                        var = snippet[2:-2].strip()
                        # 如果 '.' 不在变量名中，直接将循环变量 i 赋值给 snippet
                        if '.' not in var:
                            snippet = i
                        # '.' 在变量名中（对象.属性），说明是要获取对象的属性
                        else:
                            obj, attr = var.split('.')
                            # 将对象的属性值赋值给 snippet
                            snippet = getattr(i, attr)
                    # 保证变量值为字符串
                    if not isinstance(snippet, str):
                        snippet = str(snippet)
                    # 将解析出来的循环变量结果追加到 for 语句片段解析结果列表中
                    result.append(snippet)
        return result

    def render(self):
        """渲染"""
        # 获取 for 语句片段解析结果
        for_result = self._parse_for_snippet()
        # 将渲染结果组装成字符串并返回
        return ''.join(self.result).format(''.join(for_result))


def render_template(template, **context):
    """渲染模板"""
    # 读取 'todo_list/todo/templates' 目录下的 HTML 文件内容
    template_dir = os.path.join(BASE_DIR, 'templates')
    path = os.path.join(template_dir, template)

    with open(path, 'r', encoding='utf-8') as f:
        # 将从 HTML 中读取的内容传递给模板引擎
        t = Template(f.read(), context)

    # 调用模板引擎的渲染方法，实现模板渲染
    return t.render()
