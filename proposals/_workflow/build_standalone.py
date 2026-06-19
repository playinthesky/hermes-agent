#!/usr/bin/env python3
"""Bundle a proposal HTML into one self-contained file.

    python3 build_standalone.py <input.html> <output.html>

- Inlines the linked stylesheet (`<link rel="stylesheet" href="...css">`)
  into a `<style>` block.
- Embeds local `<img src="...">` files as base64 data URIs.
- Leaves CDN webfont `@import` rules in the CSS untouched, so fonts load when
  online and fall back to system fonts offline.

Paths in the HTML are resolved relative to the input file's directory.
"""
import base64
import mimetypes
import re
import sys
from pathlib import Path


def inline_stylesheets(html: str, base_dir: Path) -> str:
    link_re = re.compile(
        r'<link\b[^>]*\brel=["\']stylesheet["\'][^>]*\bhref=["\']([^"\']+)["\'][^>]*>',
        re.IGNORECASE,
    )

    def repl(m: re.Match) -> str:
        href = m.group(1)
        if href.startswith(("http://", "https://", "//", "data:")):
            return m.group(0)  # remote stylesheet — leave as-is
        css_path = (base_dir / href).resolve()
        if not css_path.is_file():
            print(f"  warn: stylesheet not found, left as link: {href}", file=sys.stderr)
            return m.group(0)
        css = css_path.read_text(encoding="utf-8")
        print(f"  inlined css: {href} ({len(css)} bytes)")
        return f"<style>\n{css}\n</style>"

    return link_re.sub(repl, html)


def embed_images(html: str, base_dir: Path) -> str:
    img_re = re.compile(r'(<img\b[^>]*\bsrc=["\'])([^"\']+)(["\'])', re.IGNORECASE)

    def repl(m: re.Match) -> str:
        src = m.group(2)
        if src.startswith(("http://", "https://", "//", "data:")):
            return m.group(0)
        img_path = (base_dir / src).resolve()
        if not img_path.is_file():
            print(f"  warn: image not found, left as src: {src}", file=sys.stderr)
            return m.group(0)
        mime = mimetypes.guess_type(str(img_path))[0] or "image/jpeg"
        data = base64.b64encode(img_path.read_bytes()).decode("ascii")
        print(f"  embedded image: {src} ({len(data)} b64 chars)")
        return f"{m.group(1)}data:{mime};base64,{data}{m.group(3)}"

    return img_re.sub(repl, html)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: python3 build_standalone.py <input.html> <output.html>", file=sys.stderr)
        return 2
    in_path = Path(sys.argv[1]).resolve()
    out_path = Path(sys.argv[2]).resolve()
    base_dir = in_path.parent

    html = in_path.read_text(encoding="utf-8")
    html = inline_stylesheets(html, base_dir)
    html = embed_images(html, base_dir)
    out_path.write_text(html, encoding="utf-8")
    print(f"written {out_path} ({len(html)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
