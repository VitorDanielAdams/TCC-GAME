from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image

class FinalScoreScreen(Screen):
    def __init__(self, controller, **kwargs):
        super(FinalScoreScreen, self).__init__(**kwargs)
        self.controller = controller

        # Imagem de fundo
        with self.canvas.before:
            self.bg_image = Image(source="assets/images/background.jpg", allow_stretch=True, keep_ratio=False,
                                  pos=self.pos, size=self.size)
            self.bind(size=self._update_background, pos=self._update_background)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        layout.size_hint = (0.8, 0.8)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Imagem maior centralizada acima do texto
        self.trophy_image = Image(source="assets/images/result.png", size_hint=(0.7, 0.7), pos_hint={'center_x': 0.5, 'y': 0.48})
        layout.add_widget(self.trophy_image)

        # Pontuação com destaque (texto e caixa menor)
        self.score_label = Label(text="", font_size='30sp', bold=True, color=(1, 1, 1, 1))
        self._add_text_box(self.score_label, (0.5, 0.7, 1, 0.9), padding=(10, 10))  # Caixa azul clara reduzida
        layout.add_widget(self.score_label)

        # Botões com gradiente azul
        button_colors = [
            (0.1, 0.2, 0.5, 1),  # Azul escuro
            (0.3, 0.5, 0.8, 1)   # Azul claro
        ]

        back_button = self.create_rounded_button("Voltar ao Menu", button_colors[0], self.back_to_menu)
        replay_button = self.create_rounded_button("Jogar Novamente", button_colors[1], self.replay_game)

        layout.add_widget(back_button)
        layout.add_widget(replay_button)

        self.add_widget(layout)

    def on_enter(self, *args):
        """Atualiza as mensagens e a pontuação ao entrar na tela."""
        score = self.controller.scoring_model.get_score()
        self.score_label.text = f"Sua Pontuação: {score}"

    def _update_background(self, *args):
        """Atualiza a imagem de fundo."""
        self.bg_image.size = self.size
        self.bg_image.pos = self.pos

    def _add_text_box(self, label, box_color, padding=(40, 20)):
        """Adiciona uma caixa azul clara arredondada atrás do texto com padding."""
        with self.canvas.before:
            Color(*box_color)
            rect = RoundedRectangle(size=(label.size[0] + padding[0], label.size[1] + padding[1]),
                                    pos=(label.pos[0] - padding[0] // 2, label.pos[1] - padding[1] // 2), radius=[15])
            label.bind(
                pos=lambda instance, value: setattr(rect, 'pos', (value[0] - padding[0] // 2, value[1] - padding[1] // 2)),
                size=lambda instance, value: setattr(rect, 'size', (value[0] + padding[0], value[1] + padding[1]))
            )

    def create_rounded_button(self, text, color, on_press=None):
        """Cria botões com bordas arredondadas e gradiente azul."""
        btn = Button(text=text, font_size='20sp', size_hint=(1, None), height=60,
                     background_normal='', background_down='', background_color=(0, 0, 0, 0))
        btn.button_color = color
        with btn.canvas.before:
            Color(*color)
            btn.rounded_rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[20])
            btn.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        if on_press:
            btn.bind(on_press=on_press)
        return btn

    def update_rounded_rect(self, instance, *args):
        """Atualiza os botões arredondados."""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*instance.button_color)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[20])

    def back_to_menu(self, instance):
        """Volta ao menu principal."""
        self.controller.reset_game()
        self.controller.scoring_model.reset_score()
        self.manager.current = 'menu_screen'

    def replay_game(self, instance):
        """Reinicia o jogo."""
        self.controller.reset_game()
        self.controller.scoring_model.reset_score()
        self.manager.current = 'game_screen'