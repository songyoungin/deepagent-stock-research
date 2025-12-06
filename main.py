"""주식 조사 Deep Agent 애플리케이션의 엔트리포인트입니다."""

from src.agent import create_stock_research_agent
from src.config import settings


def main() -> None:
    """메인 함수: 주식 조사 에이전트를 실행합니다."""
    print("주식 조사 Deep Agent를 시작합니다...")
    print("-" * 50)

    # 에이전트 생성
    agent = create_stock_research_agent()

    # 사용자 입력 받기
    ticker = input("분석할 종목 심볼을 입력하세요 (예: AAPL, TSLA): ").strip().upper()

    if not ticker:
        print("종목 심볼이 입력되지 않았습니다.")
        return

    print(f"\n'{ticker}' 종목 분석을 시작합니다...\n")

    # 에이전트 실행 (recursion_limit으로 최대 반복 횟수 제한)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"{ticker} 주식을 종합적으로 분석해주세요."}]},
        config={"recursion_limit": settings.max_iterations * 10},  # 서브에이전트 포함 여유 있게 설정
    )

    # 결과 출력
    print("\n" + "=" * 50)
    print("분석 완료")
    print("=" * 50)

    # 마지막 메시지 출력
    if result.get("messages"):
        last_message = result["messages"][-1]
        if hasattr(last_message, "content"):
            print(last_message.content)
        else:
            print(last_message)


if __name__ == "__main__":
    main()
