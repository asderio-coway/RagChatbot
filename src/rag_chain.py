from typing import List, Optional, Dict, Any
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from src.llm_handler import get_llm
from src.vector_store import get_vector_store
from loguru import logger
from src.document_loader import load_and_split_document

class RAGChain:
    """RAG 체인 클래스"""
    
    def __init__(self):
        """RAG 체인 초기화"""
        try:
            # LLM 초기화
            self.llm = get_llm()
            
            # 벡터 저장소 초기화
            self.vector_store = get_vector_store()
            
            # 대화 메모리 초기화
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # 프롬프트 템플릿 설정
            template = """당신은 한국어로 답변하는 RAG 챗봇입니다.
            주어진 컨텍스트를 바탕으로 정확하고 유용한 답변을 제공하세요.
            컨텍스트에 없는 정보는 모른다고 솔직하게 말하세요.
            
            컨텍스트:
            {context}
            
            대화 기록:
            {chat_history}
            
            질문: {question}
            답변:"""
            
            prompt = PromptTemplate(
                input_variables=["context", "chat_history", "question"],
                template=template
            )
            
            # RAG 체인 초기화
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_store.as_retriever(),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": prompt}
            )
            
            logger.info("RAG 체인 초기화 완료")
            
        except Exception as e:
            logger.error(f"RAG 체인 초기화 실패: {str(e)}")
            raise
    
    def query(self, query: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """쿼리에 대한 응답 생성"""
        try:
            response = self.chain({"question": query})
            return response["answer"]
        except Exception as e:
            logger.error(f"응답 생성 중 오류 발생: {str(e)}")
            raise

    def process_and_store_document(self, file_path: str) -> None:
        """문서를 처리하고 벡터 저장소에 저장"""
        try:
            # 문서 로드 및 분할
            documents = load_and_split_document(file_path)
            
            # 벡터 저장소에 저장
            self.vector_store.add_documents(documents)
            logger.info(f"문서 처리 완료: {file_path}")
        except Exception as e:
            logger.error(f"문서 처리 중 오류 발생: {str(e)}")
            raise

    def reset_vector_store(self) -> None:
        """벡터 저장소 초기화"""
        try:
            self.vector_store = get_vector_store()
            self.memory.clear()
            logger.info("벡터 저장소 초기화 완료")
        except Exception as e:
            logger.error(f"벡터 저장소 초기화 중 오류 발생: {str(e)}")
            raise

def get_rag_chain() -> RAGChain:
    """RAG 체인 인스턴스를 생성하고 반환합니다."""
    return RAGChain() 