import pandas as pd

# 加载你的训练数据集
file_path = 'F:/yuqing/Final/data_process/processed_data_with_entities.csv'
data = pd.read_csv(file_path)

# 假设你的关系标签在列 'Relation' 中
num_labels = data['Relations'].nunique()

print(f"关系类别的数量: {num_labels}")
