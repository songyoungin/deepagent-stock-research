"""주식 관련 데이터 모델을 정의하는 모듈입니다."""

from pydantic import BaseModel, Field


class StockPrice(BaseModel):
    """현재 주가 정보를 나타내는 모델입니다."""

    symbol: str = Field(description="종목 심볼")
    current_price: float = Field(description="현재가")
    previous_close: float = Field(description="전일 종가")
    change_percent: float = Field(description="등락률 (%)")
    volume: int = Field(description="거래량")
    market_cap: float | None = Field(None, description="시가총액")


class FinancialData(BaseModel):
    """재무제표 데이터를 나타내는 모델입니다."""

    symbol: str = Field(description="종목 심볼")
    revenue: float | None = Field(None, description="매출액")
    net_income: float | None = Field(None, description="순이익")
    eps: float | None = Field(None, description="주당순이익")
    pe_ratio: float | None = Field(None, description="PER")
    debt_to_equity: float | None = Field(None, description="부채비율")
