import PyQt5
from PyQt5 import QtWidgets
from qtwidgets import Toggle, AnimatedToggle

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        VideoFeedInput = Toggle()
        VideoFeedInput = AnimatedToggle(
            checked_color="green",
            pulse_checked_color="dodgerblue"
        )
        VideoFeedInput.setFixedSize(70,50)
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(VideoFeedInput)
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QtWidgets.QApplication([])
w = Window()
w.show()
app.exec_()