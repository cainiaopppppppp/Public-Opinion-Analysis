import torch
from torch.utils.data import DataLoader, random_split
from torch.utils.data.dataset import Subset
from transformers import BertTokenizerFast, BertModel
import torch.nn as nn
from datetime import datetime

from data_loader import RelationExtractionDataset
from model_enity import RelationExtractionModel

# 检查CUDA是否可用并设置设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("Using device:", device)

def calculate_entity_accuracy(logits, labels):
    # logits: (batch_size, seq_length, num_labels)
    # labels: (batch_size, seq_length)
    preds = torch.argmax(logits, dim=2)
    mask = (labels != -100)  # 忽略掉标签为-100的位置（例如padding位置）
    correct = torch.sum((preds == labels) * mask)
    total = torch.sum(mask)
    if total.item() == 0:
        return 0
    return correct.item() / total.item()

def calculate_relation_accuracy(logits, labels):
    # logits: (batch_size, num_relations)
    # labels: (batch_size, num_relations)
    preds = torch.sigmoid(logits) > 0.5  # 使用阈值0.5来确定预测标签
    correct = torch.sum((preds == labels).all(dim=1)).item()  # 所有关系都预测正确的样本数
    total = labels.size(0)
    return correct / total

def train_model(model, train_dataloader, val_dataloader, optimizer, num_epochs=30, patience=10):
    best_loss = float('inf')

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for batch in train_dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            token_type_ids = batch['token_type_ids'].to(device)
            entity_labels = batch['entity_labels'].to(device)
            relation_labels = batch['relation_labels'].to(device)

            optimizer.zero_grad()
            entity_logits, relation_logits = model(input_ids, attention_mask, token_type_ids)

            entity_loss = nn.CrossEntropyLoss()(entity_logits.view(-1, len(RelationExtractionDataset.ENTITY_LABELS)), entity_labels.view(-1))
            relation_loss = nn.BCEWithLogitsLoss()(relation_logits, relation_labels.float())

            loss = entity_loss + relation_loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_dataloader)
        print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {avg_loss:.4f}")

        # 评估部分
        entity_accuracy, relation_accuracy = evaluate_model(model, val_dataloader)
        print(f"Validation Entity Accuracy: {entity_accuracy:.4f}")
        print(f"Validation Relation Accuracy: {relation_accuracy:.4f}")

        # 检查是否有改善
        if avg_loss < best_loss:
            best_loss = avg_loss
            no_improve_epochs = 0
            # 保存最好的模型
            current_time = datetime.now().strftime('%Y%m%d-%H%M%S')
            torch.save(model.state_dict(), f'D:/Dp/Final/models/entity-best_model-{current_time}.pth')
            print("Model saved as best_model.pth")
        else:
            no_improve_epochs += 1
            if no_improve_epochs >= patience:
                print("Early stopping")
                break

def evaluate_model(model, dataloader):
    model.eval()
    total_entity_accuracy, total_relation_accuracy = 0, 0
    total_samples = 0

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            token_type_ids = batch['token_type_ids'].to(device)
            entity_labels = batch['entity_labels'].to(device)
            relation_labels = batch['relation_labels'].to(device)

            entity_logits, relation_logits = model(input_ids, attention_mask, token_type_ids)

            entity_accuracy = calculate_entity_accuracy(entity_logits, entity_labels)
            relation_accuracy = calculate_relation_accuracy(relation_logits, relation_labels)

            total_entity_accuracy += entity_accuracy
            total_relation_accuracy += relation_accuracy
            total_samples += 1

    avg_entity_accuracy = total_entity_accuracy / total_samples
    avg_relation_accuracy = total_relation_accuracy / total_samples

    return avg_entity_accuracy, avg_relation_accuracy


    # print(f"Entity Accuracy: {entity_accuracy:.4f}")
    # print(f"Relation Accuracy: {relation_accuracy:.4f}")



# 加载数据
tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
full_dataset = RelationExtractionDataset('F:/yuqing/Final/data_process/processed_data.csv', tokenizer, max_length=128)

# 划分数据集
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

# 创建数据加载器
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=32)

# 初始化模型并移到GPU
bert_model = BertModel.from_pretrained('bert-base-chinese')
model = RelationExtractionModel(
    bert_model,
    len(RelationExtractionDataset.ENTITY_LABELS),
    len(RelationExtractionDataset.RELATION_LABELS)
).to(device)

# 设置优化器
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

# 训练和评估模型
train_model(model, train_dataloader, val_dataloader, optimizer, num_epochs=30, patience=10)
