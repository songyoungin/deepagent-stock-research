"""LangGraph 에이전트의 상태 모델을 정의하는 모듈입니다."""

from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """Deep Agent의 상태를 정의하는 TypedDict입니다.

    계획 -> 수집 -> 분석 -> 비평 -> 수정 사이클 동안 에이전트 간의 상태를 전달합니다.

    Attributes:
        ticker: 조사할 종목 심볼 (예: "AAPL", "TSLA")
        messages: LangGraph 메시지 누적 리스트 (대화 이력 관리)
        research_plan: 리서치 계획 내용
        stock_data: 주가 및 재무 데이터 딕셔너리
        news_data: 뉴스 데이터 리스트
        analysis: 분석 내용 (펀더멘털, 기술적, 감성 분석 포함)
        critique: 분석에 대한 비평 내용
        needs_revision: 재분석 필요 여부 (True일 경우 분석 단계로 복귀)
        iteration_count: 현재 반복 횟수 (최대 반복 제한 체크용)
        final_report: 최종 리서치 보고서
    """

    ticker: str
    messages: Annotated[list[BaseMessage], add_messages]
    research_plan: str
    stock_data: dict[str, Any]
    news_data: list[dict[str, Any]]
    analysis: str
    critique: str
    needs_revision: bool
    iteration_count: int
    final_report: str
