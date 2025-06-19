from typing import List, Dict, Any
import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer
from config.settings import BATCH_SIZE

class EmbeddingManager:
    """임베딩 관리 클래스"""
    
    def __init__(self, model_name: str = "jhgan/ko-sroberta-multitask"):
        """임베딩 모델 초기화"""
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"임베딩 모델 로드 완료: {model_name}")
        except Exception as e:
            logger.error(f"임베딩 모델 로드 실패: {str(e)}")
            raise
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """텍스트 리스트의 임베딩을 생성"""
        try:
            # 배치 처리
            embeddings = []
            for i in range(0, len(texts), BATCH_SIZE):
                batch = texts[i:i + BATCH_SIZE]
                batch_embeddings = self.model.encode(
                    batch,
                    convert_to_numpy=True,
                    show_progress_bar=True
                )
                embeddings.extend(batch_embeddings.tolist())
            
            return embeddings
        except Exception as e:
            logger.error(f"임베딩 생성 중 오류 발생: {str(e)}")
            raise
    
    def get_embedding(self, text: str) -> List[float]:
        """단일 텍스트의 임베딩을 생성"""
        try:
            embedding = self.model.encode(
                text,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            return embedding.tolist()
        except Exception as e:
            logger.error(f"임베딩 생성 중 오류 발생: {str(e)}")
            raise
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """두 임베딩 간의 코사인 유사도 계산"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            return float(similarity)
        except Exception as e:
            logger.error(f"유사도 계산 중 오류 발생: {str(e)}")
            raise 