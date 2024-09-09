import cv2
import time
import sys
import numpy as np
from rmn import RMN
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from view.Menu import MenuScreen

rmn = RMN()

class ExpressionGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        # sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == "__main__":
    ExpressionGameApp().run()