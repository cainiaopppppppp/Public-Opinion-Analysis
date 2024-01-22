# model_entity.py
from transformers import BertModel
import torch
import torch.nn as nn

class RelationExtractionModel(nn.Module):
    def __init__(self, bert_model, num_entity_labels, num_relation_labels, lstm_hidden_size=128, num_lstm_layers=1, dropout_prob=0.1):
        super(RelationExtractionModel, self).__init__()
        self.bert = bert_model
        self.bilstm = nn.LSTM(bert_model.config.hidden_size, lstm_hidden_size, num_layers=num_lstm_layers, bidirectional=True, batch_first=True)
        self.dropout = nn.Dropout(dropout_prob)
        self.entity_classifier = nn.Linear(2 * lstm_hidden_size, num_entity_labels)
        self.relation_classifier = nn.Linear(2 * lstm_hidden_size * 2, num_relation_labels)

    def forward(self, input_ids, attention_mask, token_type_ids):
        outputs = self.bert(input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        sequence_output = outputs[0]
        lstm_output, _ = self.bilstm(sequence_output)
        lstm_output = self.dropout(lstm_output)
        entity_logits = self.entity_classifier(lstm_output)
        first_last_tokens = torch.cat((lstm_output[:, 0, :], lstm_output[:, -1, :]), dim=1)
        relation_logits = self.relation_classifier(first_last_tokens)
        return entity_logits, relation_logits
