import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 프로젝트 루트 디렉토리
ROOT_DIR = Path(__file__).parent.parent

# 데이터 디렉토리
DATA_DIR = ROOT_DIR / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
PROCESSED_DIR = DATA_DIR / "processed"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
UPLOAD_DIR = DATA_DIR / "uploads"

# 로그 디렉토리
LOG_DIR = ROOT_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

# 한국어 처리 설정
KOREAN_CHUNK_SIZE = 800
KOREAN_CHUNK_OVERLAP = 100
KOREAN_TEXT_SPLITTER = "kss"

# 메모리 최적화 설정
MAX_MEMORY_USAGE = "4GB"
BATCH_SIZE = 32
CACHE_SIZE = 1000

# 벡터 검색 최적화
VECTOR_SEARCH_THREADS = os.cpu_count()
INDEX_TYPE = "IVF_FLAT"  # Milvus 인덱스 타입

# 서버 설정
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8501

# LM Studio 설정
LOCAL_LLM_API_BASE = "http://10.129.45.22:1234/v1"  # LM Studio의 API 엔드포인트
LOCAL_LLM_MODEL = "google/gemma-3-4b"  # LM Studio에서 사용 가능한 모델 이름

# 임베딩 설정
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# 벡터 저장소 설정
VECTOR_STORE_TYPE = "chroma"  # 또는 "faiss", "milvus"
VECTOR_STORE_PATH = "data/vector_db"

# 문서 처리 설정
DOCUMENT_PROCESSING = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "supported_formats": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"]
}

# 로깅 설정
LOG_LEVEL = "INFO"

# 웹 인터페이스 설정
STREAMLIT_PORT = 8501
STREAMLIT_HOST = "localhost"

# 디렉토리 생성
for directory in [DOCUMENTS_DIR, PROCESSED_DIR, VECTOR_DB_DIR, UPLOAD_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "gpt-3.5-turbo" 