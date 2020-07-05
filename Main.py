import face_recognition
import cv2
import os
import smtplib
from email.message import EmailMessage
import imghdr 
import datetime
EMAIL_ADDDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
Time = datetime.datetime.now()
KNOWN_FACE_DIR = "Known_faces"
Known_faces_encoding = []
Known_names = []
cap = cv2.VideoCapture(0)
print("process Known Process!")
for name in os.listdir(KNOWN_FACE_DIR):
    for filename in os.listdir(f"{KNOWN_FACE_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACE_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        Known_faces_encoding.append(encoding)
        Known_names.append(name)
print("Recognizing Faces...")
while True:
    ret, frame = cap.read()
    face_location = face_recognition.face_locations(frame)
    face_encoding = face_recognition.face_encodings(frame, face_location)
    for(top, right, bottom, left), face_encodings in zip(face_location, face_encoding):
        result = face_recognition.compare_faces(Known_faces_encoding, face_encodings, tolerance=0.6)
        name = "Unknown"
        if True in result:
            name = Known_names[result.index(True)]
        print(name)
        cv2.rectangle(frame, (left, top), (right, bottom), (0,0,0), 2)
        cv2.rectangle(frame, (left, bottom + 20), (right, bottom), (0,0,0), cv2.FILLED)
        cv2.putText(frame, name, (left, bottom + 18), cv2.FONT_ITALIC, 0.7, (255,255,255), 1)
    cv2.imshow("Frame", frame)
    if name == "Unknown":
        cv2.imwrite("unknown.png",frame)
        msg = EmailMessage()
        msg['Subject'] = "Security Alert!!"
        msg['From'] = EMAIL_ADDDRESS
        msg['To'] = "prkapadnis2001@gmail.com"
        msg.set_content(f"Hey someone is entered in your house at {Time} \n\n Image Attached")
        with open("unknown.png", 'rb') as img:
            file_name = img.name
            file_data = img.read()
            file_type = imghdr.what(file_name)
        msg.add_attachment(file_data, filename = file_name, maintype = 'Image', subtype = file_type)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Send!")
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()