from sentence_transformers import SentenceTransformer
def loadtokenizer():
    # モデルのロード（文書をベクトル化するためのモデル）
    model_tokenizer = SentenceTransformer('nlp-waseda/roberta-base-japanese')
    return model_tokenizer