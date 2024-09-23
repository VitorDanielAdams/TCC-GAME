import cv2
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture

class ResultScreen(Screen):
    def __init__(self, controller, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.controller = controller

        # Fundo da tela
        with self.canvas.before:
            Color(0.31, 0.42, 0.66, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Label de pontuação no topo da tela
        self.score_label = Label(text="Pontuação: 0", font_size='20sp', color=(1, 1, 1, 1),
                                 size_hint=(None, None), size=(200, 50), pos_hint={'x': 0.75, 'y': 0.9})
        self.layout.add_widget(self.score_label)

        # Mensagem de acerto ou erro (colorida)
        self.result_message = Label(text="", font_size='30sp', color=(1, 1, 1, 1),
                                    size_hint=(None, None), size=(300, 50), pos_hint={'x': 0.35, 'y': 0.7})
        self.layout.add_widget(self.result_message)

        # Imagem da emoção (centrada na tela)
        self.result_image = Image(size_hint=(0.4, 0.4), pos_hint={'x': 0.3, 'y': 0.4})
        self.layout.add_widget(self.result_image)

        # Botão de próxima fase ou tente novamente
        self.action_button = Button(text="", font_size='20sp', size_hint=(0.4, 0.1), pos_hint={'x': 0.3, 'y': 0.1})
        self.action_button.bind(on_press=self.on_button_press)
        self.layout.add_widget(self.action_button)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_enter(self, **kwargs):
        correct = self.controller.is_correct()
        
        self.score_label.text = f"Pontuação: {self.controller.scoring_model.get_score()}"
        
        emotion_image = self.controller.get_emotion_image() 
        buf = cv2.cvtColor(emotion_image, cv2.COLOR_BGR2RGB)
        texture = Texture.create(size=(emotion_image.shape[1], emotion_image.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        
        self.result_image.texture = texture

        if correct:
            self.result_message.text = "Acertou!"
            self.result_message.color = (0, 1, 0, 1)
            self.action_button.text = "Próxima Fase"
        else:
            self.result_message.text = "Errou!"
            self.result_message.color = (1, 0, 0, 1)
            self.action_button.text = "Tente Novamente"

    def on_button_press(self, instance):
        if self.action_button.text == "Próxima Fase":
            self.controller.next_level()
            self.manager.current = 'game_screen'
        else:
            self.controller.retry_same_emotion() 
            self.manager.current = 'game_screen'
