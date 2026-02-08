# Whistle 트래픽 분석 도구

Whistle 프록시 서버의 트래픽 데이터를 분석하여 통계를 생성하는 도구입니다.

## 기능

- **기본 요청 통계**: 총 요청 수, 평균 응답 시간, 최소/최대 응답 시간, TTFB 등
- **도메인별 통계**: 도메인별 요청 수, 평균 크기, 평균 응답 시간
- **상태 코드별 통계**: HTTP 상태 코드별 요청 수
- **메서드별 통계**: GET, POST, PUT, DELETE 등 메서드별 요청 수
- **크기별 통계**: 요청/응답 크기 분포
- **HTTP 버전별 통계**: HTTP/1.1, HTTP/2 사용 현황

## 설치

```bash
# Python 스크립트와 쉘 스크립트는 이미 포함되어 있습니다.
# 실행 권한만 부여하면 됩니다.
chmod +x whistle_stats.sh
```

## 사용법

### 기본 사용

```bash
# 기본 트래픽 분석 (최근 600개 요청)
./whistle_stats.sh analyze

# 더 많은 데이터 분석
./whistle_stats.sh analyze -c 1000

# 상세 정보 표시
./whistle_stats.sh analyze -v

# JSON 결과 저장
./whistle_stats.sh export -o stats.json
```

### 실시간 모니터링

```bash
# 실시간 트래픽 모니터링 (5초 간격)
./whistle_stats.sh monitor

# 사용자 정의 간격 (10초)
./whistle_stats.sh monitor -i 10
```

### 파이썬 스크립트 직접 사용

```bash
# 쉘 스크립트 없이 직접 Python 스크립트 사용
curl -s -u "Whistle:pass_0.4840247157276468" \
  "http://127.0.0.1:8888/cgi-bin/get-data?count=600" \
  | python3 whistle_traffic_analyzer.py

# 기존 JSON 파일 분석
python3 whistle_traffic_analyzer.py -f data.json

# 상세 정보 표시
python3 whistle_traffic_analyzer.py -f data.json -v

# JSON 출력
python3 whistle_traffic_analyzer.py -f data.json --json
```

## 구성

쉘 스크립트 상단에서 다음 설정을 수정할 수 있습니다:

```bash
WHISTLE_HOST="127.0.0.1"       # Whistle 호스트
WHISTLE_PORT="8888"            # Whistle 포트
WHISTLE_USER="Whistle"          # Whistle 사용자 이름
WHISTLE_PASS="pass_0.484..."   # Whistle 비밀번호
```

## 출력 예시

```
============================================================
📊 Whistle 트래픽 통계
============================================================

【기본 요청 통계】
  총 요청 수: 100
  총 요청 크기: 34.62 KB
  총 응답 크기: 55.78 KB
  평균 요청 크기: 354.51 B
  평균 응답 크기: 571.17 B
  평균 응답 시간: 408.87 ms
  최소 응답 시간: 0.00 ms
  최대 응답 시간: 20.34 s
  평균 TTFB: 115.54 ms
  HTTP/2 사용: 80 (80.0%)

【Top 10 도메인별 통계】
  1. gemini.google.com
     요청: 20회
     평균 요청 크기: 848.45 B
     평균 응답 크기: 1.29 KB
     평균 응답 시간: 1.33 s
  ...

【상태 코드별 통계】
  200: 57회 (57.0%)
  204: 14회 (14.0%)
  304: 19회 (19.0%)
  ...

【메서드별 통계】
  GET: 28회 (28.0%)
  POST: 60회 (60.0%)
  ...
```

## 요구사항

- Python 3.6 이상
- Whistle 프록시 서버 (8888 포트 실행 중)
- curl (쉘 스크립트 사용 시)

## 제한 사항

- Whistle은 최근 600개의 트래픽 데이터만 메모리에 유지합니다.
- 데이터 수가 600을 넘더라도 최근 600개만 분석됩니다.
- DNS 시간 데이터는 일부 요청에서만 사용 가능합니다.

## 라이선스

MIT
