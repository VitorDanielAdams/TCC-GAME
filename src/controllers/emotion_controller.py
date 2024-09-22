import cv2

class EmotionController:
    def __init__(self, model):
        self.model = model

    def capture_frames(self, video_source=0, num_frames=5):
        """Captura múltiplos frames da webcam."""
        cap = cv2.VideoCapture(video_source)
        frames = []
        
        for _ in range(num_frames):
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
        
        cap.release()
        return frames