# 健康记录查询接口

基于 FastAPI + PostgreSQL 实现的健康记录查询服务，提供 `/healthRecords` 接口返回数据库中的健康记录数据。

## 一、环境要求

- Python 3.8+
- PostgreSQL 数据库（已创建好 `health_records` 表）

## 二、安装依赖

```bash
pip install fastapi uvicorn psycopg2-binary
```

> 推荐使用 `psycopg2-binary`，无需本地编译，安装更方便。

## 三、数据库准备

确保 PostgreSQL 中已存在对应的表，例如：

```sql
CREATE TABLE health_records (
    id SERIAL PRIMARY KEY,
    record_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    temperature NUMERIC(4,1),
    medication VARCHAR(255)
);
```

## 四、配置数据库连接

打开 `index.py`，确认 `get_conn()` 函数中的连接参数与你的数据库一致：

```python
def get_conn():
    return psycopg2.connect(
        host="121.43.193.127",   # 数据库地址
        database="postgres",     # 数据库名
        user="postgres",         # 用户名
        password="950929",      # 密码
        port=5432                # 端口
    )
```

如果数据库在本机，`host` 改为 `localhost` 或 `127.0.0.1`。

## 五、运行项目

在项目根目录下执行：

```bash
uvicorn index:app --reload
```

参数说明：

- `index`：文件名 `index.py`（不带后缀）
- `app`：代码中 `app = FastAPI()` 的实例名
- `--reload`：代码修改后自动重启（仅开发环境建议使用）

## 六、调用接口

### 方式一：浏览器直接访问

```
http://127.0.0.1:8000/healthRecords
```

返回示例：

```json
[
  {
    "id": 1,
    "record_time": "2026-06-24 09:40:00",
    "description": "轻微头痛，状态正常",
    "temperature": 36.7,
    "medication": "布洛芬 200mg"
  }
]
```
