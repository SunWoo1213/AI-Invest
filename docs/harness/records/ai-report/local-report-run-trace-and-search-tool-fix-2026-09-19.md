# 로컬 실제 실행으로 본 리포트 파이프라인 동작과 검색 도구 수정 (2026-09-19)

## 목적
포트폴리오 화면을 만들기 위해 로컬(임시 PostgreSQL, 실제 OpenAI · 시세 API)에서 리포트 생성을 직접 실행했다. 이 과정에서 드러난 동작과 결함을 기록한다. 사용자 요청이 리포트를 생성하는 경로는 바뀌지 않았다(스크립트에서 `generate_report_for_ticker`를 직접 호출).

## 실행 결과 요약

| 자산 | 결과 | 무슨 일이 있었나 |
| --- | --- | --- |
| NVDA | 저장 안 됨 | LLM 편집장(evaluator)이 "필수 재무 데이터(밸류에이션 · 베타) 누락"으로 거부 → `ReportQualityError`, 미저장 |
| BTC-USD, XAU (1차) | 파이프라인 중단 | 뉴스 에이전트의 DuckDuckGo 검색 도구가 `DDGSException(DNSError: wt.wikipedia.org)`를 던져 그래프 전체가 멈춤 |
| XAU (수정 후) | 저장됨 (`quality_status=pass`, `revision_count=7`) | 아래 트레이스 참고 |

## XAU 게이트 트레이스 (로그 발췌, 노드 시작 줄 생략)

```text
app.services.ai_service XAU market cache miss before report generation; attempting ticker-level cache fill
app.services.graph.nodes graph_node: financial_agent early-exit (ticker=XAU, category=COMMODITY)
app.services.graph.nodes graph_node: news_agent done (ticker=XAU)
app.services.graph.nodes graph_node: macro_agent done (ticker=XAU)
app.services.graph.nodes graph_node: synthesizer_node done (ticker=XAU)
app.services.graph.nodes graph_node: research_packet_node done (ticker=XAU)
app.services.graph.nodes graph_node: writer_node done (ticker=XAU)
app.services.graph.nodes graph_node: report_format_validator_node fail (ticker=XAU, missing=Missing asset-framework topics: 계절성, revision_count->1)
app.services.graph.nodes graph_node: writer_node done (ticker=XAU)
app.services.graph.nodes graph_node: report_format_validator_node fail (ticker=XAU, missing=Missing asset-framework topics: 계절성, revision_count->2)
app.services.graph.nodes graph_node: writer_node done (ticker=XAU)
app.services.graph.nodes graph_node: report_format_validator_node fail (ticker=XAU, missing=Missing asset-framework topics: 계절성, revision_count->3)
app.services.graph.nodes graph_node: writer_node done (ticker=XAU)
app.services.graph.nodes graph_node: report_format_validator_node pass (ticker=XAU)
app.services.graph.nodes graph_node: fact_checker_node fail (ticker=XAU, unsupported=57, revision_count->4)
app.services.graph.nodes graph_node: writer_node done (ticker=XAU)
app.services.graph.nodes graph_node: report_format_validator_node pass (ticker=XAU)
app.services.graph.nodes graph_node: fact_checker_node fail (ticker=XAU, unsupported=57, revision_count->5)
app.services.graph.nodes graph_node: writer_node done (ticker=XAU)
app.services.graph.nodes graph_node: report_format_validator_node fail (ticker=XAU, missing=Missing asset-framework topics: 계절성, revision_count->6)
app.services.graph.nodes graph_node: writer_node done (ticker=XAU)
app.services.graph.nodes graph_node: report_format_validator_node pass (ticker=XAU)
app.services.graph.nodes graph_node: fact_checker_node fail (ticker=XAU, unsupported=57, revision_count->7)
app.services.ai_service XAU fact_checker 루프 소진 후 숫자 정제 폴백으로 저장 (sanitized=['57'])
```

- 형식 게이트가 자산군 필수 토픽 "계절성" 누락으로 3회 거부 → writer가 피드백을 받아 재작성.
- 숫자 게이트가 근거 없는 숫자 `57`을 3회 거부.
- 재작성 한도(7)에 도달한 뒤 숫자 정제 폴백이 `57`만 `(수치 미확인)`으로 바꾸고 전 게이트를 다시 통과해 저장.

## 발견한 결함

1. **검색 도구 예외가 파이프라인 전체를 멈춤 (수정함)**
   - 원인: `requirements.txt`에 버전이 고정되지 않아 설치된 `ddgs 9.16.0`이 존재하지 않는 `wt.wikipedia.org`를 조회. `DuckDuckGoSearchResults`가 예외를 그대로 던져 에이전트 밖으로 전파됐다.
   - 수정: `backend/app/services/graph/tools.py`의 `search_tool`을 감싸 실패 시 "Search unavailable … use only the market data already provided" 문자열을 반환. 테스트 `backend/tests/test_graph_tools.py` 2건 추가.
2. **숫자 게이트가 시각 표기의 "초"를 근거 없는 숫자로 판단 (같은 날 수정)**
   - `57`은 리포트의 기준 시각 `04:19:57`의 초였다. 폴백이 이를 치환해 화면에 `기준 시각: 2026-09-19 04:19:(수치 미확인) (UTC)`로 표시됐다.
   - 수정: `nodes.py`에 `DATETIME_PATTERN`을 두고 `_find_unsupported_numbers` · `sanitize_unsupported_numbers`가 날짜 · 시각 표기 안의 숫자를 검사하지 않게 했다. 회귀 테스트 `test_number_gate_ignores_date_and_time_expressions` 추가.
3. **`requirements.txt` 버전 미고정 (같은 날 수정)** — 테스트(227 passed)와 실제 실행에 쓴 버전으로 `==` 고정.

## 검증
- `pytest -q -p no:cacheprovider` (backend): 226 passed.
- 수정 후 XAU 리포트 1건 생성 · 저장, 로컬 화면에서 확인(`docs/images/report.png`).

## 후속 위험
- 전이 의존성은 잠금 파일이 없어 고정되지 않는다(uv 전환 계획 참고).
