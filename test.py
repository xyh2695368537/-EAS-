
import sys
from PyQt6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)


window = QtWidgets.QWidget()
window.setWindowTitle("教务管理系统")
window.resize(800, 600)

button = QtWidgets.QPushButton("点击我", window)
button.move(400,300)

window.show()

sys.exit(app.exec())