import argparse

from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection
from aiy.vision.annotator import Annotator
from picamera import PiCamera

from gpiozero import Servo
from aiy.pins import PIN_A
