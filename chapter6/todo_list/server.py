"""
Web Server
"""
import socket
import threading

from todo.config import HOST, PORT, BUFFER_SIZE
from todo.utils import Request, Response
from todo.controllers import routes


def process_connection(client):
    """处理客户端请求"""
    # 接收请求报文数据
    request_bytes = b''
    while True:
        chunk = client.recv(BUFFER_SIZE)
        request_bytes += chunk
        if len(chunk) < BUFFER_SIZE:
            break

    # 请求报文
    request_message = request_bytes.decode('utf-8')
    print(f'request_message: {request_message}')

    # 解析请求报文，构造请求对象
    request = Request(request_message)
    # 根据请求对象构造响应报文
    response_bytes = make_response(request)
    # 返回响应
    client.sendall(response_bytes)

    # 关闭连接
    client.close()


def make_response(request, headers=None):
    """构造响应报文"""
    # 默认状态码为 200
    status = 200
    # 处理静态资源请求
    if request.path.startswith('/static'):
        route, methods = routes.get('/static')
    else:
        route, methods = routes.get(request.path)

    # 如果请求方法不被允许返回 405 状态码
    if request.method not in methods:
        status = 405
        data = 'Method Not Allowed'
    else:
        # 请求首页时 route 实际上就是我们在 controllers.py 中定义的 index 视图函数
        data = route(request)

    # 如果返回结果为 Response 对象，直接获取响应报文
    if isinstance(data, Response):
        response_bytes = bytes(data)
    else:
        # 返回结果为字符串，需要先构造 Response 对象，然后再获取响应报文
        response = Response(data, headers=headers, status=status)
        response_bytes = bytes(response)

    print(f'response_bytes: {response_bytes}')
    return response_bytes


def main():
    """入口函数"""
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f'running on http://{HOST}:{PORT}')

        while True:
            client, address = s.accept()
            print(f'client address: {address}')
            # 创建新的线程来处理客户端连接
            t = threading.Thread(target=process_connection, args=(client,))
            t.start()


if __name__ == '__main__':
    main()
