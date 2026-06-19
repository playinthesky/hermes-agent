#!/usr/bin/env python3
"""
컨설팅 도서관 인덱스 생성기.
skills/ 와 optional-skills/ 의 모든 SKILL.md frontmatter를 파싱하여
컨설턴트 관점의 '아젠다 도메인'으로 재분류한 인덱스를 생성한다.

사용법:  python3 consulting-library/build_index.py
산출물:  consulting-library/index/skills-index.md
         consulting-library/index/skills.json
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 기술 카테고리(top) -> 컨설턴트 아젠다 도메인 매핑
DOMAINS = {
    "리서치 & 인텔리전스": ["research", "data-science"],
    "콘텐츠 & 크리에이티브 제작": ["creative", "media", "social-media"],
    "생산성 & 업무 자동화": ["productivity", "email", "note-taking", "communication", "apple", "yuanbao"],
    "소프트웨어 엔지니어링 & DevOps": ["software-development", "devops", "github", "migration", "web-development", "dogfood"],
    "AI/ML 엔지니어링 & 에이전트": ["mlops", "autonomous-ai-agents", "mcp"],
    "데이터·금융·Web3": ["finance", "blockchain"],
    "보안 & 거버넌스": ["security"],
    "스마트 라이프 (홈·헬스·게임)": ["smart-home", "health", "gaming"],
}
TOP2DOMAIN = {top: dom for dom, tops in DOMAINS.items() for top in tops}

def parse_fm(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    fm = {"name": os.path.basename(os.path.dirname(path)), "description": "", "tags": []}
    if not m:
        return fm
    b = m.group(1)
    def grab(pat):
        g = re.search(pat, b, re.M)
        return g.group(1).strip().strip('"').strip("'") if g else ""
    fm["name"] = grab(r"^name:\s*(.+)$") or fm["name"]
    fm["description"] = grab(r"^description:\s*(.+?)$")
    tags = re.search(r"tags:\s*\[(.*?)\]", b, re.S)
    fm["tags"] = [t.strip().strip('"').strip("'") for t in tags.group(1).split(",")] if tags else []
    return fm

rows = []
for base, active in [("skills", True), ("optional-skills", False)]:
    for path in sorted(glob.glob(os.path.join(ROOT, base, "**/SKILL.md"), recursive=True)):
        rel = os.path.relpath(path, os.path.join(ROOT, base))
        top = rel.split("/")[0] if "/" in rel else "misc"
        fm = parse_fm(path)
        rows.append({
            "name": fm["name"], "description": fm["description"], "tags": fm["tags"],
            "top": top, "domain": TOP2DOMAIN.get(top, "기타"),
            "path": os.path.relpath(path, ROOT), "active": active,
        })

os.makedirs(os.path.join(ROOT, "consulting-library/index"), exist_ok=True)
json.dump(rows, open(os.path.join(ROOT, "consulting-library/index/skills.json"), "w"),
          ensure_ascii=False, indent=2)

# 도메인별 마크다운 인덱스
by_dom = {}
for r in rows:
    by_dom.setdefault(r["domain"], []).append(r)

lines = [
    "# 스킬 인덱스 (컨설턴트 관점)",
    "",
    "> 이 파일은 `consulting-library/build_index.py`가 `skills/`·`optional-skills/`의",
    "> 모든 `SKILL.md` frontmatter를 읽어 **자동 생성**합니다. 직접 수정하지 마세요.",
    "> 스킬을 추가/변경한 뒤 스크립트를 다시 실행하면 갱신됩니다.",
    "",
    f"- 총 스킬: **{len(rows)}개** (기본 활성 {sum(1 for r in rows if r['active'])} / 선택설치 {sum(1 for r in rows if not r['active'])})",
    f"- 아젠다 도메인: **{len(by_dom)}개**",
    "",
    "범례:  ✅ 기본 활성  ·  ⬇️ 선택 설치(`hermes skills install ...`)",
    "",
]
for dom in list(DOMAINS) + [d for d in by_dom if d not in DOMAINS]:
    items = by_dom.get(dom)
    if not items:
        continue
    lines.append(f"## {dom}  ({len(items)})")
    lines.append("")
    lines.append("| 스킬 | 설명 | 키워드 | 경로 |")
    lines.append("|------|------|--------|------|")
    for r in sorted(items, key=lambda x: x["name"].lower()):
        badge = "✅" if r["active"] else "⬇️"
        tags = ", ".join(r["tags"][:6])
        desc = r["description"].replace("|", "\\|")
        lines.append(f"| {badge} **{r['name']}** | {desc} | {tags} | [`{r['path']}`]({os.path.relpath(r['path'], 'consulting-library/index')}) |")
    lines.append("")

open(os.path.join(ROOT, "consulting-library/index/skills-index.md"), "w").write("\n".join(lines))
print(f"생성 완료: {len(rows)}개 스킬 → {len(by_dom)}개 도메인")
for d in DOMAINS:
    print(f"  {d}: {len(by_dom.get(d, []))}")
extra = {r['top'] for r in rows if r['domain']=='기타'}
if extra: print("  미매핑 top:", extra)
