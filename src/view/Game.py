import sys
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        
        # Definindo a cor de fundo com um retângulo (sem bordas arredondadas)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.size_hint = (0.6, 0.6)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        
        # Título
        title = Label(text="TCC", font_size='40sp', color=(1, 1, 1, 1))
        
        # Button
        button_sair = Button(text="Voltar", font_size='20sp', size_hint=(1, None), height="60",
                     background_normal='', background_down='',
                     background_color=(0, 0, 0, 0), on_press=self.go_back)

        # Adiciona os widgets ao layout
        layout.add_widget(title)
        layout.add_widget(button_sair)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'menu'