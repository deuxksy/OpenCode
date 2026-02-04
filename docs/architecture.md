# Architecture

## filter-gemma.py Architecture

### Overview

`filter-gemma.py`는 mitmproxy를 사용하여 Google Gemini API의 Gemma 3 계열 모델에 대한 HTTP 요청을 가로채고 수정하는 Python 스크립트입니다.

### Purpose

Gemma 3 모델은 기존 Gemini API와 호환되지 않는 부분이 있습니다. 이 스크립트는 다음 호환성 문제들을 해결합니다:

1. **Role 변환**: `system` role을 `user` role로 변환 (Gemma 3는 system role을 지원하지 않음)
2. **필드 제거**: 지원하지 않는 필드(`tools`, `toolConfig`, `thinkingConfig`) 제거
3. **토큰 최적화**: 소형 모델(1b, e2b)에 대해 적절한 토큰 제한 설정

### Component Diagram

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │ HTTP Request
       │ (to Gemini API)
       ▼
┌─────────────────┐
│  mitmproxy      │◄──────────┐
│  (Proxy Server) │            │
└────────┬────────┘            │
         │                     │
         │ flow.request        │
         ▼                     │
┌─────────────────┐            │
│ filter-gemma.py │            │
│   (Add-on)      │            │
│                 │            │
│  1. URL Check   │            │
│  2. Parse JSON  │            │
│  3. Modify      │            │
│  4. Forward     │────────────┘
└────────┬────────┘
         │ Modified Request
         ▼
┌─────────────────┐
│  Gemini API     │
│  (Google)       │
└─────────────────┘
```

### Code Flow

```
request() 함수 시작
    │
    ▼
├─ URL 분석: generativelanguage.googleapis.com 확인
    │
    ▼
├─ Gemma 3 모델 판별 (정규표현식)
    │   - URL 또는 payload의 model 필드 확인
    │   - 패턴: "gemma-3"
    │
    ▼
├─ Payload 수정 (Gemma 3인 경우)
    │
    ├─ A. Role Swap
    │   └─ system → user 변환
    │
    ├─ B. Field Pruning
    │   └─ tools, toolConfig 제거
    │
    └─ C. GenerationConfig 조정
        ├─ thinkingConfig 제거
        └─ 소형 모델 maxOutputTokens 최적화
            │
            ▼
├─ 수정된 Payload 적용
    │
    ▼
└─ 요청 전송
```

### Key Functions

#### `request(flow: http.HTTPFlow)`

mitmproxy의 request 이벤트 핸들러입니다.

**Parameters:**
- `flow`: HTTP 요청/응답 객체

**Logic:**
1. URL에서 Gemini API 확인
2. JSON payload 파싱
3. Gemma 3 모델 판별
4. 필요한 경우 payload 수정
5. 로그 출력

### Configuration

**Supported Models:**
- gemma-3-1b
- gemma-3-4b
- gemma-3-12b
- gemma-3-27b
- gemma-3-e2b

**Field Modifications:**

| Original | Modified | Reason |
|----------|----------|--------|
| role: "system" | role: "user" | Gemma 3 호환성 |
| tools | (removed) | 미지원 기능 |
| toolConfig | (removed) | 미지원 기능 |
| thinkingConfig | (removed) | 미지원 기능 |
| maxOutputTokens (1b/e2b) | 4096 max | 품질 최적화 |

### Dependencies

- **mitmproxy**: HTTP/HTTPS 프록시 서버 및 트래픽 조작
- **json**: JSON 데이터 파싱 및 직렬화
- **re**: 정규표현식 매칭

### Usage

```bash
# Start mitmproxy with the add-on
mitmdump -s filter-gemma.py

# Start mitmproxy with custom port
mitmdump -s filter-gemma.py -p 8080

# Start with interactive UI
mitmweb -s filter-gemma.py
```

### Security Considerations

1. **HTTPS Certificate**: mitmproxy CA 인증서가 클라이언트에 설치되어 있어야 함
2. **API Keys**: proxy 로그에 포함되지 않도록 주의 필요
3. **MITM Risk**: 모든 트래픽이 프록시를 통과하므로 신뢰할 수 있는 환경에서만 사용

### Future Enhancements

- [ ] Config 파일에서 규칙 로드 지원
- [ ] 요청/응답 로깅 옵션
- [ ] 더 많은 모델 지원
- [ ] 테스트 스위트 추가
