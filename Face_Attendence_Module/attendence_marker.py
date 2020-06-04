import pickle
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import sys
from time import sleep




def get_attendence(im):
    # Faces = Dictionary containing key = Roll Id value = Encoding of that face 
    pickle_in=open("encodings.pickle","rb")
    faces = pickle.load(pickle_in) # Get from pickle (Done by Encoder)
    pickle_in.close()
    faces_encoded = list(faces.values())
    known_face_roll = list(faces.keys())
    img = cv2.imread(im,1)
    # Detect all faces (+locations) in the image
    face_locations = face_recognition.face_locations(img)
    # Get the encodings of each face detected
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)
    # Present Students roll number
    face_id = []
    for face_encoding in unknown_face_encodings:
        # See for match
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown" # = Default
        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_roll[best_match_index]

        face_id.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_id):
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)
            cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)

    while True:

        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_id 


def update_attendence(attendence_file,mark):
    atten_file=open(attendence_file,"r")
    lines=atten_file.readlines()  
    lines=[line.strip() for line in lines]
    total_attendece=int(lines[0])
    lines=lines[1:]
    record={}
    for l in lines:
        temp=l.split(",")
        record[temp[0]]=int(temp[1])
    for key in mark:
        if key not in record:
            record[key]=0
        record[key]+=1
    write_file=open(attendence_file,"w")
    written=False
    write_file.write(str(total_attendece+1)+"\n")
    for key in record:
        if(written):
            write_file.write("\n")
        written=True
        string=str(key)+","+str(record[key])
        write_file.write(string)
    write_file.close()




if __name__ == "__main__":
    if(len(sys.argv)<2):
        print("Please Provide the image to mark attendence as argument")
    else:
        detected=get_attendence(sys.argv[1])
        print("Detected Rolls:",detected)
        print("Marking Attendence")
        update_attendence("Attendence_Data/attendence.txt",detected)
else:
    print("Bohot Shane ban rahe ho!, import se run karoge")
