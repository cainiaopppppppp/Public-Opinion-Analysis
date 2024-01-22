from transformers import BertTokenizer, BertForSequenceClassification
import torch
import pandas as pd

# 加载数据（假设你有一个带有文本、实体和关系标签的数据集）
file_path = 'F:/yuqing/Final/data_process/processed_data_with_entities.csv'
data = pd.read_csv(file_path)
num_labels = data['Relations'].nunique()

# 加载预训练模型和分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=41)

# 关系分类函数
def classify_relation(text, entities):
    if len(entities) < 2:
        return None  # 如果实体少于两个，则无法分类关系

    # 取出前两个实体作为实体1和实体2
    entity1, entity2 = entities[:2]

    # 将实体添加到文本中以形成输入序列
    input_sequence = f"{entity1} [SEP] {entity2} [SEP] {text}"

    # 对输入序列进行编码
    inputs = tokenizer(input_sequence, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)

    # 获取预测结果
    predictions = torch.argmax(outputs.logits, dim=1)

    return predictions.item()

# 应用关系分类
# 假设你的数据集中有列 'Entity1', 'Entity2', 和 'Text'
data['Predicted Relation'] = data.apply(lambda row: classify_relation(row['Cleaned Text'], row['Entities']), axis=1)

# 导出数据
export_path = 'F:/yuqing/Final/data_process/processed_data_entities_classify.csv'
data.to_csv(export_path, index=False)

# 展示部分结果
print(data[['Cleaned Text', 'Entities', 'Predicted Relation']].head())
