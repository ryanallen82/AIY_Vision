import argparse

from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection
from examples.vision.annotator import Annotator
from picamera import PiCamera

from gpiozero import Servo
from aiy.vision.pins import PIN_A

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--num_frames',
        '-n',
        type=int,
        dest='num_frames',
        default=-1,
        help='Sets the number of frames to run for, otherwise runs forever.')
    args = parser.parse_args()

    with PiCamera() as camera:
        camera.sensor_mode = 4
        camera.resolution = (1640, 1232)
        camera.framerate = 30
        camera.start_preview()
        servo = Servo(PIN_A, min_pulse_width=.0005, max_pulse_width=.0019)
        servo.mid()
        position = 0

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

                if faces:
                    face = faces[0]
                    x, y, width, height = face.bounding_box
                    print('             : Face is at %d' % x)
                    if x < 300:
                       print('             : Face left of center')
                       position = position + 0.1
                       if position > 1:
                           position = 0.99
                    elif x > 500:
                       print('             : Face right of center')
                       position = position - 0.1
                       if position < -1:
                           position = -0.99
                    else:
                       print('             : Face in CENTER of image')
                       positon = position

                    servo.value = position

                else:
                    servo.mid()
                    position = 0

        camera.stop_preview()

if __name__ == '__main__':
    main()
