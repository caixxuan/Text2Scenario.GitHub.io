import json
import openai
import numpy as np

openai.api_key = "sk-zkztEtfhFH3GcCapyYgMBwtKkI5CKY48kkAPa0UnqzEMZzIImz42"
openai.base_url = "https://model-bridge.okeeper.com/v1/"

# 加载知识块
knowledge_chunks = []
kb_texts = []
with open('rag_knowledge_base.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        chunk = json.loads(line.strip())
        knowledge_chunks.append(chunk)
        text = f"{chunk.get('category','')}, {chunk.get('field','')}, {chunk.get('values','')}, {chunk.get('description','')}"
        kb_texts.append(text)

def get_embedding(text):
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def query_knowledge_base(query, top_k=8):
    query_emb = get_embedding(query)
    kb_embeddings = [get_embedding(text) for text in kb_texts]
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
    query = "创建一个自动驾驶在雾天行驶的仿真场景需要哪些参数？"
    results = query_knowledge_base(query, top_k=8)
    # print("检索到的关键知识块：")
    # for i, res in enumerate(results):
    #     print(f"Top {i+1}: {res['chunk']['description']}")
    #     print(json.dumps(res['chunk'], ensure_ascii=False, indent=2))
    context = "\n".join([f"{chunk['description']} 取值：{chunk['values']}" for chunk in [r['chunk'] for r in results]])
    prompt = f"""
            你是自动驾驶仿真场景专家。基于下面的参数定义和可选项，请自动组合成一个适用于
            “薄雾天和小雨情况下自车无保护左转，NPC车辆在主车后方右侧车道向前加速行驶”
            的仿真场景配置（以JSON形式输出）。
            如果某个参数与雾天强相关（如fog等），请选择合适的高取值。其余参数合理选择即可。只输出JSON场景配置。
            
            参考案例：输入“晴天且有微风天气下自动驾驶的跟车行驶场景”，
            输出“
                weather_density: 
                    sunny: 0.8
                    wind: 0.2
                time: daytime
                actors:
                ego_vehicle:
                    type: car
                    behavior: go forward
                
                npc_actor:
                    type: car
                    initial_position_relative_to_ego: front  # 相对于自车的初始位置
                    initial_lane_relative_to_ego: same lane  # 相对于自车的初始车道
                    oracle_of_npc_actor:  # 可组合成连贯行为序列
                    constant speed
                ”

            思维链提示：参考案例中“晴天”和“微风”表示"sunny"（选择0.8，程度较高）和“wind”（选择0.2，程度较低），
            跟车行驶表示至少有2辆车，且交通车辆（NPC）在前，自动驾驶车辆（ego）在后。

            参数定义和可选项如下：
            {context}
            """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    print("\nLLM生成的仿真场景参数：")
    print(response.choices[0].message.content)
