# SOP-003 · 스킬 인덱스 유지보수

| 문서번호 | SOP-003 | 버전 | v1.0 |
|----------|---------|------|------|
| 상태 | 발효 | 발효일 | 2026-06-21 |
| 소유자 | 도서관 관리자(LIB) | 개정주기 | 변경 시 |

## 1. 목적

`skills/`·`optional-skills/`의 스킬이 추가·변경될 때 컨설턴트 인덱스를 **정확한 상태로 유지**하여,
[SOP-001](./SOP-001-consulting-intake-to-delivery.md) 4단계(역량 매핑)가 항상 최신 역량을 반영하도록 한다.

## 2. 적용 범위

스킬 디렉터리의 추가/삭제/`SOP-001`...정정, 또는 도메인 매핑 규칙 변경 시.

## 3. 용어 정의

| 용어 | 정의 |
|------|------|
| 인덱스 | `index/skills-index.md`(사람용) + `index/skills.json`(기계용). |
| 생성기 | `consulting-library/build_index.py`. SKILL.md frontmatter를 읽어 인덱스를 생성. |
| 도메인 매핑 | 생성기 내 `DOMAINS` 딕셔너리(기술 카테고리→아젠다 도메인). |

## 4. 역할 및 책임

| 약어 | 역할 | 책임 |
|------|------|------|
| LIB | 도서관 관리자 | 생성기 실행·검증·커밋, 매핑 규칙 관리 |

## 5. 절차

| # | 단계 | 활동 | 검증 |
|---|------|------|------|
| 1 | 생성 | `python3 consulting-library/build_index.py` 실행 | 콘솔의 도메인별 카운트 확인 |
| 2 | 미매핑 점검 | 출력에 "미매핑 top"이 있으면 `DOMAINS`에 카테고리 추가 후 재실행 | 미매핑 0건 |
| 3 | 산출물 확인 | `index/skills-index.md`·`skills.json` 갱신 확인 | 표 행 수 = 스킬 수 |
| 4 | 커밋 | 변경을 커밋(자동 생성물 주의 문구 유지) | diff 검토 |

### 명령

```bash
python3 consulting-library/build_index.py
```

### 판단점

- 새 기술 카테고리가 8개 도메인 어디에도 맞지 않으면 → **도서관 관리자 판단**으로 기존 도메인에 편입하거나
  신규 도메인 신설(이 경우 [AGENDA-CATALOG](../AGENDA-CATALOG.md)에도 도메인 추가).

## 6. 기록물 (Records)

| 기록물 | 위치 |
|--------|------|
| 생성된 인덱스 | `index/skills-index.md`, `index/skills.json` |

## 7. 관련 문서

- 생성기: [`build_index.py`](../build_index.py)
- 소비처: [SOP-001](./SOP-001-consulting-intake-to-delivery.md) 4단계

## 8. 개정 이력

| 버전 | 일자 | 변경 요약 | 작성 |
|------|------|-----------|------|
| v1.0 | 2026-06-21 | 최초 발효. | LIB |
