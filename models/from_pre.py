from transformers import BertTokenizer

#加载预训练字典和分词方法
tokenizer = BertTokenizer.from_pretrained(
    pretrained_model_name_or_path='bert-base-chinese',  # 可选，huggingface 中的预训练模型名称或路径，默认为 bert-base-
    cache_dir='F:/yuqing/Final/models/bert-base-chinese',  # 将数据保存到的本地位置，使用cache_dir 可以指定文件下载位置
    force_download=False,
)
