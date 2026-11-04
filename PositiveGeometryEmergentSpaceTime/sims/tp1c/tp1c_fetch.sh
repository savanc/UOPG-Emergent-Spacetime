# Pull ONLY abstracts (prereg cells D1, D2) from arXiv abs pages; title printed to verify identity.
for id in 1103.3694 2005.13302; do
 curl -s -m 60 "https://arxiv.org/abs/$id" | python3 -c '
import sys,re,html;t=sys.stdin.read()
ti=re.search(r"<title>(.*?)</title>",t,re.S); ab=re.search(r"<blockquote class=\"abstract[^>]*>(.*?)</blockquote>",t,re.S)
cl=lambda s:" ".join(html.unescape(re.sub("<[^>]+>","",s)).split())
print("TITLE",cl(ti.group(1)) if ti else "MISSING");print("ABSTRACT",cl(ab.group(1)) if ab else "MISSING");print()'
done
