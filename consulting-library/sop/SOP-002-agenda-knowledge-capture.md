# SOP-002 · 아젠다 지식 적립

| 문서번호 | SOP-002 | 버전 | v1.0 |
|----------|---------|------|------|
| 상태 | 발효 | 발효일 | 2026-06-21 |
| 소유자 | 도서관 관리자(LIB) | 개정주기 | 6개월 |

## 1. 목적

완료했거나 표준화할 가치가 있는 아젠다를 **검색 가능한 자산**으로 적립하여,
다음 유사 의뢰에서 [SOP-001](./SOP-001-consulting-intake-to-delivery.md) 3단계(유사 아젠다 검색)가
실효를 갖도록 한다. 적립이 누적될수록 도서관의 가치가 커진다.

## 2. 적용 범위

SOP-001 인도(7단계)를 마친 의뢰, 또는 신규로 표준 템플릿화할 아젠다.

> **기록 매체 주의:** 이 저장소는 현재 GitHub **Issues가 비활성화**되어 있다. 따라서 본 SOP의
> 기본 기록은 **파일 기반 레지스트리** [`agendas/`](../agendas/)로 운영한다(이슈와 동일한 라벨
> 메타데이터를 frontmatter로 보존). Issues가 활성화되면 동일 항목을 `agenda.yml` 이슈 폼으로
> 승격하고, 5단계 라벨 규칙을 그대로 적용한다.

## 3. 용어 정의

| 용어 | 정의 |
|------|------|
| 적립 | 아젠다를 GitHub `agenda` 이슈로 등록하는 행위. |
| 재사용 포인트 | 다음 유사 의뢰에서 그대로 가져다 쓸 구성·설정·주의점. |

## 4. 역할 및 책임

| 약어 | 역할 | 책임 |
|------|------|------|
| CON | 컨설턴트 | 본문 필드·재사용 포인트 작성 |
| LIB | 도서관 관리자 | 라벨 정합성 점검, 중복 병합, 템플릿 승격 |

## 5. 절차

> 매체별 1단계만 다르고 2~5단계는 동일하다. **이슈 활성 시**: 1단계는 `agenda.yml` 이슈 폼 작성.
> **이슈 비활성(현재)**: 1단계는 [`agendas/`](../agendas/) 레지스트리에 항목 추가
> (`build_agendas.py`의 `DATA`에 추가 후 재생성, 또는 기존 파일 형식대로 신규 `AG-NNN-*.md` 작성).

| # | 단계 | 입력 | 활동 | 산출물 | 책임 |
|---|------|------|------|--------|:----:|
| 1 | 항목 생성 | 확정 기획문서 | 이슈 폼 작성 **또는** `agendas/` 레지스트리 항목 추가 | 아젠다 초안 | CON |
| 2 | 라벨 부여 | 도메인 분류 | `agenda` + `domain/*` + `status/*` (파일은 frontmatter로) | 라벨링된 아젠다 | CON |
| 3 | 재사용 포인트 기록 | 회고 | 재사용 가능한 구성·주의점 요약 | 재사용 메모 | CON |
| 4 | 정합성 점검 | 아젠다 | 라벨 규칙·중복 확인, 필요 시 병합 | 확정 아젠다 | LIB |
| 5 | (선택)템플릿 승격 | 반복 패턴 | `status/template`로 표준화 | 표준 아젠다 | LIB |

### 라벨 규칙

| 라벨 | 값 |
|------|-----|
| `agenda` | 고정(필수) |
| `domain/*` | research · creative · productivity · swe · ai-ml · finance · security · smart-life |
| `status/*` | template · done · wip |

> 도메인 라벨은 [AGENDA-CATALOG](../AGENDA-CATALOG.md)의 8개 도메인과 1:1 대응.
> 상세 필드/검색 예시는 Form 문서 [`templates/agenda-entry.md`](../templates/agenda-entry.md) 참조.

## 6. 기록물 (Records)

| 기록물 | 위치 | 보존 |
|--------|------|------|
| 아젠다 항목 | [`agendas/`](../agendas/) 레지스트리 (현재) / GitHub `agenda` 이슈(활성 시) | 영구 |

## 7. 관련 문서

- 양식: [`.github/ISSUE_TEMPLATE/agenda.yml`](../../.github/ISSUE_TEMPLATE/agenda.yml), [`templates/agenda-entry.md`](../templates/agenda-entry.md)
- 선행: [SOP-001](./SOP-001-consulting-intake-to-delivery.md)

## 8. 개정 이력

| 버전 | 일자 | 변경 요약 | 작성 |
|------|------|-----------|------|
| v1.0 | 2026-06-21 | 최초 발효. | LIB |
