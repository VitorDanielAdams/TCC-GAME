from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.image import Image

class SettingsScreen(Screen):
    def __init__(self, controller, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.controller = controller

        # Imagem de fundo
        with self.canvas.before:
            self.bg_image = Image(source="assets/images/background.jpg", allow_stretch=True, keep_ratio=False,
                                  pos=self.pos, size=self.size)
            self.bind(size=self._update_background, pos=self._update_background)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.size_hint = (0.6, 0.8)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Título com destaque
        title = Label(text="Configurações", font_size='40sp', bold=True, color=(1, 1, 1, 1))
        self._add_text_box(title, (0.3, 0.3, 0.3, 0.8))
        layout.add_widget(title)

        # Texto para descrição
        description_label = Label(text="Quantidade de Rodadas:", font_size='20sp', color=(1, 1, 1, 1))
        self._add_text_box(description_label, (0.3, 0.3, 0.3, 0.8))
        layout.add_widget(description_label)

        # Select (Spinner) personalizado
        self.rounds_spinner = Spinner(
            text="Selecionar",
            values=["3 Rodadas", "5 Rodadas", "8 Rodadas", "10 Rodadas"],
            size_hint=(1, 0.5),
            background_normal='', background_color=(0.2, 0.3, 0.6, 1),
            color=(1, 1, 1, 1),  # Texto preto
            font_size='18sp'
        )
        self._add_spinner_box(self.rounds_spinner)
        layout.add_widget(self.rounds_spinner)

        back_button = self.create_rounded_button("Voltar", (0.2, 0.3, 0.6, 1), self.back_to_menu)
        save_button = self.create_rounded_button("Salvar", (0.2, 0.3, 0.6, 1), self.save_settings)

        layout.add_widget(back_button)
        layout.add_widget(save_button)

        self.add_widget(layout)

    def _update_background(self, *args):
        """Atualiza a imagem de fundo."""
        self.bg_image.size = self.size
        self.bg_image.pos = self.pos

    def _add_text_box(self, label, box_color):
        """Adiciona uma caixa arredondada atrás de um texto."""
        with self.canvas.before:
            Color(*box_color)
            rect = Rectangle(size=(label.size[0] + 40, label.size[1] + 20),
                                    pos=(label.pos[0] - 20, label.pos[1] - 10), radius=[15])
            label.bind(
                pos=lambda instance, value: setattr(rect, 'pos', (value[0] - 20, value[1] - 10)),
                size=lambda instance, value: setattr(rect, 'size', (value[0] + 40, value[1] + 20))
            )

    def _add_spinner_box(self, spinner):
        """Adiciona uma caixa arredondada ao Spinner."""
        with spinner.canvas.before:
            Color(0.5, 0.7, 1, 0.9)  # Cor azul mais claro
            spinner.spinner_rect = RoundedRectangle(size=spinner.size, pos=spinner.pos, radius=[10])
            spinner.bind(pos=lambda instance, value: setattr(spinner.spinner_rect, 'pos', value),
                         size=lambda instance, value: setattr(spinner.spinner_rect, 'size', value))

    def create_rounded_button(self, text, color, on_press=None):
        """Cria botões com bordas arredondadas e gradiente cinza."""
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
        """Atualiza o botão arredondado."""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*instance.button_color)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[20])

    def on_enter(self, *args):
        """Configura o valor inicial do Spinner."""
        current_rounds = self.controller.total_rounds
        self.rounds_spinner.text = f"{current_rounds} Rodadas"

    def back_to_menu(self, instance):
        """Volta para o menu principal."""
        self.manager.current = 'menu_screen'

    def save_settings(self, instance):
        """Salva a quantidade de rodadas selecionada."""
        selected_rounds = self.rounds_spinner.text
        rounds_number = int(selected_rounds.split()[0])  # Extrai o número do texto
        self.controller.set_total_rounds(rounds_number)
        self.back_to_menu(instance)