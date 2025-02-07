# main script: footfall_tracking.py
from camera_stream.rtsp_stream import get_rtsp_stream, read_frame
from detection.face_detector import detect_people
from tracking.tracker import track_people
import cv2

def footfall_tracking(rtsp_url):
    """Track footfall in real-time from an IP camera using RTSP, DeepSORT, and MongoDB."""
    cap = get_rtsp_stream(rtsp_url)
    if cap is None:
        return
    
    while True:
        frame = read_frame(cap)
        if frame is None:
            break
        
        frame, boxes = detect_people(frame)
        frame, tracks = track_people(frame, boxes)
        cv2.imshow("Footfall Tracking", frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    RTSP_URL = "rtsp://admin:Proglint2024@10.0.120.109:554"
    footfall_tracking(RTSP_URL)