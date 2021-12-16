from multiprocessing import Queue

import cv2.cv2
import numpy as np
import datetime
from time import sleep


# обработка видеопотока с камеры
def read_stream_from_camera(src, frames_queue: Queue, max_frames_queue_size, logger):
    camera_reader = CameraReader(src, logger)
    frame_number = np.ulonglong(0)
    while True:
        frame = camera_reader.read_frame()
        if frames_queue.qsize() < max_frames_queue_size:
            frames_queue.put((frame_number, frame, datetime.datetime.now()))
            frame_number += 1


class CameraReader:
    # подключение к камере
    def __init__(self, src, logger):
        self.logger = logger
        self.logger.info('connecting to camera...')
        while True:
            try:
                self.video_stream = cv2.cv2.VideoCapture(src)
                break
            except Exception as e:
                self.logger.error(e)
                self.logger.info('will try to reconnect after 5s')
                sleep(5)
        self.logger.info('connected to camera successfully')

    # считывание одного кадра
    def read_frame(self):
        ret, frame = self.video_stream.read()
        cv2.cv2.imshow('frame', frame)
        cv2.cv2.waitKey(1)
        rgb_image = cv2.cv2.cvtColor(frame, cv2.cv2.COLOR_BGR2RGB)
        return rgb_image
