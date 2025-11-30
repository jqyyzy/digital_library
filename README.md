1. **准备数据**（示例 CSV 列：`title,author,subject,year,abstract,tags,availability`）
    把你的数据放到 `data/items_sample.csv`。
2. **安装与导入/建模**

```
cd recsys/backend
pip install -r requirements.txt
# 环境变量（可选）切到 Postgres
# export DB_URL="postgresql+psycopg2://user:pass@host:5432/recsys"

python -m backend.ingest ../data/items_sample.csv --out ./artifacts
uvicorn backend.app:app --reload --port 8000
```

1. **前端启动**

```
cd ../frontend
npm i
npm run dev   # http://localhost:5173 ，代理到 http://localhost:8000
```

![1762866265143](D:\app_cache\WeChat Files\wxid_4d5psrb5mya312\FileStorage\Temp\1762866265143.png)

上面是为游客通过关键词搜索推荐书目，下面是为特定的用户推荐他可能喜欢的书，现在有两个存在的问题，第一个是搜索关键词出来两个相同的条目，第二个是uid也就是用户的数量太少了，需要研究一下怎么多添加几个用户，

| 分工                                                    | 姓名 |
| ------------------------------------------------------- | ---- |
| 再多添加一些图书条目，修一下条目重复的bug               |      |
| 研究一下**为你推荐**板块实现的功能和流程，多添加一些uid |      |
| 稍微美化一下前端                                        |      |
| 跑通系统，写一个用户使用文档，录一个视频去给老师演示    |      |
|                                                         |      |

