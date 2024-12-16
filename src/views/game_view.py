import random
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle, RoundedRectangle

class GameScreen(Screen):
    def __init__(self, controller, video_controller, emotion_controller, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.controller = controller
        self.video_controller = video_controller
        self.emotion_controller = emotion_controller
        self.current_emotion = controller.last_emotion

        # Fundo azul com sobreposição de imagem PNG (preenche a janela toda)
        with self.canvas.before:
            Color(0.31, 0.42, 0.66, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.bg_image = Image(source="assets/images/background.jpg", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg_image)

        # Layout principal
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Labels superiores
        self.phase_label = Label(text="Fase: 1", font_size='24sp', bold=True, color=(1, 1, 1, 1),
                                size_hint=(None, None), size=(200, 50), pos_hint={'x': 0.05, 'y': 0.9})
        self._add_text_box(self.phase_label)
        self.layout.add_widget(self.phase_label)

        self.score_label = Label(text="Pontos: ", font_size='24sp', bold=True, color=(1, 1, 1, 1),
                                 size_hint=(None, None), size=(200, 50), pos_hint={'x': 0.70, 'y': 0.9})
        self._add_text_box(self.score_label)
        self.layout.add_widget(self.score_label)

        # Instrução central
        self.instruction_label = Label(text="Imite a expressão mostrada!", font_size='28sp', bold=True, color=(1, 1, 1, 1),
                                        size_hint=(None, None), size=(400, 50), pos_hint={'x': 0.25, 'y': 0.78})
        self._add_text_box(self.instruction_label)
        self.layout.add_widget(self.instruction_label)

        # Texto da emoção (centralizado acima da imagem da esquerda)
        self.emotion_label = Label(text="Emoção", font_size='24sp', bold=True, color=(1, 1, 1, 1),
                                    size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.25, 'y': 0.3})
        self.layout.add_widget(self.emotion_label)

        # Imagem da emoção (lado esquerdo)
        self.expression_image = Image(source="assets/images/happy.jpg", size_hint=(0.4, 0.35),
                                    pos_hint={'center_x': 0.25, 'y': 0.4})
        self.layout.add_widget(self.expression_image)

        # Webcam (lado direito)
        self.webcam_image = Image(size_hint=(0.4, 0.4), pos_hint={'center_x': 0.75, 'y': 0.35})
        self.layout.add_widget(self.webcam_image)

        # Barra de progresso e texto do temporizador
        self.timer_label = Label(text="6", font_size='24sp', bold=True, color=(1, 1, 0, 1),
                                size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'y': 0.2})
        self._add_text_box(self.timer_label)
        self.layout.add_widget(self.timer_label)

        self.progress_bar = ProgressBar(max=6, value=6, size_hint=(0.8, 0.05),
                                        pos_hint={'center_x': 0.5, 'y': 0.1})
        self.layout.add_widget(self.progress_bar)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.bg_image.size = self.size

    def _add_text_box(self, label):
        with self.layout.canvas.before:
            Color(0.31, 0.42, 0.66, 0.95)  # Azul translúcido
            rect = RoundedRectangle(size=(label.size[0] + 20, label.size[1] + 10),
                                    pos=(label.pos[0] - 10, label.pos[1] - 5), radius=[10])
            label.bind(
                pos=lambda instance, value: setattr(rect, 'pos', (value[0] - 10, value[1] - 5)),
                size=lambda instance, value: setattr(rect, 'size', (value[0] + 20, value[1] + 10))
            )

    def on_enter(self, *args):
        self.phase_label.text = f"Fase: {self.controller.level}"
        Clock.schedule_interval(self.update_webcam, 1.0 / 60.0)
        self.start_phase(self.controller.level, self.controller.scoring_model.get_score())

    def update_webcam(self, dt):
        texture = self.video_controller.get_texture()
        if texture:
            self.webcam_image.texture = texture

    def on_leave(self):
        Clock.unschedule(self.update_webcam)

    def start_phase(self, phase_number, score):
        self.phase_label.text = f"Fase: {phase_number}"
        self.score_label.text = f"Pontuação: {score}"
        self.current_emotion = self.controller.get_next_emotion()

        # Atualiza a imagem e o texto da emoção
        self.expression_image.source = f"assets/images/{self.current_emotion}/{random.randrange(0,2)}.jpg"
                
        # Reinicia o temporizador
        self.timer_seconds = 6
        self.progress_bar.value = 6
        self.timer_label.text = f"{self.timer_seconds}"
        Clock.schedule_interval(self.update_timer, 1)
        self.emotion_label.text = self.emotion_controller.translate(self.current_emotion)

    def update_timer(self, dt):
        self.timer_seconds -= 1
        self.progress_bar.value = self.timer_seconds

        # Altera a cor do texto e da barra
        if self.timer_seconds > 3:
            self.timer_label.color = (1, 1, 0, 1)  # Amarelo
            self.progress_bar.background_color = (0, 0.6, 1, 1)  # Azul
        elif self.timer_seconds <= 3:
            self.timer_label.color = (1, 0, 0, 1)  # Vermelho
            self.progress_bar.background_color = (1, 0, 0, 1)  # Vermelho

        self.timer_label.text = f"{self.timer_seconds}"
        if self.timer_seconds <= 0:
            Clock.unschedule(self.update_timer)
            self.evaluate_emotion()

    def evaluate_emotion(self):
        frames = self.video_controller.capture_frames(5)
        result, result_image = self.emotion_controller.evaluate_emotion(frames, self.current_emotion)
        self.instruction_label.text = "Processando..."
        self.timer_label.color = (1, 1, 0, 1)

        if result:
            self.controller.set_result(correct=True, image=result_image)
        else:
            self.controller.set_result(correct=False, image=result_image)
        
        self.instruction_label.text = "Imite a expressão mostrada!"
        self.manager.current = 'result_screen'