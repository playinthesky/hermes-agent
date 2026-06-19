---
name: cost-breakdown-proposal
description: "Build a Korean 산출내역서/견적서 (cost-breakdown proposal) in the KoreaSpeaks/fKF AX design, render to PDF, package as a single HTML."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Proposal, Quote, 산출내역서, 견적서, Korean, HTML, PDF, KoreaSpeaks, fKF, Facilitation]
    related_skills: [powerpoint, ocr-and-documents]
---

# 산출내역서 (Cost-Breakdown Proposal)

## When to use

Use when producing a Korean **산출내역서 / 견적서** for a KoreaSpeaks(코리아스픽스)
or fKF(한국퍼실리테이터연합회) facilitation/workshop engagement — typically in
response to an RFP. The output is a designed A4 document in the **AX design system**
(navy→teal→gold left spine, Pretendard + Roboto Mono), delivered as HTML, a print
PDF, and a single self-contained HTML.

## Resources

Everything lives under `proposals/` in the `playinthesky/hermes-agent` repo:

- `proposals/_workflow/WORKFLOW.md` — the authoritative guide (input checklist,
  costing rules, tone/branding rules, render commands, review checklist). **Read it first.**
- `proposals/_workflow/TEMPLATE.html` — blank template; `{{...}}` and `.fill` spans mark fill-ins.
- `proposals/_workflow/render_pdf.js` — HTML → PDF (A4, 2cm margins, centered page numbers).
- `proposals/_workflow/build_standalone.py` — inline CSS + base64 images → one HTML file.
- `proposals/_workflow/../colors_and_type.css`, `bdlee.jpg` — shared AX tokens + portrait.
- `proposals/우송대_AI교수워크샵_산출내역서.html` — a fully worked example.

## Steps

1. **Collect inputs** using the checklist in `WORKFLOW.md §1` — 발주 주체(fKF↔코리아스픽스),
   발주처/사업명, 규모·편성, 인력 구성과 단가, 직접경비, 산출물(포함/옵션), 불포함 항목,
   목표 총액, 퍼실리테이터 약력, 연락처. Ask the user for anything missing.

2. **Apply costing rules** (`WORKFLOW.md §2`):
   - Role-split: 발주처 직접 집행분은 §4 합계 제외 → §4.2 별도 표기.
   - 인건비 = 월급여 대비 투입율(M/M), code `F-xx`.
   - 직접경비 "식(式)", code `C-xx`. 산출물 code `D-xx` (인력비 포함=0 / 별도=금액 / 옵션=0+"협의 시 +금액").
   - 목표 총액은 PM 기획·설계비 또는 기획 운영비로 차액 흡수.
   - VAT = 공급가 × 10%; 표지·§4·§4.1 세 곳 금액 일치; 만원 단위로 정리.

3. **Fill the template**: copy `TEMPLATE.html`, replace `{{...}}`/`.fill`. Follow tone rules
   (명사형, 발주 경로대로 주체 표기, 불필요한 영어 라벨 금지; §2 토의 프레임은 비토의형이면 삭제).
   If placed in `proposals/` root, fix the `../colors_and_type.css` / `../bdlee.jpg` links to `./`.

4. **Render & package**:
   ```bash
   node proposals/_workflow/render_pdf.js <name>.html <name>.pdf
   python3 proposals/_workflow/build_standalone.py <name>.html <name>_standalone.html
   ```

5. **Review** with `WORKFLOW.md §5` checklist: 합계 검산, §4 한 페이지(`.cost-keep`),
   페이지 연속, 주체 일관성, 오탈자, 미치환 `{{...}}` 없음. Deliver the standalone HTML
   (opens correctly on its own) and/or the PDF.
