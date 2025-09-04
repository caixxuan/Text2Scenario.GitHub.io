import yaml
import json

# 1. 读取yaml文件
with open('scenario_components.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

knowledge_chunks = []

# 2. weather_density
if 'weather_density' in data:
    for k, v in data['weather_density'].items():
        chunk = {
            "id": f"weather_density_{k}",
            "category": "weather_density",
            "field": k,
            "values": v,
            "description": f"{k}密度，取值范围0到1，0代表无，1代表最强。"
        }
        knowledge_chunks.append(chunk)

# 3. time
if 'time' in data:
    chunk = {
        "id": "time",
        "category": "time",
        "values": data['time'],
        "description": "一天中的时间段，包括：白天、早晨、中午、下午、黄昏、夜晚。"
    }
    knowledge_chunks.append(chunk)

# 4. road_type
if 'road_type' in data:
    chunk = {
        "id": "road_type",
        "category": "road_type",
        "values": data['road_type'],
        "description": "道路类型。"
    }
    knowledge_chunks.append(chunk)

# 5. road_maker
if 'road_maker' in data:
    chunk = {
        "id": "road_maker",
        "category": "road_maker",
        "values": data['road_maker'],
        "description": "道路标线类型。"
    }
    knowledge_chunks.append(chunk)

# 6. traffic-sign
if 'traffic-sign' in data:
    chunk = {
        "id": "traffic_sign",
        "category": "traffic_sign",
        "values": data['traffic-sign'],
        "description": "交通标志类型。"
    }
    knowledge_chunks.append(chunk)

# 7. actors
if 'actors' in data:
    for actor, fields in data['actors'].items():
        for key, value in fields.items():
            # 可嵌套oracle_of_npc_actor
            if isinstance(value, list):
                chunk = {
                    "id": f"actors_{actor}_{key}",
                    "category": "actors",
                    "actor": actor,
                    "field": key,
                    "values": value,
                    "description": f"{actor}的{key}选项。"
                }
                knowledge_chunks.append(chunk)
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    chunk = {
                        "id": f"actors_{actor}_{key}_{subkey}",
                        "category": "actors",
                        "actor": actor,
                        "field": key,
                        "subfield": subkey,
                        "values": subvalue,
                        "description": f"{actor}的{key}下的{subkey}选项。"
                    }
                    knowledge_chunks.append(chunk)

# 8. 输出为jsonl
with open('rag_knowledge_base.jsonl', 'w', encoding='utf-8') as f:
    for chunk in knowledge_chunks:
        f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

print("已生成 rag_knowledge_base.jsonl 知识库文件，每行为一个知识块。")