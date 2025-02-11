import cv2
from src.camera.ip_camera import IPCamera
from src.tracking.multi_person_tracker import MultiPersonTracker

class VideoProcessor:
    def __init__(self, video_source):
        self.video_source = video_source
        self.camera = IPCamera(video_source) if video_source.startswith("rtsp://") else cv2.VideoCapture(video_source)
        self.tracker = MultiPersonTracker()

    def process_video(self):
        while True:
            frame = self.camera.get_frame() if isinstance(self.camera, IPCamera) else self.camera.read()[1]
            if frame is None:
                continue

            frame = self.tracker.track_people(frame)

            cv2.imshow("Real-Time Tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.camera.release()
        cv2.destroyAllWindows()
