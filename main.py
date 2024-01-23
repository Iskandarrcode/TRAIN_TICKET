from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import mysql.connector as myc
import sys
import re

con = myc.connect(host="localhost", user="root", password="root")
cursor = con.cursor()

def connect_database():
    cursor.execute("create database if not exists TRAIN")
    cursor.execute("use TRAIN")
    
    cursor.execute("""create table if not exists 
    users(user_id int primary key auto_increment, name varchar(30), surname varchar(30),
    email varchar(50), password varchar(30))""")
    
    cursor.execute("""create table if not exists 
    train(id int primary key auto_increment, tr_name varchar(50), tr_time date,
    tr_price int)""")
    
    cursor.execute("""create table if not exists
    orders(order_id int primary key auto_increment, book_id int,user_id int, units int)""")
    con.commit()
    
    
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.resize(1920, 1080)
        self.setFont(QFont("Montserrat", 15))
        self.setWindowTitle("Tickets")
        self.setStyleSheet("""
            background-color: rgb(25, 25, 112);
            """)
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap('Image.png')
        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)
        self.setMinimumSize(pixmap.width(), pixmap.height())
        self.setMaximumSize(pixmap.width(), pixmap.height())
        
        # BUTTONS____
        self.radio_button1 = QRadioButton(self)
        self.radio_button1.setFont(QFont("Montserrat", 14))
        self.radio_button1.setStyleSheet("color: white;")
        self.radio_button1.setGeometry(22, 637, 20, 20)
        self.radio_button1.setStyleSheet("""
            background-color: transparent;
            """)
        self.radio_button1.clicked.connect(lambda : self.radio_btn1())
        
        self.radio_button2 = QRadioButton(self)
        self.radio_button2.setFont(QFont("Montserrat", 14))
        self.radio_button2.setStyleSheet("color: white;")
        self.radio_button2.setGeometry(22, 674, 20, 20)
        self.radio_button2.setStyleSheet("""
            background-color: transparent;
            """)
        self.radio_button2.clicked.connect(lambda : self.radio_btn2())

        self.btn = QPushButton("Find tickeds", self)
        self.btn.setFont(QFont("Montserrat", 10, weight = 80))
        self.btn.setGeometry(1489, 635, 225, 64)
        self.btn.setStyleSheet("""
            background-color: blue;
            border-radius: 25px;""")
        
        
        # LINE EDITS_____
        self.ln = QLineEdit(self)
        self.ln.setGeometry(360, 635,205, 63)
        self.ln.setFont(QFont("Montserrat",14))
        self.ln.setPlaceholderText("From")
        self.ln.setStyleSheet("""
            background-color: white;
            border-radius: 20px;""")
        
        self.ln2 = QLineEdit(self)
        self.ln2.setGeometry(640, 635,205, 63)
        self.ln2.setFont(QFont("Montserrat",14))
        self.ln2.setPlaceholderText("To")
        self.ln2.setStyleSheet("""
            background-color: white;
            border-radius: 20px;""")
        
        self.ln4 = QLineEdit(self)
        self.ln4.setGeometry(1208, 635,205, 63)
        self.ln4.setFont(QFont("Montserrat",14))
        self.ln4.setPlaceholderText("Back")
        self.ln4.setStyleSheet("""
            background-color: white;
            border-radius: 20px;""")
        
        self.ln3 = QLineEdit(self)
        self.ln3.setGeometry(936, 635,205, 63)
        self.ln3.setFont(QFont("Montserrat",14))
        self.ln3.setPlaceholderText("There")
        self.ln3.setStyleSheet("""
            background-color: white;
            border-radius: 20px;""")
    
        
    def radio_btn1(self):
        self.ln3.setGeometry(936, 635,205, 63)
        
    def radio_btn2(self):
        self.ln3.setGeometry(936, 635, 410, 63)


       
class TemporaryWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(450, 700)
        self.setMaximumSize(450, 700)
        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("bookstore.ico"))

        label = QLabel(self)
        label.setGeometry(25, 100, 400, 400)
        movie = QMovie('welcome.gif')
        movie.setScaledSize(label.size())
        label.setMovie(movie)
        movie.start()

        QTimer.singleShot(700, self.close)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.show_temporary_window()
        connect_database()
        self.main_window = None
        self.setMinimumSize(450, 700)
        self.setMaximumSize(450, 700)
        self.setStyleSheet("background-color: rgb(0, 191, 255)")
        self.setWindowTitle("Book Store")
        self.setWindowIcon(QIcon("bookstore.ico"))

        self.loginlb = QLabel(self)
        self.loginlb.setGeometry(170, 150, 150, 50)
        self.loginlb.setText("Login")
        self.loginlb.setFont(QFont("Montserrat", 20, weight=65))

        self.email_error = QLabel(self)
        self.email_error.setGeometry(50, 200, 250, 50)
        self.email_error.setFont(QFont("Montserrat", 9))
        self.email_error.setStyleSheet("color: red")
              
        self.email_edit = QLineEdit(self)
        self.email_edit.setGeometry(50, 250, 350, 50)
        self.email_edit.setFont(QFont("Montserrat", 12))
        self.email_edit.setPlaceholderText("Email")
        self.email_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        self.password_edit = QLineEdit(self)
        self.password_edit.setGeometry(50, 320, 350, 50)
        self.password_edit.setFont(QFont("Montserrat", 12))
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")
        
        self.pas_error = QLabel(self)
        self.pas_error.setGeometry(50, 370, 400, 100)
        self.pas_error.setFont(QFont("Montserrat", 8))
        self.pas_error.setStyleSheet("color: red")

        self.loginbtn = QPushButton("Login", self)
        self.loginbtn.setGeometry(50, 450, 350, 45)
        self.loginbtn.setFont(QFont("Montserrat", 12))
        self.loginbtn.setStyleSheet("border-radius: 10px; background-color: #B5FFFF")
        self.loginbtn.clicked.connect(self.check_login)

        self.regbtn = QPushButton("Register", self)
        self.regbtn.setGeometry(50, 510, 350, 45)
        self.regbtn.setFont(QFont("Montserrat", 12))
        self.regbtn.setStyleSheet("border-radius: 10px; background-color: #B5FFFF")
        self.regbtn.clicked.connect(self.showRegwindow)
        

    def show_temporary_window(self):
        temporary_window = TemporaryWindow()
        temporary_window.exec_()
        
        
    def check_login(self):
        self.__email = self.email_edit.text().strip()
        self.__password = self.password_edit.text().strip()
        
        if len(self.__email) == 0 or len(self.__password) == 0:
            self.email_error.setText("Fields must be filled")
        
        else:
            self.email_error.setText("")
            self.check_password(self.__password)
            self.check_email(self.__email)
        
        error1 = self.email_error.text().strip()
        error2 = self.pas_error.text().strip()
        if len(error1) == 0 and len(error2) == 0:
            self.check_data()
    
    
    def check_data(self):
        query = "SELECT user_id FROM users WHERE email = %s AND password = %s"

        try:
            cursor.execute(query, (self.__email, self.__password))
            data = cursor.fetchall()

            if len(data) > 0:
                global user_id
                user_id = data[0][0]
                self.show_main_window()
            else:
                self.email_error.setText("User does not exist")

        except myc.Error as e:
            print(f"Error: {e}")


    def show_main_window(self):
        
        self.close()

        if self.main_window is None:
            self.main_window = Window()
            self.main_window.show()
            
            
    def check_email(self, email):
        reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not (re.fullmatch(reg, email)):
            self.email_error.setText("invalid email")
        else:
            self.email_error.setText("")
            
            
    def check_password(self, password):
        
        alpha = 0
        digits = 0
        symb = 0
        
        for i in password:
            if i.isdigit():
                digits += 1
            elif i.isalpha():
                alpha += 1
            else:
                symb += 1
        
        if not (alpha >= 6 and digits >= 1 and symb >= 1):
            self.pas_error.setText("Password must contain at least six alpha characters\none digit and one symbol")
        else:
            self.pas_error.setText("")
    
    
    def showRegwindow(self):
        reg = RegistrationWindow()
        if reg.exec_() == QDialog.Accepted:
            self.show()
        else:
            self.close()
    
        

class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()
        connect_database()
        self.setMinimumSize(450, 700)
        self.setMaximumSize(450, 700)
        self.setStyleSheet("background-color: #EAFFFF")
        self.setWindowTitle("Book Store")
        self.setWindowIcon(QIcon("bookstore.ico"))

        self.namelb = QLabel(self)
        self.namelb.setGeometry(50, 50, 300, 40)
        self.namelb.setFont(QFont("Montserrat", 10))
        self.namelb.setStyleSheet("color:red")

        self.name_edit = QLineEdit(self)
        self.name_edit.setGeometry(50, 90, 350, 50)
        self.name_edit.setFont(QFont("Montserrat", 12))
        self.name_edit.setPlaceholderText("Name")
        self.name_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        self.surnamelb = QLabel(self)
        self.surnamelb.setGeometry(50, 140, 320, 40)
        self.surnamelb.setFont(QFont("Montserrat", 10))
        self.surnamelb.setStyleSheet("color:red")
        
        self.surname_edit = QLineEdit(self)
        self.surname_edit.setGeometry(50, 190, 350, 50)
        self.surname_edit.setFont(QFont("Montserrat", 12))
        self.surname_edit.setPlaceholderText("Surname")
        self.surname_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")
        
        self.emaillb = QLabel(self)
        self.emaillb.setGeometry(50, 240, 200, 40)
        self.emaillb.setFont(QFont("Montserrat", 10))
        self.emaillb.setStyleSheet("color:red")

        self.email_edit = QLineEdit(self)
        self.email_edit.setGeometry(50, 290, 350, 50)
        self.email_edit.setFont(QFont("Montserrat", 12))
        self.email_edit.setPlaceholderText("Email")
        self.email_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        self.passwordlb = QLabel(self)
        self.passwordlb.setGeometry(50, 340, 350, 40)
        self.passwordlb.setFont(QFont("Montserrat", 10))
        self.passwordlb.setStyleSheet("color:red")
        
        self.password_edit = QLineEdit(self)
        self.password_edit.setGeometry(50, 390, 350, 50)
        self.password_edit.setFont(QFont("Montserrat", 12))
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        self.repasswordlb = QLabel(self)
        self.repasswordlb.setGeometry(50, 440, 250, 40)
        self.repasswordlb.setFont(QFont("Montserrat", 10))
        self.repasswordlb.setStyleSheet("color:red")
        
        self.repassword_edit = QLineEdit(self)
        self.repassword_edit.setGeometry(50, 480, 350, 50)
        self.repassword_edit.setFont(QFont("Montserrat", 12))
        self.repassword_edit.setPlaceholderText("Re-enter Password")
        self.repassword_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        register_button = QPushButton("Register", self)
        register_button.setGeometry(50, 560, 350, 45)
        register_button.setFont(QFont("Montserrat", 12))
        register_button.setStyleSheet("border-radius: 10px; background-color: #B5FFFF")
        register_button.clicked.connect(self.register_button_clicked)


    def register_button_clicked(self):
        
        registration_successful = self.check_info()

        if registration_successful:
            self.accept()  # Set the result to QDialog.Accepted
            
            
    def check_info(self):
        
        self.__name = self.name_edit.text().strip()
        self.__surname = self.surname_edit.text().strip()
        self.__email = self.email_edit.text().strip()
        self.__password = self.password_edit.text().strip()
        self.__repassword = self.repassword_edit.text().strip()
        isValid = 1
        
        if len(self.__name) < 3:
            self.namelb.setText("Name cannot be that much short")
            isValid = 0
        
        if len(self.__surname) < 3:
            self.surnamelb.setText("Surname cannot be that much short")
            isValid = 0
        
        reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not (re.fullmatch(reg, self.__email)):
            self.emaillb.setText("Invalid email address")
            isValid = 0
        
        if self.check_password(self.__password):
            isValid = 0
        
        if not self.check_password(self.__password) and self.__password != self.__repassword:
            self.repasswordlb.setText("Password does not match")
            isValid = 0
        
        if isValid:
            if self.check_data():
                self.emaillb.setText("User already exists")
                QTimer.singleShot(5000, self.accept)
                return 0
            
            self.write_data()
            return True
        
        else:
            return False
    
    
    def check_data(self):
        query = "SELECT user_id FROM users WHERE email = %s"

        try:
            cursor.execute(query, (self.__email,))
            data = cursor.fetchall()
            
            if len(data) > 0:
                return 1
            else:
                return 0

        except myc.Error as e:
            print(f"Error: {e}")
        
        
    def check_password(self, password):
        
        alpha = 0
        digits = 0
        symb = 0
        
        for i in password:
            if i.isdigit():
                digits += 1
            elif i.isalpha():
                alpha += 1
            else:
                symb += 1
        
        if not (alpha >= 6 and digits >= 1 and symb >= 1):
            self.passwordlb.setText("Password must contain at least six alpha characters\none digit and one symbol")
            return 1
        else:
            return 0
    
    
    def write_data(self):
        
        query = f"""insert into users(name, surname, email, password) values(%s, %s, %s, %s)"""
        values = (self.__name, self.__surname, self.__email, self.__password)
        cursor.execute(query, values)
        con.commit() 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())
