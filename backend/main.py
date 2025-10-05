import os
from fastapi import FastAPI, HTTPException
from minio import Minio
import psycopg2
from psycopg2.extras import RealDictCursor
import uvicorn

app = FastAPI(title="Backend API")

# MinIO クライアント設定
minio_client = Minio(
    endpoint=os.getenv('MINIO_ENDPOINT', 'minio:9000'),
    access_key=os.getenv('MINIO_USER', 'minio'),
    secret_key=os.getenv('MINIO_PASSWORD', 'dev-password'),
    secure=False
)

# データベース接続設定
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DATABASE_HOST', 'db'),
        port=os.getenv('DATABASE_PORT', '5432'),
        user=os.getenv('DATABASE_USER', 'postgres'),
        password=os.getenv('DATABASE_PASSWORD', 'dev-password'),
        database=os.getenv('DATABASE_NAME', 'mydatabase')
    )

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の初期化"""
    try:
        # データベーステーブル作成
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                bucket VARCHAR(100) NOT NULL,
                size BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.get("/")
async def root():
    return {"message": "Backend API is running"}

@app.get("/health")
async def health_check():
    return {"status": "OK", "service": "Backend"}

@app.get("/files")
async def get_files():
    """データベースからファイル一覧を取得"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM files ORDER BY created_at DESC")
        files = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"files": [dict(file) for file in files]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/{filename}")
async def process_file(filename: str):
    """ファイル処理のサンプル"""
    try:
        # MinIOからファイルを取得（実際の処理をここに実装）
        # この例では、uploadsバケットからprocessedバケットへコピー
        
        # ファイル情報をデータベースに記録
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO files (filename, bucket, size) VALUES (%s, %s, %s)",
            (filename, 'processed', 0)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"message": f"File {filename} processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
