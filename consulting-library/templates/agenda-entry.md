# 아젠다 적립 양식 (Agenda Entry)

> 완료된(또는 표준화하고 싶은) 아젠다를 GitHub에 **검색 가능한 자산**으로 남기는 양식입니다.
> 실제 등록은 `agenda` 이슈 폼([`.github/ISSUE_TEMPLATE/agenda.yml`](../../.github/ISSUE_TEMPLATE/agenda.yml))으로 하며,
> 이 문서는 그 필드와 **라벨 규칙**의 레퍼런스입니다.

## 라벨 규칙

검색 일관성을 위해 모든 아젠다 이슈에 아래 라벨을 답니다.

| 라벨 | 의미 | 값 |
|------|------|-----|
| `agenda` | 아젠다 이슈임을 표시(필수) | 고정 |
| `domain/*` | 주 도메인 | `domain/research`, `domain/creative`, `domain/productivity`, `domain/swe`, `domain/ai-ml`, `domain/finance`, `domain/security`, `domain/smart-life` |
| `status/*` | 진행 상태 | `status/template`(표준 템플릿), `status/done`(완료 사례), `status/wip` |

> 도메인 라벨 값과 [`AGENDA-CATALOG.md`](../AGENDA-CATALOG.md)의 8개 도메인은 1:1로 대응합니다.

## 본문 필드

```markdown
## 의뢰 요약
{{한 줄: 누가/무엇을/왜}}

## 도메인 / 아젠다
주: {{도메인}} · 보조: {{도메인}}
참조 카탈로그 아젠다: {{예: "RAG / 벡터검색"}}

## 사용한 핵심 스킬
- `{{skill}}` — {{용도}}
- `{{skill}}` — {{용도}}

## 산출물
- {{산출물}}

## 재사용 포인트
{{다음 유사 의뢰에서 그대로 가져다 쓸 수 있는 설정/구성/주의점}}

## 기획문서 링크
{{PR 또는 문서 경로}}
```

## 검색 예시 (다음 의뢰 때)

```
label:agenda label:"domain/ai-ml" RAG 사내검색
label:agenda label:"domain/finance" DCF
label:agenda label:"status/template"
```
