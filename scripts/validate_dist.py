#!/usr/bin/env python3
"""Validate the static Hostinger deployment package before publishing."""

from __future__ import annotations

import argparse
import html.parser
import json
import posixpath
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


REQUIRED_PATHS = [
    "index.html",
    "contact.php",
    "deploy-info.json",
    "assets/css/styles.css",
    "assets/js/app.js",
    "assets/js/measurement.js",
    "logos/rito_monogram_r_01.png",
    "logos/rito_sistemas_wordmark_01.png",
    "pages/contato.html",
    "pages/projeto-piloto.html",
    "storage/.htaccess",
    "storage/index.html",
]

IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "sms", "whatsapp"}
HTML_ATTRS = {"href", "src", "poster"}


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in HTML_ATTRS and value:
                self.links.append((name, value))


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def resolve_local_url(dist_dir: Path, html_file: Path, raw_url: str) -> Path | None:
    parsed = urlparse(raw_url)

    if parsed.scheme in IGNORED_SCHEMES or raw_url.startswith("//"):
        return None

    if raw_url.startswith("#") or raw_url.startswith("data:"):
        return None

    path = unquote(parsed.path)

    if not path:
        return None

    html_url_path = "/" + html_file.relative_to(dist_dir).as_posix()
    base_url_dir = posixpath.dirname(html_url_path)

    if path.startswith("/"):
        url_path = posixpath.normpath(path)
    else:
        url_path = posixpath.normpath(posixpath.join(base_url_dir, path))

    if url_path == ".":
        return None

    if url_path == "/":
        return dist_dir / "index.html"

    if raw_url.endswith("/"):
        url_path = posixpath.join(url_path, "index.html")

    return dist_dir / url_path.lstrip("/")


def validate_links(dist_dir: Path, errors: list[str]) -> None:
    for html_file in sorted(dist_dir.rglob("*.html")):
        parser = LinkParser()
        parser.feed(html_file.read_text(encoding="utf-8"))

        for attr_name, raw_url in parser.links:
            target = resolve_local_url(dist_dir, html_file, raw_url)

            if target is None:
                continue

            if not target.exists():
                relative_html = html_file.relative_to(dist_dir).as_posix()
                relative_target = target.relative_to(dist_dir).as_posix() if dist_dir in target.parents else str(target)
                fail(
                    f"{relative_html}: {attr_name}='{raw_url}' aponta para arquivo ausente ({relative_target})",
                    errors,
                )


def validate_dist(dist_dir: Path) -> list[str]:
    errors: list[str] = []

    if not dist_dir.exists():
        return [f"dist nao existe: {dist_dir}"]

    for required_path in REQUIRED_PATHS:
        if not (dist_dir / required_path).exists():
            fail(f"arquivo obrigatorio ausente: {required_path}", errors)

    forbidden_matches = [
        *dist_dir.rglob("*.jsonl"),
        *dist_dir.rglob(".DS_Store"),
    ]

    if (dist_dir / "logos" / "logos").exists():
        fail("pasta duplicada proibida encontrada: logos/logos", errors)

    for forbidden_path in forbidden_matches:
        fail(f"arquivo proibido no deploy: {forbidden_path.relative_to(dist_dir).as_posix()}", errors)

    for html_file in dist_dir.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")

        if "__ASSET_VERSION__" in content:
            fail(f"placeholder __ASSET_VERSION__ nao substituido em {html_file.relative_to(dist_dir).as_posix()}", errors)

    deploy_info_path = dist_dir / "deploy-info.json"

    if deploy_info_path.exists():
        try:
            deploy_info = json.loads(deploy_info_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            fail(f"deploy-info.json invalido: {error}", errors)
        else:
            if not deploy_info.get("asset_version"):
                fail("deploy-info.json sem asset_version", errors)
            if not deploy_info.get("built_at"):
                fail("deploy-info.json sem built_at", errors)

    validate_links(dist_dir, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the generated Hostinger dist directory.")
    parser.add_argument("--dist", default="dist", help="Dist directory to validate. Default: dist")
    args = parser.parse_args()

    dist_dir = Path(args.dist).resolve()
    errors = validate_dist(dist_dir)

    if errors:
        print("Validacao do dist falhou:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Dist validado: {dist_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
