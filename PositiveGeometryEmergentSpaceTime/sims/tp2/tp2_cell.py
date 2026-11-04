import subprocess,re,html
t=subprocess.run(["curl","-sL","-m","90","https://arxiv.org/html/2506.19596v3"],capture_output=True,text=True).stdout
for fig in re.findall(r'<figure[^>]*ltx_table.*?</figure>',t,re.S):
    txt=" ".join(html.unescape(re.sub("<[^>]+>"," ",fig)).split())
    if re.search(r"Table\s*3[:.]",txt): print("numbers:",re.findall(r"\d\.\d+",txt))
