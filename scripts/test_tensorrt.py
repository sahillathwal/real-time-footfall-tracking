import tensorrt as trt

# Load TensorRT engine
engine_path = "models/face/yolov8-face.trt"
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

with open(engine_path, "rb") as f:
    runtime = trt.Runtime(TRT_LOGGER)
    engine = runtime.deserialize_cuda_engine(f.read())

print("✅ TensorRT Model Loaded Successfully:", engine_path)
print("✅ TensorRT Optimized for High-Speed Inference")
