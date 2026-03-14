from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
FUND = WORKSPACE / "fund_challenge"
OUT = FUND / "out"
RUNTIME = FUND / "runtime"
EVIDENCE = FUND / "evidence"


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(WORKSPACE), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def prune_runtime_cache() -> dict:
    code, out, err = run([sys.executable, "fund_challenge/scripts/runtime_cache.py", "prune"])
    if code != 0:
        raise RuntimeError(err or out or "runtime_cache_prune_failed")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out}


def remove_if_exists(path: Path) -> int:
    if path.exists():
        path.unlink()
        return 1
    return 0


def cleanup_out_dir() -> int:
    removed = 0
    removed += remove_if_exists(OUT / "preflight.fail.json")
    removed += remove_if_exists(OUT / "fail.short.txt")
    return removed


def cleanup_runtime_snapshots(keep_days: int = 3) -> int:
    cutoff = datetime.now() - timedelta(days=keep_days)
    removed = 0
    for p in RUNTIME.glob("manual_snapshot_*.json"):
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime)
        except Exception:
            continue
        if mtime < cutoff:
            p.unlink()
            removed += 1
    return removed


def archive_old_evidence(keep_days: int = 5) -> int:
    archive = EVIDENCE / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    cutoff = datetime.now() - timedelta(days=keep_days)
    moved = 0
    for p in EVIDENCE.glob("decision-*.json"):
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime)
        except Exception:
            continue
        if mtime < cutoff:
            shutil.move(str(p), str(archive / p.name))
            moved += 1
    return moved


def cleanup_pyc() -> int:
    removed = 0
    for p in FUND.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
        removed += 1
    return removed


def main() -> None:
    cache = prune_runtime_cache()
    out_removed = cleanup_out_dir()
    runtime_removed = cleanup_runtime_snapshots()
    evidence_archived = archive_old_evidence()
    pyc_removed = cleanup_pyc()

    print(
        "MAINTENANCE_OK "
        f"cache_removed={cache.get('removed', 0)} "
        f"cache_remain={cache.get('remain', '-')} "
        f"out_removed={out_removed} "
        f"runtime_snapshots_removed={runtime_removed} "
        f"evidence_archived={evidence_archived} "
        f"pycache_dirs_removed={pyc_removed}"
    )


if __name__ == "__main__":
    main()
