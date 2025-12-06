# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

[langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) 기반의 자율적인 Deep Agent로, 주식 시장 조사를 수행합니다. 계획 수립, 서브에이전트 위임, 도구 호출을 통해 종합적인 주식 분석을 제공합니다.

## 핵심 기술 스택

- **Python 3.13** (정확한 버전 요구사항)
- **deepagents**: LangChain/LangGraph 기반 에이전트 프레임워크
- **LangChain Google GenAI**: LLM 통합 (Google Gemini)
- **yfinance**: 실시간 금융 데이터 수집
- **Tavily**: 뉴스 및 웹 검색 통합

## 개발 환경 설정

### 가상 환경
- 가상 환경 위치: `.venv` (프로젝트 루트)
- 활성화: `source .venv/bin/activate` (macOS/Linux)

### 의존성 관리
- `uv`를 사용하여 의존성 관리 (uv.lock 파일 존재)
- 의존성 설치: `uv sync`
- 개발 의존성 설치: `uv sync --group dev`

## 코드 품질 도구

### Pre-commit Hooks
프로젝트는 pre-commit을 사용하여 코드 품질을 관리합니다:

```bash
# Pre-commit 설치 (처음 한 번만)
source .venv/bin/activate && pre-commit install

# 전체 파일 검사
source .venv/bin/activate && pre-commit run --all-files
```

### 검사 도구
1. **Ruff** (포매팅 및 린팅)
   - `ruff-format`: Black 대체 포매터
   - `ruff --fix`: 자동 수정 가능한 린트 오류 수정
   - 설정: pyproject.toml에 정의 (line-length=120, target-version=py313)

2. **Mypy** (정적 타입 검사)
   - 설정: strict=false, ignore_missing_imports=true
   - 외부 라이브러리 타입 누락 무시

3. **기타 검사**
   - trailing-whitespace: 줄 끝 공백 제거
   - end-of-file-fixer: 파일 끝 빈 줄 추가
   - check-yaml: YAML 문법 검사
   - check-added-large-files: 대용량 파일 체크

## 코드 스타일 규칙

- **줄 길이**: 120자
- **Import 정렬**: Ruff의 isort 규칙 사용 (E, W, F, I)
- **타입 힌트**: 권장되나 strict 모드는 비활성화

## 실행 명령어

### 메인 애플리케이션
```bash
source .venv/bin/activate && python main.py
```

## 아키텍처 가이드

### 프로젝트 구조

```
src/
├── agent.py         # 메인 에이전트 (create_deep_agent)
├── prompts.py       # 시스템 프롬프트 및 워크플로우 지침
├── config.py        # 환경 변수 및 설정 관리
├── subagents/       # 서브에이전트 정의
│   └── __init__.py  # 3개 서브에이전트 (fundamental, technical, sentiment)
├── tools/           # 커스텀 도구
│   ├── stock_data.py   # yfinance 기반 주식 데이터 도구
│   ├── news_search.py  # Tavily 기반 뉴스 검색 도구
│   └── analysis.py     # 기술적 분석 도구
└── models/          # Pydantic 데이터 모델
    ├── stock.py     # 주식 정보, 재무제표 등
    └── research.py  # 뉴스 아이템, 리서치 보고서
```

### DeepAgents 아키텍처

이 프로젝트는 `deepagents` 프레임워크를 사용하여 다음 패턴을 구현합니다:

1. **계획 수립 (Planning)**
   - `write_todos`/`read_todos` 도구로 작업 계획 관리
   - LLM이 동적으로 분석 단계를 계획

2. **서브에이전트 위임 (Sub-agent Delegation)**
   - `task` 도구로 전문 서브에이전트에 작업 위임
   - 3개의 전문 서브에이전트:
     - `fundamental-analyst`: 펀더멘털 분석 (재무제표, 밸류에이션)
     - `technical-analyst`: 기술적 분석 (이동평균, RSI)
     - `sentiment-analyst`: 뉴스/감성 분석

3. **도구 호출 (Tool Calling)**
   - LLM이 필요에 따라 도구 선택 및 호출
   - 커스텀 도구: `get_stock_price`, `get_financial_data`, `get_technical_summary`, `search_stock_news`

4. **파일시스템 (Filesystem)**
   - `write_file`/`read_file` 도구로 분석 결과 저장
   - 대용량 컨텍스트 자동 오프로딩

### 워크플로우

```
사용자 요청
    │
    ▼
┌─────────────────────────────────────────┐
│           Main Agent                     │
│  1. write_todos: 분석 계획 수립          │
│  2. task: 서브에이전트 위임              │
│     ├── fundamental-analyst             │
│     ├── technical-analyst               │
│     └── sentiment-analyst               │
│  3. 결과 종합 및 보고서 작성             │
│  4. write_file: 보고서 저장              │
└─────────────────────────────────────────┘
```

### 개발 가이드

- **새 도구 추가**: `src/tools/`에 함수 생성 후 `src/agent.py`의 `custom_tools`에 추가
- **서브에이전트 추가**: `src/subagents/__init__.py`에 정의 후 `SUBAGENTS` 리스트에 추가
- **프롬프트 수정**: `src/prompts.py`에서 워크플로우 지침 수정

## 구현 현황

### 완료된 기능

#### 1. 설정 관리 (`src/config.py`)
- Pydantic Settings 기반 타입 안전한 설정 관리
- 환경 변수 자동 로딩 (.env 파일)
- API 키 관리 (Google Gemini, Tavily)
- LLM 설정 (모델명, temperature, max_tokens)

#### 2. 커스텀 도구 (`src/tools/`)
- **stock_data.py**: 주가/재무 데이터 조회 (yfinance)
- **news_search.py**: 뉴스 검색 (Tavily)
- **analysis.py**: 기술적 분석 (이동평균, RSI, 매매 시그널)

#### 3. 데이터 모델 (`src/models/`)
- **stock.py**: `StockPrice`, `FinancialData`
- **research.py**: `NewsItem`, `ResearchReport`

#### 4. 프롬프트 (`src/prompts.py`)
- 메인 에이전트 워크플로우 지침
- 서브에이전트별 전문 프롬프트
- 위임 전략 지침

#### 5. 서브에이전트 (`src/subagents/`)
- `fundamental-analyst`: 펀더멘털 분석
- `technical-analyst`: 기술적 분석
- `sentiment-analyst`: 감성 분석

#### 6. 메인 에이전트 (`src/agent.py`)
- `create_deep_agent()` 기반 에이전트 생성
- 커스텀 도구 및 서브에이전트 통합

#### 7. 엔트리포인트 (`main.py`)
- 대화형 종목 입력
- 에이전트 실행 및 결과 출력

## 환경 변수

`.env` 파일에 다음 변수를 설정해야 합니다:

```
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```
