"""tavily 기반 뉴스 검색 도구를 정의하는 모듈입니다."""

from langchain_core.tools import tool
from tavily import TavilyClient

from src.config import settings
from src.models.research import NewsItem


def search_stock_news(ticker: str, query: str = "", max_results: int = 5) -> list[NewsItem]:
    """Tavily API를 사용하여 주식 관련 뉴스를 검색합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")
        query: 추가 검색 쿼리 (선택 사항, 기본값: "")
        max_results: 최대 결과 수 (기본값: 5)

    Returns:
        list[NewsItem]: 뉴스 아이템 리스트

    Raises:
        ValueError: API 호출 실패 또는 검색 중 오류 발생
    """
    try:
        client = TavilyClient(api_key=settings.tavily_api_key)

        # 검색 쿼리 구성
        search_query = f"{ticker} stock news"
        if query:
            search_query = f"{ticker} {query} stock news"

        # Tavily 검색 실행
        response = client.search(query=search_query, search_depth="advanced", max_results=max_results)

        # 결과 변환
        news_items = []
        for result in response.get("results", []):
            news_items.append(
                NewsItem(
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    content=result.get("content", ""),
                    published_date=result.get("published_date"),
                    score=result.get("score"),
                )
            )

        return news_items

    except Exception as e:
        raise ValueError(f"뉴스 검색 중 오류 발생: {str(e)}") from e


@tool
def news_search_tool(ticker: str, query: str = "") -> str:
    """주식 관련 뉴스를 검색합니다.

    Args:
        ticker: 주식 심볼 (예: "AAPL", "TSLA")
        query: 추가 검색 쿼리 (선택 사항)

    Returns:
        str: 뉴스 검색 결과를 담은 포맷된 문자열
    """
    try:
        news_items = search_stock_news(ticker, query)

        if not news_items:
            return f"'{ticker}'에 대한 뉴스를 찾을 수 없습니다."

        result = f"\n=== {ticker} 관련 뉴스 ({len(news_items)}개) ===\n\n"

        for i, item in enumerate(news_items, 1):
            result += f"[{i}] {item.title}\n"
            result += f"URL: {item.url}\n"
            result += f"내용: {item.content[:200]}...\n"

            if item.published_date:
                result += f"발행일: {item.published_date}\n"

            if item.score is not None:
                result += f"관련도: {item.score:.2f}\n"

            result += "\n" + "-" * 80 + "\n\n"

        return result

    except Exception as e:
        return f"오류: {str(e)}"
