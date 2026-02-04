# OpenCode + Z.ai Python Playground - Agent Guidelines

이 문서는 Z.ai (glm-4.7) 모델과 함께 OpenCode를 연습하는 Python Playground입니다.

## 0. 운영 원칙 (Operational Root)

한국어로 커뮤니케이션 합니다.

## 빌드, 린트, 테스트 명령어

### 포맷팅 및 린트
```bash
# black으로 코드 포맷팅 (line length: 100)
black .

# isort로 import 정렬
isort .

# mypy로 타입 체크
mypy .

# 세 명령어 순차 실행
black . && isort . && mypy .
```

### 테스트
```bash
# 모든 테스트 실행
pytest tests/

# 특정 테스트 파일 실행
pytest tests/test_example.py

# 단일 테스트 함수 실행
pytest tests/test_example.py::test_specific_function

# 상세 출력과 커버리지로 실행
pytest tests/ -v --cov=. --cov-report=term-missing

# 패턴과 일치하는 테스트만 실행
pytest -k "test_pattern"
```

## 코드 스타일 가이드라인

### Import
- 순서: 표준 라이브러리 → 서드파티 → 로컬
- `isort`로 순서 유지 (black 프로필)
- 와일드카드 import 피하기 (`from module import *`)
- 그룹 간 빈 줄로 구분

### 포맷팅
- 라인 길이: 100자 (pyproject.toml에 설정됨)
- `black`으로 자동 포맷팅
- 4 스페이스 들여쓰기 (탭 미사용)
- 문자열에 큰따옴표 사용

### 타입 힌트
- 모든 함수 파라미터와 반환값에 **필수**
- `typing` 모듈 사용: 필요에 따라 `Optional`, `List`, `Dict`, `Any`
- 복잡한 타입: 명확성을 위해 TypeAlias 사용
- 예시: `def process(data: Dict[str, Any]) -> Optional[Result]`

### 명명 규칙
- 함수/변수: `snake_case` (예: `process_request`, `user_id`)
- 클래스: `PascalCase` (예: `RequestFilter`, `HTTPFlow`)
- 상수: `UPPER_SNAKE_CASE` (예: `MAX_TOKENS`, `API_URL`)
- 프라이빗 메서드: `_leading_underscore`
- 설명적이고 의미 있는 이름 사용 (약어 피하기)

### 에러 처리
- 구체적인 예외 타입 사용 (`ValueError`, `KeyError`, 일반 `Exception` 미사용)
- 외부 API 호출은 항상 try/except로 감싸기
- 컨텍스트와 함께 에러 로깅: `ctx.log.error(f"Error processing {url}: {e}")`
- 우아하게 실패 - 예외로 전체 프로세스를 종료하지 않기
- 에러 값 반환 또는 메시지와 함께 정보성 예외 발생

### Docstring
- Google 스타일 docstring 사용
- 포함: 목적, args, returns, raises
- 간결하면서 유용하게 유지

### 프로젝트별 참고사항

**filter-gemma.py**: Gemma 3 API 요청을 가로채는 mitmproxy 애드온.
- 진입점: `request(flow: http.HTTPFlow)` 함수
- URL 또는 페이로드에서 Gemma 3 모델 확인
- 페이로드 수정: 지원하지 않는 필드 제거, system→user 역할 교체
- 로깅에 `ctx.log.info/error` 사용

**의존성**: mitmproxy, json, re (mitmproxy 제외 표준 라이브러리)

## 테스트 모범 사례
- pytest fixtures로 setup/teardown
- 엣지 케이스와 에러 조건 테스트
- 외부 의존성 모킹 (mitmproxy, HTTP 요청)
- 설명적인 테스트 이름: `test_gemma3_role_swap`, `test_invalid_payload`

## 일반적인 패턴

```python
# 타입 힌트와 에러 처리가 포함된 함수
def process_item(item: Dict[str, Any]) -> Optional[Result]:
    """단일 항목을 처리합니다.

    Args:
        item: 입력 딕셔너리

    Returns:
        처리된 결과, 실패 시 None
    """
    try:
        # 처리 로직
        return result
    except ValueError as e:
        ctx.log.error(f"Invalid item: {e}")
        return None
```

## MCP Tools

### Sequential Thinking

복잡한 다단계 문제나 명확하지 않은 작업 범위에 직면했을 때 `sequential-thinking` MCP 툴 사용:
- 복잡한 문제를 관리 가능한 단계로 분해
- 아키텍처 계획 분석
- 실행 중 방향 수정이 필요한 작업
- 관련 없는 정보를 필터링해야 하는 상황

사용법: 필요할 때 프롬프트에 "use sequential-thinking tool" 추가
