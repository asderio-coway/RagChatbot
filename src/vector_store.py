from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from loguru import logger
from config.settings import VECTOR_DB_DIR, VECTOR_SEARCH_THREADS, EMBEDDING_MODEL, VECTOR_STORE_PATH
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class VectorStore:
    """벡터 저장소 클래스"""
    
    def __init__(self, collection_name: str = "documents"):
        """벡터 저장소 초기화"""
        try:
            self.client = chromadb.PersistentClient(
                path=str(VECTOR_DB_DIR),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"벡터 저장소 초기화 완료: {collection_name}")
        except Exception as e:
            logger.error(f"벡터 저장소 초기화 실패: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        """문서와 임베딩을 저장소에 추가"""
        try:
            ids = [f"doc_{i}" for i in range(len(documents))]
            texts = [doc["text"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]
            
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            logger.info(f"{len(documents)}개의 문서 추가 완료")
        except Exception as e:
            logger.error(f"문서 추가 중 오류 발생: {str(e)}")
            raise
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """유사한 문서 검색"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where
            )
            
            documents = []
            for i in range(len(results["documents"][0])):
                doc = {
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                }
                documents.append(doc)
            
            return documents
        except Exception as e:
            logger.error(f"문서 검색 중 오류 발생: {str(e)}")
            raise
    
    def delete_collection(self) -> None:
        """컬렉션 삭제"""
        try:
            self.client.delete_collection(self.collection.name)
            logger.info(f"컬렉션 삭제 완료: {self.collection.name}")
        except Exception as e:
            logger.error(f"컬렉션 삭제 중 오류 발생: {str(e)}")
            raise

def get_vector_store():
    """벡터 저장소 인스턴스를 생성하고 반환합니다."""
    try:
        # 임베딩 모델 초기화
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        # Chroma 벡터 저장소 초기화
        vector_store = Chroma(
            persist_directory=VECTOR_STORE_PATH,
            embedding_function=embeddings
        )
        
        logger.info("벡터 저장소 초기화 완료")
        return vector_store
        
    except Exception as e:
        logger.error(f"벡터 저장소 초기화 실패: {str(e)}")
        raise 