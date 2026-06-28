#!/usr/bin/env python3
"""Check whether the live domain is serving the generated deployment."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


def fetch_text(url: str, timeout: int) -> tuple[int, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "RITO-deploy-check/1.0",
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        },
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
        return response.status, body


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the deployed RITO site.")
    parser.add_argument("--base-url", default="https://ritosistemas.com", help="Live site base URL")
    parser.add_argument("--dist", default="dist", help="Local dist directory")
    parser.add_argument("--timeout", type=int, default=20, help="Request timeout in seconds")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    dist_dir = Path(args.dist).resolve()
    local_deploy_info_path = dist_dir / "deploy-info.json"

    if not local_deploy_info_path.exists():
        print(f"deploy-info local nao encontrado: {local_deploy_info_path}", file=sys.stderr)
        return 1

    local_deploy_info = json.loads(local_deploy_info_path.read_text(encoding="utf-8"))
    expected_asset_version = str(local_deploy_info.get("asset_version", ""))

    checks = [
        ("/deploy-info.json", "deploy-info"),
        ("/", "home"),
        ("/pages/projeto-piloto.html", "landing"),
    ]
    fetched: dict[str, str] = {}

    try:
        for path, label in checks:
            status, body = fetch_text(f"{base_url}{path}", args.timeout)
            if status >= 400:
                print(f"{label}: HTTP {status}", file=sys.stderr)
                return 1
            fetched[label] = body
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"Nao consegui acessar {base_url}: {error}", file=sys.stderr)
        return 1

    try:
        live_deploy_info = json.loads(fetched["deploy-info"])
    except json.JSONDecodeError:
        print("O dominio nao esta servindo deploy-info.json valido.", file=sys.stderr)
        print("Isso normalmente indica que a Hostinger nao esta apontando para a branch/pasta de deploy atual.", file=sys.stderr)
        return 1

    live_asset_version = str(live_deploy_info.get("asset_version", ""))

    if expected_asset_version and live_asset_version != expected_asset_version:
        print(
            f"Deploy divergente: asset_version local={expected_asset_version}, live={live_asset_version}",
            file=sys.stderr,
        )
        return 1

    if "Projeto Piloto RITO" not in fetched["landing"]:
        print("A landing publicada nao contem 'Projeto Piloto RITO'.", file=sys.stderr)
        return 1

    print(f"Site publicado OK: {base_url}")
    print(f"asset_version: {live_asset_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
