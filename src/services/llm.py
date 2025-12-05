"""LLM 설정 및 관리를 담당하는 모듈입니다."""

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import settings


def get_llm() -> ChatGoogleGenerativeAI:
    """Google Gemini LLM 인스턴스를 생성하여 반환합니다.

    Returns:
        설정된 ChatGoogleGenerativeAI 인스턴스
    """
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=settings.temperature,
        max_output_tokens=settings.max_tokens,
        google_api_key=settings.google_api_key,
    )
