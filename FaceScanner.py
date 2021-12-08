from multiprocessing import Queue

import face_recognition
import datetime


def scan_faces(detected_faces: Queue, frames_queue: Queue, logger):
    logger.info('started scanning faces')
    while True:
        frame_number, frame, date = frames_queue.get()  # block until get frame from camera
        start = datetime.datetime.now()
        face_metrics = detect_face(frame)
        end = datetime.datetime.now()
        if face_metrics is not None:
            logger.debug('{}: detected face from {}. Diff {}s, recognition {}s'.format(datetime.datetime.now(), date, datetime.datetime.now().second - date.second, end.second - start.second))
            detected_faces.put((frame_number, frame, face_metrics))


def detect_face(frame):
    encodings = face_recognition.face_encodings(frame)
    if len(encodings) != 1:
        return None
    return encodings[0]
