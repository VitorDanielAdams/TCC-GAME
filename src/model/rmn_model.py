from rmn import RMN

class RMNModel:
    def __init__(self):
        self.model = RMN()

    def recognize_expression(self, frame):
        results = self.model.detect_emotion_for_single_frame(frame)
        if results:
            result = results[0]
            return result['emo_label'], result['emo_proba'], result['xmin'], result['xmax'], result['ymin'], result['ymax']

        return None, 0.0, {}