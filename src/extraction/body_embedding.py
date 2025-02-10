import torch
import torchreid

class BodyEmbedding:
    def __init__(self):
        self.model = torchreid.models.build_model("transreid", num_classes=1000, pretrained=True).cuda()
        self.model.eval()

    def extract_embedding(self, image):
        input_tensor = torch.Tensor(image.transpose(2, 0, 1)).unsqueeze(0).cuda()
        with torch.no_grad():
            return self.model(input_tensor).cpu().numpy()
