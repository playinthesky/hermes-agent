# SOP-004 · 일일 문서 변경 감시

| 문서번호 | SOP-004 | 버전 | v1.0 |
|----------|---------|------|------|
| 상태 | 발효 | 발효일 | 2026-06-22 |
| 소유자 | 도서관 관리자(LIB) | 실행 | 매일 19:00 (자동) |

## 1. 목적

매일 저녁, **flow(이 저장소)** 와 **Google Drive**에서 최근 24시간 내 변경된 문서를 자동 수집하여,
새 의뢰·변경 사항이 [SOP-001](./SOP-001-consulting-intake-to-delivery.md)의 입력으로 누락 없이
포착되도록 한다. 컨설턴트가 매일 수동으로 변경분을 확인하던 일을 표준 루틴으로 대체한다.

## 2. 적용 범위

- **flow**: 저장소 내 문서(`*.md/txt/pdf/docx/pptx/xlsx/csv`)의 git 변경.
- **Google Drive**: 최근 수정된 문서(`list_recent_files` / `search_files`로 `modifiedTime` 기준).
- **제외**: 본문 심층 분석은 포착된 문서에 한해 후속(SOP-001)에서 수행.

## 3. 용어 정의

| 용어 | 정의 |
|------|------|
| 다이제스트 | 당일 변경 문서를 flow/Drive로 나눠 정리한 일일 요약. |
| 후보 아젠다 | 변경 문서에서 도출된, 컨설턴트 검토 대기 상태의 아젠다 후보. |

## 4. 역할 및 책임

| 약어 | 역할 | 책임 |
|------|------|------|
| 자동 루틴 | 스케줄러(hermes cron / 웹 트리거)가 기동한 에이전트 | 스캔·다이제스트 생성·전달 |
| CON | 컨설턴트 | 다이제스트 검토, 의뢰화 여부 판단 |
| LIB | 도서관 관리자 | 루틴 상태·스코프(폴더/확장자) 관리 |

## 5. 절차 (자동 루틴이 매일 19:00 수행)

| # | 단계 | 활동 | 도구 |
|---|------|------|------|
| 1 | flow 스캔 | 최근 24h 변경 문서 집계 | `scripts/flow_doc_changes.py --since "24 hours ago"` |
| 2 | Drive 스캔 | 최근 24h 수정 문서 조회 | MCP `list_recent_files` (orderBy=lastModified) 또는 `search_files`(`modifiedTime > ...`) |
| 3 | 다이제스트 작성 | flow/Drive 변경분을 합쳐 요약, 각 문서를 도메인으로 가(假)트리아지 | [triage-guide](../intake/triage-guide.md) |
| 4 | 전달 | 다이제스트를 컨설턴트 채널로 전달 | (설정된 deliver 채널) |
| 5 | (선택)후보 적립 | 명백한 신규 의뢰는 `status/wip` 후보 아젠다로 초안화 | [SOP-002](./SOP-002-agenda-knowledge-capture.md) |

> 실행 지침(에이전트가 그대로 따르는 프롬프트): [`routines/daily-document-watch.md`](../routines/daily-document-watch.md)

### 판단점

- **2단계 스코프**: 전체 Drive가 너무 넓으면 특정 폴더(`parentId = '<folder>'`)로 한정.
- **3단계**: 변경이 0건이면 다이제스트에 "변경 없음"만 기록하고 전달은 생략(소음 방지) — 채널 설정에 따름.

## 6. 기록물 (Records)

| 기록물 | 위치 | 비고 |
|--------|------|------|
| 일일 다이제스트 | 전달 채널(또는 gitignore된 로컬 inbox) | **개인정보 주의**: Drive 문서 제목/내용은 git에 커밋하지 않는다 |

> ⚠️ Google Drive 문서는 내부·민감 자료일 수 있으므로 다이제스트를 **공개 저장소에 커밋하지 않는다**.
> 전달은 비공개 채널(Slack/메일 등) 또는 gitignore된 로컬 경로로 한정한다.

## 7. 관련 문서

- 스캐너: [`scripts/flow_doc_changes.py`](../scripts/flow_doc_changes.py)
- 실행 지침: [`routines/daily-document-watch.md`](../routines/daily-document-watch.md)
- 후속: [SOP-001](./SOP-001-consulting-intake-to-delivery.md), [SOP-002](./SOP-002-agenda-knowledge-capture.md)

## 8. 스케줄 설치 (영구 호스트 필요)

> 이 웹 세션 컨테이너는 일회성이라 스케줄을 **유지하지 못한다.** 아래 방식으로 1회 설치한다.
> **채택: Claude Code 웹 예약 트리거 + Slack 전달.**

**Claude Code 웹 예약 트리거 (채택):**
- 트리거: 매일 19:00 (사용자 시간대)
- 대상 저장소: `playinthesky/hermes-agent`
- 실행 프롬프트:
  > `consulting-library/routines/daily-document-watch.md`의 지침대로 flow와 Google Drive의
  > 최근 24시간 변경 문서를 스캔하고, 다이제스트를 Slack `#consulting-digest` 채널로 전달하라.

**대안 — hermes cron (영구 hermes 배포가 있을 때):**
```bash
hermes cron create "0 19 * * *" \
  "consulting-library/routines/daily-document-watch.md 의 지침을 수행하라." \
  --name "일일 문서 감시(flow+Drive)" \
  --deliver slack
```

## 9. 개정 이력

| 버전 | 일자 | 변경 요약 | 작성 |
|------|------|-----------|------|
| v1.0 | 2026-06-22 | 최초 발효. flow+Drive 일일 감시 루틴 신설. | LIB |
