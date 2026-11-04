# LEC-1: pull ONLY BE14 column, rows L1-L6, L8, of ar5iv 1405.6488 table (figure index 2). Parses v(err) notation.
import subprocess,re,html,math
t=subprocess.run(["curl","-sL","-m","90","https://ar5iv.labs.arxiv.org/html/1405.6488"],capture_output=True,text=True).stdout
cl=lambda s:" ".join(html.unescape(re.sub("<[^>]+>"," ",s)).split())
fig=re.findall(r'<figure[^>]*ltx_table.*?</figure>',t,re.S)[2]
L={}
for r in re.findall(r"<tr.*?</tr>",fig,re.S):
    c=re.findall(r"<t[dh].*?</t[dh]>",r,re.S)
    m=re.search(r"L_\{(\d)\}\^\{r\}",cl(c[0])) if c else None
    if m and m.group(1) in '1234568':
        txt=cl(c[1]); print(f"L{m.group(1)} BE14 cell:",txt)
        neg='-' in txt.replace('−','-'); mm=re.search(r"(\d+)\.(\d+)(?:\((\d+)\))?",txt)
        v=float(mm.group(1)+'.'+mm.group(2))*(-1 if neg else 1)
        e=int(mm.group(3))*10**-len(mm.group(2)) if mm.group(3) else None
        L[int(m.group(1))]=(v,e)
def rel(name,v,e):
    if e is None: print(f"{name} = {v:+.3f} (fixed, no error: UNSCORABLE)"); return
    print(f"{name} = {v:+.3f} ± {e:.3f}  ({abs(v)/e:.1f}σ)")
q=lambda *xs: None if None in xs else math.sqrt(sum(x*x for x in xs))
rel("L2-2L1",L[2][0]-2*L[1][0],q(L[2][1],2*L[1][1])); rel("L3+2L2",L[3][0]+2*L[2][0],q(L[3][1],2*L[2][1]))
for i in (4,6,5,8): rel(f"L{i}",*L[i])
