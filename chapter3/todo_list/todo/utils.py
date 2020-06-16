"""
工具集
"""
import os

from todo.config import BASE_DIR


class Request(object):
    """请求类"""

    def __init__(self, request_message):
        method, path, headers = self.parse_data(request_message)
        self.method = method  # 请求方法 GET、POST
        self.path = path  # 请求路径 /index
        self.headers = headers  # 请求头 {'Host': '127.0.0.1:8000'}

    def parse_data(self, data):
        """解析请求报文数据"""
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

        response_message = header + blank_line + body
        return response_message.encode('utf-8')


def render_template(template):
    """读取 HTML 内容"""
    # 读取 'todo_list/todo/templates' 目录下的 HTML 文件内容
    template_dir = os.path.join(BASE_DIR, 'templates')
    path = os.path.join(template_dir, template)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    return html
