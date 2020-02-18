import io
import time
import picamera
import stomp
import threading


class ImgSender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.topic = ""
        self.exit = False
        self.conn = stomp.Connection10([('heluox.com', 61613)])
        #self.conn = stomp.Connection10([('192.168.0.107', 61613)])

    def run(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)  # pi camera resolution
            camera.framerate = 10
            time.sleep(0.1)
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                stream.seek(0)
                self.conn.send(self.topic, (stream.read()))
                stream.seek(0)
                stream.truncate()
                if self.exit:
                    self.conn.disconnect()
                    break

    def pub(self, topic):
        self.conn.start()
        self.conn.connect()
        self.conn.subscribe(topic)
        self.topic = topic
        self.start()

    def stop(self):
        self.exit = True


if __name__ == "__main__":
    while True:
        s = input(">>>")
        if s == "run":
            img = ImgSender()
            img.pub("test/img")
        elif s == "stop":
            img.stop()
