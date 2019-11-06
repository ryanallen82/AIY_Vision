from gpiozero import Servo
from aiy.pins import PIN_A


def main():
    servo = Servo(PIN_A, min_pulse_width=.0001, max_pulse_width=.00025)
    servo.mid()
