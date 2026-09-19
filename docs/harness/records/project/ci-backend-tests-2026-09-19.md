# GitHub Actions 백엔드 테스트 CI 추가 (2026-09-19)

## 목적
README 한계 절의 "CI 없음"을 해소한다. push(main)·pull request마다 백엔드 pytest를 자동 실행한다.

## 변경
- `.github/workflows/backend-tests.yml` 추가
  - Python 3.13, `backend/requirements.txt` 설치, `python -m pytest -q -rs -p no:cacheprovider`
  - `.env` 없이 도는지 확인하기 위해 필수 설정만 더미 값으로 넣는다: `DATABASE_URL=sqlite+aiosqlite:///./ci.db`, `PROJECT_NAME`, `API_V1_STR`, `SECRET_KEY`(CI 전용, 비밀 아님). LLM·외부 API는 테스트에서 모킹한다.
- `backend/tests/test_ai_report_quality_gate.py::test_structured_external_provider_reports_missing_key_without_network`
  - **로컬 `.env`에 `COINGECKO_DEMO_API_KEY`가 있어야만 통과하던 테스트**였다. 키가 없으면 `fetch_coingecko_data_structured`가 매핑 검사 전에 `missing`을 돌려줘 `unsupported` 단언이 실패한다.
  - 테스트 안에서 `COINGECKO_DEMO_API_KEY`를 가짜 값으로 monkeypatch해 환경과 무관하게 만들었다(매핑에 없는 티커라 네트워크 호출 없음).
- README: 상단 CI 배지, 한계 절 갱신.

## 검증
- `git archive HEAD`로 만든 깨끗한 사본(.env 없음)에서 CI와 같은 환경변수로 실행: 수정 전 `1 failed, 226 passed` → 수정 후 `227 passed`.
- 로컬(.env 있음)에서도 `227 passed`.
- 푸시 후 Actions 실행 결과는 커밋 이후 확인.

## 남은 위험
- 프론트엔드(lint/build)는 CI에 넣지 않았다(팀원 담당 영역).
