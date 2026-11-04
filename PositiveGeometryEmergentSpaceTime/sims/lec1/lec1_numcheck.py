# Precheck (counts only): tables in ar5iv 1405.6488 whose text mentions BE14 and L_i rows.
import subprocess,re,html
t=subprocess.run(["curl","-sL","-m","90","https://ar5iv.labs.arxiv.org/html/1405.6488"],capture_output=True,text=True).stdout
print("page bytes",len(t))
for k,fig in enumerate(re.findall(r'<figure[^>]*ltx_table.*?</figure>',t,re.S)):
    txt=" ".join(html.unescape(re.sub("<[^>]+>"," ",fig)).split())
    cap=re.search(r"Table\s*\d+",txt)
    print(k,cap.group(0) if cap else "?", "BE14" in txt, "numeric tokens:",len(re.findall(r"\d\.\d+",txt)))
