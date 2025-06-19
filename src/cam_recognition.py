from dataclasses import dataclass

import face_recognition
import cv2
import numpy as np


@dataclass
class Face:
    id: int
    face_encoding: np.array


class CamRecognition:
    def __init__(self, video_capture, known_ids=None, known_face_encodings=None):
        self.video_capture = video_capture
        self.face_locations = []
        self.known_faces = []
        self.ids = []
        self.face_encodings = []
        self.process_this_frame = True

        for id, face_encoding, face_name in zip(known_ids, known_face_encodings):
            self.known_faces.append(Face(id, face_encoding))


    def add_encoding(self, id, face_encoding):
        self.known_faces.append(Face(id, face_encoding))


    def delete_encoding(self, to_delete_id):
        for face in self.known_faces:
            if face.id == to_delete_id:
                self.known_faces.remove(face)
                break


    def update_encoding(self, to_change_id, new_face_encoding):
        for face in self.known_faces:
            if face.id == to_change_id:
                face.face_encoding = new_face_encoding
                break


    def send_frame(self):
        ...


    def frame_recognition(self):
        ret, frame = self.video_capture.read()

        if self.process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)

            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                self.ids = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces([face.face_encoding for face in self.known_faces], face_encoding)
                    id = -1

                    # Use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance([face.face_encoding for face in self.known_faces], face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        id = self.known_faces[best_match_index].id

                    self.ids.append(id)

                    #TODO: необходимо сделать некоторую паузу после распознания лица или на бэк части не выводить одного и того же человека

        self.process_this_frame = not self.process_this_frame