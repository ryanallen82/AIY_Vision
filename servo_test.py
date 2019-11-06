from gpiozero import AngularServo
from aiy.pins import PIN_A
import time


def main():

    #with PiCamera() as camera:
    servo = AngularServo(PIN_A, initial_angle=0, min_angle=-90, max_angle=90)
    servo.angle = 0
    time.sleep(2)
    servo.angle = -90
    time.sleep(2)
    servo.angle = 0
    time.sleep(2)
    servo.angle = 90
    time.sleep(2)
    servo.angle = 0

if __name__ == '__main__':
    main()
