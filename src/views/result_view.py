import cv2
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.graphics.texture import Texture

class ResultScreen(Screen):
    def __init__(self, controller, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.controller = controller

        # Fundo da tela com imagem PNG
        with self.canvas.before:
            Color(0.31, 0.42, 0.66, 1)  # Cor de fundo
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.bg_image = Image(source="assets/images/background.jpg", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg_image)

        # Layout principal
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Label de pontuação no topo da tela
        self.score_label = Label(text="Pontuação: 0", font_size='24sp', bold=True, color=(1, 1, 1, 1),
                                 size_hint=(None, None), size=(250, 50), pos_hint={'center_x': 0.5, 'y': 0.9})
        self._add_text_box(self.score_label, color=(0.1, 0.3, 0.8, 0.7))  # Fundo azul arredondado
        self.layout.add_widget(self.score_label)

        # Mensagem de acerto ou erro (colorida e destacada)
        self.result_message = Label(text="", font_size='30sp', bold=True, color=(1, 1, 1, 1),
                                    size_hint=(None, None), size=(300, 60), pos_hint={'center_x': 0.5, 'y': 0.3})
        self._add_text_box(self.result_message)  # Caixa colorida dinâmica
        self.layout.add_widget(self.result_message)

        # Imagem da emoção (centrada na tela)
        self.result_image = Image(size_hint=(0.4, 0.4), pos_hint={'center_x': 0.5, 'y': 0.48})
        self.layout.add_widget(self.result_image)

        # Botão de próxima fase ou tente novamente
        self.action_button = Button(text="Próxima Fase", font_size='20sp', bold=True, size_hint=(0.4, 0.1),
                                    pos_hint={'center_x': 0.5, 'y': 0.1}, background_color=(0, 0.5, 1, 1))
        self._round_button(self.action_button)
        self.action_button.bind(on_press=self.on_button_press)
        self.layout.add_widget(self.action_button)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.bg_image.size = self.size

    def _add_text_box(self, label, color=None):
        """Adiciona uma caixa colorida atrás do texto."""
        with self.layout.canvas.before:
            box_color = color if color else (0, 1, 0, 0.7) if label.text == "Acertou!" else (1, 0, 0, 0.7)
            Color(*box_color)  # Cor dinâmica com transparência
            rect = RoundedRectangle(size=(label.size[0] + 20, label.size[1] + 10),
                                    pos=(label.pos[0] - 10, label.pos[1] - 5), radius=[15])
            label.bind(
                pos=lambda instance, value: setattr(rect, 'pos', (value[0] - 10, value[1] - 5)),
                size=lambda instance, value: setattr(rect, 'size', (value[0] + 20, value[1] + 10))
            )

    def _round_button(self, button):
        """Deixa o botão arredondado e colorido."""
        with button.canvas.before:
            Color(0, 0.5, 1, 1)  # Cor azul
            self.button_bg = RoundedRectangle(size=button.size, pos=button.pos, radius=[20])
            button.bind(
                pos=lambda instance, value: setattr(self.button_bg, 'pos', value),
                size=lambda instance, value: setattr(self.button_bg, 'size', value)
            )

    def on_enter(self, **kwargs):
        correct = self.controller.is_correct()

        self.score_label.text = f"Pontuação: {self.controller.scoring_model.get_score()}"

        emotion_image = self.controller.get_emotion_image()
        buf = cv2.cvtColor(emotion_image, cv2.COLOR_BGR2RGB)
        texture = Texture.create(size=(emotion_image.shape[1], emotion_image.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        self.result_message.color = (1, 1, 1, 1)

        self.result_image.texture = texture

        if correct:
            self.result_message.text = "Você Acertou!"
            self._add_text_box(self.result_message, color=(0, 1, 0, 0.7))  # Fundo verde
        else:
            self.result_message.text = "Você Errou!"
            self._add_text_box(self.result_message, color=(1, 0, 0, 0.7))  # Fundo vermelho

    def on_button_press(self, instance):
        self.controller.current_emotion = None
        if self.controller.is_last_phase():
            self.manager.current = 'final_score_screen'
        else:
            self.controller.next_level()
            self.manager.current = 'game_screen'
