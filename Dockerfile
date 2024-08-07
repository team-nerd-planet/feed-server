# 베이스 이미지 선택
FROM python:3.11

# Poetry 설치
RUN pip install poetry

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설정 파일 복사
COPY pyproject.toml poetry.lock ./

# 의존성 설치
RUN poetry install --no-root

# 애플리케이션 코드 복사
COPY . .

ENV DATABASE_URL 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
ENV OPENAI_API_KEY 'sk-1234567890abcdef1234567890abcdef'

# 배포시 3만 이상의 포트를 사용해야 함
# 포트 설정 (애플리케이션 실행 포트) -> fastapi는 기본적으로 8000번 포트를 사용
EXPOSE 8000

# 애플리케이션 실행 명령어
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
