#!/usr/bin/env python3

import json
import sys
import argparse
from collections import defaultdict, Counter
from urllib.parse import urlparse
from typing import Dict, List, Any, Union


def extract_domain(url: str) -> str:
    try:
        parsed = urlparse(url)
        return parsed.netloc or "unknown"
    except Exception:
        return "unknown"


def calculate_duration(item: Dict[str, Any]) -> float:
    start_time = item.get("startTime", 0)
    end_time = item.get("endTime", 0)
    if start_time and end_time:
        return (end_time - start_time) / 1000
    return 0.0


def calculate_ttfb(item: Dict[str, Any]) -> float:
    ttfb = item.get("ttfb", 0)
    return ttfb / 1000 if ttfb else 0.0


def calculate_dns_time(item: Dict[str, Any]) -> float:
    dns_time = item.get("dnsTime", 0)
    if dns_time and dns_time < 100000:  # timestamp 아닌 실제 DNS 시간만 계산
        return dns_time / 1000  # ms to seconds
    return 0.0


def analyze_traffic(traffic_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    if not traffic_data:
        return {"error": "No traffic data available"}

    total_requests = len(traffic_data)

    def init_domain_stats() -> Dict[str, Any]:
        return {
            "count": 0,
            "total_req_size": 0,
            "total_res_size": 0,
            "total_duration": 0.0,
            "total_ttfb": 0.0,
            "status_codes": Counter(),
            "methods": Counter(),
        }

    domains = defaultdict(init_domain_stats)
    status_codes = Counter()
    methods = Counter()

    req_sizes: List[int] = []
    res_sizes: List[int] = []
    durations: List[float] = []
    ttfbs: List[float] = []

    http_versions = Counter()
    use_h2_count = 0

    dns_times: List[float] = []

    for item in traffic_data.values():
        url = item.get("url", "")
        domain = extract_domain(url)

        domains[domain]["count"] += 1

        req_size = item.get("req", {}).get("size", 0)
        domains[domain]["total_req_size"] += req_size
        req_sizes.append(req_size)

        res_size = item.get("res", {}).get("size", 0)
        domains[domain]["total_res_size"] += res_size
        res_sizes.append(res_size)

        duration = calculate_duration(item)
        domains[domain]["total_duration"] += duration
        durations.append(duration)

        ttfb = calculate_ttfb(item)
        domains[domain]["total_ttfb"] += ttfb
        ttfbs.append(ttfb)

        status_code = item.get("res", {}).get("statusCode", 0)
        domains[domain]["status_codes"][status_code] += 1
        status_codes[status_code] += 1

        method = item.get("req", {}).get("method", "UNKNOWN")
        domains[domain]["methods"][method] += 1
        methods[method] += 1

        http_version = item.get("req", {}).get("httpVersion", "UNKNOWN")
        http_versions[http_version] += 1

        if item.get("useH2"):
            use_h2_count += 1

        dns_time = calculate_dns_time(item)
        if dns_time > 0:
            dns_times.append(dns_time)

    avg_req_size = sum(req_sizes) / len(req_sizes) if req_sizes else 0
    avg_res_size = sum(res_sizes) / len(res_sizes) if res_sizes else 0
    avg_duration = sum(durations) / len(durations) if durations else 0
    avg_ttfb = sum(ttfbs) / len(ttfbs) if ttfbs else 0
    avg_dns_time = sum(dns_times) / len(dns_times) if dns_times else 0

    total_req_size = sum(req_sizes)
    total_res_size = sum(res_sizes)

    sorted_domains = sorted(domains.items(), key=lambda x: x[1]["count"], reverse=True)

    top_domains = [
        {
            "domain": domain,
            "requests": data["count"],
            "avg_req_size": data["total_req_size"] / data["count"]
            if data["count"]
            else 0,
            "avg_res_size": data["total_res_size"] / data["count"]
            if data["count"]
            else 0,
            "avg_duration": data["total_duration"] / data["count"]
            if data["count"]
            else 0,
            "avg_ttfb": data["total_ttfb"] / data["count"] if data["count"] else 0,
            "status_codes": dict(data["status_codes"]),
            "methods": dict(data["methods"]),
        }
        for domain, data in sorted_domains[:10]
    ]

    def sort_key(x):
        key = x[0]
        try:
            return (0, int(key))
        except (ValueError, TypeError):
            return (1, str(key))

    return {
        "basic": {
            "total_requests": total_requests,
            "total_req_size": total_req_size,
            "total_res_size": total_res_size,
            "avg_req_size": avg_req_size,
            "avg_res_size": avg_res_size,
            "avg_duration": avg_duration,
            "min_duration": min(durations) if durations else 0,
            "max_duration": max(durations) if durations else 0,
            "avg_ttfb": avg_ttfb,
            "min_ttfb": min(ttfbs) if ttfbs else 0,
            "max_ttfb": max(ttfbs) if ttfbs else 0,
            "avg_dns_time": avg_dns_time,
            "http2_usage": {
                "total": use_h2_count,
                "percentage": (use_h2_count / total_requests * 100)
                if total_requests
                else 0,
            },
        },
        "domains": top_domains,
        "status_codes": dict(sorted(status_codes.items(), key=sort_key)),
        "methods": dict(methods),
        "http_versions": dict(http_versions),
        "size_distribution": {
            "total_req_size": total_req_size,
            "total_res_size": total_res_size,
            "req_size_ranges": {
                "< 1KB": sum(1 for s in req_sizes if s < 1024),
                "1KB - 10KB": sum(1 for s in req_sizes if 1024 <= s < 10240),
                "10KB - 100KB": sum(1 for s in req_sizes if 10240 <= s < 102400),
                "100KB - 1MB": sum(1 for s in req_sizes if 102400 <= s < 1048576),
                ">= 1MB": sum(1 for s in req_sizes if s >= 1048576),
            },
            "res_size_ranges": {
                "< 1KB": sum(1 for s in res_sizes if s < 1024),
                "1KB - 10KB": sum(1 for s in res_sizes if 1024 <= s < 10240),
                "10KB - 100KB": sum(1 for s in res_sizes if 10240 <= s < 102400),
                "100KB - 1MB": sum(1 for s in res_sizes if 102400 <= s < 1048576),
                ">= 1MB": sum(1 for s in res_sizes if s >= 1048576),
            },
        },
    }


def format_size(size: Union[int, float]) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def format_time(time: float) -> str:
    if time < 1.0:
        return f"{time * 1000:.2f} ms"
    return f"{time:.2f} s"


def print_statistics(stats: Dict[str, Any], verbose: bool = False):
    if "error" in stats:
        print(f"오류: {stats['error']}")
        return

    print("=" * 60)
    print("📊 Whistle 트래픽 통계")
    print("=" * 60)

    basic = stats["basic"]
    print("\n【기본 요청 통계】")
    print(f"  총 요청 수: {basic['total_requests']:,}")
    print(f"  총 요청 크기: {format_size(basic['total_req_size'])}")
    print(f"  총 응답 크기: {format_size(basic['total_res_size'])}")
    print(f"  평균 요청 크기: {format_size(basic['avg_req_size'])}")
    print(f"  평균 응답 크기: {format_size(basic['avg_res_size'])}")
    print(f"  평균 응답 시간: {format_time(basic['avg_duration'])}")
    print(f"  최소 응답 시간: {format_time(basic['min_duration'])}")
    print(f"  최대 응답 시간: {format_time(basic['max_duration'])}")
    print(f"  평균 TTFB: {format_time(basic['avg_ttfb'])}")
    print(f"  최소 TTFB: {format_time(basic['min_ttfb'])}")
    print(f"  최대 TTFB: {format_time(basic['max_ttfb'])}")
    if basic["avg_dns_time"] > 0:
        print(f"  평균 DNS 시간: {format_time(basic['avg_dns_time'])}")
    print(
        f"  HTTP/2 사용: {basic['http2_usage']['total']} ({basic['http2_usage']['percentage']:.1f}%)"
    )

    print("\n【Top 10 도메인별 통계】")
    for i, domain in enumerate(stats["domains"], 1):
        print(f"\n  {i}. {domain['domain']}")
        print(f"     요청: {domain['requests']}회")
        print(f"     평균 요청 크기: {format_size(domain['avg_req_size'])}")
        print(f"     평균 응답 크기: {format_size(domain['avg_res_size'])}")
        print(f"     평균 응답 시간: {format_time(domain['avg_duration'])}")
        if verbose and domain["status_codes"]:
            print(f"     상태 코드: {dict(domain['status_codes'])}")
        if verbose and domain["methods"]:
            print(f"     메서드: {dict(domain['methods'])}")

    def sort_key_func(x):
        key = x[0]
        try:
            return (0, int(key))
        except (ValueError, TypeError):
            return (1, str(key))

    print("\n【상태 코드별 통계】")
    for code, count in sorted(stats["status_codes"].items(), key=sort_key_func):
        percentage = (
            (count / basic["total_requests"] * 100) if basic["total_requests"] else 0
        )
        print(f"  {code}: {count}회 ({percentage:.1f}%)")

    print("\n【메서드별 통계】")
    for method, count in sorted(stats["methods"].items()):
        percentage = (
            (count / basic["total_requests"] * 100) if basic["total_requests"] else 0
        )
        print(f"  {method}: {count}회 ({percentage:.1f}%)")

    print("\n【HTTP 버전별 통계】")
    for version, count in sorted(stats["http_versions"].items()):
        percentage = (
            (count / basic["total_requests"] * 100) if basic["total_requests"] else 0
        )
        print(f"  {version}: {count}회 ({percentage:.1f}%)")

    size_dist = stats["size_distribution"]
    print("\n【요청 크기 분포】")
    for range_name, count in size_dist["req_size_ranges"].items():
        percentage = (
            (count / basic["total_requests"] * 100) if basic["total_requests"] else 0
        )
        print(f"  {range_name}: {count}회 ({percentage:.1f}%)")

    print("\n【응답 크기 분포】")
    for range_name, count in size_dist["res_size_ranges"].items():
        percentage = (
            (count / basic["total_requests"] * 100) if basic["total_requests"] else 0
        )
        print(f"  {range_name}: {count}회 ({percentage:.1f}%)")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Whistle 트래픽 통계 분석 도구")
    parser.add_argument(
        "-f", "--file", help="JSON 파일 경로 (지정하지 않으면 stdin에서 읽음)"
    )
    parser.add_argument("-o", "--output", help="JSON 결과 파일로 저장")
    parser.add_argument("-v", "--verbose", action="store_true", help="상세 정보 표시")

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    traffic_data = data.get("data", {}).get("data", {})

    stats = analyze_traffic(traffic_data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"결과가 {args.output}에 저장되었습니다.")
    else:
        print_statistics(stats, verbose=args.verbose)


if __name__ == "__main__":
    main()
