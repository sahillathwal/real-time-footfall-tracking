import cv2

RTSP_URL = "rtsp://USERNAME:PASSWORD@CAMERA_IP:PORT"

def stream_camera():
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        print("Error: Cannot open RTSP stream")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to receive frame. Retrying...")
            break

        cv2.imshow("RTSP Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_camera()