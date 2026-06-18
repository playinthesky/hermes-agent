---
description: Run Opus like Fable — apply fablize's verified procedures to the task
---

Apply the fablize operating discipline to the user's request below. Route by task signal — use the smallest matching discipline only.

- **Always**: lead with the outcome; stay within the requested scope (no incidental refactors); ground every completion claim in a tool result from this session; confirm before destructive or hard-to-reverse actions.
- **2+ sequential steps**: decompose into stories and track them with `python3 tools/fablize/scripts/goals.py` (create → next → checkpoint with evidence → final verification gate). No "done" without evidence.
- **Debugging / test failure / unknown cause / review**: follow `tools/fablize/packs/investigation-protocol.txt` — reproduce first, 3+ competing hypotheses, evidence per hypothesis, full causal chain, verify before/after.
- **Render/executable artifact (HTML, SVG, game, UI, chart)**: follow `tools/fablize/packs/verification-grounding-pack.txt` — run it in the real renderer, observe the output, fix what you see, re-run.
- **At the capability ceiling** (stuck 2+ times, out-of-spec discovery needed): report the limit honestly and escalate to `/effort xhigh`, a stronger model, or a human.

The task:

$ARGUMENTS
