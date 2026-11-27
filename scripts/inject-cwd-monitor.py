# -*- coding: utf-8 -*-
"""Inject CWD Site Monitor agent before </body> on every HTML page."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ACTIVE = """<script
  defer
  src="https://media.cwd-cdn.com/monitor/agent/v1/agent.min.js"
  data-cwd-site-id="{site_id}"
  data-cwd-environment="production"
  data-cwd-collector="https://cwd-site-monitor-collector.cwdmedia.workers.dev/v1/events">
</script>
"""

COMMENTED = """<!--
<script
  defer
  src="https://media.cwd-cdn.com/monitor/agent/v1/agent.min.js"
  data-cwd-site-id="{site_id}"
  data-cwd-environment="production"
  data-cwd-collector="https://cwd-site-monitor-collector.cwdmedia.workers.dev/v1/events">
</script>
-->
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--mode",
        choices=("active", "commented"),
        default="active",
    )
    args = parser.parse_args()
    root: Path = args.root.resolve()
    cfg = json.loads((root / "cwd-monitor.config.json").read_text(encoding="utf-8"))
    site_id = cfg["site_id"]
    snippet = (ACTIVE if args.mode == "active" else COMMENTED).format(site_id=site_id)

    changed = []
    for path in sorted(root.rglob("*.html")):
        if any(p in path.parts for p in (".git", "scripts", "node_modules")):
            continue
        text = path.read_text(encoding="utf-8")
        if "data-cwd-site-id=" in text or "agent.min.js" in text:
            continue
        if not re.search(r"</body\s*>", text, re.I):
            print("SKIP (no </body>):", path.relative_to(root))
            continue
        updated = re.sub(
            r"</body\s*>",
            snippet + "</body>",
            text,
            count=1,
            flags=re.I,
        )
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed.append(str(path.relative_to(root)))

    print(f"Injected ({args.mode}) into {len(changed)} files under {root}")
    for c in changed:
        print(" -", c)


if __name__ == "__main__":
    main()
