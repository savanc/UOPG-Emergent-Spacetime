# Pre-prereg check: do target abstracts contain numbers? Prints only title + counts of numeric tokens, never text.
import subprocess,re,html
for aid in ["2205.12293","2002.11761"]:
    t=subprocess.run(["curl","-s","-m","60",f"https://arxiv.org/abs/{aid}"],capture_output=True,text=True).stdout
    ti=re.search(r"<title>(.*?)</title>",t,re.S).group(1); ab=re.search(r'<blockquote class="abstract[^>]*>(.*?)</blockquote>',t,re.S).group(1)
    ab=html.unescape(re.sub("<[^>]+>","",ab))
    print(" ".join(ti.split()),"| numeric tokens:",len(re.findall(r"\d+\.?\d*",ab)),"| has 'micro'/'μm'/'eV':",bool(re.search(r"micro|μm|\\mu|eV",ab)))
