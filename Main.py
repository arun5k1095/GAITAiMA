from multiprocessing import Queue
from threading import*
import re
import json,requests
from PIL import Image, ImageQt
import urllib.request
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtWidgets import QApplication,QWidget,QSplashScreen,\
    QStackedLayout,QFrame,QFormLayout,QLineEdit,QPushButton,QLabel,QComboBox,QDateEdit,QMessageBox,QErrorMessage,\
    QMainWindow,QMenuBar,QGridLayout,QFileDialog,QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import Qt,QTimer
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPixmap
from qtwidgets import PasswordEdit
from FaultCodes import FaultCodes
import os
import sys
import time

import requests
import urllib.request
import time
import webbrowser
from datetime import datetime
import Resources

import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import pprint


PARAMETERS_DICT = {

    'Step_length' : [0] ,
    'SST_Right' : 0,
    'SST_Left' : 0,
    'DST' : 0,
    'STANCE' : 0,
    'SWING': 0,
    'L_Velocity' : [0],
    'R_Velocity' : [0],
    'CADENCE': 0,
    'Lstep_duration':[] ,
    'Rstep_duration' :[] ,
    'Lstride_duration':[] ,
    'Rstride_duration': [],
    'Lstride_length': [],
    'Rstride_length':[]

}



def GET_ALL_PARAMETERS(VideoFilepath):

    global PARAMETERS_DICT , VideoFeedFrame
    PARAMETERS_DICT["Step_length"] = [0]
    PARAMETERS_DICT["R_Velocity"] = [0]
    ClearPatientGraphs()

    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose(enable_segmentation=True,model_complexity=2)
    cap = cv2.VideoCapture(VideoFilepath)

    filename = VideoFilepath.split('/')[-1]

    # 185cms is the person height, 10cms is the height from eye to tip of head 
    PERSON_HEIGHT = float(160)
    PERSON_HEIGHT-=10

    print('Working on : '+filename)
    print()
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count/fps
    cnt = duration/frame_count
    width = int(cap. get(cv2. CAP_PROP_FRAME_WIDTH ))
    height = int(cap. get(cv2. CAP_PROP_FRAME_HEIGHT))

    L_ANS_ARRAY = []
    R_ANS_ARRAY = []
    STEP_LENGTH_ARRAY = []

    LCOUNT=0
    RCOUNT=0

    cadence = 0
    SWING=0
    swing_count=0
    sst_right_count=0
    sst_left_count=0
    dst_count=0

    frame_number=0
    prev_frame_number=0

    step_count=0
    height_eyetofoot=0

    left_previous = 0
    right_previous = 0

    initial_left_frame = 0
    initial_right_frame = 0
    final_left_frame=0
    final_right_frame=0

    right_prev_step=0
    left_prev_step=0

    R_stride_length_incms=0
    L_stride_length_incms=0

    prev_step_frame=0

    init_pos_left_ankle = 0
    init_pos_right_ankle = 0




    while True:
        success, img = cap.read()
        frame_number+=1
        if not success:
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            h, w, c = img.shape
            rightheel = results.pose_landmarks.landmark[30]
            leftheel = results.pose_landmarks.landmark[29].x*w
            right_eye_outer =  results.pose_landmarks.landmark[6]
            left_prev_step=leftheel
            right_prev_step=rightheel.x*w
            height_eyetofoot = abs(rightheel.y-right_eye_outer.y)*h
            init_pos_left_ankle = int(leftheel)
            init_pos_right_ankle = int(rightheel.x*w)

            break


    while True:
        success, img = cap.read()
        frame_number+=1
        if not success:
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            h, w, c = img.shape
            rightheel = int(results.pose_landmarks.landmark[30].x*w)
            leftheel = int(results.pose_landmarks.landmark[29].x*w)
            step_length = abs(rightheel-leftheel)
            step_length_incms = round((step_length*PERSON_HEIGHT)/height_eyetofoot,2)
                
            RDIFF = int(rightheel-right_previous)
            LDIFF = int(leftheel-left_previous )

            #img1 = cv2.resize(img, (480, 640))
            bytesPerLine = c * w
            mpDraw.draw_landmarks(imgRGB, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            convertToQtFormat = QImage(imgRGB.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            VideoFeedFrame.setPixmap(QtGui.QPixmap.fromImage(p))
            UpdatePatientGraphs()
            VideoFeedFrame.update()



            if LDIFF<=0.5:
                sst_left_count+=1
                
            if RDIFF<=0.5:
                sst_right_count+=1

            if LDIFF<=1 and RDIFF<=1:
                dst_count+=1

            SSTRIGHT = round(sst_right_count*cnt,2)
            SSTLEFT = round(sst_left_count*cnt,2)
            DST = round(dst_count*cnt,2)
            STANCE=max(SSTRIGHT,SSTLEFT)

            PARAMETERS_DICT['SST_Right']=SSTRIGHT
            PARAMETERS_DICT['SST_Left']=SSTLEFT
            PARAMETERS_DICT['DST']=DST
            PARAMETERS_DICT['STANCE']=STANCE


            right_step_length=abs(rightheel - init_pos_right_ankle)
            right_step_length_incms = round((right_step_length*PERSON_HEIGHT)/height_eyetofoot,2)
            right_velocity = right_step_length_incms/(frame_number*duration/frame_count)
            right_velocity = round(right_velocity/100,2)

            left_step_length=abs(leftheel - init_pos_left_ankle)
            left_step_length_incms = round((left_step_length*PERSON_HEIGHT)/height_eyetofoot,2)
            left_velocity = left_step_length_incms/(frame_number*duration/frame_count)
            left_velocity = round(left_velocity/100,2)



            if LDIFF>1 or RDIFF>1:
                swing_count+=1  

            if LDIFF==0 and frame_number-initial_left_frame>10 and leftheel-left_prev_step>20:
                LCOUNT+=1
            
                LSTRIDE_DURATION = round((frame_number-initial_left_frame)*cnt,2)
                print('LSTRIDE_DURATION : '+str(LSTRIDE_DURATION)+'s',end=" && ")
                
                LSTEP_DURATION = round((frame_number-prev_step_frame)*cnt,2)
                print('LSTEP_DURATION : '+str(LSTEP_DURATION)+'s')
                
                PARAMETERS_DICT['Lstep_duration'].append(LSTEP_DURATION)
                PARAMETERS_DICT['Lstride_duration'].append(LSTRIDE_DURATION)

                prev_step_frame=frame_number

                initial_left_frame=frame_number
            
                L_stride_length = abs(leftheel-left_prev_step)    
                left_prev_step=leftheel    

                L_stride_length_incms = round((L_stride_length*PERSON_HEIGHT)/height_eyetofoot,2)
                L_ANS_ARRAY.append(L_stride_length_incms)

                PARAMETERS_DICT['Lstride_length']=L_ANS_ARRAY

                PARAMETERS_DICT['L_Velocity'].append(left_velocity)


                if step_length_incms>10:
                    STEP_LENGTH_ARRAY.append(step_length_incms)
                    PARAMETERS_DICT['Step_length']=STEP_LENGTH_ARRAY

                # print(L_stride_length_incms)
            left_previous=leftheel  

            if RDIFF==0 and frame_number-initial_right_frame>10 and rightheel-right_prev_step>20:
                RCOUNT+=1
            
                RSTRIDE_DURATION = round((frame_number-initial_right_frame)*cnt,2)
                print('RSTRIDE_DURATION : '+str(RSTRIDE_DURATION)+'s',end=" && ")

                RSTEP_DURATION = round((frame_number-prev_step_frame)*cnt,2)
                print('RSTEP_DURATION : '+str(RSTEP_DURATION)+'s')
                
                PARAMETERS_DICT['Rstride_duration'].append(RSTRIDE_DURATION)
                PARAMETERS_DICT['Rstep_duration' ].append(RSTEP_DURATION)


                prev_step_frame=frame_number

                initial_right_frame=frame_number
            
                R_stride_length = abs(rightheel-right_prev_step)
                right_prev_step=rightheel

                R_stride_length_incms = round((R_stride_length*PERSON_HEIGHT)/height_eyetofoot,2)
                R_ANS_ARRAY.append(R_stride_length_incms)

                PARAMETERS_DICT['Rstride_length']=R_ANS_ARRAY
                PARAMETERS_DICT['R_Velocity'].append(right_velocity)
                if step_length_incms>10:
                    STEP_LENGTH_ARRAY.append(step_length_incms)
                    PARAMETERS_DICT['Step_length']=STEP_LENGTH_ARRAY

                # print(R_stride_length_incms)
            right_previous=rightheel

            step_count=LCOUNT+RCOUNT


        cadence = int(((step_count)*60)/duration)
        SWING = round(swing_count*cnt,2)

        PARAMETERS_DICT['SWING']=SWING
        PARAMETERS_DICT['CADENCE']=cadence


        # cv2.putText(img, 'STEPS: ' + str(round(step_count)), (70, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 3)
        # cv2.putText(img, 'CADENCE: ' + str(cadence)+str('steps/min'), (70, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 3)
        # cv2.putText(img, 'STEP LENGTH: ' + str(step_length_incms), (70, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 3)
        # cv2.putText(img, 'L Velocity:'+ str(left_velocity)+'m/s', (570, 100), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 0), 3)   
        # cv2.putText(img, 'R Velocity:'+ str(right_velocity)+'m/s', (570, 50), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 0), 3)   
        # cv2.putText(img, 'Swing : '+str(SWING) +str('s'), (570, 150), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 0), 3)    
        # cv2.putText(img, 'SST Right : '+str(SSTRIGHT) +str('s'), (570, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 3)
        # cv2.putText(img, 'SST Left : '+str(SSTLEFT) +str('s'), (570, 250), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 3)
        # cv2.putText(img, 'DST : '+str(DST) +str('s'), (570, 350), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 3)
        # cv2.putText(img, 'STANCE : '+str(STANCE) +str('s'), (570, 300), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 3)


        # result.write(img)
        img = cv2.resize(img, (1200,600))
        #cv2.imshow("Image", img)
        cv2.waitKey(1)

    # plt.plot(STEP_LENGTH_ARRAY)
    # plt.savefig('../plots/StepLength '+filename.split('.')[0] +'.png')    
    # plt.show()

    L_AVERAGE_STRIDE_LENGTH = round(sum(L_ANS_ARRAY)/len(L_ANS_ARRAY),2)
    R_AVERAGE_STRIDE_LENGTH = round(sum(R_ANS_ARRAY)/len(R_ANS_ARRAY),2)
    AVERAGE_STEP_LENGTH = round(sum(STEP_LENGTH_ARRAY)/len(STEP_LENGTH_ARRAY),2)

    print('Duration : '+str(duration))
    # print('step_count : '+str(step_count))
    # print('cadence : '+str(cadence))
    print('L_AVERAGE_STRIDE_LENGTH : '+str(L_AVERAGE_STRIDE_LENGTH))
    print('R_AVERAGE_STRIDE_LENGTH : '+str(R_AVERAGE_STRIDE_LENGTH))
    print('AVERAGE_STEP_LENGTH : '+str(AVERAGE_STEP_LENGTH))
    # print('Left Velocity : '+str(left_velocity)+'m/s')
    # print('Right Velocity : '+str(right_velocity)+'m/s')
    # print('Swing : '+str(SWING) +' s')
    # print('SST Right : '+str(SSTRIGHT))
    # print('SST Left : '+str(SSTLEFT))
    # print('DST : '+str(DST))
    # print('STANCE : '+str(STANCE))



    pprint.pprint(PARAMETERS_DICT)


    cap.release()
    # result.release()
    cv2.destroyAllWindows()
    return PARAMETERS_DICT


def UserRegistratiion(data):
    #try:

        user_detail = open('user_detail.json')
        DatabaseData = json.load(user_detail)
        for UID in DatabaseData:
            if data["UserID"] == UID['UserID']:
                return "100"

        # check the userid contains any special characters.
        if data["UserID"].isalnum() == False:
            return "101"

        # checks the Name is empty or not
        if not data["UserName"]:
            return "102"

        # checks the Name contains any numbers or characters.
        if data["UserName"].isalpha() == False:
            return "103"

        # Validates the mail id format
        pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if not re.match(pattern, data["UserEmail"]):
            return "104"

        # validates the mail id is empty or not.
        if not data["UserEmail"]:
            return "105"

        # checks the Gender is selected or not.
        if not data["UserGender"]:
            return "106"

        # checks the valid DOB is given or not.
        day, month, year = data["UserDoB"].split('/')

        isValidDate = True
        try:
            datetime.datetime(int(year), int(month), int(day))

        except ValueError:
            isValidDate = False
        if isValidDate == False:
            return "107"

        # Validate the password is empty or not.
        if not data["UserPswd"]:
            return "108"

        # validate the password is valid or not.
        lower, upper, special, digit = 0, 0, 0, 0
        pwd = data["UserPswd"]
        if (len(pwd) >= 6):
            for i in pwd:
                for word in pwd.split():
                    if (word[0].isupper()):
                        upper += 1
                    if (i.islower()):
                        lower += 1
                    if (i.isdigit()):
                        digit += 1
                    if (i == '@' or i == '$' or i == '_' or i == '#'):
                        special += 1
        else:
            return "109"
        if not (lower >= 1 and upper >= 1 and special >= 1 and digit >= 1):
            return "110"

        if str(UserCnfPswd.text()).strip() != data["UserPswd"]:
            return "112"

        # updating the json file with details
        with open("user_detail.json", "w") as databaseFile:
            DatabaseData.append(data)
            json.dump(DatabaseData, databaseFile)
            return "000"
    #except Exception as error: return str(error)



def showUserInfo(message):
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Information)
   msgBox.setText(message)
   msgBox.setWindowTitle("Status Update")
   msgBox.setStandardButtons(QMessageBox.Ok)
   msgBox.show()
   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Ok: pass
   else: pass

if 1:
#try:
    if __name__ == "__main__":

        def Authenticate_Login():
            UserID = UserIDInput.text().upper().strip()
            UserPswd = UserPassword.text().strip()

            #if UserID == "ADMIN" and UserPswd == "admin123":
            if 1:
                Switch_Screenpage(2)
            else : error_dialog.showMessage("Invalid Credentials , Please re-try")


        Aplication = QApplication(sys.argv)
        MainWindowGUI = QWidget()
        #MainWindowGUI.setFixedSize(1600, 800)
        MainWindowGUI.setWindowTitle('Postura')
        MainWindowGUI.setStyleSheet("background-color: black;")
        MainWindowGUI.setObjectName("MainMenu");
        IconFilepath = ":/resources/AI_Volved.ico"
        MainWindowGUI.setStyleSheet("QWidget#MainMenu{background-image: url(:/resources/Wallpaper6.jpg);}");
        MainWindowGUI.setWindowIcon(QtGui.QIcon(IconFilepath))
        splash = QSplashScreen(QPixmap(':/resources/Splashscreen.jpg'))
        splash.show()
        splash.showMessage('<h1 style="color:white; font-size: 1px;font-family: "Times New Roman", Times, serif;">Loading ..</h1>',
                           Qt.AlignBottom | Qt.AlignRight)
        time.sleep(3)
        QTimer.singleShot(0, splash.close)

        def Switch_Screenpage(pageNum):
            try:
                if pageNum ==1:
                    MainWindowGUI.setStyleSheet("QWidget#MainMenu{background-image: url(:/resources/Wallpaper8.jpg);}");
                elif pageNum==0:
                    MainWindowGUI.setStyleSheet("QWidget#MainMenu{background-image: url(:/resources/Wallpaper6.jpg);}");
                elif pageNum==2:
                    MainWindowGUI.setStyleSheet\
                        ("QWidget#MainMenu{background-image: url(:/resources/Deep Sea Space.jpg);}");

                stackedLayout_MainApp.setCurrentIndex(pageNum)
            except Exception as error : print(error)

        stackedLayout_MainApp = QStackedLayout(MainWindowGUI)

        LoginPage = QFrame(MainWindowGUI)
        LoginPageLayout = QFormLayout()

        UserIDInput = QLineEdit(LoginPage)
        UserIDInput.setFixedSize(280,53)
        UserIDInput.setClearButtonEnabled(True)
        UserIDInput.setPlaceholderText("User ID")
        UserIDInput.setFont(QFont("Segoe UI ", 10, ))
        UserIDInput.setStyleSheet("QLineEdit {border: 1px solid #075691;border-radius: 5px;color: #103560 ;}""QLineEdit:focus{border: 2px solid green;}")
        UserIDInput.move(900,350)


        UserPassword = QLineEdit(LoginPage)
        UserPassword.setFixedSize(280,53)
        UserPassword.move(900, 420)
        UserPassword.setClearButtonEnabled(True)
        UserPassword.setFont(QFont("Segoe UI ", 10))
        UserPassword.setPlaceholderText("User Password")
        UserPassword.setStyleSheet("QLineEdit {border: 1px solid #075691;border-radius: 5px;color: #103560 ;}""QLineEdit:focus{border: 2px solid green;}")
        UserPassword.setEchoMode(QLineEdit.Password)


        SingInButton = QPushButton("Login",LoginPage)
        SingInButton.move(910, 550)
        SingInButton.setFixedSize(250,45)
        SingInButton.setFont(QFont("Segoe UI ", 10, ))
        SingInButton.setStyleSheet("QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691; color : white;}""QPushButton::hover"
                                 "{"
                                 "background-color : #1a85b4;"
                                 "}")

        SingInButton.pressed.connect(Authenticate_Login)

        ButtonSignINRegisterUser = QPushButton("Register User",LoginPage)
        ButtonSignINRegisterUser.move(910, 610)
        ButtonSignINRegisterUser.setFixedSize(250,45)
        ButtonSignINRegisterUser.setFont(QFont("Segoe UI ", 10, ))
        ButtonSignINRegisterUser.setStyleSheet("QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691;color : white;}""QPushButton::hover"
                                 "{"
                                 "background-color : #1a85b4;"
                                 "}")
        ButtonSignINRegisterUser.pressed.connect(lambda : Switch_Screenpage(1))



        ForgotPassword = QPushButton("Forgot Password ?", LoginPage)
        ForgotPassword.move(980, 475)
        ForgotPassword.setFixedSize(250, 45)
        ForgotPassword.setFont(QFont("Segoe UI ", 9 ))
        ForgotPassword.setStyleSheet("QPushButton{background: transparent;color : #075691}""QPushButton::hover"
                                 "{"
                                 "color : #1a85b4;"
                                 "}")


        LoggedInPage_Dr = QFrame(MainWindowGUI)
        LoggedInPage_Dr.styleSheet()

        RegistrationPage = QFrame(MainWindowGUI)
        RegistrationPage_RegForm = QFrame(RegistrationPage)
        RegistrationPage_RegForm.move(860, 350)
        RegistrationPage_RegForm.setFixedSize(800, 800)

        RegistrationPageLayout = QFormLayout(RegistrationPage_RegForm)
        RegistrationPageLayout.setHorizontalSpacing(50)

        RegistrationFormStyleSheet = "QLineEdit " \
                                     "{border: 1px solid #075691;" \
                                     "border-radius: 5px;" \
                                     "color: #103560 ;color:#075691;}"\
                                     "QLineEdit:focus" \
                                     "{border: 2px solid green;}"
        def style_RegSheet(element):
            element.setFixedSize(285, 40)
            element.setStyleSheet(RegistrationFormStyleSheet)
            element.setFont(QFont("Segoe UI ", 12, ))


        def style_RegSheetQLabel(text):
            Label = QLabel(text)
            Label.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
            Label.setStyleSheet('color:#075691')
            Label.setFont(QFont("Segoe UI ", 12 ))
            return Label

        UserID = QLineEdit()
        UserID.setClearButtonEnabled(True)
        style_RegSheet(UserID)

        RegistrationPageLayout.addRow(style_RegSheetQLabel("User ID"), UserID)
        UserName = QLineEdit()
        UserName.setClearButtonEnabled(True)
        style_RegSheet(UserName)
        RegistrationPageLayout.addRow(style_RegSheetQLabel("Full Name"), UserName)
        UserEmail = QLineEdit()
        UserEmail.setClearButtonEnabled(True)
        style_RegSheet(UserEmail)
        RegistrationPageLayout.addRow(style_RegSheetQLabel("Email ID"), UserEmail)
        UserGender = QComboBox()
        UserGender.setFont(QFont("Segoe UI ", 12))

        UserGender.setStyleSheet("QComboBox"
                                    "{""border : 1px solid #075691; color : #075691""}"
                                 "QComboBox:focus"
                                    "{" "border : 2px solid green;""}")

        UserGender.setFixedSize(285, 40)
        UserGender.setFont(QFont("Segoe UI ", 12 ))
        UserGender.addItems(["Male" ,"Female","Other"])
        UserGender.setCurrentText(" ")
        RegistrationPageLayout.addRow(style_RegSheetQLabel("Gender"), UserGender)

        UserDoB = QDateEdit(calendarPopup=True)
        UserDoB.setFixedSize(285, 40)
        UserDoB.setFont(QFont("Segoe UI ", 12))
        UserDoB.setStyleSheet("QDateEdit"
                              "{"
                              "border : 1px solid #075691; color : #075691"

                              "}"
                              "QDateEdit:focus"
                              "{"
                              "border : 2px solid green;"
                              "}"  )
        RegistrationPageLayout.addRow(style_RegSheetQLabel("Date of birth"), UserDoB)

        UserPswd = QLineEdit()
        UserPswd.setClearButtonEnabled(True)
        UserPswd.setEchoMode(QLineEdit.Password)
        style_RegSheet(UserPswd)
        RegistrationPageLayout.addRow(style_RegSheetQLabel("Password"), UserPswd)
        UserCnfPswd = PasswordEdit()
        UserCnfPswd.setClearButtonEnabled(True)
        style_RegSheet(UserCnfPswd)
        UserCnfPswd.setEchoMode(QLineEdit.Password)
        RegistrationPageLayout.addRow(style_RegSheetQLabel("Confirm Password"), UserCnfPswd)





        ButtonRegisterUser = QPushButton("Register", RegistrationPage)
        ButtonRegisterUser.move(1080, 720)
        ButtonRegisterUser.setFixedSize(150, 53)
        ButtonRegisterUser.setFont(QFont("Segoe UI ", 10, ))
        ButtonRegisterUser.setStyleSheet(
            "QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691;color : white;}""QPushButton::hover"
            "{"
            "background-color : #1a85b4;"
            "}")

        error_dialog = QErrorMessage(MainWindowGUI)

        def Call_UserRegistration():

            try:
                UserData = {
                    "UserID": str(UserID.text()).strip().upper(),
                    "UserName": str(UserName.text()).strip().upper(),
                    "UserEmail": str(UserEmail.text()).strip().upper(),
                    "UserGender": str(UserGender.currentText()).strip().upper(),
                    "UserDoB": str(UserDoB.text()).strip().upper(),
                    "UserPswd": str(UserPswd.text()).strip().upper(),
                }
                print(UserData)


                try:
                    Acknowledgment = UserRegistratiion(UserData)
                except Exception as error :
                    Acknowledgment = str(error)

                if Acknowledgment != "000":
                    try:
                        error_dialog.showMessage(FaultCodes[int(Acknowledgment)])
                    except : error_dialog.showMessage(str(Acknowledgment))


            except Exception as error : print(error)


        ButtonRegisterUser.pressed.connect(Call_UserRegistration)

        ButtonRegisterUserCancel = QPushButton("Cancel", RegistrationPage)
        ButtonRegisterUserCancel.move(1260, 720)
        ButtonRegisterUserCancel.setFixedSize(100, 53)
        ButtonRegisterUserCancel.setFont(QFont("Segoe UI ", 10, ))
        ButtonRegisterUserCancel.setStyleSheet(
            "QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691;color : white;}""QPushButton::hover"
            "{"
            "background-color : #1a85b4;"
            "}"\
            )
        ButtonRegisterUserCancel.pressed.connect(lambda: Switch_Screenpage(0))


        def Arbitrate_loggedInScreensDr(page):
            global stackedLayout_Frm_H_Right_LoggedInPage_Dr
            stackedLayout_Frm_H_Right_LoggedInPage_Dr.setCurrentIndex(page)

        Frm_H_Left_LoggedInPage_Dr = QFrame(LoggedInPage_Dr)
        Frm_H_Left_LoggedInPage_Dr.setFrameShape(QFrame.NoFrame)
        Frm_H_Left_LoggedInPage_Dr.setFixedWidth(280)

        PatientDiagnosisButton = QPushButton("Clinical Diagnosis",Frm_H_Left_LoggedInPage_Dr)
        PatientDiagnosisButton.move(25, 50)
        PatientDiagnosisButton.setFixedSize(220,45)
        PatientDiagnosisButton.setFont(QFont("Segoe UI ", 10, ))
        PatientDiagnosisButton.setStyleSheet("QPushButton \
                                                {border: 1px blue;border-radius: 5px;  \
                                                 background-color: #075691; color : white;}"\
                                             "QPushButton::hover"
                                                "{""background-color : #1a85b4;" "}"
                                             "QPushButton::QPushButton:checked"\
                                             "{"" border: none;" "}" \
                                             "QPushButton::focus" \
                                             "{""background-color : #327A92;" "}"
                                             )
        PatientDiagnosisButton.pressed.connect(lambda: Arbitrate_loggedInScreensDr(0))




        PatientRegButton = QPushButton("Patient registration",Frm_H_Left_LoggedInPage_Dr)
        PatientRegButton.move(25, 120)
        PatientRegButton.setFixedSize(220,45)
        PatientRegButton.setFont(QFont("Segoe UI ", 10, ))
        PatientRegButton.setStyleSheet("QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691; color : white;}""QPushButton::hover"
                                 "{"
                                 "background-color : #1a85b4;"
                                 "}" \
                                       "QPushButton::focus" \
                                       "{""background-color : #327A92;" "}"
                                       )

        PatientRegButton.pressed.connect(lambda: Arbitrate_loggedInScreensDr(1))

        PatientRepAnlsButton = QPushButton("Reports analysis",Frm_H_Left_LoggedInPage_Dr)
        PatientRepAnlsButton.move(25, 190)
        PatientRepAnlsButton.setFixedSize(220,45)
        PatientRepAnlsButton.setFont(QFont("Segoe UI ", 10, ))
        PatientRepAnlsButton.setStyleSheet("QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691; color : white;}""QPushButton::hover"
                                 "{"
                                 "background-color : #1a85b4;"
                                 "}" \
                                           "QPushButton::focus" \
                                           "{""background-color : #327A92;" "}"
                                           )

        PatientRepAnlsButton.pressed.connect(lambda: Arbitrate_loggedInScreensDr(2))

        Frm_H_Right_LoggedInPage_Dr = QFrame(LoggedInPage_Dr)
        Frm_H_Right_LoggedInPage_Dr.setFrameShape(QFrame.StyledPanel)
        Frm_H_Left_LoggedInPage_Dr.setStyleSheet("#MainFrame { border: 5px solid black; }")
        Frm_H_Right_LoggedInPage_Dr.setStyleSheet("#MainFrame { border: 5px solid black; }")
        #Frm_H_Right_LoggedInPage_Dr.setFixedSize(100,500)

        grid_layout = QGridLayout(LoggedInPage_Dr)
        grid_layout.setHorizontalSpacing(0)
        grid_layout.setVerticalSpacing(0)
        LoggedInPage_Dr.setLayout(grid_layout)
        grid_layout.addWidget(Frm_H_Left_LoggedInPage_Dr, 0, 0)
        grid_layout.addWidget(Frm_H_Right_LoggedInPage_Dr, 0, 1)

        stackedLayout_Frm_H_Right_LoggedInPage_Dr = QStackedLayout(Frm_H_Right_LoggedInPage_Dr)

        import pyqtgraph as pg



        ClinicalDiagPage = QFrame()
        PatientRegPage = QFrame()
        ReportsAnlysPage = QFrame()




        #ReportsAnlysPage = pg.PlotWidget(ReportsAnlysPage)
        #my_layout.addWidget(my_plot)
        #ReportsAnlysPage.plot([5, 7,6,7,8],[5, 5,8,2,8])

        import pyqtgraph as pg
        import numpy as np


        x = []
        y=  []

        class CustomPlot(pg.PlotWidget):
            def __init__(self , X_Label , Y_Label):
                pg.PlotWidget.__init__(self)
                self.setLabel('left', Y_Label, units='Cm')
                self.addLegend()
                self.showGrid(x=True, y=True)
                # set properties of the label for x axis
                self.setLabel('bottom', X_Label, units='')
                self.plot(x,y, pen=None, symbol='o', symbolPen='g', symbolSize=10,title="Test Plot")



        VideoFeedFrame =  QLabel(ClinicalDiagPage)
        VideoFeedFrame.setFixedSize(640, 480)
        VideoFeedFrame.move(80,50)


        GraphsFrame = QFrame(ClinicalDiagPage)
        GraphsFrame.setFixedSize(1500,300)
        GraphsFrame.move(80,600)
        layout = QHBoxLayout(GraphsFrame) # create the layout



        ReportsAnlysPage.pgcustom1 = CustomPlot("Number of Steps","Step Length") # class abstract both the classes
        ReportsAnlysPage.pgcustom2 = CustomPlot("","") # "" "" ""
        ReportsAnlysPage.pgcustom3 = CustomPlot("","") # "" "" ""
        ReportsAnlysPage.pgcustom4 = CustomPlot("","") # "" "" ""
        layout.addWidget(ReportsAnlysPage.pgcustom1)
        layout.addWidget(ReportsAnlysPage.pgcustom2)
        layout.addWidget(ReportsAnlysPage.pgcustom3)
        layout.addWidget(ReportsAnlysPage.pgcustom4)

        import random
        count = 0



        def UpdatePatientGraphs():
            global x, y , count , ReportsAnlysPage
            x[:-1] = x[1:]  # shift data in the array one sample left
            y[:-1] = y[1:]  # shift data in the array one sample left
            # (see also: np.roll)

            ReportsAnlysPage.pgcustom1.plot(range(1,len(PARAMETERS_DICT['Step_length'])+1),\
                                                    PARAMETERS_DICT["Step_length"],\
                                            pen='dodgerblue', symbol='t', symbolPen='g', symbolSize=1)
            print(PARAMETERS_DICT['R_Velocity'])
            ReportsAnlysPage.pgcustom2.plot(range(1,len(PARAMETERS_DICT['R_Velocity'])+1),\
                                            PARAMETERS_DICT['R_Velocity'], \
                                            pen='dodgerblue', symbol='t', symbolPen='g', symbolSize=1)
            #ReportsAnlysPage.pgcustom3.plot(x,y, pen='dodgerblue', symbol='t', symbolPen='g', symbolSize=1)
            #ReportsAnlysPage.pgcustom4.plot(x,y, pen='dodgerblue', symbol='t', symbolPen='g', symbolSize=1)

        timer = pg.QtCore.QTimer()
        #timer.timeout.connect(UpdatePatientGraphs)
        timer.start(50)


        def ClearPatientGraphs():
            global pgcustom1,pgcustom2
            ReportsAnlysPage.pgcustom1.clear()
            ReportsAnlysPage.pgcustom2.clear()



        InputVidFeed_Button = QPushButton("Browse...",ClinicalDiagPage)
        InputVidFeed_Button.move(700, 50)
        InputVidFeed_Button.setFixedSize(150,45)
        InputVidFeed_Button.setFont(QFont("Segoe UI ", 10, ))
        InputVidFeed_Button.setStyleSheet("QPushButton {border: 1px blue;border-radius: 5px;  \
        background-color: #206075; color : white;}""QPushButton::hover"
                                 "{"
                                 "background-color : #367A90;"
                                 "}")

        def GetVideoPathLocal():
            global VideoFilepath
            VideoFilepath, checkFlag = QFileDialog.getOpenFileName(None, "Select input Video file",
                                    "", "All Files (*);;Avi(*.avi);;Webm (*.webm);;Mp4 (*.mp4);;mpeg (*.mpeg);;.WMV (* .wmv)")
            if checkFlag: 
                RESULT_DICT = GET_ALL_PARAMETERS(VideoFilepath)

        InputVidFeed_Button.pressed.connect(GetVideoPathLocal)


        stackedLayout_Frm_H_Right_LoggedInPage_Dr.addWidget(ClinicalDiagPage)
        stackedLayout_Frm_H_Right_LoggedInPage_Dr.addWidget(PatientRegPage)
        stackedLayout_Frm_H_Right_LoggedInPage_Dr.addWidget(ReportsAnlysPage)
        stackedLayout_Frm_H_Right_LoggedInPage_Dr.setCurrentIndex(0)

        mainMenu = QMenuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        stackedLayout_MainApp.addWidget(LoginPage)
        stackedLayout_MainApp.addWidget(RegistrationPage)
        stackedLayout_MainApp.addWidget(LoggedInPage_Dr)


        MainWindowGUI.showMaximized()
        sys.exit(Aplication.exec_())


