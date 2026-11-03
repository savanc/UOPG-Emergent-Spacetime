# TP-1d: pull ONLY pre-registered sentence cells. Full text never printed/saved.
import subprocess,re,tempfile,os
rules={"1103.3694":(lambda s:(("golden" in s) or re.search(r"m_?2\s*/\s*m_?1",s) or "ratio" in s) and re.search(r"\d",s),6),
       "2005.13302":(lambda s:re.search(r"m_|\bm[1-8]\b|ratio|golden",s) and re.search(r"\d\.\d",s),10)}
for aid,(f,mx) in rules.items():
    d=tempfile.mkdtemp(); p=os.path.join(d,"a.pdf")
    subprocess.run(["curl","-sL","-m","120","-o",p,f"https://arxiv.org/pdf/{aid}"],check=True)
    t=subprocess.run(["pdftotext",p,"-"],capture_output=True,text=True).stdout
    t=" ".join(t.split()); sents=[s for s in t.split(". ") if f(s)][:mx]
    print(f"== {aid}: {len(sents)} cells");[print("-",s.strip()[:600]) for s in sents]
