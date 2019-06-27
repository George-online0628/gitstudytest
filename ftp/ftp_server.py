# ftp_server.py
from socket import *
import os,sys
import signal
import time
import signal

FILE_PATH = '/home/tarena/STEP2/pyhton Thread/day4/ftp/ftpFile/'

HOST = ''
PORT = 8889
ADDR = (HOST,PORT)

class FtpServer(object):
    def __init__(self,c):
        self.c = c

    def do_list(self):
        #获取文件列表
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self.c.send('文件库为空'.encode())
            return
        else:
            self.c.send(b'OK')
            time.sleep(0.1)

        files = ''
        for file in file_list:
            if file[0] != '.' and os.path.isfile(FILE_PATH + file):
                files = files + file + '#'
        self.c.sendall(files.encode())

    def do_get(self,filename):
        try:
            f = open(FILE_PATH + filename,'rb')
        except:
            self.c.send('文件不存在'.encode())
            return
        self.c.send(b'OK')
        time.sleep(0.1)
        while True:
            data = f.read(1024)
            if not data:
                time.sleep(0.1)
                self.c.send(b'##')
                break
            self.c.send(data)
        print('文件发送完毕')

    def do_put(self,filename):
        try:
            f = open(FILE_PATH + filename,'wb')
        except:
            self.c.send('上传失败'.encode())
            return
        self.c.send(b'OK')
        while True:
            data = self.c.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()
        print('%s上传完毕'%filename)





def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    print('Listen the port 8889')
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print('error',e)
            continue

        print('已连接客户端',addr)

        pid = os.fork()
        if pid == 0:
            s.close()
            ftp = FtpServer(c)

            while True:
                data = c.recv(1024).decode()
                if not data or data[0] == 'Q':
                    c.close()
                    sys.exit('客户端退出')
                elif data[0] == 'L':
                    ftp.do_list()
                elif data[0] == 'G':
                    filename = data.split(' ')[-1]
                    ftp.do_get(filename)
                elif data[0] == 'P':
                    filename = data.split(' ')[-1]
                    ftp.do_put(filename)

        else:
            c.close()
            continue


if __name__ == '__main__':
    main()