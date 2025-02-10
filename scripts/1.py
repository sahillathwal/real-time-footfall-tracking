import torch
import torch_tensorrt

# Dummy PyTorch model
class TestModel(torch.nn.Module):
    def forward(self, x):
        return x * 2

# Create and convert model
model = TestModel().cuda().eval()
input_data = torch.ones((1, 3, 224, 224), device="cuda")

trt_model = torch_tensorrt.compile(model, inputs=[torch_tensorrt.Input(input_data.shape)])

# Run inference
output = trt_model(input_data)
print("TensorRT Model Output Shape:", output.shape)
