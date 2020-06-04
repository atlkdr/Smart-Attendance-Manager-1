# Module For Encoding images of Face_Data to be stored and used from Pickle
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import pickle



def store_encoded_faces():
    encoded = {}
    for dirpath,dnames,fnames in os.walk("./Face_Data"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("Face_Data/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    pickle_out=open("encodings.pickle","wb")
    pickle.dump(encoded,pickle_out)
    pickle_out.close()


store_encoded_faces()