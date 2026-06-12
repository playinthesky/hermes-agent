# Hermes Agent — 코리아스픽스 AI 캠프 상시 허브 설치 가이드

> 대상: 대표님(playinthesky@kspeaks.kr) / 작성: 빙허각
> 목표: **VPS 에 Hermes 를 24시간 띄워**, 텔레그램으로 어디서든 대화하고,
> 6인 캠프(별동수·구편수·빙허각…)에게 GitHub Issue 인박스로 일을 나르며,
> 세 저장소(`kspeaks-agora`·`hermes-agent`·`fkf`)의 PR 을 자동 리뷰하게 만든다.

Hermes 는 Nous Research 의 오픈소스 자가개선형 에이전트다. 모델은 무엇이든 붙일 수 있고
(여기선 **Nous Portal 한 구독**으로 통일), cron·webhook·스킬·다중 플랫폼 전달이 내장돼 있다.

이 폴더(`kspeaks-camp/`)에 캠프 전용 파일이 들어 있다:

| 파일 | 용도 |
|---|---|
| `SOUL.md` | 헤르메스의 페르소나(캠프 정체성·규칙). `~/.hermes/SOUL.md` 로 복사 |
| `setup-camp.sh` | 캠프 cron(인박스·다이제스트) + PR 리뷰 webhook 일괄 등록 |
| `README.ko.md` | 이 문서 |

---

## 0. 사전 준비

- **VPS** 한 대 (Ubuntu/Debian 권장, $5짜리면 충분). SSH 접속 가능.
- **Nous Portal 구독** — https://portal.nousresearch.com/manage-subscription
  (모델 + 웹검색 + 이미지 + TTS + 클라우드 브라우저가 한 구독에 포함)
- **텔레그램 봇 토큰** — 텔레그램 `@BotFather` 에서 `/newbot` 으로 발급 (게이트웨이 설정 때 입력)
- **GitHub `gh` CLI 인증** — 인박스 폴링·PR 리뷰가 `gh` 를 쓴다. VPS 에서 `gh auth login`.
  세 저장소 접근 권한이 있는 계정/토큰을 사용.

> 모든 비밀값(포털 토큰·봇 토큰·GitHub 토큰)은 Hermes 설정/환경변수로만 다룬다. **코드·문서·커밋에 박지 않는다.**

---

## 1. 설치 (VPS)

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc        # PATH 반영 (zsh 면 ~/.zshrc)
hermes --version
```

> 개발용으로 이 저장소를 직접 클론해 쓰려면: `./setup-hermes.sh` (루트의 스크립트).
> 이 컨테이너에서 코어 설치·구동은 검증 완료(Python 3.11 + uv).

---

## 2. Nous Portal 연결 (모델·도구 한 방에)

```bash
hermes setup --portal     # OAuth 로그인 → Nous 를 기본 제공자로 + Tool Gateway 켜기
hermes portal info        # 무엇이 연결됐는지 확인
hermes model              # (선택) 기본 모델 고르기
```

---

## 3. 페르소나 심기 (캠프 정체성)

`SOUL.md` 를 Hermes 의 주 정체성 슬롯으로 복사한다. 이걸 넣으면 Hermes 가
6인 캠프 명단·인박스 라벨·서명 의무·보호 자산 규칙을 항상 인식한다.

```bash
mkdir -p ~/.hermes
cp kspeaks-camp/SOUL.md ~/.hermes/SOUL.md
```

추가로, 저장소별 작업 시엔 그 폴더의 `AGENTS.md`/`CLAUDE.md` 가 자동 주입된다.
그래서 인박스 cron 은 `--workdir ~/kspeaks-agora` 로 **진짜 AGENTS.md(단일 진실)** 를 읽게 한다.
VPS 에 캠프 저장소를 미리 클론해 둔다:

```bash
gh repo clone playinthesky/kspeaks-agora ~/kspeaks-agora
```

---

## 4. 텔레그램 게이트웨이 (어디서든 대화)

```bash
hermes gateway setup      # 텔레그램 봇 토큰 입력, 허용 사용자(대표님) 지정
hermes gateway install    # 상시 서비스로 설치 (메시징 + cron + webhook 한 프로세스)
hermes gateway status
```

설치 후 텔레그램에서 봇에게 말을 걸면 Hermes 가 응답한다. `/new`(새 대화), `/model`,
`/usage` 같은 슬래시 명령도 텔레그램에서 그대로 쓸 수 있다.

> **"우선 대화부터"** 는 여기까지로 끝. 봇에게 한국어로 말 걸어 감을 잡은 뒤 5단계로.

---

## 5. 캠프 자동화 등록 (오케스트레이션 + 정기 리포트 + PR 리뷰)

스크립트 한 번이면 cron 2종 + webhook 1종이 등록된다.

```bash
# 필요하면 기본값을 환경변수로 덮어쓴다 (아래는 전부 선택)
export AGORA_DIR="$HOME/kspeaks-agora"     # AGENTS.md 주입 경로
export DELIVER="telegram"                  # 결과 전달 대상
# export HERMES_SIGNATURE="— 헤르메스"      # 호칭 정식 부여 시 여기만 바꾸면 됨

bash kspeaks-camp/setup-camp.sh
hermes cron list
hermes webhook list      # pr-review 의 Payload URL·HMAC secret 확인
```

등록되는 자동화:

1. **캠프 인박스 — 빙허각** (`every 15m`)
   `claude` 라벨 open Issue 중 **빙허각이 호명된 것**만 처리. 실행할 일은 직접 짜지 않고
   별동수(`codex`)·구편수(`antigravity`) 라벨 Issue 로 **위임**하고, 원본에 서명 댓글로 보고.
   처리할 게 없으면 `[SILENT]` → 알림 없음(스팸 방지).
   → 별동수·구편수의 기존 런타임(`byeoldongsu_runtime`/`gupyeonsu_runtime`)이 자기 라벨을
     이미 폴링하므로 역할이 겹치지 않는다. 헤르메스는 빙허각 인박스 + 위임만 맡는다.

2. **캠프 일일 다이제스트** (`매일 09:00`)
   세 저장소의 24시간 활동(미처리 인박스·대기 PR·CI 실패·머지 요약)을 텔레그램으로.

3. **PR 자동 리뷰 webhook** (`pr-review`)
   세 저장소의 `pull_request` 이벤트를 받아 변경 요약·리스크·보호 자산 침범 여부·
   머지 가능성(Doc-only 자동 머지 조건 포함)을 한국어로 리뷰.

---

## 6. GitHub Webhook 연결 (PR 리뷰 활성화)

5단계의 `pr-review` 가 실제로 PR 이벤트를 받으려면, 각 저장소에 webhook 을 건다.
세 저장소 모두 같은 URL 로 보내면 한 라우트가 다 받는다.

각 저장소 **Settings → Webhooks → Add webhook**:

- **Payload URL**: `https://<VPS-도메인-또는-IP>/webhooks/pr-review`
  (정확한 베이스 URL/포트는 `hermes webhook list` 와 게이트웨이 상태에서 확인)
- **Content type**: `application/json`
- **Secret**: `hermes webhook list` 가 보여주는 `pr-review` 의 HMAC secret
- **Which events**: *Let me select* → **Pull requests** 만 체크
- 저장 후 `hermes webhook test pr-review` 로 동작 점검

> 공인 URL 이 없으면(방화벽/NAT) 도메인+리버스 프록시(Caddy/Nginx) 또는 터널을 둔다.
> 자세한 게이트웨이·webhook 설정은 공식 문서 참고:
> https://hermes-agent.nousresearch.com/docs/user-guide/messaging

---

## 7. 운영·점검 명령

```bash
hermes status            # 전체 구성 상태
hermes doctor            # 문제 진단
hermes cron list         # 등록된 스케줄
hermes cron run <id>     # 특정 잡 즉시 실행 테스트
hermes cron remove <id>  # 잡 삭제 (rm/delete 별칭)
hermes webhook list      # 구독·URL·secret
hermes gateway status    # 게이트웨이/서비스 상태
hermes send <대상> "메시지"   # 스크립트/CI 에서 직접 전달
```

---

## 보안·캠프 규약 (반드시 준수)

- **비밀값은 환경변수/Hermes 설정에만.** 코드·댓글·문서·커밋에 박지 않는다.
- **`main` 직접 commit 금지** — 모든 변경은 PR(기본 draft). force push 금지.
- **보호 자산** 변경 금지(`app.py`·`tools/`·`templates/`·`static/`·`db/`·`infra/` 등).
- **Doc-only 자동 머지**는 AGENTS.md 의 4개 조건을 모두 충족할 때만.
- 모든 외부 메시지에 **서명**(`— 빙허각 (Hermes)`). 호칭이 정식 부여되면 한 곳(`HERMES_SIGNATURE`)만 변경.

## 호칭 결정 노트 (대표님 판단 필요)

헤르메스는 현재 **빙허각의 상시 분신**으로 동작하도록 설정돼 있다(서명 `— 빙허각 (Hermes)`).
정식 7번째 멤버로 올릴지, 별도 호(號)를 줄지는 6인 캠프 표준을 바꾸는 일이라 **대표님 결정 영역**이다.
결정되면 (1) `SOUL.md` 의 정체성 단락, (2) `setup-camp.sh` 의 `HERMES_SIGNATURE`,
(3) 필요 시 `kspeaks-agora/AGENTS.md` 한 줄 추가 — 세 곳만 손보면 된다.
