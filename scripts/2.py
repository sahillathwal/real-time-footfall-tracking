import torch
import torch_tensorrt

class TestModel(torch.nn.Module):
    def forward(self, x):
        return x * 2

model = TestModel().cuda().eval()
input_data = torch.ones((1, 3, 224, 224), device="cuda")

output = model(input_data)
print("PyTorch Model Output Shape:", output.shape)
