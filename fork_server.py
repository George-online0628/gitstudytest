# fork_server.py  基于fork的多进程并发程序

from socket import *
import os,sys
import signal

HOST=''
PORT = 8888
ADDR = (HOST,PORT)

def do_client(c):
    print('处理子进程的请求:',c.getpeername())
    try:
        while True:
            data = c.recv(1024)
            if not data:
                break
            print(data.decode())
            c.send(b'Receve from server')
    except (KeyboardInterrupt,SystemError):
        sys.exit('客户端退出')
    except Exception as e:
        print(e)
    c.close()
    sys.exit(0)


s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

print('进程%d等待客户端连接:'%os.getpid())

signal.signal(signal.SIGCHLD,signal.SIG_IGN)

while True:
    try:
        c,addr = s.accept()
    except KeyboardInterrupt:
        sys.exit('服务器退出')
    except Exception as e:
        print('error',e)
        continue

    pid = os.fork()

    if pid == 0:
        s.close()
        do_client(c)
    else:
        c.close()
        continue
