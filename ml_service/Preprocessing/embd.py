from sentence_transformers import SentenceTransformer
import numpy as np

class BulletEmbeddingProcessor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def process(self, data: dict) -> dict:
        """
        Extracts 'bullets_i' keys and generates 384D embeddings.
        Returns dict with raw embeddings only.
        """
        bullet_contents = []
        idx_list = []

        for key, value in data.items():
            if key.startswith("bullets_"):
                if not isinstance(value, str):
                    raise ValueError(f"{key} must contain a string")
                bullet_contents.append(value)
                idx_list.append(key.split("_")[1])

        if not bullet_contents:
            return {}

        raw_embeddings = self.model.encode(bullet_contents)
        raw_embeddings = np.array(raw_embeddings)

        output = {}
        for idx, content, emb in zip(idx_list, bullet_contents, raw_embeddings):
            output[f"bullet_{idx}"] = {
                "content": content,
                "embedding": emb.tolist()   # 384D vector
            }

        return output

# data = {
#     "bullets_1": "Worked on simulation of EV motor controllers and power electronics.",
#     "bullets_2": "Developed ML model for resume parsing using transformers.",
#     "text_1": "Some random text."
# }

# # Step 1: Generate 384D embeddings
# processor = BulletEmbeddingProcessor()
# res_embeddings = processor.process(data)
# print(res_embeddings)