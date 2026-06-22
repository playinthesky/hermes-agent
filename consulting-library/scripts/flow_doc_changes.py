#!/usr/bin/env python3
"""
flow(이 저장소)의 최근 변경 문서 감지기 — 일일 문서 감시 루틴(SOP-004)의 flow 측 스캐너.

Google Drive 측은 에이전트가 런타임에 MCP(list_recent_files/search_files)로 채운다.
이 스크립트는 git 기반으로 flow의 변경 문서를 마크다운 다이제스트 조각으로 출력한다.

사용법:
  python3 consulting-library/scripts/flow_doc_changes.py [--since "24 hours ago"]
"""
import argparse, subprocess, os

DOC_GLOBS = ["*.md", "*.txt", "*.pdf", "*.docx", "*.pptx", "*.xlsx", "*.csv", "*.rst"]

def run(args):
    return subprocess.check_output(args, text=True, cwd=os.getcwd()).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="24 hours ago")
    args = ap.parse_args()

    # since 이후 변경된 문서 파일(상태 포함) 집계
    fmt = "%h\t%ad\t%s"
    log = run(["git", "-c", "core.quotepath=false", "log", f"--since={args.since}",
               "--name-status", f"--pretty=format:@@@\t{fmt}", "--date=short", "--"] + DOC_GLOBS)

    commits = []
    cur = None
    for line in log.splitlines():
        if line.startswith("@@@\t"):
            _, h, d, s = line.split("\t", 3)
            cur = {"hash": h, "date": d, "subject": s, "files": []}
            commits.append(cur)
        elif line.strip() and cur is not None:
            parts = line.split("\t")
            status, path = parts[0], parts[-1]
            cur["files"].append((status, path))

    changed = {}  # path -> 최신 상태
    for c in commits:
        for st, p in c["files"]:
            changed.setdefault(p, st[0])  # 첫 등장(최신)을 우선

    print(f"### flow (저장소) — 최근 변경 문서  ·  기준: `{args.since}`\n")
    if not changed:
        print("_변경된 문서 없음._\n")
    else:
        print(f"변경 문서 **{len(changed)}건** (커밋 {len(commits)}개)\n")
        print("| 상태 | 문서 |")
        print("|:----:|------|")
        label = {"A": "신규", "M": "수정", "D": "삭제", "R": "이동"}
        for p, st in sorted(changed.items()):
            print(f"| {label.get(st, st)} | `{p}` |")
        print()
        print("<details><summary>커밋 내역</summary>\n")
        for c in commits:
            print(f"- `{c['hash']}` {c['date']} — {c['subject']} ({len(c['files'])} doc)")
        print("\n</details>\n")

if __name__ == "__main__":
    main()
