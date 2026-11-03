"""Hardened guard for HG-DIM-2 (2026-10-31, the author; copied unchanged in logic from sims/hgdim1/guard.py).
guard(prereg, checker) is called inside EVERY scoring/live function. On EVERY call it re-reads the prereg, re-hashes the
checker file AND this guard file against the sha256 lines in the prereg, and re-runs
`git merge-base --is-ancestor <prereg commit> origin/main`. No pass flag is kept. `git fetch` runs once per process;
the ancestry result is not cached."""
import hashlib, re, subprocess, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
_FETCHED = []
def _git(*a):
    return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)
def guard(prereg, checker):
    if not _FETCHED:
        if _git('fetch', '-q', 'origin').returncode != 0: sys.exit('GUARD REFUSED: git fetch failed')
        _FETCHED.append(1)
    osha = _git('rev-parse', '--verify', '-q', 'refs/remotes/origin/main').stdout.strip()
    if not osha: sys.exit('GUARD REFUSED: no origin/main')
    psha = _git('log', '--format=%H', '--diff-filter=A', '-n', '1', '--', prereg).stdout.strip()
    if not psha: sys.exit(f'GUARD REFUSED: {prereg} has no commit')
    if _git('merge-base', '--is-ancestor', psha, osha).returncode != 0:
        sys.exit(f'GUARD REFUSED: prereg commit {psha[:9]} not an ancestor of origin/main (not pushed)')
    txt = (REPO / prereg).read_text()
    for f in (Path(checker).resolve(), Path(__file__).resolve()):
        m = re.search(re.escape(f.name) + r'` sha256 `([0-9a-f]{64})`', txt)
        if not m: sys.exit(f'GUARD REFUSED: no sha256 for {f.name} in prereg')
        if hashlib.sha256(f.read_bytes()).hexdigest() != m.group(1): sys.exit(f'GUARD REFUSED: {f.name} hash mismatch')
    return psha
