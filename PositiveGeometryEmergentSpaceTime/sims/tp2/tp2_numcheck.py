# Precheck only: does the figure captioned "Table 3" of arXiv 2506.19596v3 contain numeric cells? Prints counts only.
import subprocess,re,html
t=subprocess.run(["curl","-sL","-m","90","https://arxiv.org/html/2506.19596v3"],capture_output=True,text=True).stdout
for fig in re.findall(r'<figure[^>]*ltx_table.*?</figure>',t,re.S):
    txt=" ".join(html.unescape(re.sub("<[^>]+>"," ",fig)).split())
    if re.search(r"Table\s*3[:.]",txt):
        anns=re.findall(r'<annotation encoding="application/x-tex">(.*?)</annotation>',fig,re.S)
        print("Table 3 found; numeric tokens (text):",len(re.findall(r"\d\.\d+",txt)),"; in TeX annotations:",sum(len(re.findall(r"\d\.\d+",a)) for a in anns))
