from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import struct
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "assets" / "drive" / "asset-manifest.json"
QUEUE_DIR = ROOT / "ops" / "ai-os" / "asset-sync" / "upload-queue"
DRIVE_ROOT = {
    "name": "RITO/assets",
    "folder_id": "1t_ZfqPZl_-hhlzgPF3Lbnf3nOYPdZz3L",
    "url": "https://drive.google.com/drive/folders/1t_ZfqPZl_-hhlzgPF3Lbnf3nOYPdZz3L",
}
MEDIA_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".docx",
    ".xlsx",
    ".pptx",
    ".mp4",
    ".mov",
    ".pdf",
    ".zip",
}
SKIP_PARTS = {
    ".git",
    ".colima",
    "dist",
    "release",
    ".sessions",
    ".session",
    "runtime",
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "asset"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> dict[str, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return {"width": width, "height": height}


def jpeg_dimensions(path: Path) -> dict[str, int] | None:
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            return None
        while True:
            marker_start = handle.read(1)
            if not marker_start:
                return None
            if marker_start != b"\xff":
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {b"\xd8", b"\xd9"}:
                continue
            length_bytes = handle.read(2)
            if len(length_bytes) != 2:
                return None
            length = struct.unpack(">H", length_bytes)[0]
            if marker in {
                b"\xc0",
                b"\xc1",
                b"\xc2",
                b"\xc3",
                b"\xc5",
                b"\xc6",
                b"\xc7",
                b"\xc9",
                b"\xca",
                b"\xcb",
                b"\xcd",
                b"\xce",
                b"\xcf",
            }:
                data = handle.read(5)
                if len(data) != 5:
                    return None
                height, width = struct.unpack(">HH", data[1:5])
                return {"width": width, "height": height}
            handle.seek(length - 2, 1)


def dimensions(path: Path) -> dict[str, int] | None:
    suffix = path.suffix.lower()
    try:
        if suffix == ".png":
            return png_dimensions(path)
        if suffix in {".jpg", ".jpeg"}:
            return jpeg_dimensions(path)
    except Exception:
        return None
    return None


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {
            "version": 1,
            "updated_at": now_iso(),
            "drive_root": DRIVE_ROOT,
            "policy": {},
            "assets": [],
        }
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(manifest: dict[str, Any]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    manifest["updated_at"] = now_iso()
    manifest["drive_root"] = DRIVE_ROOT
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def infer_campaign(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    if len(parts) >= 3 and parts[0] == "assets" and parts[1] == "social":
        return "/".join(parts[1:-1]) or "social"
    if "business-kit" in parts:
        return "business-kit"
    if len(parts) >= 3 and parts[0] == "assets" and parts[1] == "brand":
        return "/".join(parts[1:-1]) or "brand"
    return "/".join(parts[:-1]) if parts else "general"


def infer_drive_folder(path: Path) -> str:
    try:
        relative_to_assets = path.relative_to(ROOT / "assets")
        parent = relative_to_assets.parent.as_posix()
        return f"assets/{parent}" if parent != "." else "assets"
    except ValueError:
        return "assets/general"


def make_asset(path: Path, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    stat = path.stat()
    digest = sha256_file(path)
    relative_path = rel(path)
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    previous_drive = (existing or {}).get("drive") or {}
    asset_id = (existing or {}).get("asset_id") or f"{digest[:12]}-{slugify(path.stem)}"
    return {
        "asset_id": asset_id,
        "relative_path": relative_path,
        "filename": path.name,
        "campaign": infer_campaign(path),
        "mime_type": mime_type,
        "size_bytes": stat.st_size,
        "sha256": digest,
        "dimensions": dimensions(path),
        "drive": {
            "status": previous_drive.get("status") or "local_pending_upload",
            "file_id": previous_drive.get("file_id") or "",
            "url": previous_drive.get("url") or "",
            "folder": previous_drive.get("folder") or infer_drive_folder(path),
        },
        "usage": (existing or {}).get(
            "usage",
            {
                "git_policy": "drive_only",
                "site_runtime": relative_path.startswith("site/"),
            },
        ),
        "created_at": datetime.fromtimestamp(stat.st_ctime).astimezone().isoformat(timespec="seconds"),
        "updated_at": now_iso(),
    }


def scan_files(roots: list[str], min_size: int) -> list[Path]:
    files: list[Path] = []
    for item in roots:
        root = (ROOT / item).resolve()
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or should_skip(path):
                continue
            if path.suffix.lower() not in MEDIA_EXTENSIONS:
                continue
            if path.stat().st_size < min_size:
                continue
            files.append(path)
    return sorted(files)


def merge_assets(manifest: dict[str, Any], paths: list[Path]) -> list[dict[str, Any]]:
    existing_by_path = {item.get("relative_path"): item for item in manifest.get("assets", [])}
    existing_by_hash = {item.get("sha256"): item for item in manifest.get("assets", [])}
    merged = []
    seen = set()
    for path in paths:
        digest = sha256_file(path)
        relative_path = rel(path)
        existing = existing_by_path.get(relative_path) or existing_by_hash.get(digest)
        asset = make_asset(path, existing=existing)
        merged.append(asset)
        seen.add(relative_path)
    for asset in manifest.get("assets", []):
        if asset.get("relative_path") not in seen:
            asset = dict(asset)
            asset["drive"] = dict(asset.get("drive") or {})
            if asset["drive"].get("status") == "local_pending_upload":
                asset["drive"]["status"] = "local_missing"
            merged.append(asset)
    return sorted(merged, key=lambda item: item.get("relative_path", ""))


def write_queue(assets: list[dict[str, Any]]) -> Path:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    pending = [
        {
            "asset_id": item["asset_id"],
            "relative_path": item["relative_path"],
            "size_bytes": item["size_bytes"],
            "sha256": item["sha256"],
            "suggested_drive_folder": item["drive"]["folder"],
        }
        for item in assets
        if item.get("drive", {}).get("status") in {"local_pending_upload", "local_missing"}
    ]
    queue = {
        "created_at": now_iso(),
        "drive_root": DRIVE_ROOT,
        "pending_count": len(pending),
        "pending": pending,
    }
    path = QUEUE_DIR / f"{datetime.now():%Y-%m-%d-%H%M%S}-drive-upload-queue.json"
    path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def drive_file_url(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/view" if file_id else ""


def update_uploaded_assets_from_lsjson(manifest: dict[str, Any], remote_items: list[dict[str, Any]]) -> int:
    by_path = {item.get("Path"): item for item in remote_items if item.get("Path")}
    updated = 0
    for asset in manifest.get("assets", []):
        relative_path = asset.get("relative_path", "")
        remote = by_path.get(relative_path)
        if not remote:
            continue
        file_id = remote.get("ID") or remote.get("OrigID") or ""
        asset.setdefault("drive", {})
        asset["drive"].update(
            {
                "status": "uploaded",
                "file_id": file_id,
                "url": drive_file_url(file_id),
                "folder": Path(relative_path).parent.as_posix(),
            }
        )
        asset["updated_at"] = now_iso()
        updated += 1
    return updated


def cmd_scan(args: argparse.Namespace) -> int:
    min_size = int(float(args.min_mb) * 1024 * 1024)
    manifest = load_manifest()
    paths = scan_files(args.roots, min_size)
    assets = merge_assets(manifest, paths)
    print(f"Arquivos de mídia encontrados: {len(paths)}")
    print(f"Assets no manifesto resultante: {len(assets)}")
    if args.write_manifest:
        manifest["assets"] = assets
        save_manifest(manifest)
        print(f"Manifesto atualizado: {MANIFEST_PATH.relative_to(ROOT)}")
    if args.write_queue:
        queue_path = write_queue(assets)
        print(f"Fila de upload gerada: {queue_path.relative_to(ROOT)}")
    return 0


def cmd_upload(args: argparse.Namespace) -> int:
    if args.rescan:
        scan_args = argparse.Namespace(
            roots=args.roots,
            min_mb=args.min_mb,
            write_manifest=True,
            write_queue=True,
        )
        cmd_scan(scan_args)

    manifest = load_manifest()
    pending_assets = [
        asset
        for asset in manifest.get("assets", [])
        if asset.get("drive", {}).get("status") in {"local_pending_upload", "local_missing"}
    ]
    existing_assets = []
    for asset in pending_assets:
        path = ROOT / asset.get("relative_path", "")
        if path.exists() and path.is_file():
            existing_assets.append(asset)
        else:
            print(f"Ignorando arquivo local ausente: {asset.get('relative_path')}")

    if not existing_assets:
        print("Nenhum asset pendente encontrado para upload.")
        return 0

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
        files_from = Path(handle.name)
        for asset in existing_assets:
            handle.write(asset["relative_path"] + "\n")

    try:
        copy_command = [
            "rclone",
            "copy",
            str(ROOT),
            args.remote,
            "--files-from",
            str(files_from),
            "--create-empty-src-dirs",
            "--progress",
            "--stats",
            "10s",
        ]
        if args.dry_run:
            copy_command.append("--dry-run")
        print(f"Enviando {len(existing_assets)} assets para {args.remote}")
        subprocess.run(copy_command, check=True)

        if args.dry_run:
            print("Dry-run concluído. Manifesto não foi marcado como uploaded.")
            return 0

        lsjson = subprocess.run(
            ["rclone", "lsjson", args.remote, "--recursive", "--files-only"],
            check=True,
            capture_output=True,
            text=True,
        )
        remote_items = json.loads(lsjson.stdout)
        updated = update_uploaded_assets_from_lsjson(manifest, remote_items)
        save_manifest(manifest)
        print(f"Manifesto atualizado com {updated} assets enviados.")
        return 0
    finally:
        try:
            files_from.unlink()
        except FileNotFoundError:
            pass


def cmd_register(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    relative_path = rel((ROOT / args.path).resolve())
    matched = None
    for asset in manifest.get("assets", []):
        if asset.get("relative_path") == relative_path:
            matched = asset
            break
    if matched is None:
        path = (ROOT / args.path).resolve()
        if not path.exists():
            raise SystemExit(f"Arquivo não encontrado no manifesto nem no disco: {args.path}")
        matched = make_asset(path)
        manifest.setdefault("assets", []).append(matched)
    matched.setdefault("drive", {})
    matched["drive"].update(
        {
            "status": args.status,
            "file_id": args.drive_id,
            "url": args.drive_url,
            "folder": args.drive_folder or matched["drive"].get("folder") or "Assets/General",
        }
    )
    matched["updated_at"] = now_iso()
    save_manifest(manifest)
    print(f"Asset registrado: {relative_path}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    assets = manifest.get("assets", [])
    ids = [item.get("asset_id") for item in assets]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    missing_drive = [
        item.get("relative_path")
        for item in assets
        if item.get("drive", {}).get("status") == "uploaded" and not item.get("drive", {}).get("file_id")
    ]
    print(f"Assets no manifesto: {len(assets)}")
    print(f"Duplicados: {len(duplicates)}")
    print(f"Uploads sem file_id: {len(missing_drive)}")
    if duplicates:
        print("asset_id duplicados:")
        for item in duplicates:
            print(f"- {item}")
    if missing_drive:
        print("uploads sem file_id:")
        for item in missing_drive:
            print(f"- {item}")
    return 1 if duplicates or missing_drive else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gerencia manifesto de assets grandes da RITO no Google Drive.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Escanear mídia local e atualizar manifesto/fila.")
    scan.add_argument(
        "--roots",
        nargs="+",
        default=["assets/brand/logos", "assets/business-kit", "assets/social"],
        help="Pastas relativas ao repo para escanear.",
    )
    scan.add_argument("--min-mb", default="0.5", help="Tamanho mínimo em MB.")
    scan.add_argument("--write-manifest", action="store_true")
    scan.add_argument("--write-queue", action="store_true")
    scan.set_defaults(func=cmd_scan)

    upload = subparsers.add_parser("upload", help="Subir assets pendentes via rclone e atualizar manifesto.")
    upload.add_argument("--remote", default="rito-drive:", help="Remote rclone de destino.")
    upload.add_argument(
        "--roots",
        nargs="+",
        default=["assets/brand/logos", "assets/business-kit", "assets/social"],
        help="Pastas relativas ao repo para rescan.",
    )
    upload.add_argument("--min-mb", default="0.5", help="Tamanho mínimo em MB no rescan.")
    upload.add_argument("--rescan", action="store_true", help="Atualizar manifesto antes de subir.")
    upload.add_argument("--dry-run", action="store_true")
    upload.set_defaults(func=cmd_upload)

    register = subparsers.add_parser("register", help="Registrar asset já enviado ao Google Drive.")
    register.add_argument("--path", required=True, help="Caminho relativo do asset no repo.")
    register.add_argument("--drive-id", required=True)
    register.add_argument("--drive-url", required=True)
    register.add_argument("--drive-folder", default="")
    register.add_argument("--status", default="uploaded", choices=["uploaded", "approved", "archived"])
    register.set_defaults(func=cmd_register)

    check = subparsers.add_parser("check", help="Validar manifesto.")
    check.set_defaults(func=cmd_check)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
