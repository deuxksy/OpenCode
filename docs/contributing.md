# Contributing

## 기여 가이드

이 프로젝트는 OpenCode와 Z.ai를 연습하기 위한 playground입니다. 자유롭게 실험하고 기여해 주세요!

## 개발 환경 설정

### 1. 레포지토리 클론

```bash
git clone <your-repo-url>
cd OpenCode
```

### 2. 가상 환경 생성 (권장)

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate     # Windows
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

## 코드 스타일

이 프로젝트는 PEP 8을 따릅니다. 코드를 제출하기 전에 다음 명령어를 실행하세요:

```bash
# 코드 포맷팅
black .
isort .

# 타입 검사
mypy .
```

## 테스트

```bash
# 모든 테스트 실행
pytest tests/

# 커버리지 확인
pytest tests/ --cov=. --cov-report=html
```

## OpenCode 사용

### 커스텀 에이전트 사용

```bash
# 코드 리뷰
/reviewer <파일명 또는 설명>

# 코드 탐색
/explorer <질문>

# 코드 작성
/writer <작업 설명>
```

### 커스텀 명령어 사용

```bash
/test      # 테스트 실행
/lint      # 코드 검사
/run       # 앱 실행
/analyze   # 코드 분석
```

## Pull Request

1. 새로운 브랜치 생성: `git checkout -b feature/my-feature`
2. 변경 사항 커밋: `git commit -m "Add my feature"`
3. 브랜치 푸시: `git push origin feature/my-feature`
4. Pull Request 생성

## 질문?

OpenCode의 `/help` 명령어를 사용하거나 이슈를 생성하세요.
