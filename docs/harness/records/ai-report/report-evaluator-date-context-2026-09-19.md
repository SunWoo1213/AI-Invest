# LLM 편집장에 오늘 날짜 · 데이터 기준 시각 · 알려진 한계 제공 (2026-09-19)

## 목적
[반복 측정](report-generation-measurement-2026-09-19.md)에서 LLM 편집장(`evaluator_node`)이 51번 호출되어 한 번도 PASS하지 않았다. 프롬프트가 `"{current_year}년 최신성"`만 요구하고 오늘 날짜와 데이터 기준 시각을 주지 않아, 모델이 자기 학습 시점을 "현재"로 보고 2026년 데이터를 비최신으로 판단했다(한 번은 "현재 시점이 2023년"). 판단 근거를 주는 것이 목적이며, 게이트를 끄거나 느슨하게 하지 않는다.

## 변경 파일
- `backend/app/services/graph/nodes.py`
  - `_evaluator_time_context(state)` 추가: `today_utc`(`core.clock.utcnow`), `data_as_of`(`structured_facts.data_as_of` → `report_facts.price.as_of`), `known_limitations`(`data_limitations` + `missing_required_facts`).
  - `evaluator_node` 프롬프트: 오늘 날짜와 기준 시각을 "현재"로 보라고 명시, 5개 평가 항목을 구체화(최신성 = 리포트 기준 시각과 데이터 기준 시각 일치 · 오래된 정보를 현재처럼 쓰지 않음, 데이터 한계는 **명시되어 있으면** 그 자체로 FAIL 아님 · 숨기거나 없는 데이터를 있는 것처럼 쓰면 FAIL). "하나라도 미흡하면 FAIL"은 유지.
- `backend/tests/test_ai_report_quality_gate.py`: `test_evaluator_prompt_gives_today_and_data_as_of` — 프롬프트에 오늘 날짜 · 기준 시각 · 한계 목록이 들어가는지, `revision_count` 증가를 검증(LLM은 `RunnableLambda`로 대체).
- 문서: `features/asset-detail-ai-community.md` 19단계 설명 · Change Records, `feature-index.md`.

## 동작 변화
- 사용자 요청이 리포트를 생성하는 경로는 바뀌지 않았다(스케줄러 전용 유지).
- 편집장 호출 수 · 모델 · 재작성 한도는 같다. 프롬프트 입력만 늘었다.

## 검증
- `pytest -q -p no:cacheprovider` (backend): 228 passed.
- 같은 조건 재측정 20건(5개 자산 × 4회, 로컬 · 새 임시 SQLite · gpt-4o-mini · `REPORT_MAX_REVISIONS=7`, 2026-09-19 22:48~23:23 KST):

| 지표 | 수정 전 | 수정 후 |
| --- | --- | --- |
| 게이트 정상 통과(편집장 PASS 후 저장) | 0 / 20 | **5 / 20** |
| 숫자 정제 폴백 저장 | 5 / 20 | 5 / 20 |
| 거부 | 15 / 20 | 10 / 20 |
| 편집장 PASS / 호출 | 0 / 51 | 5 / 47 |
| 거부 마지막 사유 | 편집장 11 · 형식 2 · 정성 1 · 숫자 1 | 편집장 6 · 숫자 3 · 형식 1 |
| 건당 평균 비용 · 시간 · LLM 호출 | $0.0127 · 83초 · 15.4회 | $0.0120 · 78초 · 14.4회 |
| 정상 통과본의 재작성 횟수 | — | 1, 1, 3, 5, 7 (평균 $0.0112) |

자산별(수정 후): XAU 정상 4/4 · DGS10 정상 1/4 · BTC-USD 폴백 4/4 · NVDA 폴백 1/4 · 005930.KS 0/4.

## 해석 · 남은 문제
- 편집장 피드백이 "현재 시점이 2023년" 같은 날짜 오판에서 **"'6시간 전' 표현이 모호하다"는 내용 지적**으로 바뀌었다(남은 편집장 거부 6건 중 5건). writer가 상대 시각 표현을 쓰지 않고 절대 시각을 쓰게 하는 것이 다음 개선 후보다.
- 005930.KS는 형식 게이트(자산군 필수 토픽)와 편집장에서 계속 실패한다.
- DGS10은 정성 주장 게이트 6회 실패 후 숫자 게이트로 끝나는 패턴이 3건이다.
- 폴백 저장 경로는 여전히 편집장을 거치지 않는다.
- 표본이 20건이라 수치에는 실행마다 편차가 있다. 운영(Render) 수치가 아니다.
