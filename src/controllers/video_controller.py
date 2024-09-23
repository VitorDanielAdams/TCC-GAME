import cv2
from kivy.graphics.texture import Texture
from kivy.clock import Clock

class VideoController:
    def __init__(self):
        self.capture = None
        self.texture = None
        self.capturing = False

    def start_capture(self):
        if not self.capture:
            self.capture = cv2.VideoCapture(0)
            Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # Atualiza a cada 30 fps

    def update_frame(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            self.texture.blit_buffer(buf.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.texture.flip_vertical()
            self.capturing = True  # Marca que a captura está ativa

    def capture_frames(self, num_frames=5):
        frames = []
    
        for _ in range(num_frames):
            ret, frame = self.capture.read()
            if ret:
                frames.append(frame)
            else:
                break  
        
        return frames

    def is_capturing(self):
        """Retorna se a captura já está ativa."""
        return self.capturing

    def get_texture(self):
        return self.texture

    def stop_capture(self):
        if self.capture:
            self.capture.release()
            self.capture = None
            Clock.unschedule(self.update_frame)
