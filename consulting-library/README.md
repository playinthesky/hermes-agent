# 컨설팅 도서관 (Consulting Library)

> hermes-agent 프로젝트의 역량을 **휴먼 컨설턴트 관점**으로 재편한 지식 도서관입니다.
> 새로운 의뢰(client request)가 들어왔을 때, 유사한 **아젠다**를 찾아
> **기획문서**를 빠르게 생성하도록 돕습니다.

## 무엇을 푸는가

hermes-agent에는 170개의 스킬이 8개 도메인에 걸쳐 있습니다. 이 역량은 강력하지만,
의뢰를 받은 컨설턴트 입장에서는 "이 요청을 어떤 역량 조합으로, 어떤 산출물로 풀지"를
매번 맨바닥에서 설계해야 했습니다. 이 도서관은 그 간극을 메웁니다.

```
새 의뢰  →  ① 트리아지(도메인·키워드 매핑)
             ②  유사 아젠다 검색 (GitHub Issues / 카탈로그)
             ③  기획문서 템플릿에 역량을 끼워넣어 초안 생성
             ④  완료된 아젠다를 다시 도서관에 적립 (검색 자산화)
```

## 디렉터리 구조

| 경로 | 역할 |
|------|------|
| [`sop/`](./sop/) | **표준운영절차(SOP)** — 의뢰 처리의 정식 표준업무절차(번호·역할·판단점·개정 이력) |
| [`AGENDA-CATALOG.md`](./AGENDA-CATALOG.md) | 프로젝트 분석 결과 — 8개 도메인별 아젠다 카탈로그(대표 의뢰 유형·추천 스킬·산출물) |
| [`intake/triage-guide.md`](./intake/triage-guide.md) | 새 의뢰를 도메인·아젠다·스킬로 매핑하는 트리아지 가이드 |
| [`templates/planning-document.md`](./templates/planning-document.md) | **기획문서 템플릿** — 의뢰 → 기획서 초안 생성용 |
| [`templates/agenda-entry.md`](./templates/agenda-entry.md) | 아젠다를 GitHub에 적립할 때 쓰는 항목 양식 |
| [`playbooks/`](./playbooks/) | 도메인별 플레이북 — 실제 의뢰 예시 + 추천 역량 + 채워진 기획문서 샘플 |
| [`agendas/`](./agendas/) | **아젠다 레지스트리** — 검색 가능한 시드 아젠다(파일 기반, Issues 비활성 대체) |
| [`routines/`](./routines/) | 자동 루틴 실행 지침 (예: 일일 문서 감시 — SOP-004) |
| [`scripts/`](./scripts/) | 보조 스크립트 (flow 문서 변경 스캐너 등) |
| [`index/skills-index.md`](./index/skills-index.md) | **자동 생성** 스킬 인덱스(도메인 ↔ 스킬 ↔ 키워드) |
| [`index/skills.json`](./index/skills.json) | 위 인덱스의 기계 판독용 데이터 |
| [`build_index.py`](./build_index.py) | 스킬 frontmatter → 인덱스 생성 스크립트 |

## 휴먼 컨설턴트 워크플로우 — SOP 기반

이 워크플로우는 가이드가 아니라 **표준운영절차(SOP)**로 운영됩니다. 정식 절차·역할·판단점은
[`sop/`](./sop/)를 따르며, 아래는 그 요약입니다.

| 단계 | 따르는 SOP | 핵심 |
|------|-----------|------|
| 의뢰 접수~기획문서 인도 | [SOP-001](./sop/SOP-001-consulting-intake-to-delivery.md) | 접수→트리아지→유사 아젠다 검색→역량 매핑→기획문서→검수→인도 |
| 아젠다 적립 | [SOP-002](./sop/SOP-002-agenda-knowledge-capture.md) | 완료 아젠다를 `agenda` 이슈로 자산화 |
| 스킬 인덱스 유지 | [SOP-003](./sop/SOP-003-skills-index-maintenance.md) | 스킬 변경 시 인덱스 재생성 |

SOP가 참조하는 작업지시(WI)·양식(Form)·기록(Record)의 구분은
[`sop/README.md`](./sop/README.md#문서-체계-sop--wi--form--record)를 참고하세요.

## 인덱스 갱신

스킬을 추가/수정한 뒤에는 인덱스를 다시 생성하세요:

```bash
python3 consulting-library/build_index.py
```

`index/skills-index.md`와 `index/skills.json`이 `SKILL.md` frontmatter 기준으로 갱신됩니다.
