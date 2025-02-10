import torch
import torch.onnx

class TestModel(torch.nn.Module):
    def forward(self, x):
        return x * 2

# Create model & input tensor
model = TestModel().cuda().eval()
input_tensor = torch.ones((1, 3, 224, 224), device="cuda")

# Export model to ONNX
onnx_model_path = "model.onnx"
torch.onnx.export(model, input_tensor, onnx_model_path, opset_version=11)

print("ONNX Model exported successfully.")

# Now parse with TensorRT
import tensorrt as trt

logger = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(logger)
network = builder.create_network(1)  # 1 = explicit batch
parser = trt.OnnxParser(network, logger)

with open(onnx_model_path, "rb") as f:
    if not parser.parse(f.read()):
        for error in range(parser.num_errors):
            print(parser.get_error(error))

print("ONNX Model Parsed Successfully")
