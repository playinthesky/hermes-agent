# 의뢰 트리아지 가이드 (Intake Triage)

> **작업지시(WI)** · 소속 SOP: [SOP-001](../sop/SOP-001-consulting-intake-to-delivery.md) 1~4단계의 수행 세부 지침.
> 새 의뢰가 들어오면 이 가이드로 **도메인 → 아젠다 → 스킬**까지 5분 안에 좁힙니다.

## 1단계 — 의뢰 한 줄 요약

의뢰를 "누가 / 무엇을 / 왜 / 언제까지" 한 문장으로 적습니다.

> 예) "B2B SaaS 팀이 / 사내 문서 검색 챗봇을 / 고객지원 부담을 줄이려고 / 4주 안에"

## 2단계 — 키워드 → 도메인 매핑

의뢰 문장의 핵심 명사를 아래 표의 키워드와 대조해 1~2개 도메인을 고릅니다.

| 의뢰에 이런 단어가 보이면 | 도메인 |
|---------------------------|--------|
| 조사, 동향, 경쟁사, 논문, 시장, OSINT | 리서치 & 인텔리전스 |
| 디자인, 영상, 인포그래픽, 카피, 브랜드, 음악, UI 시안 | 콘텐츠 & 크리에이티브 |
| 자동화, 메일, 캘린더, 회의록, 문서, PDF, 슬라이드, 운영DB | 생산성 & 업무 자동화 |
| 코드, 레포, 버그, 리뷰, 배포, 컨테이너, 기능 개발 | 소프트웨어 엔지니어링 & DevOps |
| 모델, 파인튜닝, 서빙, RAG, 벡터검색, 평가, 에이전트, MCP, 챗봇 | AI/ML 엔지니어링 & 에이전트 |
| 재무모델, 밸류에이션, DCF, 주식, 온체인, 토큰 | 데이터·금융·Web3 |
| 취약점, 펜테스트, 포렌식, 시크릿, 자격증명 | 보안 & 거버넌스 |
| 스마트홈, 조명, 운동, 영양, 게임 서버 | 스마트 라이프 |

> 여러 도메인에 걸치면 **주 도메인 1 + 보조 도메인 N** 으로 표시합니다.
> (예: 챗봇 의뢰 = 주: AI/ML, 보조: 리서치·생산성)

## 3단계 — 유사 아젠다 검색

GitHub Issues에서 과거 아젠다를 검색합니다.

```
label:agenda label:"domain/<도메인>" <키워드>
```

- 예: `label:agenda label:"domain/ai-ml" RAG 사내검색`
- 검색 라벨 규칙은 [`templates/agenda-entry.md`](../templates/agenda-entry.md)의 라벨 표 참고.
- 검색 결과가 있으면 → 그 아젠다의 기획문서를 **출발 초안**으로 복제.
- 없으면 → [`AGENDA-CATALOG.md`](../AGENDA-CATALOG.md)에서 가장 가까운 대표 아젠다 선택.

## 4단계 — 역량(스킬) 확정

선택한 아젠다의 `핵심 스킬`을 기본으로 두고, [`index/skills-index.md`](../index/skills-index.md)에서
의뢰 특이사항에 맞는 스킬을 가감합니다. 체크 포인트:

- **활성 여부**: ⬇️(선택 설치) 스킬은 `hermes skills install official/<category>/<skill>` 필요.
- **의존성/자격증명**: 외부 API·OAuth가 필요한 스킬은 의뢰서에 사전 준비물로 명시.
- **대체재**: 같은 목적의 스킬이 여럿이면(예: 벡터DB `chroma`/`qdrant`/`pinecone`) 제약(온프레미스·예산·SLA)으로 결정.

## 5단계 — 기획문서 생성

[`templates/planning-document.md`](../templates/planning-document.md)를 복사해 채웁니다.
플레이북([`playbooks/`](../playbooks/))에 유사 사례가 있으면 그 채워진 버전을 변형하세요.

## 6단계 — 적립

완료된 의뢰는 `agenda` 이슈로 등록해 다음 의뢰의 검색 자산으로 남깁니다.
([`.github/ISSUE_TEMPLATE/agenda.yml`](../../.github/ISSUE_TEMPLATE/agenda.yml))
