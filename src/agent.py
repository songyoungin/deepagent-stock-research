"""DeepAgents 기반 주식 조사 에이전트를 정의하는 모듈입니다."""

from deepagents import create_deep_agent
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from src.config import settings
from src.prompts import STOCK_RESEARCH_WORKFLOW, SUBAGENT_DELEGATION_INSTRUCTIONS
from src.subagents import SUBAGENTS
from src.tools import get_financial_data, get_stock_price, get_technical_summary, search_stock_news


def get_model() -> BaseChatModel:
    """설정에 따라 LLM 인스턴스를 생성하여 반환합니다.

    Returns:
        설정된 LLM 인스턴스 (ChatGoogleGenerativeAI 또는 ChatOpenAI)

    Raises:
        ValueError: 선택한 provider의 API 키가 설정되지 않은 경우
    """
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OpenAI를 사용하려면 OPENAI_API_KEY 환경 변수를 설정해야 합니다.")
        return ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            api_key=settings.openai_api_key,
        )
    else:
        if not settings.google_api_key:
            raise ValueError("Gemini를 사용하려면 GOOGLE_API_KEY 환경 변수를 설정해야 합니다.")
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            temperature=settings.temperature,
            max_output_tokens=settings.max_tokens,
            google_api_key=settings.google_api_key,
        )


def create_stock_research_agent():
    """주식 조사 Deep Agent를 생성합니다.

    Returns:
        DeepAgent: 주식 조사를 수행하는 에이전트
    """
    # 시스템 프롬프트 구성
    system_prompt = f"""
{STOCK_RESEARCH_WORKFLOW}

{SUBAGENT_DELEGATION_INSTRUCTIONS}
"""

    # 메인 에이전트가 사용할 커스텀 도구
    # (서브에이전트 없이 직접 호출할 수도 있음)
    custom_tools = [
        get_stock_price,
        get_financial_data,
        get_technical_summary,
        search_stock_news,
    ]

    # Deep Agent 생성
    agent = create_deep_agent(
        model=get_model(),
        tools=custom_tools,
        subagents=SUBAGENTS,
        system_prompt=system_prompt,
    )

    return agent


# 싱글톤 에이전트 인스턴스 (필요 시 사용)
_agent_instance = None


def get_agent():
    """주식 조사 에이전트 인스턴스를 반환합니다 (싱글톤).

    Returns:
        DeepAgent: 주식 조사 에이전트
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_stock_research_agent()
    return _agent_instance
