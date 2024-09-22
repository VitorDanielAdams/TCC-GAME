from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

class FinalScoreScreen(Screen):
    def __init__(self, controller, **kwargs):
        super(FinalScoreScreen, self).__init__(**kwargs)
        self.controller = controller

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.size_hint = (0.8, 0.8)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        score_label = Label(text=f"Sua pontuação: {self.controller.scoring_model.get_score()}", font_size='40sp', color=(1, 1, 1, 1))
        layout.add_widget(score_label)

        back_button = Button(text="Voltar ao Menu", font_size='20sp', size_hint=(1, None), height=60)
        back_button.bind(on_press=self.back_to_menu)
        layout.add_widget(back_button)
        
        # Botão para jogar novamente
        replay_button = Button(text="Jogar Novamente", font_size='20sp', on_press=self.replay_game)
        layout.add_widget(replay_button)
        
        self.add_widget(layout)

    def back_to_menu(self, instance):
        self.manager.current = 'menu_screen'

    def replay_game(self, instance):
        """Reinicia o jogo a partir da primeira fase."""
        self.controller.scoring_model.reset_score()  # Reseta a pontuação
        self.manager.current = 'game_screen'