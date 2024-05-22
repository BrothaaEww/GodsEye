import sys
sys.path.append('C:/Users/Soumyajit/AppData/Local/Programs/Python/Python310/Lib/site-packages')

import os
import shutil
import PySimpleGUI as sg
import pickle
import project_functions as pf
import numpy as np

sg.theme("DarkAmber")
while True:
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

	#MAIN WINDOW
	event , values = sg.Window("Attendance System",font=("Times New Roman",16), size=(400,400), 
		layout=[[sg.Button("Add User",p=(10,50),size=(15,3))],[sg.Button("Give Attendance",p=(10,50),size=(15,3))]],
		element_justification="center").read(close=True)

	if event == sg.WIN_CLOSED:
		sg.popup("Goodbye!")
		break
	elif event == "Add User" :
		while True:
			#ADD STUDENT WINDOW
			inner_event, inner_values = sg.Window("Add User",font=("Times New Roman",16), size=(800,300), margins=(0,50),
				layout=[[sg.T("Name : ",pad=(0,10)),sg.In(key="name",pad=(0,10))],[sg.T("Image : ",pad=(0,10)),sg.T("",pad=(0,10)),sg.FileBrowse(key="Path",pad=(0,10))],[sg.Button("Submit",size=(10,0))]],
				element_justification="center").read(close=True)
			if inner_event == sg.WIN_CLOSED:
				sg.Window("Add User").close()
				break
			if inner_values["name"]=="":
				sg.popup("Please enter your name!")
				continue
			elif inner_values["name"] in known_faces_names:
				sg.popup("Name already exists! Please enter a different name!")
				continue
			if inner_values["Path"]=="":
				sg.popup("Please choose an image!")
				continue
			if not inner_values["name"]=="" and not inner_values["Path"]=="":		
				if inner_event == "Submit" :
					sg.Window("Add User").close()
					last_index = len(inner_values['Path']) - inner_values['Path'][::-1].index("/") -1 
					src_path = inner_values['Path'][:last_index]
					src_file_name = inner_values['Path'][last_index+1:]
					shutil.copy(inner_values['Path'],"photos/"+inner_values["name"].replace(" ","_")+".jpg")
					pf.add_user(inner_values["name"])
					break
	elif event == "Give Attendance" :
		pf.give_attendance()
