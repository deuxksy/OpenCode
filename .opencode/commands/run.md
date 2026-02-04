---
description: 애플리케이션 실행
template: Run the main application with proper environment variables.
---

## Run the Application

### Start filter-gemma.py with mitmproxy

```bash
mitmdump -s filter-gemma.py
```

### Command Options

**Basic run:**
```bash
mitmdump -s filter-gemma.py
```

**Custom port:**
```bash
mitmdump -s filter-gemma.py -p 8080
```

**Interactive web UI:**
```bash
mitmweb -s filter-gemma.py
```

**With SSL verification:**
```bash
mitmdump -s filter-gemma.py --ssl-insecure
```

### Environment Setup

Before running, ensure environment variables are set:

```bash
# Load environment variables from .env file (if using python-dotenv)
source .env  # or use your preferred method
```

### What It Does

- Starts mitmproxy as an HTTP/HTTPS proxy
- Loads filter-gemma.py as an add-on
- Intercepts and modifies Gemma 3 API requests
- Logs modifications to console

### Testing the Proxy

1. Configure your browser/application to use the proxy (default: 127.0.0.1:8080)
2. Make a request to Gemini API
3. Check console output for filtering activity

### Troubleshooting

**Common Issues:**
- Port already in use → Change port with `-p` flag
- Certificate warnings → Install mitmproxy CA certificate
- Permission denied → Check file permissions

**Debug Mode:**
```bash
mitmdump -s filter-gemma.py -v
```
