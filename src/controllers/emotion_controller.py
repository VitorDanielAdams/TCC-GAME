import cv2
from model.rmn_model import RMNModel

class EmotionController:
    def __init__(self):
        self.rmn_model = RMNModel()

    def process_images(self, frame):
        detected_emotion, confidence, xmin, xmax, ymin, ymax = self.rmn_model.recognize_expression(frame)
        
        annotated_frame = frame.copy()
        cv2.rectangle(annotated_frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
        cv2.putText(annotated_frame, f"{detected_emotion} ({confidence:.2f})", 
                    (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        return detected_emotion, confidence, annotated_frame
    
    def evaluate_emotion(self, frames, expected_emotion):
        result = None
        max = 0
        result_image = frames[0]
        
        for frame in frames:
            emotion, probability, result_image = self.process_images(frame)
            if probability > 0.75 and probability > max:
                result = emotion
        
        if result == expected_emotion:
            return True, result_image
        return False, result_image
    
    def translate(self, emolabel):
        self.emo_dict = {
            'happy': 'Feliz',
            'sad': 'Triste',
            'neutral': 'Neutro',
            'disgust': 'Nojo',
            'fear': 'Medo',
            'angry': 'Bravo',
            'surprise': 'Surpreso'
        }

        return self.emo_dict.get(emolabel, 'Emoção desconhecida')