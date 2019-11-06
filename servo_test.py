from gpiozero import AngularServo
from aiy.pins import PIN_A
import time


def main():


    myCorrection=0.45
    maxPW=(2.0+myCorrection)/1000
    minPW=(1.0-myCorrection)/1000

    servo = Servo(PIN_A,min_pulse_width=minPW,max_pulse_width=maxPW)

    while True:
        servo.mid()
        print("mid")
        sleep(0.5)
        servo.min()
        print("min")
        sleep(1)
        servo.mid()
        print("mid")
        sleep(0.5)
        servo.max()
        print("max")
        sleep(1)

if __name__ == '__main__':
    main()
