"""
HTTP 相关工具
"""
from urllib.parse import unquote_plus


class Request(object):
    """请求类"""

    def __init__(self, request_message):
        """初始化方法

        Args:
            request_message: 请求报文
        """
        method, path, headers, args, cookies, form = self.parse_data(request_message)
        self.method = method  # 请求方法 GET、POST
        self.path = path  # 请求路径 /index
        self.headers = headers  # 请求头 {'Host': '127.0.0.1:8000'}
        self.cookies = cookies  # Cookie
        self.args = args  # 查询参数
        self.form = form  # 请求体

    def parse_data(self, data):
        """解析请求数据

        Args:
            data: 请求数据

        Returns:
            返回解析好的各部分请求数据构成的元组
        """
        # 用请求报文中的第一个 '\r\n\r\n' 做分割，将得到请求头和请求体
        header, body = data.split('\r\n\r\n', 1)
        method, path, headers, args, cookies = self._parse_header(header)
        form = self._path_body(body)

        return method, path, headers, args, cookies, form

    def _parse_header(self, data):
        """解析请求头

        Args:
            data: 请求头数据

        Returns:
            返回解析好的各部分请求头数据构成的元组
        """
        # 拆分请求行和请求首部
        request_line, request_header = data.split('\r\n', 1)

        # 请求行拆包 'GET /index HTTP/1.1' -> ['GET', '/index', 'HTTP/1.1']
        # 因为 HTTP 版本号没什么用，所以用一个下划线 _ 变量来接收
        method, path_query, _ = request_line.split()
        path, args = self._parse_path(path_query)

        # 解析请求首部所有的键值对，组装成字典
        headers = {}
        for header in request_header.split('\r\n'):
            k, v = header.split(': ', 1)
            headers[k] = v

        cookies = self._parse_cookies(headers)
        return method, path, headers, args, cookies

    @staticmethod
    def _parse_path(data):
        """解析请求路径、请求参数

        Args:
            data: 请求行数据

        Returns:
            返回请求路径、请求参数构成的元组
        """
        args = {}
        # 请求路径和 GET 请求参数格式: /index?edit=1&content=text
        if '?' not in data:
            path, query = data, ''
        else:
            path, query = data.split('?', 1)
            for q in query.split('&'):
                k, v = q.split('=', 1)
                args[k] = v
        return path, args

    @staticmethod
    def _parse_cookies(headers):
        """解析 Cookie

        Args:
            headers: 请求头数据

        Returns:
            cookies: 所有 Cookie 组成的字典
        """
        cookies = {}
        for key, value in headers.items():
            if key.lower() == 'cookie':
                for cookie in value.split('; '):
                    if '=' in cookie:
                        k, v = cookie.split('=', 1)
                        cookies[k] = v
        return cookies

    @staticmethod
    def _path_body(data):
        """解析请求体

        Args:
            data: 请求体数据

        Returns:
            form: 所有请求体参数组成的字典
        """
        form = {}
        if data:
            # POST 请求体参数格式: username=zhangsan&password=mima
            for b in data.split('&'):
                k, v = b.split('=', 1)
                # 前端页面中通过 form 表单提交过来的数据会被自动编码，使用 unquote_plus 来解码
                # 使用 unquote_plus 能够处理空格变加号问题
                form[k] = unquote_plus(v)
        return form


class Response(object):
    """响应类"""

    # 根据状态码获取原因短语
    reason_phrase = {
        200: 'OK',
        302: 'FOUND',
        405: 'METHOD NOT ALLOWED',
    }

    def __init__(self, body, headers=None, status=200, cookies=None):
        """初始化方法

        Args:
            body: 响应体
            headers: 响应头
            status: 状态码
            cookies: Cookie
        """
        # 默认响应头，指定响应内容的类型为 HTML
        _headers = {
            'Content-Type': 'text/html; charset=utf-8',
        }

        if headers is not None:
            _headers.update(headers)
        self.headers = _headers  # 响应头
        self.body = body  # 响应体
        self.status = status  # 状态码
        self.cookies = cookies  # Cookie

    def __bytes__(self):
        """构造响应报文"""
        # 状态行 'HTTP/1.1 200 OK\r\n'
        header = f'HTTP/1.1 {self.status} {self.reason_phrase.get(self.status, "")}\r\n'
        # 响应首部
        header += ''.join(f'{k}: {v}\r\n' for k, v in self.headers.items())
        # Cookie
        if self.cookies:
            header += 'Set-Cookie: ' + \
                      '; '.join(f'{k}={v}' for k, v in self.cookies.items())
        # 空行
        blank_line = '\r\n'
        # 响应体
        body = self.body

        # body 支持 str 或 bytes 类型
        if isinstance(body, str):
            body = body.encode('utf-8')
        response_message = (header + blank_line).encode('utf-8') + body
        return response_message


def redirect(url, status=302, cookies=None):
    """重定向

    Args:
        url: 重定向目标 URL 地址
        status: 状态码
        cookies: Cookie

    Returns:
        Response 对象
    """
    headers = {
        'Location': url,
    }
    body = ''
    return Response(body, headers=headers, status=status, cookies=cookies)
