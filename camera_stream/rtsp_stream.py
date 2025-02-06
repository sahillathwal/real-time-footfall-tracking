import cv2

RTSP_URL = "rtsp://USERNAME:PASSWORD@CAMERA_IP:PORT"

def get_rtsp_stream(rtsp_url):
    """Capture frames from an IP camera using RTSP."""
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Cannot open IP camera stream")
        return None
    return cap

def read_frame(cap):
    """Read a frame from the RTSP stream."""
    ret, frame = cap.read()
    if not ret:
        print("Error: Cannot read frame from IP camera")
        return None
    return frame