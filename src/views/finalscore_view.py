from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle

class FinalScoreScreen(Screen):
    def __init__(self, controller, **kwargs):
        super(FinalScoreScreen, self).__init__(**kwargs)
        self.controller = controller
        
        # Definindo a cor de fundo azul
        with self.canvas.before:
            Color(0.31, 0.42, 0.66, 1)  # Cor de fundo azul
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.size_hint = (0.8, 0.8)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Label de pontuação
        self.score_label = Label(text=f"Sua pontuação: {self.controller.scoring_model.get_score()}", font_size='40sp', color=(1, 1, 1, 1))
        layout.add_widget(self.score_label)

        # Botão Voltar ao Menu
        back_button = self.create_rounded_button("Voltar ao Menu", (0.4, 0.25, 0.2, 1), self.back_to_menu)
        layout.add_widget(back_button)

        # Botão para Jogar Novamente
        replay_button = self.create_rounded_button("Jogar Novamente", (0.5, 0.35, 0.25, 1), self.replay_game)
        layout.add_widget(replay_button)

        self.add_widget(layout)

    def on_enter(self, *args):
        self.score_label.text = f"Sua pontuação: {self.controller.scoring_model.get_score()}"

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def create_rounded_button(self, text, color, on_press=None, height=60, radius=20):
        # Função para criar botões com bordas arredondadas
        btn = Button(text=text, font_size='20sp', size_hint=(1, None), height=height, background_normal='', background_down='', background_color=(0, 0, 0, 0))
        
        # Configura o canvas para criar um botão arredondado
        with btn.canvas.before:
            Color(*color)
            btn.rounded_rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[radius])
            btn.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        
        if on_press:
            btn.bind(on_press=on_press)

        return btn

    def update_rounded_rect(self, instance, *args):
        # Atualiza o tamanho e a posição do botão quando redimensionado
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.5, 0.4, 0.3, 1)  # Ajuste a cor conforme necessário
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[20])

    def back_to_menu(self, instance):
        self.controller.reset_game()
        self.controller.scoring_model.reset_score() 
        self.manager.current = 'menu_screen'

    def replay_game(self, instance):
        """Reinicia o jogo a partir da primeira fase."""
        self.controller.reset_game()
        self.controller.scoring_model.reset_score() 
        self.manager.current = 'game_screen'