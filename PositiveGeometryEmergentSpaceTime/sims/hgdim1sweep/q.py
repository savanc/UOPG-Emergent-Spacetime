import urllib.request,urllib.parse,re,sys,time
for q in sys.argv[1:]:
    url="https://export.arxiv.org/api/query?"+urllib.parse.urlencode({"search_query":q,"max_results":25})
    s=None
    for k in range(3):
        try: s=urllib.request.urlopen(url,timeout=60).read().decode(); break
        except Exception as e: err=e; time.sleep(6)
    if s is None: print("###",q,"-> ERROR",err); continue
    n=re.search(r"<opensearch:totalResults[^>]*>(\d+)",s).group(1)
    ents=re.findall(r"<entry>.*?<id>(.*?)</id>.*?<title>(.*?)</title>",s,re.S)
    print(f"### {q} -> {n}")
    for i,t in ents: print("  ",i.split('/abs/')[-1]," ".join(t.split()))
    time.sleep(3)
