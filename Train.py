from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import mysql.connector as myc
import sys



        


app = QApplication(sys.argv)
db = Window()
db.show()
sys.exit(app.exec_())