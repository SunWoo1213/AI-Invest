# JWT SECRET_KEY 하드코딩 기본값 제거 (2026-09-19)

## 목적

`backend/app/core/config.py`의 `SECRET_KEY` 기본값이 코드에 하드코딩되어 공개 저장소에 노출되어 있었다. 기본값을 없애고, 운영 환경에서 키가 없거나 노출된 값이면 기동을 거부한다.

## 변경 파일

- `backend/app/core/config.py` (커밋 81d5bef)

## 동작 변화

- `SECRET_KEY` 기본값을 빈 문자열로 바꿨다.
- `resolve_secret_key` 검증기(`model_validator(mode="after")`)를 추가했다.
  - 예전에 공개된 값(`LEAKED_SECRET_KEYS`)이 설정되어 있으면 `ValueError`로 거부한다.
  - 값이 비어 있고 `ENVIRONMENT != "development"`이면 `ValueError`로 기동을 거부한다.
  - 값이 비어 있고 개발 환경이면 `secrets.token_urlsafe(32)`로 프로세스별 임시 키를 만들고 WARNING 로그를 남긴다. 재시작하면 기존 토큰은 무효가 된다.
- 사용자 요청이 AI 리포트 생성을 일으키는지 여부는 바뀌지 않는다(생성하지 않음).

## 검증

- `cd backend; pytest` → 227 passed

## 후속 위험

- 운영(Render 등)에서 `SECRET_KEY`를 설정하지 않았다면 이제 기동이 실패한다. 배포 전 새 랜덤 값을 환경변수로 넣어야 한다.
- 예전 값은 git 기록에 남아 있으므로 노출된 것으로 본다. 그 값을 쓰던 환경이 있다면 키를 새로 만들어야 하며, 기존 JWT는 모두 무효가 된다.
