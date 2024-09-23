from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class LoadingScreen(Screen):
    def __init__(self, video_controller, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.video_controller = video_controller  # Controlador de vídeo
        self.capture_started = False

        # Fundo azul
        with self.canvas.before:
            Color(0.31, 0.42, 0.66, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        layout.size_hint = (0.6, 0.6)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Texto "Carregando..."
        self.label = Label(text="Carregando...", font_size='30sp', color=(1, 1, 1, 1), size_hint=(1, 0.2))
        layout.add_widget(self.label)

        # Barra de progresso
        self.progress_bar = ProgressBar(max=100, size_hint=(1, 0.2))
        layout.add_widget(self.progress_bar)

        self.add_widget(layout)

        # Valor de progresso
        self.progress_value = 0

    def on_enter(self, *args):
        """Inicia o carregamento e a captura da câmera."""
        Clock.schedule_interval(self.update_progress, 1 / 30.0)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_progress(self, dt):
        if self.progress_value < 70:
            # Progresso inicial até 70% antes de iniciar a câmera
            self.progress_value += (70 / (10 * 30))  # Avança em 10 segundos * 30fps
        elif not self.capture_started:
            # Inicializa a captura de vídeo e espera até estar ativo
            self.video_controller.start_capture()
            self.capture_started = True
        else:
            # Verifica se a câmera está capturando e completa o progresso
            if self.video_controller.is_capturing():
                self.progress_value += (30 / (2 * 60))  # Completa os 30% restantes em 5 segundos * 60fps

        self.progress_bar.value = self.progress_value

        if self.progress_value >= 100:
            Clock.unschedule(self.update_progress)
            # Transição para a tela do jogo
            self.manager.current = 'game_screen'
