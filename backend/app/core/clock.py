from datetime import datetime, timezone


def utcnow() -> datetime:
    """UTC 현재 시각(naive). DB 컬럼이 timezone 없는 DateTime이라 기존 datetime.utcnow()와 같은 값을 돌려준다."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
