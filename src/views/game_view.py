from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from controllers.emotion_controller import EmotionController

class GameScreen(Screen):
    def __init__(self, controller, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.controller = controller
        self.emotion_controller = EmotionController(controller.rmn_model)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        # Imagem da emoção atual
        self.expression_image = Image(source="assets/images/default.png", size_hint=(1, 0.4))
        layout.add_widget(self.expression_image)

        # Temporizador e resultado
        self.timer_label = Label(text="Tempo restante: 10s", font_size='25sp')
        layout.add_widget(self.timer_label)
        self.result_label = Label(text="", font_size='25sp')
        layout.add_widget(self.result_label)

        # Botões
        self.next_button = Button(text="Próxima Fase", font_size='20sp', disabled=True)
        self.retry_button = Button(text="Tente Novamente", font_size='20sp', disabled=True)

        layout.add_widget(self.next_button)
        layout.add_widget(self.retry_button)

        self.add_widget(layout)
        self.start_phase()

    def start_phase(self):
        self.current_emotion = self.controller.get_next_emotion()
        self.expression_image.source = f"assets/images/{self.current_emotion}.png"
        self.timer_seconds = 10
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.timer_seconds -= 1
        if self.timer_seconds == 0:
            Clock.unschedule(self.update_timer)
            self.evaluate_expression()

    def evaluate_expression(self):
        frames = self.emotion_controller.capture_frames()
        detected_emotion, confidence = self.controller.evaluate_emotion(frames)

        if detected_emotion == self.current_emotion:
            self.result_label.text = f"Acertou! ({confidence:.2f}% de confiança)"
            self.next_button.disabled = False
        else:
            self.result_label.text = f"Errou! ({confidence:.2f}% de confiança)"
            self.retry_button.disabled = False