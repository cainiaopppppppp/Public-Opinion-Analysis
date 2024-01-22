import pandas as pd
import json

# 文件路径
file_path = 'F:/yuqing/Final/data_process/all.jsonl'

# 提取实体和关系的函数
def extract_entities_relations(record):
    # 提取实体
    entities = '; '.join([
        f"{e['label']}({e['start_offset']}-{e['end_offset']}): {record['text'][e['start_offset']:e['end_offset']]}"
        for e in record['entities']
    ])

    # 提取关系
    entity_map = {entity['id']: entity for entity in record['entities']}
    relations = '; '.join([
        f"{r['type']}<{record['text'][entity_map[r['from_id']]['start_offset']:entity_map[r['from_id']]['end_offset']]},{record['text'][entity_map[r['to_id']]['start_offset']:entity_map[r['to_id']]['end_offset']]}>"
        for r in record['relations']
    ])

    return entities, relations


# 用于处理数据的函数
def process_data(file_path):
    processed_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            record = json.loads(line)
            entities, relations = extract_entities_relations(record)
            processed_data.append([record['id'], record['text'], entities, relations])

    return pd.DataFrame(processed_data, columns=['ID', 'Text', 'Entities', 'Relations'])

# 处理数据
df = process_data(file_path)

# 查看处理后的数据
print(df.head())

# 将处理后的数据保存为CSV
output_path = 'F:/yuqing/Final/data_process/processed_data.csv'  # 更改为您的输出路径
df.to_csv(output_path, index=False)
