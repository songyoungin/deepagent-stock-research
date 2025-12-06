"""yfinance 기반 주식 데이터 조회 도구를 정의하는 모듈입니다."""

import yfinance as yf
from langchain_core.tools import tool

from src.models.stock import FinancialData, StockPrice


def get_stock_price(ticker: str) -> StockPrice:
    """yfinance를 사용하여 현재 주가 정보를 조회합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")

    Returns:
        StockPrice: 현재가, 전일 종가, 등락률, 거래량, 시가총액 정보

    Raises:
        ValueError: 유효하지 않은 티커이거나 데이터를 가져올 수 없는 경우
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # 필수 데이터 확인
        if not info or "currentPrice" not in info:
            raise ValueError(f"티커 '{ticker}'에 대한 데이터를 가져올 수 없습니다.")

        current_price = info.get("currentPrice") or info.get("regularMarketPrice", 0)
        previous_close = info.get("previousClose", 0)

        # 등락률 계산
        if previous_close > 0:
            change_percent = ((current_price - previous_close) / previous_close) * 100
        else:
            change_percent = 0.0

        return StockPrice(
            symbol=ticker.upper(),
            current_price=current_price,
            previous_close=previous_close,
            change_percent=round(change_percent, 2),
            volume=info.get("volume", 0),
            market_cap=info.get("marketCap"),
        )

    except Exception as e:
        raise ValueError(f"주가 데이터 조회 중 오류 발생: {str(e)}") from e


def get_financial_data(ticker: str) -> FinancialData:
    """yfinance를 사용하여 재무제표 데이터를 조회합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")

    Returns:
        FinancialData: 매출액, 순이익, EPS, PER, 부채비율 정보

    Raises:
        ValueError: 유효하지 않은 티커이거나 데이터를 가져올 수 없는 경우
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info:
            raise ValueError(f"티커 '{ticker}'에 대한 데이터를 가져올 수 없습니다.")

        return FinancialData(
            symbol=ticker.upper(),
            revenue=info.get("totalRevenue"),
            net_income=info.get("netIncomeToCommon"),
            eps=info.get("trailingEps"),
            pe_ratio=info.get("trailingPE"),
            debt_to_equity=info.get("debtToEquity"),
        )

    except Exception as e:
        raise ValueError(f"재무 데이터 조회 중 오류 발생: {str(e)}") from e


@tool
def stock_price_tool(ticker: str) -> str:
    """주식의 현재 가격 정보를 조회합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")

    Returns:
        str: 주가 정보를 담은 포맷된 문자열
    """
    try:
        price_data = get_stock_price(ticker)
        return f"""
주식 심볼: {price_data.symbol}
현재가: ${price_data.current_price:,.2f}
전일 종가: ${price_data.previous_close:,.2f}
등락률: {price_data.change_percent:+.2f}%
거래량: {price_data.volume:,}
시가총액: ${price_data.market_cap:,.0f} (데이터 있는 경우)
"""
    except Exception as e:
        return f"오류: {str(e)}"


@tool
def financial_data_tool(ticker: str) -> str:
    """주식의 재무제표 데이터를 조회합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")

    Returns:
        str: 재무 데이터를 담은 포맷된 문자열
    """
    try:
        financial = get_financial_data(ticker)

        def format_value(value: float | None, prefix: str = "$", suffix: str = "") -> str:
            if value is None:
                return "N/A"
            return f"{prefix}{value:,.2f}{suffix}"

        return f"""
주식 심볼: {financial.symbol}
매출액: {format_value(financial.revenue)}
순이익: {format_value(financial.net_income)}
주당순이익(EPS): {format_value(financial.eps)}
PER: {format_value(financial.pe_ratio, prefix="", suffix="배")}
부채비율: {format_value(financial.debt_to_equity, prefix="", suffix="%")}
"""
    except Exception as e:
        return f"오류: {str(e)}"
