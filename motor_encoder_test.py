# coding:utf8

from gpiozero import Motor
from gpiozero import Button
from time import sleep
import time
import RPi.GPIO as g

# c_left = Button(2)
# c_right = Button(3)
motor_left = Motor(forward=14, backward=15)
motor_right = Motor(forward=24, backward=23)

cn1 = 0
cn2 = 0
t = time.perf_counter()


def signal_get(a):
    global cn1, cn2
    if a == 2:
        cn1 += 1
    elif a == 3:
        cn2 += 1
    # print(f"c1 {cn1}")

class PIDController:
    def __init__(self):
        self.last_sensor = 0
        self.last_p = 0
        self.last_d = 0

    def pid_det(self, sensor_det_target, sensor):
        sensor_det = sensor - self.last_sensor
        p = sensor_det_target - sensor_det
        d = p - self.last_p
        y = p * 5 + d * 11
        if y > 500:
            y = 500
        if y < -500:
            y = -500
        self.last_p = p
        self.last_d = d
        self.last_sensor = sensor
        return 0.5+ y/1000

    def pid_follow(self,sensor1, sensor2):
        p = sensor2 - sensor1
        d = p - self.last_p
        y = p * 51 + d * 57
        if y > 500:
            y = 500
        if y < -500:
            y = -500
        self.last_p = p
        self.last_d = d
        return 0.5+ y/1000

if __name__ == "__main__":
    try:
        # c_left.when_pressed = signal_get_left
        # c_right.when_pressed = signal_get_right
        g.setup(2, g.IN, pull_up_down=g.PUD_UP)  # physicall no7
        g.add_event_detect(2, g.FALLING, callback=signal_get)
        g.setup(3, g.IN, pull_up_down=g.PUD_UP)  # physicall no7
        g.add_event_detect(3, g.FALLING, callback=signal_get)
        motor_left.forward(0.5)
        motor_right.forward(0.5)
        m_left = PIDController()
        while True:
            ret1=m_left.pid_follow(cn1,cn2)
            motor_left.forward(ret1)
            if time.perf_counter() - t >= 1:
                t = time.perf_counter()
                print(f"l {cn1:8d} r {cn2:8d} {cn1-cn2:8d} {ret1:.2f}")
            time.sleep(0.05)

    except KeyboardInterrupt:
        motor_left.stop()
        motor_right.stop()
        print("user stop")
