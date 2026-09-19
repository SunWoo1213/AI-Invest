# print 로그 정리와 datetime.utcnow() 교체 (2026-09-19)

## 목적

- 기동·시장 캐시 작업의 상태 출력이 `print()`로 남아 있어 로그 레벨·포맷을 따르지 않고, 예외 `repr`이 마스킹 없이 표준출력으로 나갔다.
- `datetime.utcnow()`가 Python 3.12부터 폐기 예정이라 pytest 실행 시 DeprecationWarning이 279건 나왔다.

## 변경 파일

- `backend/app/main.py`, `backend/app/services/market_service.py`: `print()` → `logger.info` / `logger.warning`. 예외는 `redact_secrets(repr(exc))`로 마스킹 후 기록.
- `backend/app/core/clock.py` (신규): `utcnow()` — `datetime.now(timezone.utc)`에서 tzinfo를 뗀 naive UTC. DB 컬럼이 timezone 없는 `DateTime`이라 기존 값과 동일하다.
- `backend/app/models.py`, `services/{notification,payment,profile,subscription}_service.py`, 관련 테스트 7개: `datetime.utcnow` → `utcnow`.
- `README.md`: "FastAPI API 46개" → 41개(직접 정의한 라우트 수 기준 재집계).

## 동작 변화

- 저장·비교되는 시각 값은 바뀌지 않는다(둘 다 naive UTC).
- 사용자 요청이 AI 리포트 생성을 일으키는지 여부는 바뀌지 않는다(생성하지 않음).

## 검증

- `cd backend; pytest -q` → 227 passed, 경고 0건 (변경 전 279건)
