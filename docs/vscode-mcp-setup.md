# VSCode에서 MCP(Model Context Protocol) 추가하는 방법

## 1. MCP 소개

MCP(Model Context Protocol)는 AI 에이전트와 다양한 도구/리소스 간의 통신을 위한 표준 프로토콜입니다. VSCode에서 MCP를 사용하면 다양한 서비스와 통합할 수 있습니다.

## 2. 사전 요구사항

- VSCode 설치됨
- Node.js 및 npm 설치됨 (MCP 서버 실행용)
- MCP 서버 패키지 설치

## 3. MCP 서버 설치

### 방법 A: npm으로 MCP 서버 설치

```bash
# 전역으로 설치
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-github

# 또는 프로젝트 로컬로 설치
npm install @modelcontextprotocol/server-filesystem
npm install @modelcontextprotocol/server-github
```

### 방법 B: GitHub에서 복제하여 실행

```bash
git clone https://github.com/modelcontextprotocol/servers.git
cd servers
npm install
```

## 4. VSCode 설정에 MCP 추가

### 4.1 settings.json 파일 위치

**macOS**: `~/.config/Code/User/settings.json`
**Windows**: `%APPDATA%\Code\User\settings.json`
**Linux**: `~/.config/Code/User/settings.json`

### 4.2 MCP 설정 추가

settings.json 파일에 다음 설정을 추가합니다:

```json
{
  "mcp.servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/crong/git/OpenCode"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

### 4.3 로컬 MCP 서버 사용

로컬에 설치된 MCP 서버를 사용하는 경우:

```json
{
  "mcp.servers": {
    "custom-server": {
      "command": "node",
      "args": ["/Users/crong/git/mcp-servers/dist/index.js"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 5. MCP 확장 프로그램 설치

VSCode 마켓플레이스에서 MCP 관련 확장을 설치할 수도 있습니다:

1. VSCode를 열고 `Cmd+Shift+X` (macOS) 또는 `Ctrl+Shift+X` (Windows/Linux)를 누릅니다
2. 검색창에 "MCP" 또는 "Model Context Protocol"을 검색합니다
3. 확장 프로그램을 설치합니다

추천 확장:
- `Cline` (OpenCode에서 사용하는 AI 에이전트)
- `Continue.dev` (MCP 지원)

## 6. MCP 서버 확인

MCP 서버가 정상적으로 작동하는지 확인하려면:

1. VSCode를 다시 시작합니다
2. Output 패널에서 "MCP" 채널을 확인합니다
3. 로그 메시지를 통해 연결 상태를 확인합니다

## 7. 사용자 정의 MCP 서버 만들기

자신만의 MCP 서버를 만들 수 있습니다:

```bash
# 프로젝트 생성
mkdir my-mcp-server
cd my-mcp-server
npm init -y

# 의존성 설치
npm install @modelcontextprotocol/sdk

# 서버 코드 작성 (src/index.js)
# 예: 도구와 리소스 정의
```

서버 예시:

```javascript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server(
  {
    name: 'my-custom-server',
    version: '1.0.0'
  },
  {
    capabilities: {
      tools: {},
      resources: {}
    }
  }
);

// 도구 정의
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'custom_tool',
        description: '사용자 정의 도구',
        inputSchema: {
          type: 'object',
          properties: {
            message: { type: 'string' }
          }
        }
      }
    ]
  };
});

// 서버 시작
const transport = new StdioServerTransport();
await server.connect(transport);
```

## 8. OpenCode와 MCP 통합

이 프로젝트에서 MCP를 사용하는 경우, `opencode.json` 설정을 통해 에이전트와 MCP를 통합할 수 있습니다:

```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/crong/git/OpenCode"]
      }
    }
  }
}
```

## 9. 문제 해결

### 문제: MCP 서버가 연결되지 않음
- 해결: npm 패키지가 올바르게 설치되었는지 확인
- 해결: settings.json 경로가 올바른지 확인

### 문제: 권한 오류 발생
- 해결: 파일 시스템 경로에 대한 접근 권한 확인
- 해결: API 토큰이 올바른지 확인

### 문제: 서버가 느리게 응답
- 해결: npx 대신 전역으로 설치된 패키지 사용
- 해결: 서버 로그를 확인하여 병목 지점 찾기

## 10. 유용한 MCP 서버 목록

- `@modelcontextprotocol/server-filesystem`: 파일 시스템 접근
- `@modelcontextprotocol/server-github`: GitHub API 통합
- `@modelcontextprotocol/server-puppeteer`: 웹 스크래핑
- `@modelcontextprotocol/server-sqlite`: SQLite 데이터베이스
- `@modelcontextprotocol/server-postgres`: PostgreSQL 데이터베이스

## 추가 자료

- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [MCP 서버 저장소](https://github.com/modelcontextprotocol/servers)
- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk)