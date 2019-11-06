from gpiozero import AngularServo
from aiy.pins import PIN_A
import time


def main():

    myCorrection=0.45
    maxPW=(2.0+myCorrection)/1000
    minPW=(1.0-myCorrection)/1000

    servo = AngularServo(PIN_A, initial_angle=0, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW)
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
