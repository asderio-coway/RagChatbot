from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger

def load_and_split_document(file_path: str) -> List[Document]:
    """문서를 로드하고 청크로 분할"""
    try:
        # 문서 로드
        loader = UnstructuredFileLoader(file_path)
        documents = loader.load()
        
        # 텍스트 분할기 설정
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # 문서 분할
        split_docs = text_splitter.split_documents(documents)
        logger.info(f"문서 로드 및 분할 완료: {file_path} ({len(split_docs)} 청크)")
        
        return split_docs
    except Exception as e:
        logger.error(f"문서 로드 및 분할 중 오류 발생: {str(e)}")
        raise 