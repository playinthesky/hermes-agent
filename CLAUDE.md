@AGENTS.md

## Why this file exists

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. Until this file existed, none of
the 1,369 lines in `AGENTS.md` reached a Claude Code session — the Contribution
Rubric, Important Policies, and Known Pitfalls were all invisible to the agent
they were written for.

`AGENTS.md` stays the single source of truth. Do not copy rules into this file;
edit `AGENTS.md` instead.

### Known trade-off

`AGENTS.md` is ~72KB and loads in full at the start of every session. That is a
lot of context, but the alternative it replaced was loading none of it. The next
step is to keep the always-on sections here and move the reference sections into
`.claude/rules/*.md` with `paths:` frontmatter, so they load only when Claude
touches matching files. See the Claude Code memory docs for the rules format.
