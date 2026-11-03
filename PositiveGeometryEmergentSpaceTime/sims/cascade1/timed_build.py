#!/usr/bin/env python3
"""Resource meter for the LEAN-CERT-1 kill criteria (wall < 1 h, peak RSS < 15 GB).
Replaces the prereg's `/usr/bin/time -v` (not installed on the box; declared deviation in the result).
Peak RSS = resource.getrusage(RUSAGE_CHILDREN).ru_maxrss (max over waited-for descendants, i.e. the lean process).
Hard timeout 3600 s = the kill threshold. Not a scoring script (no guard)."""
import resource, subprocess, sys, time
cmd = sys.argv[1:]
t0 = time.time()
try:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    rc, out = p.returncode, p.stdout + p.stderr
except subprocess.TimeoutExpired as e:
    rc, out = 'TIMEOUT(3600s)', (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or '')
wall = time.time() - t0
rss_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
print(out)
print(f"CMD: {' '.join(cmd)}")
print(f"EXIT: {rc}")
print(f"WALL_SECONDS: {wall:.1f}")
print(f"PEAK_RSS_GB: {rss_kb / 1024 / 1024:.3f}")
print(f"KILL_THRESHOLDS: wall<3600s {'OK' if wall < 3600 else 'EXCEEDED'}; rss<15GB {'OK' if rss_kb < 15 * 1024 * 1024 else 'EXCEEDED'}")
