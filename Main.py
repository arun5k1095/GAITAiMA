# -*- coding: utf-8 -*-


#___________________________________________________
# Tool = "Postura"
# HandcraftedBy : "__"
# Version = "1.1"
# LastModifiedOn : "5th April 2022"
#___________________________________________________

from multiprocessing import Queue
from threading import*
import re
import json,requests
import urllib.request
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtWidgets import QApplication,QWidget,QSplashScreen,\
    QStackedLayout,QFrame,QFormLayout,QLineEdit,QPushButton,QLabel,QComboBox,QDateEdit,QMessageBox,QErrorMessage,\
    QMainWindow,QMenuBar,QGridLayout,QFileDialog
from PyQt5.QtCore import Qt,QTimer
from PyQt5 import QtGui
from qtwidgets import PasswordEdit
from FaultCodes import FaultCodes
from threading import*
import os
import sys
import time

import requests
import urllib.request
import time
import webbrowser
from datetime import datetime
import Resources


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

try:
    if __name__ == "__main__":

        def Authenticate_Login():
            UserID = UserIDInput.text().upper().strip()
            UserPswd = UserPassword.text().strip()

            if UserID == "ADMIN" and UserPswd == "admin123":
                Switch_Screenpage(2)
            else : error_dialog.showMessage("Invalid Credentials , Please re-try")


        Aplication = QApplication(sys.argv)
        MainWindowGUI = QWidget()
        #MainWindowGUI.setFixedSize(1600, 800)
        MainWindowGUI.setWindowTitle('GAIT AiMA')
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
        ClinicalDiagPage = QFrame()
        PatientRegPage = QFrame()
        ReportsAnlysPage = QFrame()

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
            VideoFilepath, checkFlag = QFileDialog.getOpenFileName(None, "Select input Video file",
                                    "", "All Files (*);;Avi(*.avi);;Webm (*.webm);;Mp4 (*.mp4);;mpeg (*.mpeg);;.WMV (* .wmv)")
            if checkFlag: print(VideoFilepath)
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
except Exception as error : print(error)

