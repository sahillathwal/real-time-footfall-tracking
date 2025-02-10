import faiss
import numpy as np

res = faiss.StandardGpuResources()  # Allocate GPU resources
index = faiss.IndexFlatL2(512)  # 512D feature vector
gpu_index = faiss.index_cpu_to_gpu(res, 0, index)

# Create random embeddings for testing
embedding1 = np.random.random((1, 512)).astype("float32")
embedding2 = np.random.random((1, 512)).astype("float32")

# Add and search
gpu_index.add(embedding1)
D, I = gpu_index.search(embedding2, 1)

print("✅ FAISS-GPU Initialized")
print("✅ Similarity Distance:", D[0][0])
