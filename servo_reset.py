from gpiozero import AngularServo, Servo
from aiy.pins import PIN_A
from time import sleep


def main():

    servo = Servo(PIN_A)
    servo.mid()


if __name__ == '__main__':
    main()
