# 一个用于检索《欧陆风云4》wiki的RAG问答系统

## 运行
```bash
pip install -r requirements.txt
python src/rag.py
```

## 爬取网页、切块和建立索引
```bash
# 爬取wiki网页
python src/crawler.py

# 切块并建立索引
python src/embed.py
```