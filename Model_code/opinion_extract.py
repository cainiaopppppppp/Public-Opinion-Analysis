# opinion_extract.py
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 加载处理后的数据
file_path = 'F:/yuqing/Final/data_process/test1.csv'
graph_data = pd.read_csv(file_path)

# 创建图（无向图）
G = nx.Graph()

# 添加节点和边
for _, row in graph_data.iterrows():
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

        # 添加实体节点
        if not G.has_node(entity1):
            G.add_node(entity1)
        if not G.has_node(entity2):
            G.add_node(entity2)

        # 添加关系和情感
        G.add_edge(entity1, entity2, sentiment=sentiment)

# 可视化图
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # 布局
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000)
edge_labels = nx.get_edge_attributes(G, 'sentiment')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Topic-Opinion Graph")
plt.show()
