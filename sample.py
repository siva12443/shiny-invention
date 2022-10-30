import kivy
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock
from kivymd.uix.textfield import MDTextField
from kivy.lang.builder import Builder
import cv2
import mysql.connector
from kivy.core.window import Window
from pyzbar.pyzbar import decode
from kivymd.uix.dialog import MDDialog
import time
from collections import OrderedDict
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
kivy.require('1.11.1')

Window.size = (300,500)

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement,self).__init__(**kwargs)

class Db_Operations:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='Test123',
            database='siva'
        )
        self.mycursor = self.mydb.cursor()

    def get_userName(self, Name):
        _users = OrderedDict()
        _users['name'] = {}
        _users['number'] = {}
        _users['password'] = {}
        sql = "SELECT * FROM users_table WHERE name = '" + Name + "'"
        self.mycursor.execute(sql)
        users = self.mycursor.fetchall()
        for user in users:
            global name 
            name = ""
            name = f'{name}{user[1]}'
            global passw
            passw = ""
            passw = f'{passw}{user[3]}'
    
    def get_studentDetails(self):
        _student = OrderedDict()
        _student['studRoll'] = {}
        global studRoll
        studRoll = []
        sql = "SELECT * FROM student_table"
        self.mycursor.execute(sql)
        students = self.mycursor.fetchall()
        for student in students:
            studRoll.append(student[2])
        users_length = len(studRoll)
        idx = 0
        while idx < users_length:
            _student['studRoll'][idx] = studRoll[idx]
            idx += 1

TopAppTool = """

MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Login"

    MDLabel:
        text: "  "
		font_size: 14
        halign: "center"
	
"""

class LoginApp(Screen):
    def __init__(self, **kwargs):
       super(LoginApp,self).__init__(**kwargs)
       TopAppTools = Builder.load_string(TopAppTool)
       CollegeLogo = Image(source = "logo.png", size_hint_y = None, height ='2.5cm', pos_hint = {'center_x': 0.5, 'center_y': 0.7})
       NameTextField = MDTextField(  pos_hint = {'center_x': 0.5, 'center_y': 0.5},
        size_hint_x = None,
        halign = "center",
        icon_right = "account",
        width = "200",
        _line_color_normal = [0,1,1,1],
        _icon_right_color = [0,1,1,1],
        hint_text = "UserName")
       NameTextField.bind(text = self.on_text)
       PassTextField = MDTextField( pos_hint = {'center_x': 0.5, 'center_y': 0.4},
        size_hint_x = None,
        halign = "center",
        password = True,
        width = "200dp",
        icon_right = "key-variant",
        hint_text = "Password")
       PassTextField.bind(text = self.on_text2)
       LoginButton = MDRaisedButton(pos_hint = {'center_x': 0.5, 'center_y': 0.2}, text = "Submit", halign = "center", on_press = self.OnPressLoginButton)
       Db_Operations.get_userName
       self.add_widget(TopAppTools)
       self.add_widget(CollegeLogo)
       self.add_widget(NameTextField)
       self.add_widget(PassTextField)
       self.add_widget(LoginButton) 
    def on_text(self, instance, value):
        global userName
        userName = value
    def on_text2(self, instance, value):
        global password
        password = value
    def OnPressLoginButton(self, *args):
        connection = Db_Operations()
        values = connection.get_userName(userName)
        if userName == name and password == passw:
            self.manager.current = "second"
        else:
               self.dialog = MDDialog(
                text="Invalid UserName or Password",
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_press = self.MoveFirstScreen
                    ),
                ],)
               self.dialog.open()
    def MoveFirstScreen(self, *args):
        self.dialog.dismiss(force=True)

class QrScanner(Screen):
    def __init__(self, **kwargs):
       super(QrScanner,self).__init__(**kwargs)
       layout=MDBoxLayout(orientation='vertical')
       TopBar = MDTopAppBar(title = "QRScanner")
       #, left_action_items = [["arrow-left-circle-outline", lambda *args : setattr(self.manager, "current", "third")]]
       ViewReport = MDFlatButton(text = "View Report", on_press = self.MovetoFourScreen, pos_hint = {'center_x': 0.5, 'center_y': 0.2})
       self.add_widget(layout)
       layout.add_widget(TopBar)
       self.image=Image()
       layout.add_widget(self.image)
        #self.save_img_button=(MDFillRoundFlatButton(text="Detect URL",pos_hint={'center_x':0.5,'center_y':0.3},size_hint=(None,None)))
        #self.save_img_button.bind(on_press=self.take_picture)
        #layout.add_widget(self.save_img_button)
       self.capture=cv2.VideoCapture(0)
       self.detector = cv2.QRCodeDetector()
       Clock.schedule_interval(self.load_video,1.0/30.0)
       layout.add_widget(ViewReport)

    def load_video(self,*args):
        ret,frame=self.capture.read()
        for code in decode(frame):
            print(code.data.decode('utf-8'))
            time.sleep(5)
            connections = Db_Operations()
            values = connections.get_studentDetails()
            if code.data.decode('utf-8') in studRoll:
                self.manager.current = "third"
                
            # else:
            #    self.dialog = MDDialog(
            #     text="Invalid QR",
            #     buttons=[
            #         MDFlatButton(
            #             text="Ok",
            #             on_press = self.dialog.dismiss(force=True)
            #         ),
            #     ],)
            #    self.dialog.open()
        self.image_frame=frame
        buffer=cv2.flip(frame,0).tobytes()
        texture=Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture
    
    def MovetoFourScreen(self, *args):
        self.manager.current = "fourth"

TopTool = """

MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Student Details"
		left_action_items: [["arrow-left-circle-outline", lambda *args : setattr(app.manager, "current", "second")]]

    MDLabel:
        text: "  "
		font_size: 14
        halign: "center"
	
"""

class DetailsScreen(Screen):        
    def __init__(self, **kwargs):
        super(DetailsScreen,self).__init__(**kwargs)    
		
		#Adding widgets
        TopTools = Builder.load_string(TopTool)
        Name_Label = MDLabel(text = "Name: Stud_Name", font_size = 14, halign = "center", pos_hint = {'center_x' : 0.5, 'center_y' : 0.7}, theme_text_color = "Custom",text_color = (1,0.5,0,1))
        Roll_Label = MDLabel(text = "Roll No: Stud_Roll", font_size = 14, halign = "center", pos_hint = {'center_x' : 0.5, 'center_y' : 0.6}, theme_text_color = "Custom",text_color = (1,0.5,0,1))
        Choose_Label = MDLabel(text = "Choose the food type", font_size = 18, halign = "center", pos_hint = {'center_x' : 0.5, 'center_y' : 0.4}, bold = True)
        Snack_Button = MDFillRoundFlatIconButton(icon = "coffee-outline", text = "Snack", halign = "center", pos_hint = {'center_x' : 0.5, 'center_y' : 0.3})
        Lunch_Button = MDFillRoundFlatIconButton(icon = "bowl-mix", text = "Lunch", halign = "center", pos_hint = {'center_x' : 0.5, 'center_y' : 0.2})

		#Adding all the widgets to the screen
        self.add_widget(TopTools)
        self.add_widget(Name_Label)
        self.add_widget(Roll_Label)
        self.add_widget(Choose_Label)
        self.add_widget(Snack_Button)
        self.add_widget(Lunch_Button)
    
    def go_home(self, *args):
        # Access the `ScreenManager` and change the screen.
        self.manager.current = "second"
        # Some other actions.

FourthTool = """

MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Report Screen"
		left_action_items: [["arrow-left-circle-outline", lambda x: app.callback(x)]]

    MDLabel:
        text: "  "
		font_size: 14
        halign: "center"
	
"""

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super(ReportScreen,self).__init__(**kwargs)

        TopTools = Builder.load_string(FourthTool)
        Name_Label = MDLabel(text = "This is Student Report Screen", font_size = 14, halign = "center", pos_hint = {'center_x' : 0.5, 'center_y' : 0.7})
        self.add_widget(TopTools)
        self.add_widget(Name_Label)
    
    def go_home(self, *args):
        self.manager.current = "second"
    
class NavigationScreen(MDApp):
    title="Scanner"
    def build(self):
        self.theme_cls.theme_style='Light'
        self.theme_cls.primary_palette='DeepPurple'
        AllScreen = ScreenManagement(transition=FadeTransition())
        AllScreen.add_widget(LoginApp(name="first"))
        AllScreen.add_widget(QrScanner(name="second"))
        AllScreen.add_widget(DetailsScreen(name="third"))
        AllScreen.add_widget(ReportScreen(name = "fourth"))
        return AllScreen

if __name__ == '__main__':
    NavigationScreen().run()