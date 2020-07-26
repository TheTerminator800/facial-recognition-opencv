import cv2
import pickle

#get labels in .pkl file saved in face_train.py
labels = {}
with open("labels.pkl", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()} #invert the dictionary so that key is value (0 or 1) and value is key (aryan, ansh)
#labels: keys = id_ (0,1); values = aryan or ansh

#define the cascade that finds faces
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

#initialize recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

#load training
recognizer.read("trainer.yml")

cap = cv2.VideoCapture(0)

while True:
    #capture frame-by-frame
    ret, frame = cap.read()

    #convert frames to grayscale so classifier works (see documentation)
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #flip horizontally (experimentation)
    flipped = cv2.flip(grayscale, 1)

    #find faces in frame (detectMultiScale returns list of rectangles where face found)
    faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.5, minNeighbors=4)

    #iterate over rectangles returned by faces
    for (x, y, w, h) in faces:

        #region of interest (isolate the rectangle in the image with my face)
        roi_color = frame[y:y+h, x:x+w]
        roi_gray = grayscale[y:y+h, x:x+w]

        #predict the face's ID (id_) and (loss): the lower the better   --> try scikit-learn
        id_, loss = recognizer.predict(roi_gray)

        font = cv2.FONT_HERSHEY_COMPLEX
        name = labels[id_]
        color = (0, 255, 0) #BGR
        stroke = 2
        cv2.putText(frame, name, (x,y), font, 1, color, thickness=stroke, lineType=cv2.LINE_AA)

        #save the region of interest as an image
        cv2.imwrite("color_face.png", roi_color)

        #draw a rectangle surrounding face
        rec_color = (0, 0, 255) #BGR
        rec_stroke = 2 #thickness
        cv2.rectangle(frame, (x, y), (x+w, y+h), rec_color, rec_stroke)

    #display resulting frame
    cv2.imshow('Live Security Feed', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#when everything is done, release the capture (end)
cap.release()
cv2.destroyAllWindows()
