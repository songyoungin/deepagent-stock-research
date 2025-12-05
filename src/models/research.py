"""리서치 결과 데이터 모델을 정의하는 모듈입니다."""

from datetime import datetime

from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    """뉴스 아이템을 나타내는 모델입니다."""

    title: str = Field(description="뉴스 제목")
    url: str = Field(description="뉴스 URL")
    content: str = Field(description="뉴스 내용")
    published_date: str | None = Field(None, description="발행일")
    score: float | None = Field(None, description="관련도 점수")


class ResearchReport(BaseModel):
    """최종 리서치 보고서를 나타내는 모델입니다."""

    ticker: str = Field(description="종목 심볼")
    generated_at: datetime = Field(default_factory=datetime.now, description="생성 시간")

    # 분석 섹션
    summary: str = Field(description="요약")
    fundamental_analysis: str = Field(description="펀더멘털 분석")
    technical_analysis: str = Field(description="기술적 분석")
    sentiment_analysis: str = Field(description="시장 감성 분석")

    # 결론
    recommendation: str = Field(description="투자 의견")
    key_risks: list[str] = Field(default_factory=list, description="주요 리스크")

    # 메타데이터
    iteration_count: int = Field(description="반복 횟수")
    confidence_score: float = Field(ge=0, le=1, description="신뢰도 점수")
