#!/usr/bin/env python3
"""
아젠다 레지스트리 생성기 (SOP-002 / Issues 비활성 환경의 파일 기반 대체 기록).
DATA 목록으로부터 agendas/AG-NNN-*.md 와 인덱스 README.md를 생성한다.

사용법:  python3 consulting-library/agendas/build_agendas.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# (id, domain, status, title, skills[(name,용도)], 산출물, 재사용포인트, 기획문서링크)
DATA = [
    ("AG-001", "research", "template", "학술/특허 리뷰",
     [("arxiv", "논문 검색/수집"), ("research-paper-writing", "리뷰/요약 구조화"),
      ("llm-wiki", "개념·배경 보강"), ("ocr-and-documents", "PDF 본문 추출(필요 시)")],
     "문헌 리뷰 문서, 핵심 요약 노트, 출처 목록",
     "「수집(arxiv) → 요약/구조화(research-paper-writing) → 출처표기」 3단 구성은 모든 문헌 리뷰 의뢰에 재사용.",
     "SOP-001에 따라 `templates/planning-document.md` 복제하여 작성."),
    ("AG-002", "creative", "template", "인포그래픽/도식화",
     [("baoyu-infographic", "인포그래픽 생성"), ("concept-diagrams", "개념 도식"),
      ("architecture-diagram", "구조 다이어그램"), ("excalidraw", "손그림 스타일 편집")],
     "SVG/PNG 다이어그램, 인포그래픽",
     "개념→도식 변환은 baoyu-infographic을 1차로, 정밀 편집은 excalidraw로 분담.",
     "SOP-001에 따라 `templates/planning-document.md` 복제하여 작성."),
    ("AG-003", "productivity", "template", "문서 파이프라인",
     [("ocr-and-documents", "스캔/PDF 텍스트화"), ("nano-pdf", "PDF 조작"),
      ("powerpoint", "슬라이드 생성"), ("notion", "지식베이스 정리")],
     "정규화된 문서, 슬라이드 덱",
     "OCR→정규화→산출(슬라이드/노션) 파이프라인은 문서처리 의뢰 전반에 재사용.",
     "SOP-001에 따라 `templates/planning-document.md` 복제하여 작성."),
    ("AG-004", "swe", "template", "기능 개발(계획→구현)",
     [("plan", "설계/계획"), ("spike", "실현가능성 검증"),
      ("test-driven-development", "테스트 우선 구현"), ("subagent-driven-development", "병렬 구현 오케스트레이션")],
     "설계서, 구현 PR, 테스트",
     "불확실 영역은 spike 선행 → plan 확정 → TDD 구현 순서가 표준.",
     "SOP-001에 따라 `templates/planning-document.md` 복제하여 작성."),
    ("AG-005", "ai-ml", "template", "모델 파인튜닝",
     [("fine-tuning-with-trl", "SFT/선호 학습"), ("unsloth", "경량·고속 파인튜닝"),
      ("peft-fine-tuning", "LoRA/어댑터"), ("axolotl", "구성 기반 학습 파이프라인")],
     "학습 파이프라인, 체크포인트, 평가",
     "데이터 규모·GPU 예산에 따라 unsloth(소규모)↔axolotl(구성형) 선택. 어댑터는 peft 우선.",
     "SOP-001에 따라 `templates/planning-document.md` 복제하여 작성."),
    ("AG-006", "finance", "template", "재무 모델링",
     [("3-statement-model", "3재무제표 연동"), ("dcf-model", "현금흐름할인 가치평가"),
      ("lbo-model", "LBO 분석"), ("merger-model", "M&A 시너지/희석 분석")],
     "Excel 재무모델, 밸류에이션",
     "3-statement를 코어로 두고 목적에 따라 dcf/lbo/merger를 얹는 구조.",
     "SOP-001에 따라 `templates/planning-document.md` 복제하여 작성."),
    ("AG-007", "security", "template", "웹 펜테스트",
     [("web-pentest", "웹 취약점 점검"), ("godmode", "심층 진단(인가 범위 내)")],
     "취약점 리포트, 재현 절차, 완화 권고",
     "⚠️ 인가된 대상에 한해 수행. 의뢰서에 범위·권한 근거를 반드시 명시.",
     "SOP-001에 따라 `templates/planning-document.md` 복제하여 작성. (인가 근거 첨부 필수)"),
    ("AG-008", "smart-life", "template", "스마트홈 자동화",
     [("openhue", "Philips Hue 조명 제어")],
     "자동화 시나리오, 씬 구성",
     "조명 자동화 시나리오는 openhue 씬/룰로 표준화.",
     "SOP-001에 따라 `templates/planning-document.md` 복제하여 작성."),
    ("AG-009", "ai-ml", "done", "사내 문서 RAG 챗봇",
     [("chroma", "온프레미스 벡터 저장/검색"), ("fastmcp", "검색 도구를 MCP로 노출"),
      ("hermes-agent", "대화 오케스트레이션"), ("evaluating-llms-harness", "정확도 평가")],
     "RAG 파이프라인, 검색 MCP 서버, 챗봇, 평가 리포트",
     "온프레미스 RAG 스택(chroma+fastmcp+hermes-agent)은 사내검색 의뢰에 그대로 재사용.",
     "[playbooks/ai-ml-rag-chatbot.md](../playbooks/ai-ml-rag-chatbot.md)"),
    ("AG-010", "research", "done", "시장·경쟁 스캔",
     [("duckduckgo-search", "웹 검색"), ("searxng-search", "메타 검색/폴백"),
      ("osint-investigation", "경쟁사 인텔"), ("baoyu-infographic", "브리프 시각화")],
     "시장 브리프 덱, 경쟁사 프로파일, 출처 목록",
     "「수집→OSINT→리포트(infographic)」 3단 구성은 모든 시장조사 의뢰에 재사용.",
     "[playbooks/research-market-scan.md](../playbooks/research-market-scan.md)"),
]

DOMAIN_LABEL = {
    "research": "리서치 & 인텔리전스", "creative": "콘텐츠 & 크리에이티브",
    "productivity": "생산성 & 업무 자동화", "swe": "소프트웨어 엔지니어링 & DevOps",
    "ai-ml": "AI/ML 엔지니어링 & 에이전트", "finance": "데이터·금융·Web3",
    "security": "보안 & 거버넌스", "smart-life": "스마트 라이프",
}

def slug(t):
    return t.replace("/", "-").replace(" ", "-").replace("(", "").replace(")", "").replace("→", "to")

for ag_id, domain, status, title, skills, deliver, reuse, plan_link in DATA:
    fn = f"{ag_id}-{slug(title)}.md"
    skill_names = ", ".join(s[0] for s in skills)
    lines = [
        "---",
        f"id: {ag_id}",
        f"domain: {domain}",
        f"status: {status}",
        f'title: "{title}"',
        f"skills: [{skill_names}]",
        "---",
        "",
        f"# {ag_id} · {title}",
        "",
        f"> 라벨: `agenda` · `domain/{domain}` · `status/{status}`  ·  "
        f"적립 절차: [SOP-002](../sop/SOP-002-agenda-knowledge-capture.md)",
        "",
        "## 도메인 / 아젠다",
        f"주: {DOMAIN_LABEL[domain]} · 참조 카탈로그 아젠다: 「{title}」",
        "",
        "## 핵심 스킬",
    ]
    for name, use in skills:
        lines.append(f"- `{name}` — {use}")
    lines += [
        "",
        "## 산출물",
        f"- {deliver}",
        "",
        "## 재사용 포인트",
        reuse,
        "",
        "## 기획문서",
        plan_link,
        "",
    ]
    open(os.path.join(HERE, fn), "w").write("\n".join(lines))

# 인덱스 README
idx = [
    "# 아젠다 레지스트리 (Agenda Registry)",
    "",
    "> 완료/표준 아젠다를 **검색 가능한 자산**으로 적립한 레지스트리입니다.",
    "> 이 저장소는 GitHub Issues가 비활성화되어 있어, [SOP-002](../sop/SOP-002-agenda-knowledge-capture.md)의",
    "> 기록을 **파일 기반**으로 운영합니다. (Issues 활성화 시 동일 항목을 `agenda` 이슈로 승격 가능)",
    "",
    "- 생성기: `build_agendas.py` (`python3 consulting-library/agendas/build_agendas.py`)",
    "- 검색 팁: GitHub 코드검색에서 `domain: ai-ml`, `status: template`, 스킬명 등으로 grep.",
    "",
    "| ID | 도메인 | 아젠다 | 상태 | 핵심 스킬 |",
    "|----|--------|--------|:----:|-----------|",
]
for ag_id, domain, status, title, skills, *_ in DATA:
    fn = f"{ag_id}-{slug(title)}.md"
    idx.append(f"| [{ag_id}](./{fn}) | `{domain}` | {title} | `{status}` | {', '.join(s[0] for s in skills)} |")
idx.append("")
open(os.path.join(HERE, "README.md"), "w").write("\n".join(idx))

print(f"생성: 아젠다 {len(DATA)}건 + 인덱스")
for d in DOMAIN_LABEL:
    n = sum(1 for x in DATA if x[1] == d)
    print(f"  {d}: {n}")
