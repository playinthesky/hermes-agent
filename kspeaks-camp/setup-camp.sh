#!/usr/bin/env bash
# ============================================================================
# 코리아스픽스 AI 캠프 — Hermes 자동화 등록 스크립트
# ============================================================================
# Hermes 가 이미 설치·설정(`hermes setup --portal`)되고, 텔레그램 게이트웨이
# (`hermes gateway setup`)와 `gh auth login` 이 끝난 VPS 에서 실행한다.
#
# 등록 항목:
#   1) 캠프 인박스 폴링 cron      — claude 인박스(빙허각 호명) 확인·위임
#   2) 캠프 일일 다이제스트 cron  — 세 저장소 PR·이슈 활동 요약
#   3) PR 자동 리뷰 webhook        — 세 저장소 pull_request 이벤트 리뷰
#
# 주의: 이 스크립트는 멱등하지 않다. 재실행하면 cron 잡이 중복 생성된다.
#       다시 돌리기 전에 `hermes cron list` / `hermes webhook list` 로 확인하고
#       필요하면 `hermes cron delete <id>` / `hermes webhook remove <name>` 하라.
# ============================================================================
set -euo pipefail

# ── 설정 (환경변수로 덮어쓸 수 있음) ───────────────────────────────────────
AGORA_REPO="${AGORA_REPO:-playinthesky/kspeaks-agora}"
HERMES_REPO="${HERMES_REPO:-playinthesky/hermes-agent}"
FKF_REPO="${FKF_REPO:-playinthesky/fkf}"
# 인박스 폴링 시 AGENTS.md/CLAUDE.md 컨텍스트를 주입할 로컬 클론 경로
AGORA_DIR="${AGORA_DIR:-$HOME/kspeaks-agora}"
# 자동화 결과 전달 대상. 팀 채널 #표준컨설팅업무 (fkf2026 워크스페이스)로 기본 전송.
#   채널을 바꾸려면: export DELIVER="slack:<채널ID>"  /  다른 플랫폼: telegram | discord | local
DELIVER="${DELIVER:-slack:C0B6MBYJJKX}"   # #표준컨설팅업무
# 서명 — 캠프 호칭. 호칭이 바뀌면 이 한 곳만 바꾸면 된다.
SIG="${HERMES_SIGNATURE:-— 파발}"
# 폴링 주기 / 다이제스트 시각
INBOX_EVERY="${INBOX_EVERY:-every 15m}"
DIGEST_CRON="${DIGEST_CRON:-0 9 * * *}"   # 매일 09:00

echo "⚕ 캠프 자동화 등록 시작"
echo "  인박스 저장소 : $AGORA_REPO  (컨텍스트 경로: $AGORA_DIR)"
echo "  전달 대상     : $DELIVER"
echo "  서명          : $SIG"
echo ""

# ── 1) 캠프 인박스 폴링 (빙허각 인박스 + 위임) ─────────────────────────────
hermes cron create "$INBOX_EVERY" \
  "당신은 파발, 빙허각의 상시 전령이다. 다음을 한국어로 수행하라:
1) \`gh issue list --repo $AGORA_REPO --label claude --state open\` 로 claude 인박스를 조회한다.
2) 제목 또는 본문에 '빙허각'이 호명된 open Issue만 대상으로 한다. (다른 Claude 호명 건은 건너뛴다.)
3) 마지막 댓글이 내 서명('$SIG' 또는 '— 빙허각')이 아니면 = 미처리. 내용을 읽고 처리한다.
4) 실행이 필요한 일은 직접 코드를 짜지 말고 위임한다: 새 Issue 생성 →
   별동수(Codex)면 라벨 codex, 구편수(Antigravity)면 라벨 antigravity → 제목 '[수신자] ...' →
   본문에 명세를 박고 서명.
5) 처리/위임 결과를 원본 Issue 에 댓글로 보고하고 끝에 '$SIG' 서명을 붙인다.
6) 처리할 새 항목이 없으면 정확히 [SILENT] 한 단어만 출력한다 (알림 보내지 않음)." \
  --name "캠프 인박스 — 빙허각" \
  --workdir "$AGORA_DIR" \
  --skill github-issues \
  --deliver "$DELIVER"
echo "✓ 인박스 폴링 cron 등록"

# ── 2) 캠프 일일 다이제스트 ────────────────────────────────────────────────
hermes cron create "$DIGEST_CRON" \
  "세 저장소($AGORA_REPO, $HERMES_REPO, $FKF_REPO)의 최근 24시간 활동을 \`gh\` 로 모아
한국어 일일 다이제스트를 만들어라. 우선순위로 표시할 것:
(a) 내(claude) 인박스에서 빙허각이 호명된 미처리 Issue,
(b) 리뷰·머지 대기 중인 열린 PR(특히 CI 실패),
(c) 어제 머지된 PR 요약.
500자 이내로 간결하게, 각 항목에 링크. 끝에 '$SIG' 서명." \
  --name "캠프 일일 다이제스트" \
  --deliver "$DELIVER"
echo "✓ 일일 다이제스트 cron 등록"

# ── 2.5) 주간보고 봇 (MVP — 매주 금요일 17시, 한 주 마감) ───────────────────
# "분리된 별채"의 실체: 아고라 앱을 건드리지 않고 파발 cron 으로 도는 독립 자동화.
# 데이터 소스는 GitHub(추가 키 0). 시트·슬랙 지표는 후속 버전에서 확장.
WEEKLY_CRON="${WEEKLY_CRON:-0 17 * * 5}"   # 매주 금요일 17:00
hermes cron create "$WEEKLY_CRON" \
  "이번 주(지난 7일) 캠프 주간보고를 한국어로 작성하라. 세 저장소
($AGORA_REPO, $HERMES_REPO, $FKF_REPO)를 \`gh\` 로 집계한다:
1) 이번 주 머지된 PR (저장소별 건수 + 핵심 항목),
2) 아직 열린 PR·리뷰 대기 (특히 CI 실패),
3) claude/codex/antigravity 인박스의 미처리 Issue 수,
4) 한 줄 총평(이번 주 진척 / 다음 주 막힌 곳).
슬랙용으로 짧은 불릿 + 핵심 숫자 표. 각 항목 링크. 끝에 '$SIG' 서명." \
  --name "캠프 주간보고 봇" \
  --deliver "$DELIVER"
echo "✓ 주간보고 봇 cron 등록 (금 17:00)"

# ── 2.7) 독촉·에스컬레이션 (일 안 하면 재촉, 정 안 들으면 대표님 호출) ───────
# 대표님 지시: "일 안 하면 재촉도 해. 정 말을 안 들으면 날 불러."
# 별동수(codex)·구편수(antigravity) 인박스에 위임된 일이 방치되면 파발이 독촉하고,
# 그래도 무반응이면 대표님께 슬랙으로 에스컬레이션한다.
NUDGE_EVERY="${NUDGE_EVERY:-every 6h}"
NUDGE_STALE_HOURS="${NUDGE_STALE_HOURS:-8}"      # 담당 무응답 N시간 → 독촉
ESCALATE_HOURS="${ESCALATE_HOURS:-24}"           # 무응답 M시간/독촉 2회+ → 대표님 호출
hermes cron create "$NUDGE_EVERY" \
  "$AGORA_REPO 의 codex·antigravity 라벨 open Issue 를 \`gh\` 로 점검하라. 각 이슈에서
담당(별동수=codex, 구편수=antigravity)의 응답 여부와 마지막 활동 시각을 본다.
- 라벨 부여 후 담당 응답이 없고 ${NUDGE_STALE_HOURS}시간 이상 지난 이슈: 정중한 **독촉 댓글**을 단다
  (예: '진행 상황 공유 부탁드립니다. 막히면 이 이슈에 댓글로 남겨주세요'). 끝에 '$SIG' 서명.
  단, 마지막 댓글이 이미 나(파발)의 독촉이면 **중복 금지** — 건너뛴다.
- 라벨 부여 후 ${ESCALATE_HOURS}시간 넘게 무응답이거나 독촉 2회 이상에도 반응이 없는 이슈:
  대표님께 **에스컬레이션** — 이슈 링크 + '며칠/몇 시간째 무응답' 요약을 보고하고
  '직접 한 번 찔러주셔야 할 것 같습니다'라고 알린다.
- 조치할 게 없으면 정확히 [SILENT] 만 출력(알림 없음)." \
  --name "캠프 독촉·에스컬레이션" \
  --workdir "$AGORA_DIR" \
  --skill github-issues \
  --deliver "$DELIVER"
echo "✓ 독촉·에스컬레이션 cron 등록 (${NUDGE_EVERY})"

# ── 3) PR 자동 리뷰 webhook (세 저장소 공용 라우트) ────────────────────────
# 한 라우트로 세 저장소를 받는다. 각 저장소 Settings→Webhooks 에서
# Payload URL = https://<VPS도메인>/webhooks/pr-review 로 추가하고,
# 아래 출력되는 HMAC secret 을 그대로 넣는다. Content type: application/json,
# 이벤트: "Pull requests" 만 선택.
hermes webhook subscribe pr-review \
  --events "pull_request" \
  --description "캠프 세 저장소 PR 자동 리뷰" \
  --prompt "저장소 {repository.full_name} 의 PR #{pull_request.number} '{pull_request.title}'
(작성자 {pull_request.user.login}). 변경 요약, 잠재 리스크, 보호 자산 침범 여부,
머지 가능성(Doc-only 자동 머지 조건 충족 여부 포함)을 한국어로 간단히 리뷰하라. 끝에 '$SIG' 서명." \
  --skills "github-code-review" \
  --deliver "$DELIVER"
echo "✓ PR 리뷰 webhook(pr-review) 등록"

echo ""
echo "완료. 점검:"
echo "  hermes cron list"
echo "  hermes webhook list      # pr-review 의 URL·secret 확인"
echo "  hermes gateway status"
echo ""
echo "다음: 각 저장소 GitHub Settings→Webhooks 에 pr-review URL/secret 을 등록하라."
