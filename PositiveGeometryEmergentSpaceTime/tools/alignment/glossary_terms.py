"""Glossary term list (curated) and locator: first use per paper, and context, for status judgement."""
import re, json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
PAPERS = {"I": "papers/human-agentic-methods-2026-10/tex/main.tex",
          "II": "papers/paper-ii-evidence/tex/main.tex",
          "C": "papers/paper-curvature/main.tex"}
TERMS = [  # (term, regex)
 ("hidden zero", r"hidden[- ]zero"), ("Lovelace--Shapiro amplitude", r"Lovelace|\bLS\b"),
 ("Legendre coefficient / partial-wave coupling", r"Legendre"), ("Adler zero", r"Adler zero"),
 ("kinematic associahedron (ABHY)", r"kinematic associahedron"), ("mass offsets", r"mass offset"),
 ("chamber / wall (offset arrangement)", r"chamber"), ("scale-blind map", r"scale-blind"),
 ("homogeneous of degree k", r"homogeneous"), ("Ising cell / star network", r"star network|Ising cell"),
 ("momentum amplituhedron", r"momentum amplituhedron"), ("colour factor / sign-coherent", r"sign-coherent"),
 ("crossed box (= K_{3,3})", r"crossed[- ]box"), ("pointwise stabiliser", r"pointwise stabili[sz]er"),
 ("exceptional Jordan algebra J_3(O)", r"J_3\(\\mathbb\{O\}\)"), ("baryon triality", r"triality"),
 ("exactness window / anomaly window", r"exactness window"), ("graded positroid / Cartan grading", r"graded"),
 ("anomaly-cancellation conditions (ACC)", r"anomaly[- ]cancellation|N_\{\\rm ACC\}"),
 ("modular fixed point tau=omega", r"\\tau=\\omega"), ("Zee--Babu model", r"Zee"),
 ("colour-ordered amplitude", r"colour-ordered"), ("stage-3 relations", r"stage-3 relation"),
 ("certificate (integer / mod-p)", r"certificate"), ("fusion-rule (WZW) matrix", r"fusion-rule"),
 ("Ollivier--Ricci curvature", r"Ollivier"), ("idleness / lazy random walk", r"idleness|lazy"),
 ("Wasserstein-1 / transport cost W_1", r"W_1|Wasserstein|transport cost"),
 ("Forman curvature kappa_F", r"Forman"), ("p(e): diagonal sides of the flip quadrilateral", r"p\(e\)"),
 ("capped-Forman bound B(e)", r"capped"), ("per-face weight g_k(m)", r"g_k"),
 ("permutohedron P_n / h(e) hexagons", r"permutohedron"), ("LLY curvature kappa_L", r"LLY|Lin--Lu--Yau"),
 ("Hankel / Toeplitz 2x2 minor", r"Toeplitz|Hankel"), ("reflection positivity", r"reflection positiv|reflected"),
 ("flip graph / triangulation / Catalan number", r"flip graph"), ("ear (of a triangulation)", r"\bears?\b"),
 ("blueprint row", r"blueprint row"), ("second formalisation", r"second formali[sz]ation"),
 ("sanity theorem", r"sanity theorem"), ("PROVED tag", r"\\PROVED\{\} means|PROVED\} means|\\PROVED & "),
 ("PAPERPROVED tag", r"PAPERPROVED"), ("SIM tag", r"\\SIM\{\} means|\\SIM & "),
 ("preregistration", r"preregistration"), ("planted control / null", r"planted"),
 ("sorry / standard axioms", r"sorry"), ("rung", r"\brung\b"), ("Birkhoff reduction / Kantorovich duality", r"Birkhoff|Kantorovich"),
 ("RG flow variable u=1/y^2", r"u=1/y\^2"), ("convention re-check", r"convention re-check"),
]
def lines(p): return (ROOT / p).read_text().splitlines()
def locate():
    out = []
    for term, rx in TERMS:
        r = re.compile(rx)
        hits = {}
        for k, p in PAPERS.items():
            L = lines(p); sec = ""
            for i, l in enumerate(L, 1):
                m = re.search(r"\\(sub)*section\*?\{([^}]*)\}|\\paragraph\{([^}]*)\}", l)
                if m: sec = (m.group(2) or m.group(3) or "")[:40]
                if r.search(l) and not l.lstrip().startswith("%"):
                    hits[k] = (i, sec, l.strip()); break
        out.append({"term": term, "rx": rx, "hits": {k: v[:2] for k, v in hits.items()},
                    "ctx": {k: v[2][:400] for k, v in hits.items()}})
    return out
if __name__ == "__main__":
    res = locate()
    json.dump(res, open(ROOT / "tools/alignment/out/glossary_locate.json", "w"), indent=1)
    for r in res:
        print("##", r["term"], r["hits"])
        if "-v" in sys.argv:
            for k, c in r["ctx"].items(): print("  ", k, c[:300])
