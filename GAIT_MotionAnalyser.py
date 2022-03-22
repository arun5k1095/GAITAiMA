# -*- coding: utf-8 -*-


#___________________________________________________
# Tool = "GAIT AIMA"
# HandcraftedBy : "__"
# Version = "1.0"
# LastModifiedOn : "13th Mar 2022"
#___________________________________________________

import Resources
from threading import*
import json,requests
import urllib.request
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from qtwidgets import PasswordEdit

from threading import*
import os
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import requests
import urllib.request
import time
import webbrowser
from datetime import datetime



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


if __name__ == "__main__":

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

    def Siwtch_page(pageNum):
        try:
            if pageNum ==1:
                MainWindowGUI.setStyleSheet("QWidget#MainMenu{background-image: url(:/resources/Wallpaper8.jpg);}");
            elif pageNum==0:
                    MainWindowGUI.setStyleSheet("QWidget#MainMenu{background-image: url(:/resources/Wallpaper6.jpg);}");

            stackedLayout.setCurrentIndex(pageNum)
        except Exception as error : print(error)

    stackedLayout = QStackedLayout(MainWindowGUI)

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



    ButtonSignINRegisterUser = QPushButton("Register User",LoginPage)
    ButtonSignINRegisterUser.move(910, 610)
    ButtonSignINRegisterUser.setFixedSize(250,45)
    ButtonSignINRegisterUser.setFont(QFont("Segoe UI ", 10, ))
    ButtonSignINRegisterUser.setStyleSheet("QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691;color : white;}""QPushButton::hover"
                             "{"
                             "background-color : #1a85b4;"
                             "}")
    ButtonSignINRegisterUser.pressed.connect(lambda : Siwtch_page(1))



    ForgotPassword = QPushButton("Forgot Password ?", LoginPage)
    ForgotPassword.move(980, 475)
    ForgotPassword.setFixedSize(250, 45)
    ForgotPassword.setFont(QFont("Segoe UI ", 9 ))
    ForgotPassword.setStyleSheet("QPushButton{background: transparent;color : #075691}""QPushButton::hover"
                             "{"
                             "color : #1a85b4;"
                             "}")


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
                                     "{"
                                     "border : 1px solid #075691; color : #075691"
                                        
                                     "}"
                                     "QComboBox:focus"
                                     "{"
                                     "border : 2px solid green;"
                                     "}")
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
                          "}")
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


    ButtonRegisterUserCancel = QPushButton("Cancel", RegistrationPage)
    ButtonRegisterUserCancel.move(1260, 720)
    ButtonRegisterUserCancel.setFixedSize(100, 53)
    ButtonRegisterUserCancel.setFont(QFont("Segoe UI ", 10, ))
    ButtonRegisterUserCancel.setStyleSheet(
        "QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691;color : white;}""QPushButton::hover"
        "{"
        "background-color : #1a85b4;"
        "}")
    ButtonRegisterUserCancel.pressed.connect(lambda: Siwtch_page(0))


    stackedLayout.addWidget(LoginPage)
    stackedLayout.addWidget(RegistrationPage)


    MainWindowGUI.showMaximized()
    sys.exit(Aplication.exec_())

