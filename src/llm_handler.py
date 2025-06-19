from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional
import requests
from config.settings import LOCAL_LLM_API_BASE, LOCAL_LLM_MODEL
import json

class LocalLLM(LLM):
    """LM Studio를 사용하는 로컬 LLM 클래스"""
    
    @property
    def _llm_type(self) -> str:
        return "local_llm"

    @property
    def api_base(self):
        return LOCAL_LLM_API_BASE

    @property
    def model(self):
        return LOCAL_LLM_MODEL
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """LM Studio API를 호출하여 응답을 받아옵니다."""
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API 호출 실패: {response.status_code} - {response.text}")
                
        except Exception as e:
            raise Exception(f"LLM 호출 중 오류 발생: {str(e)}")

def get_llm() -> LLM:
    """LLM 인스턴스를 생성하고 반환합니다."""
    return LocalLLM() 