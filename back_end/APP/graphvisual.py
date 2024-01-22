from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
from transformers import BertTokenizerFast, BertModel
from .model_enity import RelationExtractionModel
from .data_loader import RelationExtractionDataset
import pandas as pd
import torch

app = Flask(__name__)
CORS(app)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 加载模型
def load_model(model_path):
    # 确保此处的模型参数与训练时一致
    bert_model = BertModel.from_pretrained('bert-base-chinese')
    model = RelationExtractionModel(
        bert_model,
        len(RelationExtractionDataset.ENTITY_LABELS),
        len(RelationExtractionDataset.RELATION_LABELS),
        lstm_hidden_size=128,  # 确保与训练时的参数一致
        num_lstm_layers=1,     # 确保与训练时的参数一致
        dropout_prob=0.1       # 确保与训练时的参数一致
    ).to(device)

    model.load_state_dict(torch.load(model_path, map_location=device))
    return model

# 反转标签字典
def reverse_dict(input_dict):
    return {value: key for key, value in input_dict.items()}

# 处理模型输出
def process_model_output(entity_logits, relation_logits, tokens):
    entity_label_map = reverse_dict(RelationExtractionDataset.ENTITY_LABELS)
    relation_label_map = reverse_dict(RelationExtractionDataset.RELATION_LABELS)

    entity_preds = torch.argmax(entity_logits, dim=2)
    print(entity_preds)
    relation_preds = torch.sigmoid(relation_logits) > 0.4
    print(relation_preds)

    entities = []
    current_entity = []
    for label, token in zip(entity_preds[0], tokens):
        label_str = entity_label_map.get(label.item(), "O")
        if label_str.startswith("B-"):
            if current_entity:
                entities.append(" ".join(current_entity))
                current_entity = []
            current_entity.append(token)
        elif label_str.startswith("I-") and current_entity:
            current_entity.append(token)
        else:
            if current_entity:
                entities.append(" ".join(current_entity))
                current_entity = []

    # Add the last entity if any
    if current_entity:
        entities.append(" ".join(current_entity))

    nodes = [{"id": idx + 1, "label": entity} for idx, entity in enumerate(entities)]

    edges = []
    for i, is_related in enumerate(relation_preds[0]):
        if is_related:
            relation_label = relation_label_map.get(i, "N/A")
            entities = relation_label.split('-')
            if len(entities) < 2:
                continue
            source_label, target_label = entities
            source = next((node['id'] for node in nodes if node['label'].startswith(source_label)), None)
            target = next((node['id'] for node in nodes if node['label'].startswith(target_label)), None)
            if source and target:
                edges.append({"from": source, "to": target})

    print(edges)  # 这里应该打印出所有的边，而不是每次循环都打印

    return {"nodes": nodes, "edges": edges}