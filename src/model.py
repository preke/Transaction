from transformers import RobertaConfig, RobertaModel, RobertaPreTrainedModel, RobertaTokenizer, RobertaForSequenceClassification
from transformers import BertConfig, BertModel, BertPreTrainedModel
import torch.nn as nn
import torch.nn.functional as F
import torch
import re

# ======== BERT ========

class ClassificationHead(nn.Module):
    
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()        
        self.dense = nn.Linear(input_size, hidden_size)
        self.dropout = nn.Dropout(0.1)
        self.out_proj = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.dropout(x)
        x = self.dense(x)
        x = torch.tanh(x)
        x = self.dropout(x)
        x = self.out_proj(x)
        return x
    
class Emo_Generation(BertPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)
        self.num_labels = 7
        self.mid_size = 100 
        self.bert = BertModel(config)
        
        self.mood_to_hidden = nn.Linear(3, config.hidden_size)
        # self.classifier = ClassificationHead(3, config.hidden_size, 7)
        # self.emo_recognizer = nn.Linear(config.hidden_size, 3)
        self.classifier = nn.Linear(config.hidden_size, 7)

    def forward(self, input_ids, attn_masks, uttr_vad, personality, init_mood):
        
        bert_outputs = self.bert(input_ids, attention_mask=attn_masks)
        bert_hidden = bert_outputs[1]
        response_mood = init_mood + uttr_vad * personality
        emo_embedding = bert_hidden + self.mood_to_hidden(response_mood)
        # user_emo = self.emo_recognizer(bert_hidden)
        response_emo = self.classifier(emo_embedding)
        return response_emo, response_mood #, user_emo

# ======== RoBERTa ========

# class ClassificationHead(nn.Module):
    
#     def __init__(self, input_size, hidden_size, output_size):
#         super().__init__()  
#         self.dim_trans = nn.Linear(input_size, hidden_size)
#         self.dense = nn.Linear(hidden_size, hidden_size)
#         self.dropout = nn.Dropout(0.1)
#         self.out_proj = nn.Linear(hidden_size, output_size)

#     def forward(self, x):
#         x = self.dim_trans(x) # 16 1 768
#         x = self.dropout(x)
#         x = self.dense(x)
#         x = torch.tanh(x)
#         x = self.dropout(x)
#         x = self.out_proj(x)
#         return x

    
    
# class Emo_Generation(RobertaPreTrainedModel):

#     def __init__(self, config):
#         super().__init__(config)
#         self.num_labels = 7
#         self.mid_size = 100 
#         self.roberta = RobertaModel(config)
#         self.uttr_to_vad = nn.Linear(config.hidden_size, 3)
#         # self.classifier = ClassificationHead(3, config.hidden_size, 7)
#         self.classifier = nn.Linear(3, 7)

#     def forward(self, input_ids, attn_masks, uttr_vad, personality, init_mood):
        
#         roberta_outputs = self.roberta(input_ids, attention_mask=attn_masks)
#         roberta_hidden = roberta_outputs[0][:, 0, :]
        
#         response_mood = init_mood + uttr_vad
#         emo_embedding = self.uttr_to_vad(roberta_hidden) * personality + response_mood
#         response_emo = self.classifier(emo_embedding)
        
#         return response_emo, response_mood
    
    