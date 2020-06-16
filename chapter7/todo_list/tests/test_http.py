"""
测试 HTTP
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from todo.utils.http import Request, Response


def test_request():
    """测试 Request 类"""
    request_message = 'GET /moin/PythonBooks HTTP/1.1\r\n' \
                      'Host: wiki.python.org\r\n' \
                      'Connection: keep-alive\r\n' \
                      'Cache-Control: max-age=0\r\n' \
                      'Upgrade-Insecure-Requests: 1\r\n' \
                      'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36\r\n' \
                      'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n' \
                      'Accept-Encoding: gzip, deflate, br\r\n' \
                      'Accept-Language: zh-CN,zh;q=0.9\r\n\r\n'
    request = Request(request_message)

    assert request.method == 'GET'
    assert request.path == '/moin/PythonBooks'
    assert request.args == {}
    assert request.form == {}
    assert len(request.headers) == 8
    assert request.headers['Host'] == 'wiki.python.org'


def test_response():
    """测试 Response 类"""
    body = b'Hello World.'
    headers = {
        'Server': 'Python Server',
    }
    response = Response(body, headers=headers)

    assert response.headers['Server'] == headers['Server']
    assert body in bytes(response)
    assert response.status == 200


def main():
    test_request()
    test_response()


if __name__ == '__main__':
    main()
