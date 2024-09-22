from model.rmn_model import RMNModel
from model.scoring_model import ScoringModel
import random

class LevelController:
    def __init__(self):
        self.level = 1
        self.total_rounds = 3  # Padrão inicial, pode ser configurado via tela de configurações
        self.rmn_model = RMNModel()
        self.scoring_model = ScoringModel()
        self.last_emotion = None

    def get_next_emotion(self):
        emotions = ["felicidade", "tristeza", "raiva", "medo", "nojo", "surpresa"]
        emotion = random.choice(emotions)

        # Evitar repetição da mesma emoção
        while emotion == self.last_emotion:
            emotion = random.choice(emotions)

        self.last_emotion = emotion
        return emotion

    def evaluate_emotion(self, frames):
        """Avaliando a emoção com base nos frames capturados."""
        detected_emotion, confidence = self.rmn_model.recognize_expression(frames[0])  # Use o primeiro frame
        return detected_emotion, confidence

    def next_level(self):
        self.level += 1
        if self.level > self.total_rounds:
            self.level = 1

    def set_total_rounds(self, rounds):
        self.total_rounds = rounds
