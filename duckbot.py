from mrc.infer import tokenize_function, data_collator, extract_answer
from mrc.model.mrc_model import MRCQuestionAnswering
from transformers import AutoTokenizer
from transformers import RobertaForSequenceClassification, RobertaConfig
from vncorenlp import VnCoreNLP
from transformers import AutoTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import torch
import numpy as np
import pandas as pd
import nltk
import json
import random

# CONFIG ARGUMENT
NUMLABLES = 2000
model_checkpoint = "nguyenvulebinh/vi-mrc-large"
FILE_TEXT_CLASSIFICTION = "model_train/data.pth"
config = RobertaConfig.from_pretrained(
    "transformers/PhoBERT_base_transformers/config.json", from_tf=False, num_labels = NUMLABLES, output_hidden_states=False,
)
data = torch.load(FILE_TEXT_CLASSIFICTION, map_location=torch.device('cpu'))
model_state = data["model_state"]
dataset_path = 'data/intents_gia.json'
# dataset_path = 'data/intents.json'

device= 'cpu'


def convert_data_to_df(json_data):
    tag= []
    context = []
    linking = []
    question = []
    for intent in json_data['intents']:
        tag.append(intent['tag'])
        context.append(intent['context'])
        question.append(intent['question'])
        try:
            linking.append(intent['linking'])
        except:
            linking.append('')
    
    return pd.DataFrame(list(zip(tag, context, linking, question)), columns=['tag', 'context', 'linking', 'question'])


class DuckBot():
    def __init__(self):
        print('Loading...')
        # SET UP MODEL QUESTION ANSWERING
        self.tokenizer_question_answering = AutoTokenizer.from_pretrained(model_checkpoint)
        self.model_question_anwering = MRCQuestionAnswering.from_pretrained(model_checkpoint)

        # SETTUP MODEL TEXT CLASSIFICATION
        self.model_text_classification = RobertaForSequenceClassification.from_pretrained(
            "transformers/PhoBERT_base_transformers/model.bin",
            config=config
        )
        self.model_text_classification.load_state_dict(model_state)

        self.rdrsegmenter = VnCoreNLP("transformers/vncorenlp/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')
        self.tokenizer_text_classification = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

        # LOAD DATA JSON
        with open(dataset_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        self.df = convert_data_to_df(json_data)
        self.tags = self.df['tag'].tolist()

    def embeding_input(self, question):
        X = self.rdrsegmenter.tokenize(question)
        X = ' '.join([' '.join(x) for x in X])
        X += ' </s>'    
        endcode = self.tokenizer_text_classification.encode(X)
        endcode = [endcode]
        X = pad_sequences(endcode, maxlen = 125, dtype="long", value=0, truncating="post", padding="post")
        mask = [int(token_id > 0) for token_id in X[0]]
        mask = np.array([mask])
        b_input_ids = torch.from_numpy(X)
        b_input_mask = torch.from_numpy(mask)

        return b_input_ids, b_input_mask
        

    #funtction get tag from question using the first model
    def get_tag(self, question):
        input_ids, input_mask = self.embeding_input(question)
        with torch.no_grad():
            outputs = self.model_text_classification(input_ids,
            token_type_ids=None,
            attention_mask=input_mask)
            logits = outputs[0]
            logits = logits.detach().cpu().numpy()

        print(f" logic {logits}")
        preds = np.argmax(logits, axis = 1)
        print(f"preds {preds}")
        probs = torch.softmax(outputs[0], dim=1)
        probs = probs.numpy()
        print(f"probs ",probs)  
        print(f"probs {probs[0]}")
        prob = probs[0][preds.item()]
        print(f"prob {prob}")
        tag = self.tags[preds.item()]
        print(f"tag {tag}") 
        print(f"Tỉ lệ: {prob.item()}")
        variance_value = np.var(probs[0])

        print(f"variance_value ", variance_value)
        if variance_value > 0.00001 or prob.item() > 0.02:
            tag = self.tags[preds.item()]
        else:
            tag= None

        return tag

    def get_answer(self, question, context):
        QA_input = {
            'question': question,
            'context': context
        }
        inputs = [tokenize_function(QA_input, self.tokenizer_question_answering)]
        inputs_ids = data_collator(inputs, self.tokenizer_question_answering)
        outputs = self.model_question_anwering(**inputs_ids)
        answer = extract_answer(inputs, outputs, self.tokenizer_question_answering)
        return answer[0]['answer']

    def create_more_info(self, tag):
        question = self.df.loc[self.df['tag'] == tag, 'question'].values[0]
        print("question ",question)
        link = self.df.loc[self.df['tag'] == tag, 'linking'].values[0]
        print("Link: ",link)
        img_text = str(link) 
        suggest_text = str(question)
        return img_text, suggest_text  

    def run(self, question, last_tag= None):
        list_dia_chi = [
    "Xin lỗi, có thể cho biết địa chỉ cụ thể của bạn được không?",
    "Để hỗ trợ bạn tốt hơn, vui lòng cung cấp địa chỉ chi tiết.",
    "Bạn có thể chia sẻ địa chỉ chính xác để chúng tôi có thể giúp đỡ?",
    "Để tôi có thể cung cấp thông tin chính xác, bạn có thể nói rõ địa chỉ được không?"
]
        random.shuffle(list_dia_chi)
        
        tag = self.get_tag(question)
        print("tag ", tag)
        if tag == None:
            tag = last_tag
            img_text = ""
            print(f'tag = null')
            img_text, suggest_text = self.create_more_info(tag)
        
        if tag == None:
            answer = "Xin lỗi tôi không hiểu câu hỏi của bạn!, bạn có thể nói rõ địa chỉ được không?"
            answer = random.choice(list_dia_chi)
            print(f'Xin lỗi tôi không hiểu câu hỏi của bạn!')
            img_text = ""
        else:
            context = self.df.loc[self.df['tag'] == tag, 'context'].values[0]
            img_text, suggest_text = self.create_more_info(tag)
            print(f'dang tim cau context {context}')
            for item in context:
                answer = self.get_answer(question, item)
                print(f'answer : {answer}')
                if answer != '':
                    break
                
        if answer == '':
            answer = 'Xin lỗi, câu hỏi này nằm ngoài hiểu biết của tôi rồi!'
            answer = random.choice(list_dia_chi)
            img_text = ""
        print("answer in run: ", answer)
        return answer, tag, img_text, suggest_text