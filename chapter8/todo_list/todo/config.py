"""
配置信息
"""
import os

# todo/ 目录绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# IP
HOST = '127.0.0.1'
# 端口
PORT = 8000

# 缓冲大小
BUFFER_SIZE = 1024

SECRET = 'random string'
