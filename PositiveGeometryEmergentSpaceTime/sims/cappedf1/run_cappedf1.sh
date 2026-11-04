#!/bin/bash
# CAPPED-FORMAN-1 runner: planted -> broken -> live; 45 min timeout per mode; RSS sampler (kill at 8 GB -> PARTIAL-LIMIT)
cd "$(dirname "$0")"
RID="CAPPEDF1-$(date -u +%Y%m%dT%H%M%SZ)"
M=run_manifest.txt
{ echo "run_id $RID"; echo "start $(date -u +%FT%TZ)"; echo "head $(git rev-parse HEAD)";
  python3 -c "import sys,numpy,scipy,networkx;print('python',sys.version.split()[0],'numpy',numpy.__version__,'scipy',scipy.__version__,'networkx',networkx.__version__)";
  sha256sum cappedf1_checker.py guard.py ../../prereg/CAPPED-FORMAN-1-capped-forman-equality-2026-10-31.md;
  echo "seeds: SEED=20261031 (unused globally); rdual seeds 0..119,1000..1059,2000..2039,3000..3015; GA random 4000..4023; truncations 5000..5059";
  echo "cmd: python3 cappedf1_checker.py {planted,broken,live}; timeout 2700 s each; workers 7"; } > $M
PEAK=0
for mode in planted broken live; do
  t0=$(date +%s)
  timeout 2700 python3 cappedf1_checker.py $mode > cappedf1_$mode.log 2>&1 &
  P=$!
  while kill -0 $P 2>/dev/null; do
    R=$(ps -eo rss,cmd | awk '/cappedf1_checker.py/ && !/awk/ {s+=$1} END {print s+0}')
    [ "$R" -gt "$PEAK" ] && PEAK=$R
    if [ "$R" -gt 8388608 ]; then pkill -f cappedf1_checker.py; echo "PARTIAL-LIMIT memory $mode" >> $M; fi
    sleep 2
  done
  wait $P; rc=$?
  echo "$mode exit $rc secs $(( $(date +%s) - t0 ))" >> $M
  [ $mode = live ] && echo "$RID live wall seconds $(( $(date +%s) - t0 ))" > live_time.txt
done
echo "peak_rss_kb $PEAK" >> $M
echo "end $(date -u +%FT%TZ)" >> $M
sha256sum cappedf1_planted.json cappedf1_broken.json cappedf1_live.json cappedf1_*.log > result_sha256.txt
echo "$RID done"
