# DD-1: pull ONLY abstract sentences containing a digit (prereg cells D1, D2).
import subprocess,re,html
for tag,aid in [("D1","2205.12293"),("D2","2002.11761")]:
    t=subprocess.run(["curl","-s","-m","60",f"https://arxiv.org/abs/{aid}"],capture_output=True,text=True).stdout
    ab=re.search(r'<blockquote class="abstract[^>]*>(.*?)</blockquote>',t,re.S).group(1)
    ab=" ".join(html.unescape(re.sub("<[^>]+>","",ab)).split()).replace("Abstract:","")
    print("==",tag,aid); [print("-",s) for s in re.split(r"(?<=\.)\s+",ab) if re.search(r"\d",s)]
