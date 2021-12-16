from multiprocessing import Queue

import face_recognition
import datetime


def scan_faces(detected_faces: Queue, frames_queue: Queue, logger):
    logger.info('started scanning faces')
    while True:
        frame_number, frame, date = frames_queue.get()  # block until get frame from camera
        start = datetime.datetime.now()
        face_metrics, face_location = detect_face(frame)
        end = datetime.datetime.now()
        if face_metrics is not None:
            logger.debug('{}: detected face from {}. Diff {}s, recognition {}s'
                         .format(datetime.datetime.now(), date,
                                 datetime.datetime.now().second - date.second, end.second - start.second))
            detected_faces.put((frame_number, frame, face_metrics, face_location))


def detect_face(frame):
    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) != 1:
        return None, None
    encodings = face_recognition.face_encodings(frame, known_face_locations=face_locations)
    if len(encodings) != 1:
        return None, None
    return encodings[0], face_locations[0]
