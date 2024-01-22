from transformers import BertTokenizer, BertModel
import torch
import pandas as pd

# 加载预训练模型和分词器
tokenizer = BertTokenizer.from_pretrained('F:/yuqing/Final/bert-base-chinese/')
model = BertModel.from_pretrained('F:/yuqing/Final/bert-base-chinese/')

# 加载数据
file_path = 'F:/yuqing/Final/data_process/processed_data.csv'  # 替换为您的文件路径
data = pd.read_csv(file_path)

# 实体识别函数
def entity_recognition(text):
    # 对文本进行编码
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)

    # 获取编码后的最后一层隐藏状态
    last_hidden_states = outputs.last_hidden_state
    tokenized_text = tokenizer.tokenize(text)

    entities = []
    current_entity = ""
    for token, state in zip(tokenized_text, last_hidden_states[0]):
        if token.startswith("##"):
            current_entity += token[2:]
        else:
            if current_entity:
                entities.append(current_entity)
                current_entity = ""
            current_entity = token

    # 添加最后一个实体
    if current_entity:
        entities.append(current_entity)

    return entities

# 应用实体识别
data['Entities'] = data['Cleaned Text'].apply(lambda text: entity_recognition(text) if pd.notna(text) else [])

# 导出数据到CSV
export_path = 'F:/yuqing/Final/data_process/processed_data_with_entities.csv'  # 指定导出文件的路径
data.to_csv(export_path, index=False)

# 展示部分结果
print(data[['Cleaned Text', 'Entities']].head())
