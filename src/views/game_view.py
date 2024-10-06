import random
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class GameScreen(Screen):
    def __init__(self, controller, video_controller, emotion_controller, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.controller = controller
        self.video_controller = video_controller
        self.emotion_controller = emotion_controller
        self.current_emotion = controller.last_emotion

        # Fundo da tela
        with self.canvas.before:
            Color(0.31, 0.42, 0.66, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Espaçamento superior entre o topo e os textos de fase e pontuação
        self.phase_label = Label(text="Fase: 1", font_size='20sp', color=(1, 1, 1, 1),
                                 size_hint=(None, None), size=(200, 50), pos_hint={'x': 0.05, 'y': 0.9})
        self.score_label = Label(text="Pontuação: 0", font_size='20sp', color=(1, 1, 1, 1),
                                 size_hint=(None, None), size=(200, 50), pos_hint={'x': 0.75, 'y': 0.9})
        
        self.layout.add_widget(self.phase_label)
        self.layout.add_widget(self.score_label)

        # Texto com instrução para o jogador
        self.instruction_label = Label(text="Ao final do tempo, imite a emoção", font_size='25sp', color=(1, 1, 1, 1),
                                       size_hint=(None, None), size=(300, 50), pos_hint={'x': 0.35, 'y': 0.80})
        self.layout.add_widget(self.instruction_label)

        # Temporizador no rodapé
        self.timer_label = Label(text="Tempo restante: 10s", font_size='20sp', color=(1, 1, 1, 1),
                                 size_hint=(None, None), size=(300, 50), pos_hint={'x': 0.35, 'y': 0.75})
        self.layout.add_widget(self.timer_label)


        # Texto da emoção (centralizado acima da imagem da esquerda)
        self.emotion_label = Label(text="Emoção", font_size='20sp', color=(1, 1, 1, 1),
                                   size_hint=(None, None), size=(200, 50), pos_hint={'x': 0.15, 'y': 0.63})
        self.layout.add_widget(self.emotion_label)

        # Imagem da emoção
        self.expression_image = Image(source="assets/images/happy.jpg", size_hint=(0.4, 0.4), pos_hint={'x': 0.05, 'y': 0.23})
        self.layout.add_widget(self.expression_image)

        # Imagem da webcam (centralizada)
        self.webcam_image = Image(size_hint=(0.4, 0.4), pos_hint={'x': 0.55, 'y': 0.23})
        self.layout.add_widget(self.webcam_image)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_enter(self, *args):
        # Inicia a exibição da webcam e o temporizador ao entrar na tela do jogo
        self.instruction_label.text = "Ao final do tempo, imite a emoção"
        self.phase_label.text = f"Fase: {self.controller.level}"
        Clock.schedule_interval(self.update_webcam, 1.0 / 60.0)
        self.start_phase(self.controller.level, self.controller.scoring_model.get_score())

    def update_webcam(self, dt):
        # Atualiza a textura da webcam
        texture = self.video_controller.get_texture()
        if texture:
            self.webcam_image.texture = texture

    def on_leave(self):
        # Para a exibição da webcam ao sair da tela
        Clock.unschedule(self.update_webcam)

    def start_phase(self, phase_number, score):
        # Define a fase e a pontuação
        self.phase_label.text = f"Fase: {phase_number}"
        self.score_label.text = f"Pontuação: {score}"
        
        # if self.controller.last_result is not None:
        self.current_emotion = self.controller.get_next_emotion()

        # Atualiza a imagem e o texto da emoção
        self.expression_image.source = f"assets/images/{self.current_emotion}/{random.randrange(0,1)}.jpg"

        self.emotion_label.text = self.emotion_controller.translate(self.current_emotion)
        
        # Reinicia o temporizador
        self.timer_seconds = 6
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.timer_seconds -= 1
        self.timer_label.text = f"Tempo restante: {self.timer_seconds}s"
        if self.timer_seconds == 0:
            Clock.unschedule(self.update_timer)
            self.instruction_label.text = "Imite a emoção"
            self.evaluate_emotion()

    def evaluate_emotion(self):
        frames = self.video_controller.capture_frames(5)
        result, result_image = self.emotion_controller.evaluate_emotion(frames, self.current_emotion)
        self.timer_seconds = 6

        if result:
            self.controller.set_result(correct=True, image=result_image) 
        else:
            self.controller.set_result(correct=False, image=result_image)

        self.manager.current = 'result_screen'
