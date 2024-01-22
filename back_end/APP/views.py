# /APP/views.py
# 路由 + 视图函数

from .models import *
import jieba
from flask import jsonify, render_template, Blueprint, request, redirect, session, Flask
from .graphvisual import load_model, process_model_output
import torch
from transformers import BertTokenizerFast, BertModel, BertTokenizer, BertForSequenceClassification
import pandas as pd
import networkx as nx
from collections import Counter
from .model_enity import RelationExtractionModel

blue = Blueprint("user", __name__)


@blue.route("/")
@blue.route("/home/")
def home():
    # username = request.cookies.get("user")
    username = session.get("user")
    return render_template("home.html",username = username)


@blue.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if  username == "dp" and password == "666":
            response = redirect("/home/")
            # response.set_cookie("user",username,max_age=30*24*3600)
            session["user"] = username

            return response

        else :
            return "用户名或密码错误"

@blue.route("/logout/")
def logout():
    response = redirect("/home/")
    # response.delete_cookie("user")
    session.pop("user")
    return response

@blue.route('/charts')
def wordcloud():
    with open("F:/yuqing/Final/data/content.txt", "r", encoding="utf-8") as file:
        data = file.read()

    words = jieba.cut(data)
    word_count = Counter(words)

    # 只保留出现频率大于1次的词汇，并按频率降序排序
    # 然后选取前20个词汇
    # 过滤掉出现频率为1次或字数少于2的词
    word_freq = [{"name": word, "value": count} for word, count in word_count.items() if count > 30 and len(word) > 1]
    word_freq = sorted(word_freq, key=lambda x: x['value'], reverse=True)[:30]

    return jsonify(word_freq)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path = 'F:/yuqing/Final/back_end/APP/models/entity-best_model-20231207-203113.pth'  # 替换为模型的实际路径
model = load_model(model_path)
model = model.to(device)
tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')

@blue.route('/graph', methods=['GET'])
def get_graph_data():
    query = request.args.get('query')

    inputs = tokenizer.encode_plus(
        query,
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

    graph_data = process_model_output(entity_logits, relation_logits)
    print(graph_data)  # 打印输出来检查数据
    return jsonify(graph_data)


# 加载情感分析模型
sentiment_model_dir = 'F:/yuqing/Final/models/bert-sentiment-20231203-184759'
sentiment_tokenizer = BertTokenizer.from_pretrained(sentiment_model_dir)
sentiment_model = BertForSequenceClassification.from_pretrained(sentiment_model_dir)
sentiment_model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
sentiment_model.eval()

# 加载情感数据
sentiment_data_file = 'F:/yuqing/Final/data_process/processed_data_sentiment.csv'
sentiment_data = pd.read_csv(sentiment_data_file)


# 情感分析函数
def extract_sentiments(texts):
    sentiments = []
    for text in texts:
        inputs = sentiment_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = sentiment_model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
        label_map = {0: 'neutral', 1: 'positive', 2: 'negative'}
        sentiments.append(label_map[prediction])
    return sentiments


# 提取情感和构建图数据的API
@blue.route('/sentiment', methods=['GET'])
def get_graph_data_sentiment():
    graph = nx.Graph()

    # 从情感数据中提取节点和边
    for index, row in sentiment_data.iterrows():
        entity = row['Entity']
        relation = row['Relation']
        sentiment = row['Sentiment']

        # 解析实体对
        if pd.notna(relation):
            relation_type, entities = relation.split('<')
            entity1, entity2 = entities.strip('>').split(',')
            entity1 = entity1.strip()
            entity2 = entity2.strip()

            # 跳过命名一样的实体
            if entity1 == entity2:
                continue

            # 添加实体节点和关系
            graph.add_node(entity1)
            graph.add_node(entity2)
            graph.add_edge(entity1, entity2, sentiment=sentiment)

    # 将图数据转换为前端需要的格式
    nodes = [{'id': node, 'label': node} for node in graph.nodes()]
    edges = [{'from': u, 'to': v, 'label': d['sentiment']} for u, v, d in graph.edges(data=True)]

    graph_data = {'nodes': nodes, 'edges': edges}
    # print(graph_data)
    return jsonify(graph_data)

# 比较情感倾向的API
@blue.route('/compare-sentiments', methods=['POST'])
def compare_sentiments():
    data = request.json
    entity1 = data['entity1']
    entity2 = data['entity2']

    # 查找两个实体间的情感倾向
    matched_rows = sentiment_data[(sentiment_data['Entity'] == entity1) | (sentiment_data['Entity'] == entity2)]
    if not matched_rows.empty:
        # 如果找到匹配的行，返回情感
        opinion = matched_rows.iloc[0]['Sentiment']
    else:
        # 如果没有找到直接的关系，返回'unknown'
        opinion = 'unknown'

    return jsonify({"opinion": opinion})


@blue.route('/entities', methods=['GET'])
def get_entities():
    unique_entities = sentiment_data['Entity'].unique().tolist()
    return jsonify({'entities': unique_entities})

@blue.route('/analyze-text', methods=['POST'])
def analyze_text():
    data = request.json
    text = data['text']

    # Tokenize the input text and obtain the tokens
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        return_token_type_ids=True,
        return_attention_mask=True,
        truncation=True,
        return_tensors="pt"
    )
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    token_type_ids = inputs['token_type_ids'].to(device)

    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])  # Convert input IDs to tokens

    with torch.no_grad():
        entity_logits, relation_logits = model(input_ids, attention_mask, token_type_ids)

    # Process model output and extract graph data
    graph_data = process_model_output(entity_logits, relation_logits, tokens)

    # 情感分析
    sentiments = extract_sentiments([text])

    # 构建图
    graph = nx.Graph()
    for node in graph_data['nodes']:  # 修改了这里
        graph.add_node(node['label'], sentiment=node.get('sentiment', 'unknown'))

    # 添加边
    for edge in graph_data['edges']:  # 以及这里
        graph.add_edge(edge['from'], edge['to'])

    # 转换图数据为前端格式
    nodes = [{'id': node, 'label': node, 'sentiment': graph.nodes[node]['sentiment']} for node in graph.nodes]
    edges = [{'from': u, 'to': v} for u, v in graph.edges]

    return jsonify({'graph': {'nodes': nodes, 'edges': edges}})


