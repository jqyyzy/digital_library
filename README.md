# 数字图书馆中的推荐系统

## 快速上手

### 导入数据

通过位于`scripts/fetch_openlibrary.py`的脚本，可以从**OpenLibrary**网站抓取数据，并生成抓取后的数据到`data/item_sample.csv`文件中。运行示例：`uv run python scripts/fetch_openlibrary.py`。

### 建模和启动后端

首先安装运行项目所需要的Python包，命令如下：

```bash
cd ./backend
uv sync  # 或使用 uv add -r requirements.txt
```

在项目根目录下运行如下命令后，会进行建模并插入到数据库中。数据库默认为**sqlite3**数据库，文件位于`./recsys.db`。

```bash
uv run python -m backend.ingest ./data/items_sample.csv --out ./artifacts
```

（可选）也可以通过设置环境变量`DB_URL`访问其他数据库，如：

```bash
export DB_URL="postgresql+psycopg2://user:pass@host:5432/recsys"
```

在建模完成后，输入如下命令运行后端：

```bash
uv run uvicorn backend.app:app --reload --port 8000
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

### 添加更多用户和测试

#### 添加用户ID和模拟行为数据

项目提供了 `scripts/add_users.py` 脚本，用于批量添加新用户ID和模拟用户行为数据，解决用户数量不足的问题。

```bash
uv run python scripts/add_users.py
```

默认会添加10个新用户（user1000, user1001, ...），每个用户有5条随机事件记录。你可以修改脚本中的 `num_users` 和 `events_per_user` 参数。

#### 测试推荐系统

项目提供了 `scripts/test_recommendation.py` 脚本，用于测试推荐系统对不同用户（包括新用户）的推荐效果。

```bash
uv run python scripts/test_recommendation.py
```

该脚本会测试现有用户、新用户和基于查询的推荐，并输出数据库统计信息。
