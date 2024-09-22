from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, RoundedRectangle

class SettingsScreen(Screen):
    def __init__(self, controller, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.controller = controller
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.size_hint = (0.6, 0.6)
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        title = Label(text="Configurações", font_size='40sp', color=(1, 1, 1, 1))

        # Botões de configuração para número de rodadas
        self.rounds_buttons = [
            self.create_rounded_button("3 Rodadas", (0.4, 0.25, 0.2, 1), self.set_rounds(3)),
            self.create_rounded_button("5 Rodadas", (0.5, 0.35, 0.25, 1), self.set_rounds(5)),
            self.create_rounded_button("8 Rodadas", (0.6, 0.45, 0.35, 1), self.set_rounds(8)),
            self.create_rounded_button("10 Rodadas", (0.7, 0.55, 0.45, 1), self.set_rounds(10)),
        ]
        
        layout.add_widget(title)
        for button in self.rounds_buttons:
            layout.add_widget(button)

        back_button = self.create_rounded_button("Voltar", (0.5, 0.4, 0.3, 1), self.back_to_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def create_rounded_button(self, text, color, on_press=None):
        btn = Button(text=text, font_size='20sp', size_hint=(1, None), height=60, background_normal='', background_down='', background_color=(0, 0, 0, 0))
        with btn.canvas.before:
            Color(*color)
            btn.rounded_rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[20])
            btn.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        if on_press:
            btn.bind(on_press=on_press)
        return btn

    def set_rounds(self, rounds):
        def inner(instance):
            self.controller.set_total_rounds(rounds)
            self.back_to_menu(None)
        return inner

    def update_rounded_rect(self, instance, *args):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[20])

    def back_to_menu(self, instance):
        self.manager.current = 'menu_screen'