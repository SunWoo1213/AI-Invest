# 저장소 문서 재배치 및 포트폴리오 README 작성

- 날짜: 2026-09-17
- 작업자: Claude Code (사용자 요청)
- 영역: 프로젝트 전반 (문서 구조)

## 목적

취업 포트폴리오로 쓰기 위해 루트, `최종산출물/`, `docs/harness/`(평면 약 170개)에 흩어져 있던 문서를 목적별로 정리하고, 루트에 프로젝트 소개용 `README.md`를 작성한다.

사용자 지시: **진행 기록 파일은 증거물로 보존하므로 삭제하지 않는다.** 이번 작업에서 삭제한 파일은 없고, 모두 `git mv`로 이동했다(히스토리 보존).

## 변경 내용

### 이동

| 이전 위치 | 새 위치 |
| --- | --- |
| 루트 `ARCHITECTURE.md`, `CODE_UNDERSTANDING.md`, `PROJECT_STRUCTURE_ANALYSIS.md`, `PROJECT_FUNCTION_DETAIL_SPEC.md` | `docs/architecture/` |
| 루트 `ENVIRONMENT_VARIABLE_SETUP.md`, `ENVIRONMENT_VARIABLE_RECOMMENDATIONS.md`, `GMAIL_OAUTH_REFRESH_TOKEN_SETUP.md`, `STOOQ_APIKEY_GUIDE.md`, `TELEGRAM_MESSAGE_RECEIVE_PROCEDURE.md`, `VERCEL_SUPABASE_INTEGRATION_GUIDE.md` | `docs/guides/` |
| `최종산출물/*` | `docs/deliverables/` |
| `docs/harness/<기록>.md` (feature-index, feature-documentation-guide, error-casebook 제외) | `docs/harness/records/<영역>/` |
| 루트 `backend_server.*.log`, `frontend_server.*.log` (빈 파일) | `.codex-runtime/` |
| 루트 `test_api.py`, `test_db.py` | `scripts/` |

`records/` 영역 분류 (파일명 접두어 기준): `ai-report`(43), `market-data`(36), `deployment`(23), `notifications`(21), `project`(16+1), `billing`(12), `chatbot`(8), `user-features`(6), `auth`(4).

### 신규

- `README.md` — 포트폴리오용 프로젝트 소개 (기능, 아키텍처·AI 파이프라인 Mermaid 다이어그램, 기술 스택, 트러블슈팅, 하네스 개발 프로세스, 실행 방법).
- `docs/README.md` — 문서 색인.
- 이 기록 문서.

### 참조 보정

- 이동한 문서를 가리키는 모든 Markdown 상대 링크와 백틱 경로(`docs/harness/...`, `ARCHITECTURE.md` 등)를 스크립트로 일괄 재계산했다.
- 저장소 루트 기준으로 쓰인 링크(`](backend/...)` 형태, IDE 워크스페이스 기준)는 기존 관례대로 유지했다.
- `AGENTS.md`: Repository Map 갱신, §12 변경 기록 저장 위치를 `docs/harness/records/<area>/`로 명시.
- `CLAUDE.md`: `CODE_UNDERSTANDING.md` 경로 갱신.
- `.claude/commands/harness-{plan,implement,verify}.md`, `.claude/agents/harness-doc-writer.md`, `.codex/agents/harness-doc-writer.toml`: 기록 파일 경로 템플릿을 `docs/harness/records/<영역>/...`로 변경.
- `docs/harness/feature-documentation-guide.md`, `docs/harness/feature-index.md`: 기록 위치 규칙과 색인 갱신.
- `docs/architecture/CODE_UNDERSTANDING.md`(§2, §9), `ARCHITECTURE.md`, `PROJECT_STRUCTURE_ANALYSIS.md`: 구조 트리 갱신.
- `scripts/check_env_var_doc_sync.py`: `DOC_SET` 경로를 `docs/guides/`로 갱신.
- `scripts/test_db.py`: 이동에 맞춰 `sys.path`를 저장소 루트로 보정 (`backend.app...` import 유지).

## 동작 변화

애플리케이션 코드(`backend/app`, `frontend/src`)는 바뀌지 않았다. 하네스가 새 기록을 `docs/harness/records/<영역>/`에 쓰도록 규칙이 바뀌었다.

## 검증

- 전체 Markdown 상대 링크 검사: `node_modules` 내부(서드파티)를 제외하면 깨진 링크 0건.
- `python scripts/check_env_var_doc_sync.py --check`: 변경한 경로(`docs/guides/...`)로 정상 동작. 다만 exit 1 — 이번 작업과 무관하게 원래 있던 드리프트 8건(`CHATBOT_*` 5개, `DATA_GO_KR_*` 2개, `REPORT_MAX_REVISIONS`가 `.env.example`에 없음).

## 실행하지 않은 명령

- `pytest`, `npm run lint/build`: 애플리케이션 코드 변경이 없어 실행하지 않음.
- `scripts/test_api.py`, `scripts/test_db.py`: 실제 OpenAI 호출과 DB 연결이 필요해 실행하지 않음.

## 후속 위험

- 위 환경변수 드리프트 8건은 이번 범위 밖이라 수정하지 않았다. `.env.example`과 환경변수 가이드에 추가해야 한다.
- 이 날짜 이전 기록 본문 안의 `docs/harness/<파일>` 경로는 새 경로로 바뀌었으므로, 당시 문맥과 경로가 달라 보일 수 있다(내용은 그대로).
- 사용하지 않는 `.pytest_deps/`(벤더링 패키지), `.obsidian/`, `.codex-runtime/` 로그, Vite 템플릿 그대로인 `frontend/README.md`는 사용자 지시에 따라 그대로 두었다. 공개 전에 정리할지는 사용자가 결정한다.
- `backend/node_modules/`가 `.gitignore`에 없다(현재 추적되지는 않음).
- README의 배포 URL은 문서 기록 기준이며, 현재 서비스가 켜져 있는지는 확인하지 않았다.
