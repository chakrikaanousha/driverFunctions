import argparse
import sys
import time
import cv2

import sys
sys.path.append('/home/rasp/myenv/lib/python3.11/site-packages')
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

def run(model: str, camera_id: int, width: int,hieght: int, num_threads: int, enable_edgetpu: bool) -> None:
    counter, fps = 0,0
    start_time = time.time()

    #cap=cv2.VideoCapture(camera_id)
    cap=cv2.VideoCapture('/home/rasp/myenv/tfliterpipothole-main/pothole1.mp4')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    row_size=20
    left_margin=24
    text_color=(0,0,225)
    font_size=1
    font_thickness=1
    fps_avg_frame_count=10

    base_options=core.Baseoptions(
        file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options=processor.DetectionOptions(
        max_results=3, score_threshold=0.3)
    options=vision.ObjectDetectorOptions(
        base_options=base_options,detction_options=detection_options)
    detector=vision.ObjectDetector.create_from_options(options)

    while cap.isOpened():
        success, image=cap.read()
        if not sucess:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
                )
            counter += 1
                      image=cv2.flip(image, 1)
            image=cv2.resize(image,(640,480))

            rgb_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

            input_tensor=vision.TensorImage.create_from_array(rgb_image)

            detection_result=detector.detect(input_tensor)

            image=utils.visualize(image,detection_result)

            if counter % fps_avg_frame_count == 0:
                end_time = time.time()
                fps=fps_avg_frame_count / (end_time - start_time)
                start_time= time.time()

            fps_text= 'FPS = {:.1f}'.format(fps)
            text_location=(left_margin,row_size)
            cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, font_size, text_color, fonr_thickness)

            if cv2.waitKey(1) ==27:
                break
            cv2.imshow('object_detector',image)

            cap.release()
            cv2.destroyAllWindows()
def main():
    parser=argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path of the object detection model.',
        required=False,
        # Main model with camera
        # default='efficient+lite0.tflite')
        # Without camera
        default='model.tflite')

    parser.add_argument(
        '--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=640)
