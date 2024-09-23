class ScoringModel:
    def __init__(self):
        self.score = 0

    def add_score(self, points=1):
        self.score += points

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score