"""주식 분석 도구를 정의하는 모듈입니다."""

import yfinance as yf
from langchain_core.tools import tool


def calculate_moving_averages(ticker: str, periods: list[int] = [20, 50, 200]) -> dict[str, float | None]:
    """이동평균선을 계산합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")
        periods: 계산할 기간 리스트 (기본값: [20, 50, 200]일)

    Returns:
        dict[str, float | None]: 각 기간별 이동평균 값 (예: {"MA_20": 150.5, "MA_50": 145.2})

    Raises:
        ValueError: 데이터 조회 실패 또는 계산 중 오류 발생
    """
    try:
        stock = yf.Ticker(ticker)
        hist_data = stock.history(period="1y")

        if hist_data.empty:
            raise ValueError(f"티커 '{ticker}'에 대한 과거 데이터를 가져올 수 없습니다.")

        result: dict[str, float | None] = {}
        for period in periods:
            ma = hist_data["Close"].rolling(window=period).mean()
            latest_ma = ma.iloc[-1]

            if not isinstance(latest_ma, (int, float)):
                result[f"MA_{period}"] = None
            else:
                result[f"MA_{period}"] = round(float(latest_ma), 2)

        return result

    except Exception as e:
        raise ValueError(f"이동평균 계산 중 오류 발생: {str(e)}") from e


def calculate_rsi(ticker: str, period: int = 14) -> float:
    """RSI (Relative Strength Index)를 계산합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")
        period: RSI 계산 기간 (기본값: 14일)

    Returns:
        float: RSI 값 (0-100)

    Raises:
        ValueError: 데이터 조회 실패 또는 계산 중 오류 발생
    """
    try:
        stock = yf.Ticker(ticker)
        hist_data = stock.history(period="3mo")

        if hist_data.empty:
            raise ValueError(f"티커 '{ticker}'에 대한 과거 데이터를 가져올 수 없습니다.")

        # 일일 가격 변화 계산
        delta = hist_data["Close"].diff()

        # 상승/하락 분리
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # 평균 상승/하락 계산
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        # RSI 계산
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        latest_rsi = rsi.iloc[-1]

        if not isinstance(latest_rsi, (int, float)):
            raise ValueError("RSI 계산 결과가 유효하지 않습니다.")

        return round(float(latest_rsi), 2)

    except Exception as e:
        raise ValueError(f"RSI 계산 중 오류 발생: {str(e)}") from e


def get_technical_summary(ticker: str) -> dict:
    """기술적 분석 요약을 제공합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")

    Returns:
        dict: 이동평균, RSI, 매매 시그널을 포함한 기술적 분석 요약

    Raises:
        ValueError: 데이터 조회 실패 또는 분석 중 오류 발생
    """
    try:
        # 이동평균 계산
        moving_averages = calculate_moving_averages(ticker)

        # RSI 계산
        rsi = calculate_rsi(ticker)

        # 현재가 조회
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get("currentPrice") or info.get("regularMarketPrice", 0)

        # 시그널 판단
        ma_50 = moving_averages.get("MA_50")
        signal = "NEUTRAL"

        if ma_50 and current_price > 0:
            if current_price > ma_50 and rsi < 70:
                signal = "BUY"
            elif current_price < ma_50 and rsi > 30:
                signal = "SELL"

        return {
            "current_price": current_price,
            "moving_averages": moving_averages,
            "rsi": rsi,
            "signal": signal,
        }

    except Exception as e:
        raise ValueError(f"기술적 분석 중 오류 발생: {str(e)}") from e


@tool
def technical_analysis_tool(ticker: str) -> str:
    """주식의 기술적 분석을 수행합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")

    Returns:
        str: 기술적 분석 결과를 담은 포맷된 문자열
    """
    try:
        summary = get_technical_summary(ticker)

        result = f"\n=== {ticker} 기술적 분석 ===\n\n"
        result += f"현재가: ${summary['current_price']:,.2f}\n\n"

        result += "이동평균선:\n"
        for key, value in summary["moving_averages"].items():
            if value is not None:
                result += f"  {key}: ${value:,.2f}\n"
            else:
                result += f"  {key}: N/A\n"

        result += f"\nRSI (14일): {summary['rsi']:.2f}\n"

        # RSI 해석
        rsi = summary["rsi"]
        if rsi > 70:
            rsi_interpretation = "과매수 구간"
        elif rsi < 30:
            rsi_interpretation = "과매도 구간"
        else:
            rsi_interpretation = "중립 구간"

        result += f"RSI 해석: {rsi_interpretation}\n\n"

        # 시그널
        signal = summary["signal"]
        signal_kr = {"BUY": "매수", "SELL": "매도", "NEUTRAL": "중립"}
        result += f"매매 시그널: {signal_kr.get(signal, signal)}\n"

        return result

    except Exception as e:
        return f"오류: {str(e)}"
