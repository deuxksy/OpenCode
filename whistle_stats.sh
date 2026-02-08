#!/bin/bash

# Whistle 트래픽 분석 도구 래퍼 스크립트

set -e

# 설정
WHISTLE_HOST="127.0.0.1"
WHISTLE_PORT="8888"
WHISTLE_USER="Whistle"
WHISTLE_PASS="pass_0.4840247157276468"
WHISTLE_URL="http://${WHISTLE_HOST}:${WHISTLE_PORT}"

# 임시 파일
TEMP_DIR="/tmp/whistle_traffic"
TEMP_FILE="${TEMP_DIR}/data.json"
OUTPUT_DIR="${TEMP_DIR}/reports"

# 색상
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 도움말
show_help() {
    cat << EOF
Whistle 트래픽 분석 도구

사용법:
    $(basename "$0") [옵션] [명령]

명령:
    analyze           트래픽 통계 분석 (기본)
    monitor           실시간 트래픽 모니터링
    export            통계 내보내기 (JSON)
    help              도움말 표시

옵션:
    -c, --count N     가져올 데이터 수 (기본: 600)
    -o, --output FILE 출력 파일 (JSON)
    -v, --verbose     상세 정보 표시
    -f, --file FILE   기존 JSON 파일 사용
    --json            JSON 형식으로 출력

예시:
    $(basename "$0") analyze
    $(basename "$0") analyze -c 1000 -v
    $(basename "$0") monitor
    $(basename "$0") export -o stats.json
EOF
}

# 초기화
init() {
    mkdir -p "$TEMP_DIR"
    mkdir -p "$OUTPUT_DIR"
}

# Whistle에서 데이터 가져오기
fetch_data() {
    local count="${1:-600}"
    
    echo -e "${BLUE}Whistle에서 트래픽 데이터 가져오는 중...${NC}"
    
    curl -s -u "${WHISTLE_USER}:${WHISTLE_PASS}" \
        "${WHISTLE_URL}/cgi-bin/get-data?count=${count}" \
        -o "$TEMP_FILE"
    
    if [ ! -f "$TEMP_FILE" ] || [ ! -s "$TEMP_FILE" ]; then
        echo -e "${RED}데이터를 가져오는 데 실패했습니다.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}데이터 가져오기 완료!${NC}"
}

# 트래픽 분석
analyze_traffic() {
    local count="$1"
    local output="$2"
    local verbose="$3"
    local json_output="$4"
    
    init
    
    if [ -n "$4" ] && [ -f "$4" ]; then
        TEMP_FILE="$4"
        echo -e "${BLUE}기존 파일 사용: $4${NC}"
    else
        fetch_data "$count"
    fi
    
    local analyzer_dir
    analyzer_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local analyzer="${analyzer_dir}/whistle_traffic_analyzer.py"
    
    local cmd=("python3" "$analyzer" "-f" "$TEMP_FILE")
    
    if [ -n "$output" ]; then
        cmd+=("-o" "$output")
    fi
    
    if [ "$verbose" = true ]; then
        cmd+=("-v")
    fi
    
    echo -e "${BLUE}트래픽 분석 중...${NC}"
    
    if [ "$json_output" = true ]; then
        "${cmd[@]}" | python3 -m json.tool
    else
        "${cmd[@]}"
    fi
}

# 실시간 모니터링
monitor_traffic() {
    local count="${1:-100}"
    local interval="${2:-5}"
    
    echo -e "${BLUE}실시간 트래픽 모니터링 (Ctrl+C로 종료)${NC}"
    echo -e "${YELLOW}데이터 수: $count, 갱신 주기: ${interval}초${NC}"
    echo ""
    
    init
    
    while true; do
        fetch_data "$count"
        
        clear
        echo -e "${BLUE}실시간 트래픽 모니터링 - $(date '+%Y-%m-%d %H:%M:%S')${NC}"
        echo -e "${YELLOW}데이터 수: $count, 갱신 주기: ${interval}초${NC}"
        echo ""
        
        local analyzer_dir
        analyzer_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        local analyzer="${analyzer_dir}/whistle_traffic_analyzer.py"
        
        python3 "$analyzer" -f "$TEMP_FILE" 2>&1 | head -50
        
        echo ""
        echo -e "${GREEN}다음 갱신까지 ${interval}초 대기 중... (Ctrl+C로 종료)${NC}"
        
        sleep "$interval"
    done
}

# 메인
main() {
    local command="analyze"
    local count=600
    local output=""
    local verbose=false
    local json_output=false
    local file=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            analyze|monitor|export|help)
                command="$1"
                shift
                ;;
            -c|--count)
                count="$2"
                shift 2
                ;;
            -o|--output)
                output="$2"
                shift 2
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            -f|--file)
                file="$2"
                shift 2
                ;;
            --json)
                json_output=true
                shift
                ;;
            -h|--help|help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}알 수 없는 옵션: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    case $command in
        analyze)
            analyze_traffic "$count" "$output" "$verbose" "$json_output" "$file"
            ;;
        monitor)
            monitor_traffic "$count"
            ;;
        export)
            if [ -z "$output" ]; then
                timestamp=$(date +%Y%m%d_%H%M%S)
                output="${OUTPUT_DIR}/stats_${timestamp}.json"
            fi
            analyze_traffic "$count" "$output" "$verbose" false "$file"
            ;;
        help)
            show_help
            ;;
        *)
            echo -e "${RED}알 수 없는 명령: $command${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
