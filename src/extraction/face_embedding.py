from insightface.app import FaceAnalysis

class FaceEmbedding:
    def __init__(self):
        self.model = FaceAnalysis(name="buffalo_l")
        self.model.prepare(ctx_id=0)  # Use GPU (ctx_id=0)

    def extract_embedding(self, image):
        faces = self.model.get(image)
        return faces[0].normed_embedding if faces else None
