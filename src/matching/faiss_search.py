import faiss
import numpy as np

class FAISSMatcher:
    def __init__(self):
        res = faiss.StandardGpuResources()  # GPU resources
        self.index = faiss.IndexHNSWFlat(512, 32)  # FAISS-GPU index
        self.index = faiss.index_cpu_to_gpu(res, 0, self.index)

    def add_embedding(self, person_id, embedding):
        self.index.add(np.array([embedding]).astype("float32"))

    def search_embedding(self, embedding):
        D, I = self.index.search(np.array([embedding]).astype("float32"), 1)
        return I[0][0] if D[0][0] < 0.6 else None
