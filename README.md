# 数字图书馆中的推荐系统

## 快速上手

### 导入数据

通过位于`scripts/fetch_openlibrary.py`的脚本，可以从**OpenLibrary**网站抓取数据，并生成抓取后的数据到`data/item_sample.csv`文件中。

### 建模和启动后端

首先安装运行项目所需要的Python包，命令如下：

```bash
cd ./backend
pip install -r requirements.txt
```

在项目根目录下运行如下命令后，会进行建模并插入到数据库中。数据库默认为**sqlite3**数据库，文件位于`./recsys.db`。

```bash
python -m backend.ingest ./data/items_sample.csv --out ./artifacts
```

（可选）也可以通过设置环境变量`DB_URL`访问其他数据库，如：

```bash
export DB_URL="postgresql+psycopg2://user:pass@host:5432/recsys"
```

在建模完成后，输入如下命令运行后端：

```bash
uvicorn backend.app:app --reload --port 8000
```

### 启动前端

在启动后端后，在项目根目录下输入如下命令运行前端：

```bash
cd ./frontend
npm i
npm run dev
```

![alt text](assets/README/image.png)

此时在浏览器中输入命令行输出的网址即可访问网站。

---

上面是为游客通过关键词搜索推荐书目，下面是为特定的用户推荐他可能喜欢的书，现在有两个存在的问题，第一个是搜索关键词出来两个相同的条目，第二个是uid也就是用户的数量太少了，需要研究一下怎么多添加几个用户，

| 分工                                                 | 姓名 |
| :-: | :-: |
| 再多添加一些图书条目，修一下条目重复的bug               |      |
| 研究一下**为你推荐**板块实现的功能和流程，多添加一些uid |      |
| 稍微美化一下前端                                      |      |
| 跑通系统，写一个用户使用文档，录一个视频去给老师演示     |      |
