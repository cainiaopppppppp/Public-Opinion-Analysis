import torch
from transformers import BertTokenizerFast, BertModel
from model_enity import RelationExtractionModel

class RelationExtractionDataset:
    ENTITY_LABELS = {
        "B-国家": 0, "I-国家": 1,
        "B-机构": 2, "I-机构": 3,
        "B-人物": 4, "I-人物": 5,
        "O": 6  # 'O' 代表 'Outside'，即非实体
    }
    RELATION_LABELS = {
        "国家间": 0, "机构间": 1,
        "国家-机构": 2, "机构-人物": 3,
        "国家-人物": 4, "No Relation": 5
    }

# 检查CUDA是否可用并设置设备
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

# 将预测结果转换为中文标签
def convert_predictions_to_labels(entity_predictions, relation_predictions, dataset):
    entity_label_map = {v: k for k, v in dataset.ENTITY_LABELS.items()}
    entity_labels = [entity_label_map.get(idx.item(), "N/A") for idx in entity_predictions[0]]

    relation_label_map = {v: k for k, v in dataset.RELATION_LABELS.items()}
    relation_labels = [relation_label_map[idx] for idx, val in enumerate(relation_predictions[0]) if val]

    return entity_labels, relation_labels

# 预测函数
def predict(text, model, tokenizer):
    model.eval()
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        return_token_type_ids=True,
        return_attention_mask=True,
        truncation=True
    )

    input_ids = torch.tensor([inputs['input_ids']], dtype=torch.long).to(device)
    attention_mask = torch.tensor([inputs['attention_mask']], dtype=torch.long).to(device)
    token_type_ids = torch.tensor([inputs['token_type_ids']], dtype=torch.long).to(device)

    with torch.no_grad():
        entity_logits, relation_logits = model(input_ids, attention_mask, token_type_ids)
    entity_preds = torch.argmax(entity_logits, dim=2)
    relation_preds = torch.sigmoid(relation_logits) > 0.5

    return entity_preds, relation_preds

# 主函数
def main():
    model_path = 'F:/yuqing/Final/models/entity-best_model-20231207-203113.pth'
    model = load_model(model_path)
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')

    test_text = "本届年会由亚太传播学会联盟与亚洲舆论学会联合举办，由清华大学新闻与传播学院、《全球传媒学刊》承办。清华大学原党委常委、副书记韩景阳，清华大学新闻与传播学院院长周庆安，亚太新闻传播学会联盟主席、清华大学新闻与传播学院教授陈昌凤，亚洲舆论学会会长、菲律宾圣保罗大学教授简媞玛·科考，中国新闻史学会会长、中国人民大学新闻学院副院长王润泽等致欢迎辞。"
    entity_predictions, relation_predictions = predict(test_text, model, tokenizer)

    entity_labels, relation_labels = convert_predictions_to_labels(entity_predictions, relation_predictions, RelationExtractionDataset)

    print("实体预测：", entity_labels)
    print("关系预测：", relation_labels)

if __name__ == "__main__":
    main()
