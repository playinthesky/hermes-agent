# 실행 지침 — 일일 문서 변경 감시 (매일 19:00)

> 이 문서는 스케줄러(hermes cron / 웹 예약 트리거)가 기동한 **에이전트가 그대로 수행**하는
> 실행 지침입니다. 절차의 표준은 [SOP-004](../sop/SOP-004-daily-document-watch.md).

## 수행 단계

1. **flow 변경 스캔**
   ```bash
   python3 consulting-library/scripts/flow_doc_changes.py --since "24 hours ago"
   ```
   출력(마크다운 조각)을 다이제스트의 "flow" 섹션으로 사용한다.

2. **Google Drive 변경 스캔** — MCP 도구 사용:
   - `list_recent_files(orderBy="lastModified", pageSize=20, excludeContentSnippets=true)` 호출,
     `modifiedTime`이 최근 24시간 이내인 항목만 채택. (또는
     `search_files(query="modifiedTime > '<24h전 RFC3339>'")`)
   - 각 항목에서 `title`, `mimeType`, `modifiedTime`, `viewUrl`을 추출.
   - 스코프가 넓으면 특정 폴더(`parentId = '<folder id>'`)로 한정한다.

3. **다이제스트 작성** — 아래 형식으로 합친다:
   ```
   # 📄 일일 문서 다이제스트 — {YYYY-MM-DD}
   {flow 섹션: 스크립트 출력}
   ## Google Drive — 최근 변경 문서
   | 변경시각 | 문서 | 유형 | 링크 |
   | ... |
   ## 가(假)트리아지
   - {문서} → 추정 도메인 {domain} (근거: 제목 키워드)
   ```
   각 문서는 [triage-guide](../intake/triage-guide.md)의 키워드 표로 도메인을 추정해 붙인다.

4. **전달** — 다이제스트를 설정된 비공개 채널로 전달한다(Slack/메일 등).
   변경이 flow·Drive 모두 0건이면 "변경 없음"만 전달하거나 생략(소음 방지).

5. **(선택) 후보 아젠다 초안** — 명백히 새 의뢰로 보이는 문서가 있으면
   [SOP-002](../sop/SOP-002-agenda-knowledge-capture.md) 절차로 `status/wip` 후보 아젠다를 초안화한다.

## ⚠️ 개인정보·보안 주의

- Google Drive 문서는 **내부·민감 자료일 수 있다.** 다이제스트(제목/내용 포함)를
  **공개 git 저장소에 커밋하지 않는다.** 전달은 비공개 채널 또는 gitignore된 로컬 경로로 한정한다.
- 문서 본문은 필요한 경우에만 `read_file_content`로 열람하고, 요약은 최소 정보로 한정한다.
