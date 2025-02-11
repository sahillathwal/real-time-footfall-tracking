import argparse
from src.camera.video_processing import VideoProcessor

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default="rtsp://admin:Proglint2024@10.0.120.109:554/live",
                        help="RTSP URL or local video file")
    args = parser.parse_args()

    processor = VideoProcessor(args.source)
    processor.process_video()
