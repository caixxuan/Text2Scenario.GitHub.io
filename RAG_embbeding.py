import json
import openai
import numpy as np
import yaml

openai.api_key = "sk-zkztEtfhFH3GcCapyYgMBwtKkI5CKY48kkAPa0UnqzEMZzIImz42"
openai.base_url = "https://model-bridge.okeeper.com/v1/"

def get_embedding(text):
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

# 1. 加载知识库
knowledge_chunks = []
kb_texts = []
with open('rag_knowledge_base.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        chunk = json.loads(line.strip())
        knowledge_chunks.append(chunk)
        text = f"{chunk.get('category','')}, {chunk.get('field','')}, {chunk.get('values','')}, {chunk.get('description','')}"
        kb_texts.append(text)

# 2. 生成知识库embedding（首次运行建议批量生成并缓存）
kb_embeddings = [get_embedding(text) for text in kb_texts]

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def query_knowledge_base(query, top_k=3):
    query_emb = get_embedding(query)
    sims = [cosine_similarity(query_emb, emb) for emb in kb_embeddings]
    idxs = np.argsort(sims)[::-1][:top_k]
    results = []
    for i in idxs:
        results.append({
            "score": float(sims[i]),
            "chunk": knowledge_chunks[i]
        })
    return results

if __name__ == "__main__":
    query = input("请输入你的问题：")
    results = query_knowledge_base(query)
    print("\n最相关的知识块：")
    for i, res in enumerate(results):
        print(f"Top {i+1}: 相似度分数：{res['score']:.4f}")
        print(json.dumps(res['chunk'], ensure_ascii=False, indent=2))
