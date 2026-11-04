# Structure precheck: prints ONLY header row and first-column labels of BE14 tables (no values).
import subprocess,re,html
t=subprocess.run(["curl","-sL","-m","90","https://ar5iv.labs.arxiv.org/html/1405.6488"],capture_output=True,text=True).stdout
cl=lambda s:" ".join(html.unescape(re.sub("<[^>]+>"," ",s)).split())
for k,fig in enumerate(re.findall(r'<figure[^>]*ltx_table.*?</figure>',t,re.S)):
    if "BE14" not in cl(fig): continue
    rows=re.findall(r"<tr.*?</tr>",fig,re.S)
    cells=[re.findall(r"<t[dh].*?</t[dh]>",r,re.S) for r in rows]
    print("table",k,"ncols",[len(c) for c in cells][:3])
    print(" header:",[cl(c) for c in cells[0]])
    print(" labels:",[cl(c[0]) for c in cells[1:] if c])
