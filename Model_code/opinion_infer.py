# opinion_infer.py
import pandas as pd

# 加载数据集
file_path = 'F:/yuqing/Final/data_process/test1.csv'
data = pd.read_csv(file_path)

# 已知观点
known_opinions = {}

for index, row in data.iterrows():
    relation = row['Relation']
    sentiment = row['Sentiment']

    if pd.notna(relation):
        # 解析实体对
        relation_type, entities = relation.split('<')
        entity1, entity2 = entities.strip('>').split(',')
        entity1 = entity1.strip()
        entity2 = entity2.strip()

        # 跳过命名一样的实体
        if entity1 == entity2:
            continue

        # 存储双向关系
        known_opinions[(entity1, entity2)] = sentiment
        known_opinions[(entity2, entity1)] = sentiment

# 定义推理规则
def infer_opinion(entity1, entity2, known_opinions):
    # 直接查找已知观点
    if (entity1, entity2) in known_opinions:
        return known_opinions[(entity1, entity2)]

    # 关系的传递性推理
    for key, sentiment in known_opinions.items():
        if key[0] == entity1 or key[1] == entity1:
            other_entity = key[1] if key[0] == entity1 else key[0]
            if (other_entity, entity2) in known_opinions:
                other_sentiment = known_opinions[(other_entity, entity2)]
                # 如果两个情感相同或都是中立
                if sentiment == other_sentiment or (sentiment == 'neutral' and other_sentiment == 'neutral'):
                    return sentiment

    return 'unknown'

# 进行观点推理
inferred_opinion = infer_opinion('五里冲街道办事处', '亚太中心党建联盟', known_opinions)
print(f"推理观点：<五里冲街道办事处，亚太中心党建联盟，{inferred_opinion}>")
