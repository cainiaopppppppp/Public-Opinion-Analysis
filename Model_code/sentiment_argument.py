# sentiment_argument.py
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# 加载分词器和模型
model_dir = 'F:/yuqing/Final/models/bert-sentiment-20231203-184759'
tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertForSequenceClassification.from_pretrained(model_dir)

# 使用gpu
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

def extract_sentiments(texts):
    model.eval()
    sentiments = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)

        prediction = torch.argmax(outputs.logits, dim=1).item()
        label_map = {0: 'neutral', 1: 'positive', 2: 'negative'}
        sentiments.append(label_map[prediction])
    return sentiments

# 加载数据
file_path = 'F:/yuqing/Final/data_process/processed_data.csv'
data = pd.read_csv(file_path)

# 提取文本并进行情感分析
texts = data['Text'].tolist()
sentiments = extract_sentiments(texts)

# 解析实体和关系
def parse_entities_relations(row):
    if pd.isna(row['Entities']):
        return []
    else:
        entities = row['Entities'].split('; ')
        relations = row['Relations'].split('; ') if pd.notna(row['Relations']) else ['']*len(entities)
        return list(zip(entities, relations))

# 结合实体、关系和情感分析结果
rows = []
for index, row in data.iterrows():
    sentiment = sentiments[index]
    for entity, relation in parse_entities_relations(row):
        entity_type, entity_name = entity.split(': ')
        new_row = {
            'Entity': entity_name.strip(),
            'Relation': relation,
            'Sentiment': sentiment
        }
        rows.append(new_row)

graph_data = pd.DataFrame(rows)

# 显示结果
print(graph_data.head())

# 保存到新的CSV文件
output_file_path = 'F:/yuqing/Final/data_process/processed_data_sentiment.csv'
graph_data.to_csv(output_file_path, index=False)
