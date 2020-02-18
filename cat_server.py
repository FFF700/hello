# coding:utf8
import socket
import action_ctr
from time import sleep
from threading import Thread
from img import ImgSender
import stomp

server_ip = ('192.168.0.107', 9000)
#mq_server = ('192.168.0.107', 61613)
mq_server = ('heluox.com', 61613)

conn = stomp.Connection10([mq_server])


def get_uuid():
    return 'A00001'


class SampleListener(object):

    def on_message(self, headers, message: str):
        ss = message.split()
        if len(ss) == 0:
            return
        if ss[0] == 'move':
            if len(ss) != 3:
                return
            spd = float(ss[1])
            dirs = float(ss[2])
            action_ctr.move(spd, dirs)
        elif ss[0] == 'io':
            if len(ss) != 3:
                return
            ioid = int(ss[1])
            std = ss[2]
            action_ctr.io(ioid, std)


def listen(server):
    while True:
        data, addr = server.recvfrom(1024)
        print('server:%s %s' % (addr, data))
        # server.sendto(data.upper(),addr)
        s = data.decode()
        ss = s.split()

        if len(ss) == 0:
            continue

        if ss[0] == 'channel':
            if len(ss) != 2:
                continue
            if ss[1] == 'open':
                img = ImgSender()
                img.pub("%s/img" % get_uuid())
                conn.set_listener("__listener_name", SampleListener())
                conn.start()
                conn.connect()
                conn.subscribe("%s/rx" % get_uuid())
            elif ss[1] == "close":
                img.stop()


def heart(server):
    while True:
        server.sendto(('%s' % get_uuid()).encode(), server_ip)
        sleep(60)


if __name__ == "__main__":
    ip_port = ('0.0.0.0', 60000)
    _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _s.bind(ip_port)
    print("sever started.")
    li = Thread(target=listen, args=(_s,))
    li.setDaemon(True)
    li.start()
    h = Thread(target=heart, args=(_s,))
    h.setDaemon(True)
    h.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("user stop")
    _s.close()
