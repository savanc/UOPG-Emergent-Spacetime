"""Post-run timing probe (not a scoring function): re-check each certificate by kernel decide in a
standalone file importing PositiveGeometryEmergentSpaceTime.LeanCert; records wall time and the profiler's type-checking time."""
import subprocess, time, re, json, os, resource
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lean'))
out = {}
for tag in ['gpos', 'abhy5', 'abhy6', 'abhy7']:
    src = f"""import PositiveGeometryEmergentSpaceTime.LeanCert
open PositiveGeometryEmergentSpaceTime.LeanCert
set_option maxRecDepth 100000 in
example : checkZero {tag}_M {tag}_K = true ∧ checkSplit {tag}_P {tag}_M {tag}_K {tag}_Q {tag}_d = true ∧
    checkInj {tag}_Q {tag}_K {tag}_d = true := by decide +kernel
"""
    fn = f'/tmp/lcprobe/{tag}.lean'; open(fn, 'w').write(src)
    reps = []
    for r in range(3):
        t = time.time()
        p = subprocess.run(['lake', 'env', 'lean', '-Dprofiler=true', '-Dprofiler.threshold=1', fn], capture_output=True, text=True)
        w = time.time() - t
        tc = re.findall(r'^\s*type checking ([\d.]+)(ms|s)', p.stdout + p.stderr, re.M)
        tcs = sum(float(v) / (1000 if u == 'ms' else 1) for v, u in tc)
        reps.append({'exit': p.returncode, 'wall_s': round(w, 2), 'type_checking_s': round(tcs, 3)})
    out[tag] = reps
out['peak_rss_children_gb'] = round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024**2, 3)
print(json.dumps(out, indent=1))
