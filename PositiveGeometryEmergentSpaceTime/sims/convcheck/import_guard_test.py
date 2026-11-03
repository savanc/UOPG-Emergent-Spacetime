"""Import/CLI refusal test: before the prereg is on origin/main, importing and calling any scoring function must exit."""
import subprocess, sys
for mode in ('planted', 'live'):
    r = subprocess.run([sys.executable, sys.argv[1], mode], capture_output=True, text=True)
    print(mode, 'rc', r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:])
