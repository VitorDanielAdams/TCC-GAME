from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle

class SettingsScreen(Screen):
    def __init__(self, controller, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.controller = controller

        # Fundo azul
        with self.canvas.before:
            Color(0.31, 0.42, 0.66, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[0])
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.size_hint = (0.6, 0.6)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Título da tela
        title = Label(text="Configurações", font_size='40sp', color=(1, 1, 1, 1), size_hint=(1, 0.2))
        layout.add_widget(title)

        # Texto pequeno para descrição
        description_label = Label(text="Quantidade de rodadas:", font_size='20sp', color=(1, 1, 1, 1), size_hint=(1, 0.1))
        layout.add_widget(description_label)

        # Select para quantidade de rodadas (Spinner)
        self.rounds_spinner = Spinner(
            text="",
            values=["3 Rodadas", "5 Rodadas", "8 Rodadas", "10 Rodadas"],
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.rounds_spinner)

        # Botão "Voltar"
        back_button = self.create_rounded_button("Voltar", (0.5, 0.4, 0.3, 1), self.back_to_menu)
        layout.add_widget(back_button)

        # Botão "Salvar"
        save_button = self.create_rounded_button("Salvar", (0.5, 0.4, 0.3, 1), self.save_settings)
        layout.add_widget(save_button)

        self.add_widget(layout)

    def on_enter(self, *args):
        # Configura o valor inicial do Spinner com base na configuração atual do controller
        current_rounds = self.controller.total_rounds
        self.rounds_spinner.text = f"{current_rounds} Rodadas"

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def create_rounded_button(self, text, color, on_press=None):
        btn = Button(text=text, font_size='20sp', size_hint=(1, None), height=60, background_normal='', background_down='', background_color=(0, 0, 0, 0))
        with btn.canvas.before:
            btn.button_color = color
            btn.rounded_rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[20])
            btn.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        if on_press:
            btn.bind(on_press=on_press)
        return btn

    def update_rounded_rect(self, instance, *args):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*instance.button_color)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[20])

    def back_to_menu(self, instance):
        self.manager.current = 'menu_screen'

    def save_settings(self, instance):
        # Lógica para salvar a quantidade de rodadas
        selected_rounds = self.rounds_spinner.text
        rounds_number = int(selected_rounds.split()[0])  # Extrai o número do texto
        self.controller.set_total_rounds(rounds_number)
        self.back_to_menu(instance)
