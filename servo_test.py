from gpiozero import AngularServo, Servo
from aiy.pins import PIN_A
from time import sleep


def main():


    myCorrectionMin=0.3
    myCorrectionMax=0.275
    maxPW=(2.0+myCorrectionMax)/1000
    minPW=(1.0-myCorrectionMin)/1000

    servo = Servo(PIN_A,min_pulse_width=minPW,max_pulse_width=maxPW)
    #servo = Servo(PIN_A)
    i = 0
    while i in range(0,3):
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
        servo.mid()
        i+=1

if __name__ == '__main__':
    main()
