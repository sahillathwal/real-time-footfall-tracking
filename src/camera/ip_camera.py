import cv2
import threading

class IPCamera:
    def __init__(self, rtsp_url="rtsp://admin:Proglint2024@10.0.120.109:554/live"):
        self.rtsp_url = rtsp_url
        self.cap = cv2.VideoCapture(rtsp_url)
        self.frame = None
        self.running = True
        self.thread = threading.Thread(target=self._update_frame, daemon=True)
        self.thread.start()

    def _update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def get_frame(self):
        return self.frame

    def release(self):
        self.running = False
        self.cap.release()