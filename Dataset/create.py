# Updating dataset to req condition
import numpy as np
import cv2
import matplotlib.pyplot as plt

# video to list of frames
def split_into_frames(vid):
    frames = []
    while(True):
        ret, frame = vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
        else:
            break
    return frames

# Croping faces and reducing frames
def crop_faces(clip):
    frames = split_into_frames(clip)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    crop_face = []
    try:
        # Detecting face, croping and resizing to 150*150*3
        for i in range(len(frames)):
            faces = face_cascade.detectMultiScale(frames[i], 1.1, 10)
            x, y, w, h = faces[0]   # Face start and End
            crop_face.append(cv2.resize(frames[i][y:y+h, x:x+w], (150, 150)))
    except:
        pass                    
    # converting list of array to array
    crop_face = np.stack(crop_face, axis=0)
    return crop_face



