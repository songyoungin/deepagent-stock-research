# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

LangGraph 기반의 자율적인 Deep Agent로, 주식 시장 조사를 수행합니다. 실시간 금융 데이터 분석, 뉴스 종합, 자기 수정 추론을 결합한 시스템입니다.

## 핵심 기술 스택

- **Python 3.13** (정확한 버전 요구사항)
- **LangGraph**: Agent 오케스트레이션 및 워크플로우 관리
- **LangChain Google GenAI**: LLM 통합
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

프로젝트는 기능별 모듈 구조로 조직되어 있습니다:

```
src/
├── agents/          # LangGraph 에이전트 정의
│   ├── graph.py     # StateGraph 정의 및 노드/엣지 연결
│   ├── nodes.py     # 각 노드의 실행 로직
│   └── state.py     # 에이전트 상태 모델 (TypedDict)
├── tools/           # 에이전트가 사용하는 도구들
│   ├── stock_data.py   # yfinance 기반 주식 데이터 도구
│   ├── news_search.py  # Tavily 기반 뉴스 검색 도구
│   └── analysis.py     # 기술적/펀더멘털 분석 도구
├── models/          # Pydantic 데이터 모델
│   ├── stock.py     # 주식 정보, 재무제표 등
│   └── research.py  # 리서치 결과 데이터 모델
├── services/        # 서비스 레이어
│   ├── llm.py       # LLM 설정 및 관리 (Google GenAI)
│   └── data_provider.py  # 외부 API 통합
└── config.py        # 환경 변수 및 설정 관리
```

### 아키텍처 설계 원칙

1. **LangGraph Agent 워크플로우**
   - `agents/graph.py`: StateGraph로 주식 조사 워크플로우 정의
   - `agents/nodes.py`: 각 단계를 노드 함수로 구현 (계획 → 데이터 수집 → 분석 → 종합 → 자기 수정)
   - `agents/state.py`: TypedDict로 에이전트 간 전달되는 상태 정의

2. **도구 기반 아키텍처**
   - `tools/` 모듈의 각 도구는 LangChain Tool로 래핑
   - yfinance, Tavily API를 추상화하여 에이전트에서 쉽게 호출

3. **타입 안전성**
   - `models/`의 Pydantic 모델로 데이터 검증
   - 명시적 타입 힌트 사용 (mypy 호환)

4. **서비스 레이어 분리**
   - `services/llm.py`: LLM 초기화 및 관리
   - `services/data_provider.py`: 외부 데이터 소스 통합 로직

### 개발 가이드

- **새 도구 추가**: `src/tools/`에 새 파일 생성 후 LangChain Tool로 래핑
- **노드 추가**: `agents/nodes.py`에 함수 추가 후 `agents/graph.py`에서 그래프에 연결
- **상태 확장**: `agents/state.py`의 TypedDict에 필드 추가

## 구현 진행 상황

### Phase 1: 기반 인프라 (완료)

#### 1. 설정 관리 (`src/config.py`)
- Pydantic Settings 기반 타입 안전한 설정 관리
- 환경 변수 자동 로딩 (.env 파일)
- API 키 관리 (Google Gemini, Tavily)
- LLM 설정 (모델명, temperature, max_tokens)
- Deep Agent 설정 (max_iterations)

#### 2. LLM 서비스 (`src/services/llm.py`)
- `get_llm()`: ChatGoogleGenerativeAI 인스턴스 생성 팩토리 함수
- 설정 기반 자동 초기화

#### 3. 에이전트 상태 (`src/agents/state.py`)
- `AgentState` TypedDict 정의
- Deep Agent 워크플로우 상태 관리
- Google 스타일 Docstring으로 각 필드 설명 포함
- 필드: ticker, messages, research_plan, stock_data, news_data, analysis, critique, needs_revision, iteration_count, final_report

#### 4. 데이터 모델 (`src/models/`)
- **stock.py**:
  - `StockPrice`: 현재 주가 정보 (symbol, current_price, previous_close, change_percent, volume, market_cap)
  - `FinancialData`: 재무제표 데이터 (symbol, revenue, net_income, eps, pe_ratio, debt_to_equity)
- **research.py**:
  - `NewsItem`: 뉴스 아이템 (title, url, content, published_date, score)
  - `ResearchReport`: 최종 리서치 보고서 (summary, fundamental_analysis, technical_analysis, sentiment_analysis, recommendation, key_risks, iteration_count, confidence_score)

#### 5. 의존성
- `pydantic-settings>=2.7.1` 추가

### Phase 2: 도구 구현 (예정)
- `src/tools/stock_data.py`: yfinance 기반 주식 데이터 조회 도구
- `src/tools/news_search.py`: Tavily 기반 뉴스 검색 도구
- `src/tools/analysis.py`: 기술적 분석 도구

### Phase 3: 에이전트 노드 (예정)
- `src/agents/nodes.py`: plan, collect_data, analyze, critique, should_continue 노드

### Phase 4: 그래프 구성 (예정)
- `src/agents/graph.py`: StateGraph 구성 및 컴파일

### Phase 5: 통합 및 실행 (예정)
- `main.py`: 애플리케이션 엔트리포인트
