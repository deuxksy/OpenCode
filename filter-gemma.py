import json
import re
from mitmproxy import http
from mitmproxy import ctx

def request(flow: http.HTTPFlow):
    # 1. 대상 도메인 및 모델 식별 (Gemma 3 계열 전체)
    url = flow.request.pretty_url
    is_gemini_api = "generativelanguage.googleapis.com" in url
    
    if is_gemini_api:
        try:
            payload_text = flow.request.get_text()
            data = json.loads(payload_text)
            modified = False

            # 2. Gemma 3 제품군 판별 (URL 또는 Payload 내 model 필드 확인)
            # 1b, 4b, 12b, 27b, e2b 등 모든 gemma-3 패턴 매칭
            is_gemma3 = re.search(r'gemma-3', url) or re.search(r'gemma-3', str(data.get("model", "")))

            if is_gemma3:
                # A. [기존] Role Swap: system -> user
                for field in ["contents", "messages"]:
                    if field in data and isinstance(data[field], list):
                        for item in data[field]:
                            if item.get("role") == "system":
                                item["role"] = "user"
                                modified = True

                # B. [핵심] Gemma 3 호환성 처리 (Payload Pruning)
                # 지원하지 않는 필드들 숙청
                bad_fields = ["tools", "toolConfig"]
                for field in bad_fields:
                    if field in data:
                        del data[field]
                        modified = True
                        ctx.log.info(f"🚫 [GEMMA-3] Removed unsupported field: {field}")

                # C. generationConfig 세부 조정
                if "generationConfig" in data:
                    gen_cfg = data["generationConfig"]
                    # thinkingConfig 제거
                    if "thinkingConfig" in gen_cfg:
                        del gen_cfg["thinkingConfig"]
                        modified = True
                    
                    # 체급별 maxOutputTokens 최적화 (Senior's Touch)
                    # 1b/e2b 등 소형 모델은 컨텍스트가 너무 크면 추론 품질이 급격히 떨어집니다.
                    if "1b" in url or "e2b" in url:
                        if gen_cfg.get("maxOutputTokens", 0) > 4096:
                            gen_cfg["maxOutputTokens"] = 4096
                            modified = True

                if modified:
                    flow.request.text = json.dumps(data)
                    ctx.log.info(f"✅ [GEMMA-3] Payload sanitized for {url.split('/')[-1]}")

        except Exception as e:
            ctx.log.error(f"❌ [GEMMA-3] Filter Error: {e}")
