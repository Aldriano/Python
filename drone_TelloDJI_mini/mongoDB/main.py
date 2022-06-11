from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.network.urlrequest import UrlRequest

import cv2
import cv2.aruco as aruco
import numpy as np 
import base64
from PIL import Image

from util.functions import write_file
from util.functions import camera
from connection import getImgFromDb

KV = '''
MDFloatLayout:

    MDFlatButton:
        text: "Teste App Python com Kivy - by Nome_Aluno"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_alert_dialog() 
'''

class Example(MDApp):
    dialog = None
    imgInit = ''

    def build(self):
        self.imgInit = getImgFromDb()
        return Builder.load_string(KV)

    def show_alert_dialog(self):
        print(self.imgInit)

        if not self.dialog:
            self.dialog = MDDialog(
                text="Abrir camera?",
                buttons=[
                    MDFlatButton(
                        text="NÃO",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release= self.closeDialog
                    ),
                    MDFlatButton(
                        text="SIM",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release= self.openCamera
                    )
                ]
            )
        
        self.dialog.open()

    def closeDialog(self, inst):
        self.dialog.dismiss()

    def openCamera(self, inst):
        img = base64.urlsafe_b64decode(self.imgInit)

        write_file(img, "test.jpeg")
        
        camera()

        self.dialog.dismiss()

Example().run()