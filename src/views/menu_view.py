import sys
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        # Adiciona imagem de fundo
        with self.canvas.before:
            self.bg_image = Image(source="assets/images/background.jpg", allow_stretch=True, keep_ratio=False,
                                  pos=self.pos, size=self.size)
            self.bind(size=self._update_background, pos=self._update_background)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.size_hint = (0.7, 0.7)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Título com destaque
        title = Label(text="Expression Game TCC", font_size='40sp', bold=True, color=(1, 1, 1, 1),
                      size_hint=(1, 0.2))
        self._add_text_box(title, (0.1, 0.2, 0.5, 0.95))  # Caixa azul escura atrás
        layout.add_widget(title)

        # Espaçamento
        spacer = Widget(size_hint=(1, 0.1))
        layout.add_widget(spacer)

        # Gradiente de cores para os botões
        button_colors = [
            (0.1, 0.2, 0.4, 1),  # Azul mais escuro
            (0.2, 0.3, 0.6, 1),  # Azul intermediário
            (0.3, 0.5, 0.8, 1)   # Azul mais claro
        ]

        # Botões padronizados com cores em gradiente
        button_jogar = self.create_rounded_button("Jogar", button_colors[0], self.start_game)
        button_settings = self.create_rounded_button("Configuração", button_colors[1], self.settings)
        button_sair = self.create_rounded_button("Sair", button_colors[2], self.exit_game)

        # Adiciona os botões ao layout
        layout.add_widget(button_jogar)
        layout.add_widget(button_settings)
        layout.add_widget(button_sair)

        self.add_widget(layout)

    def _update_background(self, *args):
        """Atualiza a imagem de fundo."""
        self.bg_image.size = self.size
        self.bg_image.pos = self.pos

    def _add_text_box(self, label, box_color):
        """Adiciona uma caixa arredondada azul escura atrás de um texto."""
        with self.canvas.before:
            Color(*box_color)  # Cor azul escura
            rect = RoundedRectangle(size=(label.size[0] + 40, label.size[1] + 20),
                                    pos=(label.pos[0] - 20, label.pos[1] - 10), radius=[15])
            label.bind(
                pos=lambda instance, value: setattr(rect, 'pos', (value[0] - 20, value[1] - 10)),
                size=lambda instance, value: setattr(rect, 'size', (value[0] + 40, value[1] + 20))
            )

    def create_rounded_button(self, text, color, on_press=None):
        """Cria botões com bordas arredondadas e cor de fundo personalizada."""
        btn = Button(text=text, font_size='20sp', size_hint=(1, None), height=60,
                     background_normal='', background_down='', background_color=(0, 0, 0, 0))
        btn.button_color = color  # Define a cor do botão
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
            Color(*instance.button_color)  # Usa a cor definida explicitamente
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[20])

    def start_game(self, instance):
        """Ação para iniciar o jogo."""
        self.manager.current = 'loading_screen'

    def settings(self, instance):
        """Ação para abrir configurações."""
        self.manager.current = 'settings_screen'

    def exit_game(self, instance):
        """Ação para sair do jogo."""
        App.get_running_app().stop()
        sys.exit()
