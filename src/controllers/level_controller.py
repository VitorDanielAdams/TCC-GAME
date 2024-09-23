from model.scoring_model import ScoringModel
import random

class LevelController:
    def __init__(self):
        self.level = 1
        self.total_rounds = 3  # Padrão inicial, pode ser configurado via tela de configurações
        self.scoring_model = ScoringModel()
        self.last_emotion = None
        self.current_emotion = None
        self.last_result = None

    def get_next_emotion(self):
        emotions = ["happy", "sad", "angry", "fear", "disgust", "surprise"]
        emotion = random.choice(emotions)

        # Evitar repetição da mesma emoção
        while emotion == self.last_emotion:
            emotion = random.choice(emotions)

        self.last_emotion = emotion
        return emotion

    def next_level(self):
        self.level += 1
        self.current_emotion = None
        if self.level > self.total_rounds:
            self.level = 1

    def set_total_rounds(self, rounds):
        self.total_rounds = rounds

    def set_result(self, correct, image):
        self.last_result = correct
        self.emotion_image = image
        if correct:
            self.scoring_model.add_score()

    def get_emotion_image(self):
        return self.emotion_image

    def is_correct(self):
        return self.last_result
    
    def is_last_phase(self):
        return self.level >= self.total_rounds

    def retry_same_emotion(self):
        self.last_result = None

    def reset_game(self):
        self.current_phase = 1
        self.last_result = None
        self.emotion_image = None
        self.current_emotion = None
        self.scoring_model.reset_score()