# 문서 색인

프로젝트 문서는 목적에 따라 네 폴더로 나뉩니다. 문서와 코드가 다르면 **현재 코드가 기준**입니다.

## architecture/ — 구조와 설계

| 문서 | 내용 |
| --- | --- |
| [CODE_UNDERSTANDING.md](architecture/CODE_UNDERSTANDING.md) | 처음 읽을 문서. 전체 구조, API, 스케줄러, AI 파이프라인, 데이터 흐름 |
| [ARCHITECTURE.md](architecture/ARCHITECTURE.md) | 런타임 경계와 아키텍처 개요 (일부 초기 청사진 서술 포함) |
| [PROJECT_STRUCTURE_ANALYSIS.md](architecture/PROJECT_STRUCTURE_ANALYSIS.md) | 폴더 소유권 지도 |
| [PROJECT_FUNCTION_DETAIL_SPEC.md](architecture/PROJECT_FUNCTION_DETAIL_SPEC.md) | 초기 기능 상세 명세 (로그인 방식 등 일부는 현재 코드와 다름) |

## guides/ — 설정 가이드

| 문서 | 내용 |
| --- | --- |
| [ENVIRONMENT_VARIABLE_SETUP.md](guides/ENVIRONMENT_VARIABLE_SETUP.md) | 환경변수 설정 방법 |
| [ENVIRONMENT_VARIABLE_RECOMMENDATIONS.md](guides/ENVIRONMENT_VARIABLE_RECOMMENDATIONS.md) | 환경별 권장값 |
| [GMAIL_OAUTH_REFRESH_TOKEN_SETUP.md](guides/GMAIL_OAUTH_REFRESH_TOKEN_SETUP.md) | Gmail 발송용 OAuth refresh token 발급 |
| [TELEGRAM_MESSAGE_RECEIVE_PROCEDURE.md](guides/TELEGRAM_MESSAGE_RECEIVE_PROCEDURE.md) | Telegram 알림 연결 절차 |
| [STOOQ_APIKEY_GUIDE.md](guides/STOOQ_APIKEY_GUIDE.md) | Stooq API 키 발급 |
| [VERCEL_SUPABASE_INTEGRATION_GUIDE.md](guides/VERCEL_SUPABASE_INTEGRATION_GUIDE.md) | Vercel·Render·Supabase 배포 연동 |

## deliverables/ — 캡스톤 최종 산출물

[README](deliverables/README.md) 참고. 시스템 흐름도, 스토리보드, 기능상세 명세서, ERD, API 명세서, 개발 환경, 방학 목표 7종.

## harness/ — AI 코딩 하네스 문서와 개발 기록

| 위치 | 내용 |
| --- | --- |
| [feature-index.md](harness/feature-index.md) | 기능 영역별 문서·코드·기록 색인 |
| [feature-documentation-guide.md](harness/feature-documentation-guide.md) | 문서 작성 규칙 |
| [features/](harness/features/) | 기능별 설명 문서 |
| [error-casebook-2026-06-03.md](harness/error-casebook-2026-06-03.md) | 오류 사례 모음 |
| [records/](harness/records/) | 계획·구현·검증·분석 기록 (영역별) |

`records/` 하위 영역:

| 폴더 | 내용 |
| --- | --- |
| [ai-report/](harness/records/ai-report/) | LangGraph 리포트 품질 게이트, 스케줄러, 리포트 생성 장애 대응 |
| [market-data/](harness/records/market-data/) | 시세·뉴스 공급자 전환, 캐시, 대시보드 지수 |
| [chatbot/](harness/records/chatbot/) | 챗봇 기능, LLM 의도 분류, 멀티턴 |
| [notifications/](harness/records/notifications/) | 즐겨찾기 알림, Gmail·Telegram 발송, 다이제스트 |
| [billing/](harness/records/billing/) | 구독 등급, 결제(Mock·Toss) |
| [auth/](harness/records/auth/) | Google 로그인 |
| [user-features/](harness/records/user-features/) | 즐겨찾기, 커뮤니티 댓글, 마이페이지 |
| [deployment/](harness/records/deployment/) | Docker, Vercel, Render, Supabase 배포와 런타임 |
| [project/](harness/records/project/) | 전체 결함 감사, 로드맵, 최종 산출물, 하네스 구축 |

파일 이름 규칙: `<주제>-<plan|implementation|verification|...>-<YYYY-MM-DD>.md`
