import sys
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        
        # Definindo a cor de fundo com um retângulo (sem bordas arredondadas)
        with self.canvas.before:
            Color(0.31, 0.42, 0.66, 1)  # Cor de fundo azul
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.size_hint = (0.6, 0.6)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        
        # Título
        title = Label(text="TCC", font_size='40sp', color=(1, 1, 1, 1))

        # Adiciona um espaçamento entre o título e os botões
        spacer = Widget(size_hint=(1, 0.2))  # Espaçamento (ajustar conforme necessário)
        
        # Botões arredondados
        button_jogar = self.create_rounded_button("Jogar", (0.4, 0.25, 0.2, 1), self.start_game)
        button_settings = self.create_rounded_button("Configuração", (0.5, 0.35, 0.25, 1), self.settings)
        button_sair = self.create_rounded_button("Sair", (0.5, 0.4, 0.3, 1), self.exit_game)
        
        # Adiciona os widgets ao layout
        layout.add_widget(title)
        layout.add_widget(spacer) 
        layout.add_widget(button_jogar)
        layout.add_widget(button_settings)
        layout.add_widget(button_sair)
        
        self.add_widget(layout)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def create_rounded_button(self, text, color, on_press=None, height=60, radius=20):
        # Função para criar botões com bordas arredondadas e altura ajustável
        btn = Button(text=text, font_size='20sp', size_hint=(1, None), height=height,  # Definindo altura do botão
                     background_normal='', background_down='',  # Remove imagens padrão
                     background_color=(0, 0, 0, 0))  # Fundo transparente para permitir o uso de Canvas
        
        # Armazena a cor como atributo do botão
        btn.button_color = color

        # Configurando canvas para criar um botão arredondado
        with btn.canvas.before:
            btn.rounded_rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[radius])  # Definindo o radius para controle do arredondamento
            btn.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        
        if on_press:
            btn.bind(on_press=on_press)
        
        return btn

    def update_rounded_rect(self, instance, *args):
        # Atualiza o tamanho e a posição do botão quando redimensionado
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*instance.button_color)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[20])  # Botões arredondados

    def start_game(self, instance):
        # Ação para iniciar o jogo
        self.manager.current = 'game_screen'

    def settings(self, instance):
        self.manager.current = 'settings_screen'

    def exit_game(self, instance):
        # Ação para sair do jogo
        App.get_running_app().stop()
        sys.exit()