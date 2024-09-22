from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from views.menu_view import MenuScreen
from views.game_view import GameScreen
from views.settings_view import SettingsScreen
from views.finalscore_view import FinalScoreScreen
from controllers.level_controller import LevelController

class ExpressionGameApp(App):
    def build(self):
        controller = LevelController()
        sm = ScreenManager()

        # Adicionando telas ao gerenciador de telas
        sm.add_widget(MenuScreen(name='menu_screen'))
        sm.add_widget(GameScreen(controller, name='game_screen'))
        sm.add_widget(SettingsScreen(controller, name='settings_screen'))
        sm.add_widget(FinalScoreScreen(controller, name='final_score_screen'))

        return sm

if __name__ == "__main__":
    ExpressionGameApp().run()