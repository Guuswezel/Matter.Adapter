#!/usr/bin/env python3
"""Download pinned upstream firmware; never access or flash a board."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def fetch(url: str, target: Path, sha256: str) -> None:
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == sha256:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    # Keep a previous download intact until the replacement is verified.
    temporary = target.with_suffix(target.suffix + ".part")
    try:
        with urllib.request.urlopen(url, timeout=60) as response, temporary.open("wb") as output:
            digest = hashlib.sha256()
            total = 0
            while chunk := response.read(65536):
                total += len(chunk)
                if total > 16 * 1024 * 1024:
                    raise ValueError("Firmware download exceeded 16 MiB")
                digest.update(chunk)
                output.write(chunk)
        if digest.hexdigest() != sha256:
            raise ValueError(f"SHA-256 mismatch for {target.name}")
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    manifest = json.loads((ROOT / "firmware/manifest.json").read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootloader", action="store_true", help="Also download the optional recovery bootloader")
    parser.add_argument("--output-dir", type=Path, default=ROOT / ".cache/firmware")
    args = parser.parse_args()
    base = manifest["release_url"].replace("/tag/", "/download/")
    for name in ["application"] + (["bootloader"] if args.bootloader else []):
        artifact = manifest[name]
        target = args.output_dir / artifact["filename"]
        fetch(f"{base}/{artifact['filename']}", target, artifact["sha256"])
        print(f"Verified {target}")


if __name__ == "__main__":
    main()
