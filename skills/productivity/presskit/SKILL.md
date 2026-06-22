---
name: presskit
description: "Build a project press kit (프레스킷): clone the standard template, auto-collect media sources A–F, fill the 0–4 sections, and hand a GAP checklist to the human consultant. Data spec kspeaks.presskit.v1."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Consulting, PressKit, 프레스킷, Branding, Research]
    related_skills: [google-workspace]
---

# 프레스킷 (Press Kit)

**프레스킷** = 한 프로젝트의 시각·언어·자료 정체성을 한곳에 모은 **기준 원본**.
한 번 v1.0으로 확정되면, 그 프로젝트의 모든 인쇄물·발표자료·보고서·카드뉴스·웹
출력물은 반드시 이 프레스킷을 따른다. 이 스킬은 **생성 → 수집 → 채움 → GAP 인계**
까지를 담당한다. v1.0 확정·디자인 결정은 휴먼 컨설턴트의 몫이다.

## 언제 시작하나 (트리거)

| 사업 유형 | 시작 시점 |
|---|---|
| **입찰 (RFP)** | 입찰 단계부터 — RFP 접수 시 즉시 빈 프레스킷 생성·수집 |
| **숙의 계약** | 계약 체결 이후 — 확정 후 v1.0으로 모든 산출물 적용 |

## 절차

### 1. 입력 정규화
- 클라이언트(사업명) → `slug` 생성: **영문 + 하이픈**(예: `seoul-edu-2026`).
- **한글 파일명 금지** (모바일 표시 실패). 모든 산출 파일명은 영문 + 버전 suffix
  (예: `presskit_v1.0.md`).

### 2. 템플릿 복제
- `_TEMPLATE/presskit.md` → `presskits/{slug}/presskit.md` 로 복제.
- 폴더가 이미 있으면 새로 만들지 말고 **비어 있는 칸만** 다시 채운다(idempotent).

### 3. 기본 채움 (섹션 0~2)
- **0. 정체성**: 사업명·주최·수행기관·기간·참여규모·보관위치.
- **1. 비주얼**: 대표색(HEX)·로고·폰트·헤더 규격. 공식 색이 있으면 그대로, 없으면 지정.
- **2. 문서 규격**: 표지 필수항목·금액 기재 규칙·파일명·버전 규칙.

### 4. 자료 자동수집 (섹션 3, 매체 A~F)
| 매체 | 어디서 |
|---|---|
| **A. 공식 보도** | 주최의 보도자료 채널에서 사업명·주제로 검색 |
| **B. 외부 언론** | 주제 관련 주요 언론. 정량 결과 있는 것 우선 |
| **C. 참여·의제** | 주최 누리집 시민참여/의견수렴 게시판 |
| **D. 영상·SNS** | 주최 공식 유튜브·인스타·블로그 |
| **E. 보고서·연구** | 정책연구소·웹진·학술DB(KCI/DBpia) |
| **F. 브랜드 자산** | 주최 CI/휘장·서체·문서서식 다운로드 위치 |

**수집 규칙 (반드시 지킬 것)**
- 자료가 **있으면 채우고, 없으면 GAP**. **URL을 추측해서 만들지 않는다.**
- 공식 SNS 계정은 **역링크 확인 후에만** `verified` 표시 (동명·사칭 주의).
- 내부자료성은 `[내부자료]`로 표시.

### 5. GAP 인계
- 못 채운 칸을 **GAP 체크리스트**로 모은다: 각 항목 + "어디서 확인하면 되는지" 힌트.
- 입찰 건은 RFP 진입 채널 스레드, 숙의 건은 표준컨설팅업무 채널로 전달.
- 휴먼이 채우면 컨설턴트가 `presskit_v1.0.md`로 확정하고 선언을 적용한다.

## 용어 표준 (모든 프레스킷 공통)
- 발주측 = **주최** (※ "발주처" 금지)
- 수행측 = **수행기관**, 공동수행 = **컨소시엄**

## 데이터 규격 `kspeaks.presskit.v1`

```json
{
  "spec": "kspeaks.presskit.v1",
  "slug": "seoul-edu-2026",
  "identity": {"project_name": "", "host": "", "operator": "",
               "period": "", "scale": "", "storage_url": ""},
  "visual": {"colors": {"primary": "", "secondary": "", "accent": ""},
             "logo": "", "fonts": {"title": "", "body": ""}, "header_rule": ""},
  "doc_standard": {"cover_required": [], "amount_rule": "",
                   "filename_rule": "en+version"},
  "sources": {"A_official": [], "B_press": [], "C_participation": [],
              "D_video_sns": [], "E_research": [], "F_brand_assets": []},
  "meta": {"version": "v1.0", "updated": "", "author": "", "storage_url": ""},
  "gaps": [{"field": "", "note": "", "internal": false}]
}
```

## 버전 규칙
- 항목 추가/삭제 = 마이너↑ · 오탈자/링크 수정 = 패치↑ · 성격 전환 = 메이저↑.
- 변경 시 **문서를 먼저 갱신**하고 버전을 올린다.

## 보관 위치
- 권장 정식 보관소: `kspeaks-agora` 저장소의 `presskits/` 폴더 (항상 같은 자리).
- 단일 보관 주소를 프레스킷 0번 "보관 위치"와 4번 메타에 기재한다.
