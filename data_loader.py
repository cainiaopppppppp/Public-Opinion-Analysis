# data_loader.py
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast
import torch

class RelationExtractionDataset(Dataset):
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

    def __init__(self, filename, tokenizer, max_length):
        self.dataframe = pd.read_csv(filename)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        data = self.dataframe.iloc[idx]
        text = data['Text']
        entities = data['Entities'] if not pd.isna(data['Entities']) else ''
        relations = data['Relations'] if not pd.isna(data['Relations']) else ''

        inputs = self.tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            return_token_type_ids=True,
            return_offsets_mapping=True,
            truncation=True
        )

        # 实体和关系标签的转换
        entity_labels = self.convert_entities_to_labels(entities, inputs['offset_mapping'])
        relation_labels = self.convert_relations_to_labels(relations)

        return {
            'input_ids': torch.tensor(inputs['input_ids'], dtype=torch.long),
            'attention_mask': torch.tensor(inputs['attention_mask'], dtype=torch.long),
            'token_type_ids': torch.tensor(inputs['token_type_ids'], dtype=torch.long),
            'entity_labels': torch.tensor(entity_labels, dtype=torch.long),  # 确保这里是整数列表
            'relation_labels': torch.tensor(relation_labels, dtype=torch.long)  # 确保关系标签也是整数
        }

    def convert_entities_to_labels(self, entities_str, offset_mapping):
        labels = [self.ENTITY_LABELS['O']] * len(offset_mapping)

        if entities_str:
            for entity in entities_str.split('; '):
                entity_info, _ = entity.split(': ')
                entity_type, entity_range = entity_info.split('(')
                start, end = map(int, entity_range.strip(')').split('-'))

                for i, (token_start, token_end) in enumerate(offset_mapping):
                    if start <= token_start < end:
                        label_key = 'B-' + entity_type if token_start == start else 'I-' + entity_type
                        labels[i] = self.ENTITY_LABELS[label_key]

        return labels

    def convert_relations_to_labels(self, relations_str):
        labels = [0] * len(self.RELATION_LABELS)

        if relations_str:
            for relation in relations_str.split('; '):
                relation_info = relation.split('<')[0].strip()
                relation_index = self.RELATION_LABELS.get(relation_info, self.RELATION_LABELS["No Relation"])
                labels[relation_index] = 1

        return labels

# tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
# dataset = RelationExtractionDataset('processed_data.csv', tokenizer, max_length=128)
# dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
