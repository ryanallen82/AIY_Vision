from gpiozero import Servo
from aiy.pins import PIN_A
import time


def main():

    #with PiCamera() as camera:
    servo = Servo(PIN_A)
    servo.mid()
    time.sleep(2)
    servo.min()
    time.sleep(2)
    servo.mid()
    time.sleep(2)
    servo.max()
    time.sleep(2)
    servo.mid()

if __name__ == '__main__':
    main()
