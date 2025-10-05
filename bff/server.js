const express = require('express');
const cors = require('cors');
const multer = require('multer');
const Minio = require('minio');

const app = express();
const port = 8080;



// CORS設定
app.use(cors());
app.use(express.json());

// MinIO クライアント設定
const minioClient = new Minio.Client({
  endPoint: process.env.MINIO_ENDPOINT || 'minio',
  port: 9000,
  useSSL: false,
  accessKey: process.env.MINIO_USER || 'minio',
  secretKey: process.env.MINIO_PASSWORD || 'dev-password'
});

// バケット初期化
const initializeBuckets = async () => {
  const buckets = ['uploads', 'processed', 'backups'];
  
  for (const bucket of buckets) {
    try {
      const exists = await minioClient.bucketExists(bucket);
      if (!exists) {
        await minioClient.makeBucket(bucket, 'us-east-1');
        console.log(`Bucket ${bucket} created successfully`);
      }
    } catch (error) {
      console.error(`Error creating bucket ${bucket}:`, error);
    }
  }
};

// ファイルアップロード設定
const upload = multer({ storage: multer.memoryStorage() });

// ヘルスチェック
app.get('/health', (req, res) => {
  res.json({ status: 'OK', service: 'BFF' });
});

// ファイルアップロード
app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const fileName = `${Date.now()}-${req.file.originalname}`;
    
    await minioClient.putObject('uploads', fileName, req.file.buffer, req.file.size, {
      'Content-Type': req.file.mimetype
    });

    res.json({ 
      message: 'File uploaded successfully',
      fileName: fileName,
      size: req.file.size
    });
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ error: 'Upload failed' });
  }
});

// ファイル一覧取得
app.get('/files/:bucket?', async (req, res) => {
  try {
    const bucket = req.params.bucket || 'uploads';
    const files = [];
    
    const stream = minioClient.listObjects(bucket, '', true);
    
    stream.on('data', (obj) => {
      files.push({
        name: obj.name,
        size: obj.size,
        lastModified: obj.lastModified
      });
    });
    
    stream.on('end', () => {
      res.json({ files });
    });
    
    stream.on('error', (error) => {
      res.status(500).json({ error: error.message });
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// サーバー起動
app.listen(port, async () => {
  console.log(`BFF server running on port ${port}`);
  await initializeBuckets();
});
