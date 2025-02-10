import cv2

def resize_frame(frame, width=640, height=480):
    return cv2.resize(frame, (width, height))

def adjust_fps(cap, target_fps=30):
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int((1 / target_fps) * 1000)
    return max(1, delay - int(actual_fps))

if __name__ == "__main__":
    cap = cv2.VideoCapture("rtsp://admin:Proglint2024@10.0.120.109:554/live")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = resize_frame(frame)
        cv2.imshow("Processed Video", frame)
        if cv2.waitKey(adjust_fps(cap)) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
