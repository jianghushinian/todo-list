"""
Hello World Web Server
"""
import socket


def main():
    # 创建 socket 对象
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 允许端口复用
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定 IP 和端口
    sock.bind(('127.0.0.1', 8000))
    # 开始监听
    sock.listen(5)

    while True:
        # 等待客户端请求
        client, addr = sock.accept()
        print(f'client type: {type(client)}\naddr: {addr}')

        # 接收客户端发来的数据
        data = b''
        while True:
            chunk = client.recv(1024)
            data += chunk
            if len(chunk) < 1024:
                break

        # 打印从客户端接收的数据
        print(f'data: {data}')
        # 给客户端发送响应数据
        client.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello World</h1>')

        # 关闭客户端连接对象
        client.close()


if __name__ == '__main__':
    main()
