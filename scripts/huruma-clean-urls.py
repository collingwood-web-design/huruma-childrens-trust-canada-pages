# -*- coding: utf-8 -*-
"""One-shot Huruma clean-URL rewrite for folder + FR flat HTML layout."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CLIENT_REDIRECT = """    <script>
      /* Prefer clean URLs when someone lands on the .html form (http/https only). */
      (function () {
        if (window.location.protocol === "file:") return;
        var path = window.location.pathname;
        if (!/\\.html$/i.test(path)) return;
        var clean = path.replace(/\\.html$/i, "");
        if (/\\/index$/i.test(clean)) clean = clean.replace(/\\/index$/i, "/") || "/";
        if (clean === "") clean = "/";
        window.location.replace(clean + window.location.search + window.location.hash);
      })();
    </script>
"""


def is_redirect_stub(text: str) -> bool:
    low = text.lower()
    return (
        "location.replace" in text
        and len(text) < 2500
        and (
            'http-equiv="refresh"' in low
            or "http-equiv='refresh'" in low
            or text.count("<") < 40
        )
    )


def is_fr(path: Path) -> bool:
    return "fr" in path.parts


def rewrite_html(path: Path, text: str) -> str:
    abs_map = [
        (
            "https://hurumachildrenstrustcanada.org/fr/donation-costs.html",
            "https://hurumachildrenstrustcanada.org/fr/donation-costs",
        ),
        (
            "https://hurumachildrenstrustcanada.org/fr/mamas-health.html",
            "https://hurumachildrenstrustcanada.org/fr/mamas-health",
        ),
        (
            "https://hurumachildrenstrustcanada.org/fr/reports.html",
            "https://hurumachildrenstrustcanada.org/fr/reports",
        ),
        (
            "https://hurumachildrenstrustcanada.org/fr/donate.html",
            "https://hurumachildrenstrustcanada.org/fr/donate",
        ),
        (
            "https://hurumachildrenstrustcanada.org/fr/index.html",
            "https://hurumachildrenstrustcanada.org/fr/",
        ),
        (
            "https://hurumachildrenstrustcanada.org/donation-costs.html",
            "https://hurumachildrenstrustcanada.org/donation-costs",
        ),
        (
            "https://hurumachildrenstrustcanada.org/index.html",
            "https://hurumachildrenstrustcanada.org/",
        ),
    ]
    for a, b in abs_map:
        text = text.replace(a, b)

    pairs = [
        ('href="../index.html#mama"', 'href="../#mama"'),
        ('href="../index.html"', 'href="../"'),
        ('href="index.html#mama"', 'href="./#mama"'),
        ('href="index.html"', 'href="./"'),
        ('href="../donation-costs.html"', 'href="../donation-costs"'),
        ('href="donation-costs.html"', 'href="donation-costs"'),
        ('href="../fr/donation-costs.html"', 'href="../fr/donation-costs"'),
        ('href="../fr/mamas-health.html"', 'href="../fr/mamas-health"'),
        ('href="../fr/reports.html"', 'href="../fr/reports"'),
        ('href="../fr/donate.html"', 'href="../fr/donate"'),
        ('href="fr/donation-costs.html"', 'href="fr/donation-costs"'),
        ('href="fr/mamas-health.html"', 'href="fr/mamas-health"'),
        ('href="fr/reports.html"', 'href="fr/reports"'),
        ('href="fr/donate.html"', 'href="fr/donate"'),
        ('href="fr/index.html"', 'href="fr/"'),
        ('href="fr/404.html"', 'href="fr/404"'),
        ('href="404.html"', 'href="404"'),
    ]
    for a, b in pairs:
        text = text.replace(a, b)

    if is_fr(path):
        fr_pairs = [
            ('href="reports.html#summer-2026"', 'href="reports#summer-2026"'),
            ('href="reports.html#january-2026"', 'href="reports#january-2026"'),
            ('href="reports.html#march-2026"', 'href="reports#march-2026"'),
            ('href="reports.html"', 'href="reports"'),
            ('href="mamas-health.html"', 'href="mamas-health"'),
            ('href="donate.html"', 'href="donate"'),
        ]
        for a, b in fr_pairs:
            text = text.replace(a, b)
    else:
        en_pairs = [
            (
                'href="reports.html#summer-2026"',
                'href="reports-from-board-of-directors/#summer-2026"',
            ),
            (
                'href="reports.html#january-2026"',
                'href="reports-from-board-of-directors/#january-2026"',
            ),
            (
                'href="reports.html#march-2026"',
                'href="reports-from-board-of-directors/#march-2026"',
            ),
            ('href="reports.html"', 'href="reports-from-board-of-directors/"'),
            ('href="mamas-health.html"', 'href="mamas-health/"'),
            ('href="donate.html"', 'href="donate-now/"'),
        ]
        for a, b in en_pairs:
            text = text.replace(a, b)

    if not is_redirect_stub(text) and "Prefer clean URLs when someone lands" not in text:
        if re.search(r"<head[^>]*>", text, re.I):
            text = re.sub(
                r"(<head[^>]*>)",
                r"\1\n" + CLIENT_REDIRECT,
                text,
                count=1,
                flags=re.I,
            )

    return text


def main() -> None:
    changed: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if "scripts" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = rewrite_html(path, original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed.append(str(path.relative_to(ROOT)))

    abs_map = [
        (
            "https://hurumachildrenstrustcanada.org/fr/donation-costs.html",
            "https://hurumachildrenstrustcanada.org/fr/donation-costs",
        ),
        (
            "https://hurumachildrenstrustcanada.org/fr/mamas-health.html",
            "https://hurumachildrenstrustcanada.org/fr/mamas-health",
        ),
        (
            "https://hurumachildrenstrustcanada.org/fr/reports.html",
            "https://hurumachildrenstrustcanada.org/fr/reports",
        ),
        (
            "https://hurumachildrenstrustcanada.org/fr/donate.html",
            "https://hurumachildrenstrustcanada.org/fr/donate",
        ),
        (
            "https://hurumachildrenstrustcanada.org/fr/index.html",
            "https://hurumachildrenstrustcanada.org/fr/",
        ),
        (
            "https://hurumachildrenstrustcanada.org/donation-costs.html",
            "https://hurumachildrenstrustcanada.org/donation-costs",
        ),
        (
            "https://hurumachildrenstrustcanada.org/index.html",
            "https://hurumachildrenstrustcanada.org/",
        ),
    ]
    for name in ("sitemap.xml", "llms.txt", "robots.txt"):
        p = ROOT / name
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        o = t
        for a, b in abs_map:
            t = t.replace(a, b)
        if t != o:
            p.write_text(t, encoding="utf-8", newline="\n")
            changed.append(name)

    print(f"Updated {len(changed)} files")
    for c in changed:
        print(" -", c)


if __name__ == "__main__":
    main()
