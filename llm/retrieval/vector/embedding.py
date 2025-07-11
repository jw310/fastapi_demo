from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

def get_embedding(sentences, model: str = ""):
    # Load default model
    if model == "":
        try:
          model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
          embeddings = model.encode(sentences)

          return embeddings
        except Exception as e:
            raise(f"Error loading SentenceTransformer: {e}")

#Mean Pooling - Take attention mask into account for correct averaging
# def mean_pooling(model_output, attention_mask):
#     #第一個 model_output 的元素包含所有 token embeddings
#     token_embeddings = model_output[0]

#     # 對注意力遮罩進行擴展，在最後一個維度添加一個大小為 1 的新維度，使其形狀與單詞嵌入相同。這樣我們就可以逐個元素地將它們相乘。
#     input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()

#     # 單詞嵌入和擴展後的注意力遮罩進行逐元素相乘。1 表示沿著第二個維度求和，並除以每個句子中的實際單詞數量（由input_mask_expanded.sum(1)給出）。torch.clamp用於防止除以零。
#     return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


# # 要 embedding 的句字
# sentences = ["我會披星戴月的想你，我會奮不顧身的前進，遠方煙火越來越唏噓，凝視前方身後的距離",
#               "鯊魚寶寶 doo doo doo doo doo doo, 鯊魚寶寶"]

# # Load model
# tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
# model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# # # 把模型存到本地端
# # tokenizer.save_pretrained("nlp_models/all-MiniLM-L6-v2")
# # model.save_pretrained("nlp_models/all-MiniLM-L6-v2")

# # 分詞
# encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

# # 計算 token embeddings
# with torch.no_grad():
#     model_output = model(**encoded_input)

# # 使用 mean_pooling
# sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

# # dim 1 表示沿著第二個維度，並使用 L2 正規化
# sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

# print("Sentence embeddings:")
# print(sentence_embeddings)