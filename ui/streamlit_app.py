import streamlit as st
from streamlit_chat import message
import sys
from pathlib import Path
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.rag_chain import RAGChain
from config.settings import DOCUMENTS_DIR

# OpenAI API 설정
# OPENAI_API_KEY=your-api-key-here  # ❌ Python 코드에서 이렇게 쓰면 안 됩니다!

# 기타 설정
# MODEL_NAME=gpt-3.5-turbo
# EMBEDDING_MODEL=text-embedding-3-small
# TEMPERATURE=0.7
# MAX_TOKENS=2000

# 기존
LOCAL_LLM_API_BASE = "http://localhost:1234/v1"

# 변경
LOCAL_LLM_API_BASE = "http://10.129.45.22:1234/v1"

def initialize_session_state():
    """세션 상태 초기화"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = RAGChain()
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

def main():
    """메인 애플리케이션"""
    st.set_page_config(
        page_title="RAG 챗봇",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 RAG 챗봇")
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 사이드바
    with st.sidebar:
        st.header("📄 문서 관리")
        if st.button("📂 문서 자동 처리 (documents 폴더)"):
            with st.spinner("documents 폴더의 모든 문서를 처리 중입니다..."):
                files = [f for f in os.listdir(DOCUMENTS_DIR) if (DOCUMENTS_DIR / f).is_file()]
                for file in files:
                    file_path = DOCUMENTS_DIR / file
                    # 이미 처리된 파일인지 확인
                    if str(file_path) not in st.session_state.processed_files:
                        try:
                            st.session_state.rag_chain.process_and_store_document(str(file_path))
                            st.session_state.processed_files.add(str(file_path))
                            st.success(f"{file} 처리 완료!")
                        except Exception as e:
                            st.error(f"{file} 처리 실패: {str(e)}")
                    else:
                        st.info(f"{file} 이미 처리됨")
            st.success("모든 문서 처리 완료!")
        st.divider()
        if st.button("🗑️ 대화 기록 초기화"):
            st.session_state.messages = []
            st.session_state.processed_files.clear()
            st.session_state.rag_chain.reset_vector_store()
            st.success("대화 기록이 초기화되었습니다.")
    
    # 채팅 인터페이스
    chat_container = st.container()
    
    # 사용자 입력
    user_input = st.chat_input("메시지를 입력하세요...")
    
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 챗봇 응답 생성
        with st.spinner("답변을 생성하고 있습니다..."):
            response = st.session_state.rag_chain.query(
                query=user_input,
                chat_history=st.session_state.messages[:-1]  # 현재 메시지 제외
            )
        
        # 챗봇 응답 추가
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 메시지 표시
    with chat_container:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                message(msg["content"], is_user=True, key=f"user_{i}")
            else:
                message(msg["content"], is_user=False, key=f"assistant_{i}")

if __name__ == "__main__":
    main() 