from gpiozero import Servo
from aiy.pins import PIN_A


def main():

    #with PiCamera() as camera:
    servo = Servo(PIN_A, min_pulse_width=.0001, max_pulse_width=.00025)
    servo.mid()
    #camera.start_preview()
    servo.value = 1
    servo.mid()

if __name__ == '__main__':
    main()
