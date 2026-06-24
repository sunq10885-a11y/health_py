from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="121.43.193.127",
        database="postgres",
        user="postgres",
        password="950929",
        port=5432
    )

# 请求体模型：新增记录时前端需要传的字段
class HealthRecordCreate(BaseModel):
    description: Optional[str] = None
    temperature: Optional[float] = None
    medication: Optional[str] = None
    recordTime: Optional[str] = None

# 查询
@app.get("/healthRecords")
def get_health_records():
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM health_records")
        rows = cursor.fetchall()

        return [
            {
                "id": r[0],
                "recordTime": str(r[1]),
                "description": r[2],
                "temperature": r[3],
                "medication": r[4]
            }
            for r in rows
        ]
    finally:
        conn.close()

# 新增
@app.post("/healthRecords")
def create_health_record(record: HealthRecordCreate):
    conn = get_conn()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO health_records (record_time, description, temperature, medication)
            VALUES (%s, %s, %s, %s)
            RETURNING id, record_time, description, temperature, medication
            """,
            (record.recordTime, record.description, record.temperature, record.medication)
        )

        row = cursor.fetchone()
        conn.commit()

        return {
            "id": row[0],
            "recordTime": row[1],
            "description": row[2],
            "temperature": row[3],
            "medication": row[4]
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()