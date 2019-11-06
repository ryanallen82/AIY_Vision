import argparse

from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection
from aiy.vision.annotator import Annotator
from picamera import PiCamera

from gpiozero import Servo, AngularServo
from aiy.pins import PIN_A

from math import atan2, ceil
from time import sleep

def main():

    def face_data(face):
        x, y, width, height = face.bounding_box
        x_mean = int(x + width/2)
        angle = atan2(x_mean - x_center,focal_length)
        distance = 0
        if width > 0:
            distance = focal_length * real_face_width_inch / width
        return angle, distance

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--num_frames',
        '-n',
        type=int,
        dest='num_frames',
        default=-1,
        help='Sets the number of frames to run for, otherwise runs forever.')
    args = parser.parse_args()

    focal_length = 1320                             # focal length in pixels for 1640 x 1232 resolution - found by calibration
    camera_resolution = (1640, 1232)
    x_center = int(camera_resolution[0] / 2)
    real_face_width_inch = 11                       # width/height of bounding box of human face in inches
    min_angle = atan2(-x_center,focal_length)       # min angle where face can be detected (leftmost area) in radians
    max_angle = atan2(x_center,focal_length)
    face_detected_on_prev_frame = False

    with PiCamera(sensor_mode=4, resolution=(1640, 1232), framerate=30) as camera:
        myCorrectionMin=0.3
        myCorrectionMax=0.275
        maxPW=(2.0+myCorrectionMax)/1000
        minPW=(1.0-myCorrectionMin)/1000
        camera.start_preview()
        #servo = AngularServo(PIN_A, min_pulse_width=minPW, max_pulse_width=maxPW)
        servo = AngularServo(PIN_A, max_pulse_width = maxPW)
        servo.max()
        sleep(1)
        servo.min()
        sleep(1)
        servo.mid()


        annotator = Annotator(camera, dimensions=(320, 240))
        scale_x = 320 / 1640
        scale_y = 240 / 1232

        def transform(bounding_box):
            x, y, width, height = bounding_box
            return (scale_x * x, scale_y * y, scale_x * (x + width),
                    scale_y * (y + height))

        with CameraInference(face_detection.model()) as inference:
            for i, result in enumerate(inference.run()):
                if i == args.num_frames:
                    break
                faces = face_detection.get_faces(result)
                annotator.clear()
                for face in faces:
                    annotator.bounding_box(transform(face.bounding_box), fill=0)
                annotator.update()
                print('Iteration #%d: num_faces=%d' % (i, len(faces)))
                previous_angle = 0
                if faces:
                    if face_detected_on_prev_frame:
                        angle, distance = face_data(face)
                        #if angle < min_angle:
                        #    angle = min_angle
                        #if angle > max_angle:
                        #    angle = max_angle
                        servo.angle = angle*(-100)
                        previous_angle = angle*(-100)
                        print('Angle:' + str(angle))
                        sleep(.5)
                    face_detected_on_prev_frame = True
                else:
                    if not face_detected_on_prev_frame:
                        servo.angle = previous_angle
                        sleep(.5)
                        pass
                    face_detected_on_prev_frame = False
        camera.stop_preview()

if __name__ == '__main__':
    main()
