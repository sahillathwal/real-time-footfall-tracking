import torch

# Allocate a dummy tensor to force memory allocation
dummy_tensor = torch.randn(1024, 1024, device="cuda")
print("✅ PyTorch Version:", torch.__version__)
print("✅ CUDA Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("✅ CUDA Version:", torch.version.cuda)
    print("✅ cuDNN Version:", torch.backends.cudnn.version())
    print("✅ GPU Name:", torch.cuda.get_device_name(0))
    print("✅ GPU Memory Allocated:", torch.cuda.memory_allocated(0) / 1024**3, "GB")
    print("✅ GPU Memory Reserved:", torch.cuda.memory_reserved(0) / 1024**3, "GB")
else:
    print("❌ CUDA not detected. Check your installation.")
