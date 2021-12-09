import cv2.cv2
import numpy as np
import face_recognition
import PrinterManager
import bisect

from DatabaseManager import DatabaseManager

candidates = []
candidates_frames = []
database_manager = DatabaseManager()


def process_faces(detected_faces, min_frames_count, max_frames_distance, print_tickets, enqueue_events, logger):
    logger.info('started processing faces')
    while True:
        frame_number, frame, face_metrics = detected_faces.get(True)  # block until some face was recognized
        logger.debug('got detected face')
        matches: list = face_recognition.compare_faces(candidates, face_metrics)
        matches_count = matches.count(True)
        if matches_count == 1:
            match = matches.index(True)
            bisect.insort(candidates_frames[match], frame_number)
            if is_enough_frames(candidates_frames[match], min_frames_count, max_frames_distance):
                logger.debug('found new candidate')
                added, person_id, ticket_number = enqueue(face_metrics, logger)
                if added:
                    logger.info(f'added new person to the queue: person_id={person_id}, ticket_number={ticket_number}')
                    enqueue_events.put(ticket_number)
                    if print_tickets:
                        PrinterManager.print_ticket_number(ticket_number)
                    else:
                        bgr_image = cv2.cv2.cvtColor(frame, cv2.cv2.COLOR_RGB2BGR)
                        cv2.cv2.imshow(str(ticket_number), bgr_image)
                else:
                    logger.debug(f'repeating person was not added: person_id={person_id}, ticket_number={ticket_number}')
        elif matches_count == 0:
            candidates.append(face_metrics)
            candidates_frames.append([frame_number])
        clear_old_candidates_frames(max_frames_distance)
        print(candidates_frames)
        if not print_tickets:
            cv2.cv2.waitKey(1)


def enqueue(face_metrics, logger):
    queue_contents = database_manager.select_all()
    queue_metrics = [np.fromstring(row[1][1:-1], sep=' ') for row in queue_contents]
    matches: list = face_recognition.compare_faces(queue_metrics, face_metrics)
    if matches.count(True) > 0:
        match = matches.index(True)
        logger.debug(f'found match in db: person_id={queue_contents[match][0]}')
        if queue_contents[match][2] is not None:  # avoid repeating person in queue
            return False, queue_contents[match][0], queue_contents[match][2]  # id and number of ticket of that person
        else:
            # person found in db, but not in queue
            ticket_number = database_manager.enqueue_by_id(queue_contents[match][0])
            return True, queue_contents[match][0], ticket_number
    # if person was not found in db, add new person
    logger.debug('did not find match in db')
    person_id, ticket_number = database_manager.enqueue_by_metrics(np.array2string(face_metrics))
    return True, person_id, ticket_number


def is_enough_frames(frames, min_count, max_distance):
    if len(frames) < min_count:
        return False
    return frames[-1] - frames[0] < max_distance


def clear_old_candidates_frames(max_distance):
    global candidates_frames
    cleared_candidates_frames = []
    for i in range(len(candidates_frames)):
        cleared_frames = clear_old_frames(candidates_frames[i], max_distance)
        if len(cleared_frames) == 0:
            candidates.pop(i)
        else:
            cleared_candidates_frames.append(cleared_frames)
    candidates_frames = cleared_candidates_frames


def clear_old_frames(frames, max_distance):
    max_frame = frames[-1]
    return [x for x in frames if max_frame - max_distance < x]
