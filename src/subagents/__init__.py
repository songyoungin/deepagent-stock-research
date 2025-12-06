"""서브에이전트 정의 모듈입니다."""

from src.prompts import FUNDAMENTAL_ANALYST_PROMPT, SENTIMENT_ANALYST_PROMPT, TECHNICAL_ANALYST_PROMPT
from src.tools import get_financial_data, get_stock_price, get_technical_summary, search_stock_news

# 펀더멘털 분석 서브에이전트
FUNDAMENTAL_ANALYST = {
    "name": "fundamental-analyst",
    "description": "펀더멘털 분석 수행 (재무제표, 밸류에이션, 수익성 지표)",
    "system_prompt": FUNDAMENTAL_ANALYST_PROMPT,
    "tools": [get_stock_price, get_financial_data],
}

# 기술적 분석 서브에이전트
TECHNICAL_ANALYST = {
    "name": "technical-analyst",
    "description": "기술적 분석 수행 (이동평균, RSI, 차트 패턴, 매매 시그널)",
    "system_prompt": TECHNICAL_ANALYST_PROMPT,
    "tools": [get_technical_summary],
}

# 감성 분석 서브에이전트
SENTIMENT_ANALYST = {
    "name": "sentiment-analyst",
    "description": "뉴스 및 시장 감성 분석 (최신 뉴스, 시장 심리, 이슈 파악)",
    "system_prompt": SENTIMENT_ANALYST_PROMPT,
    "tools": [search_stock_news],
}

# 모든 서브에이전트 목록
SUBAGENTS = [FUNDAMENTAL_ANALYST, TECHNICAL_ANALYST, SENTIMENT_ANALYST]

__all__ = [
    "FUNDAMENTAL_ANALYST",
    "TECHNICAL_ANALYST",
    "SENTIMENT_ANALYST",
    "SUBAGENTS",
]
