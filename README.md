# OpenCode + Z.ai Python Playground

OpenCode와 Z.ai(coding plan - glm-4.7)를 사용하여 Python 개발을 연습하기 위한 playground 템플릿입니다.
최종 목적은 mitmproxy 로 트래픽을 변조해서 OpenCode 에서 Google AI Studio 에 있는 Gemma 3 를 사용하기

## 📋 목표

- OpenCode의 다양한 기능 테스트 및 연습
- Z.ai glm-4.7 모델을 활용한 Python 개발
- 커스텀 에이전트 및 명령어 사용법 학습

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. OpenCode 설정

이 프로젝트는 이미 OpenCode 설정(`opencode.json`)이 되어 있습니다.

```bash
opencode
```

### 3. 프로젝트 초기화

OpenCode TUI에서 다음 명령어를 실행하세요:

```
/init
```

이는 프로젝트 구조를 분석하고 `AGENTS.md`를 생성/업데이트합니다.

## 📁 프로젝트 구조

```
.
├── README.md              # 이 파일
├── AGENTS.md              # OpenCode용 프로젝트 가이드라인
├── opencode.json          # OpenCode 설정
├── filter-gemma.py        # 샘플 Python 코드
├── requirements.txt       # Python 의존성
├── pyproject.toml         # Python 프로젝트 설정
├── docs/                  # 문서
│   ├── architecture.md    # 아키텍처 설명
│   └── contributing.md    # 기여 가이드
└── .opencode/             # OpenCode 커스터마이징
    ├── agents/            # 커스텀 에이전트
    └── commands/          # 커스텀 명령어
```

## 🔧 사용 가능한 명령어

OpenCode TUI에서 다음 커스텀 명령어를 사용할 수 있습니다:

- `/test` - pytest로 테스트 실행
- `/lint` - black, isort, mypy로 코드 검사
- `/run` - filter-gemma.py 실행
- `/analyze` - 코드베이스 분석

## 🤖 사용 가능한 에이전트

- `reviewer` - Python 코드 리뷰 전문가
- `explorer` - Python 코드베이스 탐색 전문가
- `writer` - Python 기능 작성 전문가

## 📝 filter-gemma.py 샘플 코드

이 프로젝트는 mitmproxy를 사용하여 OpenCode 에서 Gemma 3 API 사용 할수있도록 트래픽을 변조하는 샘플 코드를 포함합니다.

### 사용 방법

```bash
mitmdump -s filter-gemma.py
```

## 🛠️ 개발 도구

이 프로젝트는 다음 Python 개발 도구를 사용합니다:

- **black** - 코드 포맷터
- **isort** - import 정리
- **mypy** - 정적 타입 검사
- **pytest** - 테스트 프레임워크

## 📚 추가 리소스

- [OpenCode 문서](https://opencode.ai/docs)
- [Z.ai 문서](https://z.ai/docs)
- [PEP 8 - Python 스타일 가이드](https://peps8.org/)
