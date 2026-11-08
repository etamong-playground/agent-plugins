#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


EXPECTED_CSP = {
    "default-src": ("'none'",),
    "img-src": ("data:",),
    "style-src": ("'unsafe-inline'",),
    "script-src": ("'unsafe-inline'",),
    "connect-src": ("'none'",),
    "frame-src": ("'none'",),
    "object-src": ("'none'",),
    "base-uri": ("'none'",),
    "form-action": ("'none'",),
}
REQUIRED_SECTIONS = {"background", "intuition", "code", "quiz"}
BANNED_ELEMENTS = {"base", "embed", "frame", "iframe", "object"}
RESOURCE_ATTRIBUTES = {
    "audio": {"src"},
    "form": {"action"},
    "image": {"href", "xlink:href"},
    "img": {"src", "srcset"},
    "input": {"formaction", "src"},
    "link": {"href"},
    "script": {"src"},
    "source": {"src", "srcset"},
    "track": {"src"},
    "use": {"href", "xlink:href"},
    "video": {"poster", "src"},
}
UNSAFE_SCRIPT = re.compile(
    r"\b(fetch|XMLHttpRequest|WebSocket|sendBeacon)\s*\(|"
    r"\.(innerHTML|outerHTML)\s*=|\.(insertAdjacentHTML|write|writeln)\s*\(|"
    r"\bwindow\.open\s*\(|\blocation\.(assign|replace)\s*\(|"
    r"\b(?:window\.)?location\s*=",
    re.IGNORECASE,
)
UNSAFE_CSS = re.compile(r"@import|url\s*\(", re.IGNORECASE)


def parse_csp(content: str) -> dict[str, tuple[str, ...]]:
    directives: dict[str, tuple[str, ...]] = {}
    for item in content.split(";"):
        parts = item.split()
        if parts:
            directives[parts[0].lower()] = tuple(parts[1:])
    return directives


class ExplainerValidator(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []
        self.sections: Counter[str] = Counter()
        self.csp_values: list[str] = []
        self.script_depth = 0
        self.style_depth = 0
        self.quiz_scripts = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = {name.lower(): value or "" for name, value in attrs}
        line, _ = self.getpos()

        if tag in BANNED_ELEMENTS:
            self.errors.append(f"line {line}: forbidden <{tag}> element")

        element_id = values.get("id")
        if element_id in REQUIRED_SECTIONS:
            self.sections[element_id] += 1

        if tag == "meta" and values.get("http-equiv", "").lower() == "content-security-policy":
            self.csp_values.append(values.get("content", ""))
        elif tag == "meta" and values.get("http-equiv", "").lower() == "refresh":
            self.errors.append(f"line {line}: meta refresh is forbidden")

        if tag == "script":
            self.script_depth += 1
            self.quiz_scripts += 1
        elif tag == "style":
            self.style_depth += 1

        for name in RESOURCE_ATTRIBUTES.get(tag, set()):
            value = values.get(name, "").strip()
            if not value:
                continue
            if tag == "img" and name == "src" and value.lower().startswith("data:image/"):
                continue
            if tag == "use" and value.startswith("#"):
                continue
            self.errors.append(f"line {line}: forbidden {tag}[{name}] resource")

        for name in values:
            if name.startswith("on"):
                self.errors.append(f"line {line}: inline event handler {name} is forbidden")

        if "style" in values and UNSAFE_CSS.search(values["style"]):
            self.errors.append(f"line {line}: CSS resource loading is forbidden")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() == "script":
            self.script_depth -= 1
        elif tag.lower() == "style":
            self.style_depth -= 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self.script_depth:
            self.script_depth -= 1
        elif tag.lower() == "style" and self.style_depth:
            self.style_depth -= 1

    def handle_data(self, data: str) -> None:
        line, _ = self.getpos()
        if self.script_depth and UNSAFE_SCRIPT.search(data):
            self.errors.append(f"line {line}: network or unsafe DOM API in script")
        if self.style_depth and UNSAFE_CSS.search(data):
            self.errors.append(f"line {line}: CSS resource loading is forbidden")

    def finish(self) -> list[str]:
        for section in sorted(REQUIRED_SECTIONS):
            if self.sections[section] != 1:
                self.errors.append(
                    f"section id={section!r} appears {self.sections[section]} times; expected once"
                )
        if self.quiz_scripts == 0:
            self.errors.append("quiz script is missing")
        if len(self.csp_values) != 1:
            self.errors.append(f"found {len(self.csp_values)} CSP declarations; expected one")
        elif parse_csp(self.csp_values[0]) != EXPECTED_CSP:
            self.errors.append("CSP does not match the required directive set")
        return self.errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_html.py EXPLAINER.html", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).resolve()
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        return 2

    if path.parent.name == "explain" and path.parent.parent.name == ".tmp":
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.html", path.name):
            print("default output filename is not YYYY-MM-DD-safe-slug.html", file=sys.stderr)
            return 1

    parser = ExplainerValidator()
    parser.feed(path.read_text(encoding="utf-8"))
    errors = parser.finish()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"valid explainer: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
