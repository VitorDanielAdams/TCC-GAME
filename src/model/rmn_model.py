from rmn import RMN

class RMNModel:
    def __init__(self):
        self.model = RMN()

    def recognize_expression(self, frame):
        results = self.model.detect_emotion_for_single_frame(frame)
        if results:
            return results[0]['emo_label'], results[0]['emo_proba']
        return None, 0.0