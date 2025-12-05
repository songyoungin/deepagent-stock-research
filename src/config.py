"""애플리케이션 설정 및 환경 변수를 관리하는 모듈입니다."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정을 관리하는 클래스입니다.

    환경 변수나 .env 파일에서 자동으로 값을 로드합니다.
    """

    # API Keys
    google_api_key: str = Field(description="Google API 키")
    tavily_api_key: str = Field(description="Tavily API 키")

    # LLM 설정
    gemini_model: str = Field(default="gemini-2.0-flash-exp", description="Google Gemini 모델 이름")
    temperature: float = Field(default=0.7, description="온도 값")
    max_tokens: int = Field(default=8000, description="최대 토큰 수")

    # Deep Agent 최대 반복 횟수 설정
    max_iterations: int = Field(default=3, description="최대 반복 횟수")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


# 싱글톤 인스턴스
settings = Settings()
