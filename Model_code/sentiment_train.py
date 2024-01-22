from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
import torch
import pandas as pd
from datetime import datetime

# 检查CUDA是否可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 加载数据
file_path = 'F:/yuqing/Final/data/sentiment1.csv'
data = pd.read_csv(file_path)

# 情感标签映射
label_map = {'neutral': 0, 'positive': 1, 'negative': 2}
data['label'] = data['label'].map(label_map)


# 数据集类
class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, item):
        text = str(self.texts[item])
        label = self.labels[item]

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
        )

        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


# 分割数据集
train_data, test_data = train_test_split(data, test_size=0.1)
train_texts = train_data['text'].tolist()
train_labels = train_data['label'].tolist()
test_texts = test_data['text'].tolist()
test_labels = test_data['label'].tolist()

# 参数设置
MAX_LEN = 128
BATCH_SIZE = 16
EPOCHS = 4

# 加载预训练模型和分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=3)

# 将模型移动到GPU
model = model.to(device)

# 创建数据加载器
train_dataset = SentimentDataset(train_texts, train_labels, tokenizer, MAX_LEN)
train_data_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE)

validation_dataset = SentimentDataset(test_texts, test_labels, tokenizer, MAX_LEN)
validation_data_loader = DataLoader(validation_dataset, batch_size=BATCH_SIZE)

# 训练模型
optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)

for epoch in range(EPOCHS):
    model.train()
    total_train_loss = 0
    for batch in train_data_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        model.zero_grad()
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_train_loss += loss.item()
        loss.backward()
        optimizer.step()

    avg_train_loss = total_train_loss / len(train_data_loader)
    print(f"Epoch {epoch + 1}/{EPOCHS}, Average Training Loss: {avg_train_loss:.4f}")

    # 在验证集上评估模型
    model.eval()
    total_eval_loss = 0
    for batch in validation_data_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        total_eval_loss += outputs.loss.item()

    avg_val_loss = total_eval_loss / len(validation_data_loader)
    print(f"Epoch {epoch + 1}/{EPOCHS}, Average Validation Loss: {avg_val_loss:.4f}")

# 当前日期和时间
current_time = datetime.now().strftime('%Y%m%d-%H%M%S')
model_save_path = f'F:/yuqing/Final/models/bert-sentiment-{current_time}'

# 保存模型和分词器
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)
