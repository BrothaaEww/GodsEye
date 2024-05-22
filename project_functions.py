import sys
sys.path.append('C:/Users/Soumyajit/AppData/Local/Programs/Python/Python310/Lib/site-packages')

import face_recognition
import cv2
import numpy as np
import csv
import glob
import os
from datetime import datetime
import pickle
import PySimpleGUI as sg
import time

sg.theme("DarkAmber")


def add_user(name):
	user_image = face_recognition.load_image_file("F:/Coding/Python_VS_Code/GodsEye/photos/"+name.replace(" ","_")+".jpg")
	user_encoding = face_recognition.face_encodings(user_image)[0]
	try :
		with open("F:/Coding/Python_VS_Code/GodsEye/cache/known_face_encoding.pki","rb") as fp:
			known_face_encoding = pickle.load(fp)
	except :
		known_face_encoding = []	
	known_face_encoding.append(user_encoding)
	with open("F:/Coding/Python_VS_Code/GodsEye/cache/known_face_encoding.pki","wb") as fp:
		pickle.dump(known_face_encoding,fp)

	try :
		with open("F:/Coding/Python_VS_Code/GodsEye/cache/known_faces_names.pki","rb") as fp:
			known_faces_names = pickle.load(fp)
	except :
		known_faces_names = []
	known_faces_names.append(name)
	with open("F:/Coding/Python_VS_Code/GodsEye/cache/known_faces_names.pki","wb") as fp:
		pickle.dump(known_faces_names,fp)

def give_attendance():
	video_capture = cv2.VideoCapture(0)

	try :
		with open("F:/Coding/Python_VS_Code/GodsEye/cache/known_face_encoding.pki","rb") as fp:
			known_face_encoding = pickle.load(fp)
	except :
		known_face_encoding = []
	try :
		with open("F:/Coding/Python_VS_Code/GodsEye/cache/known_faces_names.pki","rb") as fp:
			known_faces_names = pickle.load(fp)
	except :
		known_faces_names = []

	users = known_faces_names.copy()

	face_locations = []
	face_encodings = []
	face_names = []
	exit = False
	s =  True

	now = datetime.now()
	current_date = now.strftime("%Y-%m-%d")

	if not os.path.isfile('F:/Coding/Python_VS_Code/GodsEye/logs/'+current_date+'.csv') :
		f = open('F:/Coding/Python_VS_Code/GodsEye/logs/'+current_date+'.csv','w+')
		lnwriter = csv.writer(f)
		lnwriter.writerow(['Name','Time'])

	f = open('F:/Coding/Python_VS_Code/GodsEye/logs/'+current_date+'.csv','a+',newline='')
	lnwriter = csv.writer(f)

	sg.popup("Make sure your camera is not covered!")
	while True:
		_,frame = video_capture.read()
		small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
		rgb_small_frame = np.ascontiguousarray(frame[:, :, ::-1]);time.sleep(10)
		if s:
			face_locations = face_recognition.face_locations(rgb_small_frame)
			face_encodings = face_recognition.face_encodings(rgb_small_frame)
			face_names = []
			for face_encoding in face_encodings:
				matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
				name = ""
				face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
				best_match_index = np.argmin(face_distance) if len(face_distance) > 0 else print('The face_distance array is empty. Cannot calculate argmin.')
				print(face_distance)
				print(best_match_index)
				if face_distance[best_match_index] < 0.5 :
					if matches[best_match_index]:
						name = known_faces_names[best_match_index]

					face_names.append(name)
					if name in known_faces_names:
						if name in users:
							users.remove(name)
							sg.popup("Face Identified : "+name)
							current_time = now.strftime("%H:%M:%S")
							lnwriter.writerow([name,current_time])
							exit = True
							break
				else : 
					sg.popup("Face Not Identified!")
		cv2.imshow("Attendance System",frame)
		if exit :
			break
		elif cv2.waitKey(1) & 0xFF == ord('q'):
			break
	video_capture.release()
	cv2.destroyAllWindows()
	f.close()
