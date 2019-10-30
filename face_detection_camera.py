import argparse

from picamera import PiCamera

from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection
from aiy.vision.annotator import Annotator
from aiy.leds import Leds, Color
from aiy.toneplayer import TonePlayer

LEFT_COLOR = (204, 0, 255)
LOAD_SOUND = ('G5e', 'f5e', 'd5e', 'A5e', 'g5e', 'E5e', 'g5e', 'C6e')
BUZZER_GPIO = 22


def avg_joy_score(faces):
    if faces:
        return sum(face.joy_score for face in faces) / len(faces)
    return 0.0

def main():
    """Face detection camera inference example."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_frames', '-n', type=int, dest='num_frames', default=None,
        help='Sets the number of frames to run for, otherwise runs forever.')
    args = parser.parse_args()

    # Forced sensor mode, 1640x1232, full FoV. See:
    # https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
    # This is the resolution inference run on.
    with PiCamera(sensor_mode=4, resolution=(1640, 1232), framerate=30) as camera,\
                        Leds() as leds:
        leds.update(Leds.privacy_on())
        leds.update(Leds.rgb_on(Color.BLUE))
        camera.start_preview()
        tone_player = TonePlayer(BUZZER_GPIO, bpm=70)
        tone_player.play(*LOAD_SOUND)


        # Annotator renders in software so use a smaller size and scale results
        # for increased performace.
        annotator = Annotator(camera, dimensions=(320, 240))
        scale_x = 320 / 1640
        scale_y = 240 / 1232

        w_last = 0

        # Incoming boxes are of the form (x, y, width, height). Scale and
        # transform to the form (x1, y1, x2, y2).
        def transform(bounding_box):
            x, y, width, height = bounding_box
            return (scale_x * x, scale_y * y, scale_x * (x + width),
                    scale_y * (y + height))

        with CameraInference(face_detection.model()) as inference:
            for result in inference.run(args.num_frames):
                faces = face_detection.get_faces(result)
                annotator.clear()
                for face in faces:
                    #annotator.bounding_box(transform(face.bounding_box), fill=0)
                    annotator.bounding_box(face.bounding_box, fill=0)
                    x, y, width, height = face.bounding_box

                annotator.update()


                if len(faces) >= 1:
                    print('#%05d (%5.2f fps): num_faces=%d, avg_joy_score=%.2f, x=%.2f, y=%.2f, width=%.2f, height=%.2f' %
                        (inference.count, inference.rate, len(faces), avg_joy_score(faces), x, y, width, height))
                    #camera.annotate_text = '%d' % x
                    alpha = (x+.01)/1200
                    leds.update(Leds.rgb_on(Color.blend(LEFT_COLOR, Color.GREEN, alpha)))

                    if w_last > width:
                        camera.annotate_text = 'Further'
                    elif w_last < width:
                        camera.annotate_text = 'Closer'
                    else:
                        camera.annotate_text ='Same'

                    #camera.annotate_text = 'Last Width: %d, Current Width: %d' % (w_last, width)
                    w_last = width


                else:
                    print('#%05d (%5.2f fps): num_faces=%d, avg_joy_score=%.2f' %
                        (inference.count, inference.rate, len(faces), avg_joy_score(faces)))

        camera.stop_preview()


if __name__ == '__main__':
    main()
