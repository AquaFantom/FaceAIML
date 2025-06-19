import face_recognition
import cv2
import numpy as np



class CamRecognition:
    def __init__(self, video_capture, known_ids, known_face_encodings, known_face_names):
        self.video_capture = video_capture
        self.known_ids = known_ids
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names
        self.face_locations = []
        self.ids = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True


    def add_encoding(self, id, face_encoding, face_name):
        self.known_ids.append(id)
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(face_name)


    def delete_encoding(self, to_delete_id):
        index = self.known_ids.index(to_delete_id)
        self.known_ids.pop(index)
        self.known_face_names.pop(index)
        self.known_face_encodings.pop(index)


    def update_encoding(self, to_change_id, new_face_encoding, new_face_name):
        index = self.known_ids.index(to_change_id)
        self.known_face_encodings[index] = new_face_encoding
        self.known_face_names[index] = new_face_name


    def send_frame(self):
        ...


    #TODO: возможно, стоит избавиться от переменной face_names за ненадобностью - куда лучше будет записывать id и их отправлять бэку
    def frame_recognition(self):
        ret, frame = self.video_capture.read()

        if self.process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            self.ids = []
            self.face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                id = -1
                name = "Unknown"

                # Use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    id = self.known_ids[best_match_index]
                    name = self.known_face_names[best_match_index]

                self.ids.append(id)
                self.face_names.append(name)

                #TODO: необходимо сделать некоторую паузу после распознания лица или на бэк части не выводить одного и того же человека

        self.process_this_frame = not self.process_this_frame