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
| [`AGENDA-CATALOG.md`](./AGENDA-CATALOG.md) | 프로젝트 분석 결과 — 8개 도메인별 아젠다 카탈로그(대표 의뢰 유형·추천 스킬·산출물) |
| [`intake/triage-guide.md`](./intake/triage-guide.md) | 새 의뢰를 도메인·아젠다·스킬로 매핑하는 트리아지 가이드 |
| [`templates/planning-document.md`](./templates/planning-document.md) | **기획문서 템플릿** — 의뢰 → 기획서 초안 생성용 |
| [`templates/agenda-entry.md`](./templates/agenda-entry.md) | 아젠다를 GitHub에 적립할 때 쓰는 항목 양식 |
| [`playbooks/`](./playbooks/) | 도메인별 플레이북 — 실제 의뢰 예시 + 추천 역량 + 채워진 기획문서 샘플 |
| [`index/skills-index.md`](./index/skills-index.md) | **자동 생성** 스킬 인덱스(도메인 ↔ 스킬 ↔ 키워드) |
| [`index/skills.json`](./index/skills.json) | 위 인덱스의 기계 판독용 데이터 |
| [`build_index.py`](./build_index.py) | 스킬 frontmatter → 인덱스 생성 스크립트 |

## 휴먼 컨설턴트 워크플로우

1. **의뢰 접수.** [`intake/triage-guide.md`](./intake/triage-guide.md)로 의뢰를 1개 이상의
   도메인과 키워드로 분류합니다.
2. **유사 아젠다 검색.** GitHub Issues에서 `agenda` 라벨 + 도메인 라벨로 과거 아젠다를
   검색합니다. (예: `label:agenda label:"domain/research" 시장조사`)
   없으면 [`AGENDA-CATALOG.md`](./AGENDA-CATALOG.md)의 대표 아젠다를 출발점으로 삼습니다.
3. **역량 매핑.** 해당 아젠다가 추천하는 스킬을 [`index/skills-index.md`](./index/skills-index.md)에서
   확인하고, 의뢰에 맞게 가감합니다.
4. **기획문서 초안.** [`templates/planning-document.md`](./templates/planning-document.md)를 복사해
   채웁니다. 플레이북에 채워진 샘플이 있으면 그대로 변형합니다.
5. **아젠다 적립.** 완료한 아젠다를 `agenda` 이슈로 등록합니다
   ([`.github/ISSUE_TEMPLATE/agenda.yml`](../.github/ISSUE_TEMPLATE/agenda.yml)).
   이렇게 쌓인 이슈가 다음 의뢰의 검색 자산이 됩니다.

## 인덱스 갱신

스킬을 추가/수정한 뒤에는 인덱스를 다시 생성하세요:

```bash
python3 consulting-library/build_index.py
```

`index/skills-index.md`와 `index/skills.json`이 `SKILL.md` frontmatter 기준으로 갱신됩니다.
