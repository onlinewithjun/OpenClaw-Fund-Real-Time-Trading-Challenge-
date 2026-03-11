#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
from pathlib import Path

OPENCLAW_HOME = Path(os.environ.get("USERPROFILE", "")) / ".openclaw"
SESSIONS_JSON = OPENCLAW_HOME / "agents" / "main" / "sessions" / "sessions.json"
CRON_JOBS = OPENCLAW_HOME / "cron" / "jobs.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def ms(ts0: float, ts1: float) -> int:
    return int((ts1 - ts0) * 1000)


def main() -> int:
    t0 = time.perf_counter()
    if not SESSIONS_JSON.exists():
        print("TOKEN_PROBE_FAIL sessions.json missing")
        return 1

    t1 = time.perf_counter()
    sessions = load_json(SESSIONS_JSON)
    t2 = time.perf_counter()

    now_ms = int(time.time() * 1000)
    cutoff = now_ms - 7 * 24 * 3600 * 1000

    job_name = {}
    if CRON_JOBS.exists():
        c0 = time.perf_counter()
        data = load_json(CRON_JOBS)
        c1 = time.perf_counter()
        for j in data.get("jobs", []):
            job_name[str(j.get("id", ""))] = str(j.get("name", ""))
    else:
        c0 = c1 = time.perf_counter()

    a0 = time.perf_counter()
    total_in = 0
    total_out = 0
    cron_in = 0
    by_job = {}

    for key, s in sessions.items():
        updated = int(s.get("updatedAt", 0) or 0)
        if updated < cutoff:
            continue

        in_t = int(s.get("inputTokens", 0) or 0)
        out_t = int(s.get("outputTokens", 0) or 0)
        total_in += in_t
        total_out += out_t

        if ":cron:" in key:
            cron_in += in_t
            marker = key.split(":cron:", 1)[1]
            job_id = marker.split(":", 1)[0]
            by_job[job_id] = by_job.get(job_id, 0) + in_t

    top = sorted(by_job.items(), key=lambda x: x[1], reverse=True)[:3]

    def pretty_job(jid: str) -> str:
        name = (job_name.get(jid) or "").strip()
        if name:
            return name
        # historical/deleted cron ids may not exist in current jobs.json
        return f"UNKNOWN_TASK({jid[:8]})"

    top_str = ", ".join(
        f"{pretty_job(jid)}:{val}" for jid, val in top
    ) if top else "none"
    a1 = time.perf_counter()

    t3 = time.perf_counter()
    print(
        f"WEEKLY_TOKEN_REPORT in={total_in} out={total_out} cron_in={cron_in} "
        f"cron_share={(cron_in / total_in * 100 if total_in else 0):.1f}% top3=[{top_str}]"
    )
    print(
        "TOKEN_PROBE_MS "
        f"bootstrap={ms(t0,t1)} load_sessions={ms(t1,t2)} "
        f"load_cron={ms(c0,c1)} aggregate={ms(a0,a1)} total={ms(t0,t3)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
