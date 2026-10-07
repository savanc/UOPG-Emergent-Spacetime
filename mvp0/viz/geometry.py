#!/usr/bin/env python3
"""Exact numerical shadow of the proved identities, and the schematic atlas.

The Lean proofs are the authority. This file recomputes the same identities
in exact rational arithmetic, then draws pictures of them. MVP-0, the orthant
coefficient, the algebraic face residue, and the rank-one rescaling are
checked here. The face sweep is a picture of the residue, not a new claim.
Later rungs are contracts: they say what a later milestone has to prove.
They are not results, and they contain no fitted mass.

Run from anywhere:

    python3 mvp0/viz/geometry.py --check   # stdlib only
    python3 mvp0/viz/geometry.py --write   # also needs Pillow, to redraw
"""

from __future__ import annotations

import argparse
import itertools
import math
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "docs" / "figures"

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

PAPER = (251, 248, 243)
INK = (26, 24, 20)
MUTED = (90, 84, 74)
RULE = (217, 211, 199)
GREEN = (27, 94, 69)
GREEN_BG = (229, 242, 235)
BLUE = (30, 58, 95)
BLUE_BG = (232, 238, 245)
AMBER = (138, 90, 18)
AMBER_BG = (248, 241, 227)
RED = (143, 45, 58)
RED_BG = (248, 232, 232)
WHITE = (255, 255, 255)

PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_NAME = {
    (0, 1): ("P01", "<12>"),
    (0, 2): ("P02", "<13>"),
    (0, 3): ("P03", "<14>"),
    (1, 2): ("P12", "<23>"),
    (1, 3): ("P13", "<24>"),
    (2, 3): ("P23", "<34>"),
}


def q(x: F) -> str:
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def det2(m) -> F:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def plucker(C, i: int, j: int) -> F:
    return C[0][i] * C[1][j] - C[1][i] * C[0][j]


def minors(C) -> dict:
    return {ij: plucker(C, *ij) for ij in PAIRS}


def plucker_quad(C) -> F:
    P = minors(C)
    return P[(0, 1)] * P[(2, 3)] - P[(0, 2)] * P[(1, 3)] + P[(0, 3)] * P[(1, 2)]


def left_mul(g, C):
    """(g C)[a][j], g a 2x2 matrix on the left."""
    rows = []
    for a in range(2):
        rows.append(tuple(g[a][0] * C[0][j] + g[a][1] * C[1][j] for j in range(4)))
    return tuple(rows)


def sub2(x, y):
    return tuple(tuple(x[a][b] - y[a][b] for b in range(2)) for a in range(2))


def angle(u, v) -> F:
    return u[0] * v[1] - u[1] * v[0]


def region_matrix(zp, z):
    """Affine event through two twistors. Same formula as UOPG0.regionMatrix."""
    delta = angle(zp["lam"], z["lam"])
    if delta == 0:
        raise RuntimeError("consecutive angle bracket vanished")
    rows = []
    for a in range(2):
        c0 = (z["lam"][1] * zp["mu"][a] - zp["lam"][1] * z["mu"][a]) / delta
        c1 = (-z["lam"][0] * zp["mu"][a] + zp["lam"][0] * z["mu"][a]) / delta
        rows.append((c0, c1))
    return tuple(rows)


def mat_str(m) -> str:
    return "[[%s, %s], [%s, %s]]" % (q(m[0][0]), q(m[0][1]), q(m[1][0]), q(m[1][1]))


def lightcone_tx(m):
    """Read a diagonal matrix [[u, 0], [0, v]] as u = t+x, v = t-x."""
    u, off, off2, v = m[0][0], m[0][1], m[1][0], m[1][1]
    if off != 0 or off2 != 0:
        raise RuntimeError("light-cone reading requires a diagonal matrix")
    return (u + v) / 2, (u - v) / 2


def gauge_chart(C):
    """Left GL(2) taking columns 0 and 2 to the identity. Returns g, gC, (x,y,z,w)."""
    a, b = C[0][0], C[0][2]
    c, d = C[1][0], C[1][2]
    delta = a * d - b * c
    if delta == 0:
        raise RuntimeError("columns 0 and 2 are dependent; chart unavailable")
    g = ((d / delta, -b / delta), (-c / delta, a / delta))
    gC = left_mul(g, C)
    # Target shape [[1, y, 0, -w], [0, x, 1, z]].
    x, y, z, w = gC[1][1], gC[0][1], gC[1][3], -gC[0][3]
    return g, gC, (x, y, z, w)


def outer(u, v):
    return tuple(tuple(u[a] * v[b] for b in range(2)) for a in range(2))


def factor_rank1(m):
    """Exhibit m = u v^T. Exists for every 2x2 matrix with det 0."""
    if det2(m) != 0:
        raise RuntimeError("not singular")
    col0 = (m[0][0], m[1][0])
    col1 = (m[0][1], m[1][1])
    if col0 != (0, 0):
        # col1 = v1/v0 * col0 if v0 != 0; take u = col0, v = (1, ratio)
        if col0[0] != 0:
            ratio = col1[0] / col0[0]
        else:
            ratio = col1[1] / col0[1]
        u, v = col0, (F(1), ratio)
    elif col1 != (0, 0):
        u, v = col1, (F(0), F(1))
    else:
        u, v = (F(0), F(0)), (F(0), F(0))
    if outer(u, v) != m:
        raise RuntimeError("rank-one factorisation failed")
    return u, v


def build_shadow() -> dict:
    C = ((F(1), F(1), F(1), F(1)), (F(0), F(1), F(2), F(3)))
    P = minors(C)
    residual = plucker_quad(C)
    if residual != 0:
        raise RuntimeError("witness fails the Plücker relation")
    expected = {
        (0, 1): F(1),
        (0, 2): F(2),
        (0, 3): F(3),
        (1, 2): F(1),
        (1, 3): F(2),
        (2, 3): F(1),
    }
    if P != expected:
        raise RuntimeError(f"witness minors drifted: {P}")
    if any(v <= 0 for v in P.values()):
        raise RuntimeError("witness is not positive")

    g_chart, gC, chart = gauge_chart(C)
    x, y, z, w = chart
    if gC != ((F(1), y, F(0), -w), (F(0), x, F(1), z)):
        raise RuntimeError("gauge-fixed matrix is not in the positive chart")
    if min(x, y, z, w) <= 0:
        raise RuntimeError("chart coordinates are not all positive")
    if minors(gC) != {ij: det2(g_chart) * P[ij] for ij in PAIRS}:
        raise RuntimeError("GL(2) weight failed on the gauge element")
    adj = x * y * z * w
    if adj != F(3, 16):
        raise RuntimeError(f"chart adjacent product drifted: {adj}")
    orthant = F(1) / adj
    if orthant != F(16, 3):
        raise RuntimeError(f"orthant coefficient drifted: {orthant}")
    cyclic = -adj
    parke = F(1) / cyclic
    if parke != -orthant or parke != F(-16, 3):
        raise RuntimeError(f"Parke-Taylor coefficient drifted: {parke}")
    if x * y * z * w * orthant != 1:
        raise RuntimeError("algebraic residue is not 1")
    adj_C = P[(0, 1)] * P[(1, 2)] * P[(2, 3)] * P[(0, 3)]
    if det2(g_chart) ** 4 * adj_C != adj:
        raise RuntimeError("GL(2) weight of the adjacent product failed")

    # Algebraic face. Dropping one coordinate cancels it. P13 is not a wall.
    drop_x, drop_y, drop_z, drop_w = x * orthant, y * orthant, z * orthant, w * orthant
    if drop_x != 1 / (y * z * w) or drop_x != F(8, 3):
        raise RuntimeError(f"drop-x residue drifted: {drop_x}")
    if drop_y != 1 / (x * z * w) or drop_y != F(8, 3):
        raise RuntimeError(f"drop-y residue drifted: {drop_y}")
    if drop_z != 1 / (x * y * w) or drop_z != F(8):
        raise RuntimeError(f"drop-z residue drifted: {drop_z}")
    if drop_w != 1 / (x * y * z) or drop_w != F(8, 3):
        raise RuntimeError(f"drop-w residue drifted: {drop_w}")

    def p13(a, b, c, d):
        return b * c + a * d

    face_p13 = p13(F(0), y, z, w)
    if face_p13 != F(3, 4):
        raise RuntimeError(f"P13 on the x=0 face drifted: {face_p13}")
    if not (
        p13(F(0), y, z, w) > 0
        and p13(x, F(0), z, w) > 0
        and p13(x, y, F(0), w) > 0
        and p13(x, y, z, F(0)) > 0
    ):
        raise RuntimeError("P13 vanished on a codimension-1 face")
    off_p13 = p13(F(1), F(1), F(-1), F(1))
    off_prod = F(1) * F(1) * F(-1) * F(1)
    if off_p13 != 0 or off_prod == 0 or off_prod != F(-1):
        raise RuntimeError("off-chamber P13 counterexample drifted")

    # Finite exact ensemble. No floats, no seed, no fit.
    sl_n = gl_n = 0
    for entries in itertools.product((F(-1), F(0), F(1), F(2)), repeat=4):
        g = (entries[0:2], entries[2:4])
        delta = det2(g)
        if delta == 0:
            continue
        got = minors(left_mul(g, C))
        if got != {ij: delta * P[ij] for ij in PAIRS}:
            raise RuntimeError(f"GL(2) weight failed for {g}")
        if delta == 1:
            sl_n += 1
        else:
            gl_n += 1
    show_sl = ((F(1), F(3)), (F(0), F(1)))
    show_gl = ((F(2), F(0)), (F(0), F(1)))
    if det2(show_sl) != 1 or minors(left_mul(show_sl, C)) != P:
        raise RuntimeError("displayed SL(2) sample is wrong")
    if minors(left_mul(show_gl, C)) != {ij: F(2) * P[ij] for ij in PAIRS}:
        raise RuntimeError("displayed GL(2) sample is wrong")

    # Rational twistor polygon. Events come out of regionMatrix, not a drawing.
    Z = (
        {"lam": (F(0), F(1)), "mu": (F(0), F(0))},
        {"lam": (F(1), F(0)), "mu": (F(2), F(0))},
        {"lam": (F(0), F(1)), "mu": (F(0), F(2))},
        {"lam": (F(1), F(0)), "mu": (F(0), F(0))},
    )
    events = []
    brackets = []
    for i in range(4):
        prev, tw = Z[(i - 1) % 4], Z[i]
        delta = angle(prev["lam"], tw["lam"])
        brackets.append(delta)
        if delta == 0:
            raise RuntimeError("a consecutive angle bracket vanished")
        events.append(region_matrix(prev, tw))
    momenta = [sub2(events[i], events[(i + 1) % 4]) for i in range(4)]
    total = (
        (
            sum(p[0][0] for p in momenta),
            sum(p[0][1] for p in momenta),
        ),
        (
            sum(p[1][0] for p in momenta),
            sum(p[1][1] for p in momenta),
        ),
    )
    if total != ((F(0), F(0)), (F(0), F(0))):
        raise RuntimeError("edge momenta do not sum to zero")
    factors = []
    for i, p in enumerate(momenta):
        if det2(p) != 0:
            raise RuntimeError(f"edge {i} is not null")
        # Lean's edge kills λ_i.
        lam = Z[i]["lam"]
        image = (
            p[0][0] * lam[0] + p[0][1] * lam[1],
            p[1][0] * lam[0] + p[1][1] * lam[1],
        )
        if image != (F(0), F(0)):
            raise RuntimeError(f"edge {i} does not kill its spinor")
        u, v = factor_rank1(p)
        # Opposite rescaling leaves the outer product fixed. Lemma, not a helicity.
        t = F(2)
        if outer(tuple(t * c for c in u), tuple(c / t for c in v)) != p:
            raise RuntimeError("little-group rescaling moved the momentum")
        factors.append((u, v))
    expected_factors = (
        ((F(-2), F(0)), (F(1), F(0))),
        ((F(0), F(-2)), (F(0), F(1))),
        ((F(2), F(0)), (F(1), F(0))),
        ((F(0), F(2)), (F(0), F(1))),
    )
    if factors != list(expected_factors):
        raise RuntimeError(f"edge factors drifted from the Lean witness: {factors}")
    tx = [lightcone_tx(e) for e in events]

    # Face sweep of the proved residue. y, z, w stay at the witness.
    # x * 1/(x y z w) = 1/(y z w) = 8/3 for every positive sample.
    # P13 = y z + x w stays positive. x = 0 is the wall, not a sample of the coefficient.
    sweep_x = (F(1, 8), F(1, 4), F(1, 2), F(1), F(3, 2), F(2), F(3))
    sweep = []
    for xs in sweep_x:
        prod = xs * y * z * w
        coeff = F(1) / prod
        residue = xs * coeff
        p13s = p13(xs, y, z, w)
        if residue != F(1) / (y * z * w) or residue != drop_x:
            raise RuntimeError(f"sweep residue drifted at x={xs}: {residue}")
        if p13s <= 0:
            raise RuntimeError(f"sweep P13 is not positive at x={xs}: {p13s}")
        # The adjacent product scales exactly with x. No division: prod * x = xs * adj.
        if prod * x != xs * adj:
            raise RuntimeError(f"sweep product drifted at x={xs}: {prod}")
        sweep.append((xs, prod, coeff, residue, p13s))
    if F(0) * y * z * w != 0:
        raise RuntimeError("the x=0 wall is not a zero of the product")

    # Column shift is not the cluster exchange. One rational point, labeled as such.
    shifted_col = tuple(C[a][3] + C[a][1] + C[a][2] for a in range(2))
    shifted = (
        (C[0][0], C[0][1], C[0][2], shifted_col[0]),
        (C[1][0], C[1][1], C[1][2], shifted_col[1]),
    )
    Ps = minors(shifted)
    if plucker_quad(shifted) != 0:
        raise RuntimeError("a 2-plane left the quadric; that should be impossible")
    if Ps[(2, 3)] != 0:
        raise RuntimeError("expected this column shift to hit the P23 = 0 wall")

    # Exchange identity is the Plücker relation, rearranged. Proved, not fitted.
    exchange_left = P[(0, 2)] * P[(1, 3)]
    exchange_right = P[(0, 1)] * P[(2, 3)] + P[(0, 3)] * P[(1, 2)]
    if exchange_left != exchange_right:
        raise RuntimeError("exchange identity failed on the witness")

    return {
        "C": C,
        "P": P,
        "residual": residual,
        "g_chart": g_chart,
        "chart": chart,
        "orthant": orthant,
        "parke": parke,
        "adjacent_chart": adj,
        "drop_x": drop_x,
        "drop_y": drop_y,
        "drop_z": drop_z,
        "drop_w": drop_w,
        "face_p13": face_p13,
        "off_product": off_prod,
        "sl_n": sl_n,
        "gl_n": gl_n,
        "show_sl": show_sl,
        "show_gl": show_gl,
        "sl_minors": minors(left_mul(show_sl, C)),
        "gl_minors": minors(left_mul(show_gl, C)),
        "Z": Z,
        "events": events,
        "tx": tx,
        "brackets": brackets,
        "momenta": momenta,
        "factors": factors,
        "sweep": sweep,
        "shifted_minors": Ps,
        "exchange": (exchange_left, exchange_right),
    }


def shadow_text(s: dict) -> str:
    lines = [
        "UOPG exact shadow",
        "arithmetic: rational",
        "authority: Lean theorems in mvp0/DICTIONARY.md, mvp1/DICTIONARY.md, mvp2/DICTIONARY.md, and lemma/DICTIONARY.md",
        "no fitted scale",
        "",
        "witness rows (1 1 1 1) and (0 1 2 3)",
    ]
    for ij in PAIRS:
        lean, phys = PAIR_NAME[ij]
        lines.append(f"  {lean} = {phys} = {q(s['P'][ij])}")
    lines.append(f"plucker residual P01*P23 - P02*P13 + P03*P12 = {q(s['residual'])}")
    x, y, z, w = s["chart"]
    lines.append(
        "positive chart after left GL(2): "
        f"x={q(x)} y={q(y)} z={q(z)} w={q(w)}"
    )
    lines.append(
        "orthant coefficient 1/(x*y*z*w) = " + q(s["orthant"])
    )
    lines.append(
        "Parke-Taylor coefficient 1/cyclic = " + q(s["parke"])
    )
    lines.append("cyclic product = -(x*y*z*w); angle <41> = -P03")
    lines.append("residue x*y*z*w*(orthant coefficient) = 1")
    lines.append("face residue drop x = " + q(s["drop_x"]))
    lines.append("face residue drop y = " + q(s["drop_y"]))
    lines.append("face residue drop z = " + q(s["drop_z"]))
    lines.append("face residue drop w = " + q(s["drop_w"]))
    lines.append("P13 on the face x=0 is " + q(s["face_p13"]))
    lines.append("off chamber, P13 = 0 while x*y*z*w = " + q(s["off_product"]))
    lines.append(f"SL(2) samples with det 1, minors unchanged: {s['sl_n']}")
    lines.append(f"GL(2) samples with det != 0,1, minors scaled by det: {s['gl_n']}")
    lines.append("polygon events in the reading u=t+x, v=t-x, det=t^2-x^2")
    for i, (t, xcoord) in enumerate(s["tx"]):
        lines.append(f"  x{i} (t,x)=({q(t)},{q(xcoord)}) matrix {mat_str(s['events'][i])}")
    for i, p in enumerate(s["momenta"]):
        lines.append(f"  p{i} = x{i}-x{(i + 1) % 4} = {mat_str(p)} det={q(det2(p))}")
    lines.append("sum of p_i = 0")
    lines.append("rank-one factors; rescaling by t=2 fixes each edge")
    for i, (u, v) in enumerate(s["factors"]):
        lines.append(
            "  edge %s u=(%s, %s) v=(%s, %s)"
            % (i, q(u[0]), q(u[1]), q(v[0]), q(v[1]))
        )
    lines.append(
        "face sweep, y and z and w fixed at the witness; x*coeff stays "
        + q(s["drop_x"])
        + " and P13 stays positive"
    )
    for xs, prod, coeff, residue, p13s in s["sweep"]:
        lines.append(
            "  x=%s product=%s coeff=%s x*coeff=%s P13=%s"
            % (q(xs), q(prod), q(coeff), q(residue), q(p13s))
        )
    lines.append("at x=0 the product is 0 and P13 = " + q(s["face_p13"]))
    lines.append("column shift at lambda=1 sends P23 from 1 to " + q(s["shifted_minors"][(2, 3)]))
    lines.append("exchange <13><24> = <12><34> + <14><23> = " + q(s["exchange"][0]))
    lines.append("")
    return "\n".join(lines) + "\n"


# --- drawing ---------------------------------------------------------------

_FONTS: dict = {}


def font(kind: str, size: int):
    from PIL import ImageFont

    key = (kind, size)
    if key not in _FONTS:
        path = {"sans": SANS, "bold": SANSB, "serif": SERIFB, "mono": MONO}[kind]
        _FONTS[key] = ImageFont.truetype(path, size)
    return _FONTS[key]


def hex_rgb(c) -> str:
    return "#{:02x}{:02x}{:02x}".format(*c)


class Fig:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.ops = []

    def rect(self, x, y, w, h, fill, stroke=None, sw=1, rx=0):
        self.ops.append(("rect", x, y, w, h, fill, stroke, sw, rx))

    def line(self, x1, y1, x2, y2, stroke, sw=1.5):
        self.ops.append(("line", x1, y1, x2, y2, stroke, sw, None))

    def dash(self, x1, y1, x2, y2, stroke, sw=1.5, pattern=(6, 5)):
        self.ops.append(("line", x1, y1, x2, y2, stroke, sw, pattern))

    def poly(self, pts, fill, stroke=None, sw=1.5):
        self.ops.append(("poly", pts, fill, stroke, sw))

    def circle(self, cx, cy, r, fill, stroke=None, sw=1):
        self.ops.append(("circle", cx, cy, r, fill, stroke, sw))

    def text(self, x, y, s, size=15, fill=INK, anchor="start", kind="sans"):
        self.ops.append(("text", x, y, s, size, fill, anchor, kind))

    def arrow(self, x1, y1, x2, y2, stroke, sw=1.8, head=9):
        self.line(x1, y1, x2, y2, stroke, sw)
        ang = math.atan2(y2 - y1, x2 - x1)
        a1 = ang + 2.6
        a2 = ang - 2.6
        pts = [
            (x2, y2),
            (x2 + head * math.cos(a1), y2 + head * math.sin(a1)),
            (x2 + head * math.cos(a2), y2 + head * math.sin(a2)),
        ]
        self.poly(pts, stroke, None, 0)

    def save(self, stem: str):
        FIG.mkdir(parents=True, exist_ok=True)
        self._png(FIG / f"{stem}.png")
        self._svg(FIG / f"{stem}.svg")

    def _png(self, path: Path, scale: int = 2):
        from PIL import Image, ImageDraw

        im = Image.new("RGB", (self.w * scale, self.h * scale), PAPER)
        dr = ImageDraw.Draw(im)
        S = scale
        for op in self.ops:
            kind = op[0]
            if kind == "rect":
                _, x, y, w, h, fill, stroke, sw, rx = op
                box = [x * S, y * S, (x + w) * S, (y + h) * S]
                dr.rounded_rectangle(
                    box,
                    radius=rx * S,
                    fill=fill,
                    outline=stroke,
                    width=max(1, int(sw * S)) if stroke else 0,
                )
            elif kind == "line":
                _, x1, y1, x2, y2, stroke, sw, pattern = op
                if pattern is None:
                    dr.line(
                        [(x1 * S, y1 * S), (x2 * S, y2 * S)],
                        fill=stroke,
                        width=max(1, int(round(sw * S))),
                    )
                else:
                    self._dash(dr, x1, y1, x2, y2, stroke, sw, pattern, S)
            elif kind == "poly":
                _, pts, fill, stroke, sw = op
                xy = [(p[0] * S, p[1] * S) for p in pts]
                dr.polygon(xy, fill=fill, outline=stroke)
            elif kind == "circle":
                _, cx, cy, r, fill, stroke, sw = op
                box = [(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S]
                dr.ellipse(
                    box,
                    fill=fill,
                    outline=stroke,
                    width=max(1, int(sw * S)) if stroke else 0,
                )
            elif kind == "text":
                _, x, y, s, size, fill, anchor, fkind = op
                pil_anchor = {"start": "ls", "middle": "ms", "end": "rs"}[anchor]
                dr.text(
                    (x * S, y * S),
                    s,
                    font=font(fkind, size * S),
                    fill=fill,
                    anchor=pil_anchor,
                )
        im.save(path, "PNG")

    @staticmethod
    def _dash(dr, x1, y1, x2, y2, stroke, sw, pattern, S):
        length = math.hypot(x2 - x1, y2 - y1)
        if length == 0:
            return
        ux, uy = (x2 - x1) / length, (y2 - y1) / length
        dash, gap = pattern
        t = 0.0
        on = True
        while t < length:
            step = dash if on else gap
            t2 = min(length, t + step)
            if on:
                dr.line(
                    [((x1 + ux * t) * S, (y1 + uy * t) * S), ((x1 + ux * t2) * S, (y1 + uy * t2) * S)],
                    fill=stroke,
                    width=max(1, int(round(sw * S))),
                )
            on = not on
            t = t2

    def _svg(self, path: Path):
        bits = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">',
            f'<rect width="100%" height="100%" fill="{hex_rgb(PAPER)}"/>',
        ]
        family = {
            "sans": "DejaVu Sans, Liberation Sans, sans-serif",
            "bold": "DejaVu Sans, Liberation Sans, sans-serif",
            "serif": "DejaVu Serif, Liberation Serif, serif",
            "mono": "DejaVu Sans Mono, Liberation Mono, monospace",
        }
        for op in self.ops:
            kind = op[0]
            if kind == "rect":
                _, x, y, w, h, fill, stroke, sw, rx = op
                stroke_attr = (
                    f' stroke="{hex_rgb(stroke)}" stroke-width="{sw}"' if stroke else ""
                )
                bits.append(
                    f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                    f'fill="{hex_rgb(fill)}"{stroke_attr}/>'
                )
            elif kind == "line":
                _, x1, y1, x2, y2, stroke, sw, pattern = op
                dash = f' stroke-dasharray="{pattern[0]} {pattern[1]}"' if pattern else ""
                bits.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{hex_rgb(stroke)}" stroke-width="{sw}"{dash}/>'
                )
            elif kind == "poly":
                _, pts, fill, stroke, sw = op
                points = " ".join(f"{p[0]},{p[1]}" for p in pts)
                fill_s = hex_rgb(fill) if fill else "none"
                stroke_attr = (
                    f' stroke="{hex_rgb(stroke)}" stroke-width="{sw}"' if stroke else ""
                )
                bits.append(f'<polygon points="{points}" fill="{fill_s}"{stroke_attr}/>')
            elif kind == "circle":
                _, cx, cy, r, fill, stroke, sw = op
                stroke_attr = (
                    f' stroke="{hex_rgb(stroke)}" stroke-width="{sw}"' if stroke else ""
                )
                bits.append(
                    f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{hex_rgb(fill)}"{stroke_attr}/>'
                )
            elif kind == "text":
                _, x, y, s, size, fill, anchor, fkind = op
                weight = ' font-weight="700"' if fkind in ("bold", "serif") else ""
                bits.append(
                    f'<text x="{x}" y="{y}" fill="{hex_rgb(fill)}" font-size="{size}" '
                    f'font-family="{family[fkind]}" text-anchor="{anchor}"{weight}>'
                    f"{_xml(s)}</text>"
                )
        bits.append("</svg>")
        path.write_text("\n".join(bits) + "\n", encoding="utf-8")


def _xml(s: str) -> str:
    return s.replace("&", "&").replace("<", "<").replace(">", ">")


def footer(fig: Fig, y: int, proved: bool, word: str | None = None):
    if word is None:
        word = "proved identities only" if proved else "contract, not a theorem"
    fig.text(
        28,
        y,
        f"UOPG atlas  ·  {word}  ·  python3 mvp0/viz/geometry.py",
        size=12,
        fill=MUTED,
        kind="sans",
    )


def status_pill(fig: Fig, x: int, y: int, proved: bool):
    label = "PROVED" if proved else "CONTRACT"
    bg, fg = (GREEN, WHITE) if proved else (AMBER, WHITE)
    w = 92 if proved else 112
    fig.rect(x, y, w, 22, bg, rx=11)
    fig.text(x + w / 2, y + 16, label, size=12, fill=WHITE, anchor="middle", kind="bold")


def frame(fig: Fig, proved: bool, title: str, subtitle: str):
    fig.rect(0, 0, fig.w, 8, GREEN if proved else AMBER)
    fig.text(28, 46, title, size=26, fill=INK, kind="serif")
    fig.text(28, 72, subtitle, size=14, fill=MUTED, kind="sans")
    status_pill(fig, fig.w - 28 - (92 if proved else 112), 30, proved)


def draw_ladder(_s: dict):
    fig = Fig(960, 1040)
    frame(
        fig,
        False,
        "What each rung is",
        "One object, Gr+(2,4). Green is checked in Lean. Amber is the job, not a result.",
    )
    # The ladder as a whole is mixed, so the corner pill says CONTRACT would be wrong
    # for rung 0. Replace the corner pill with a quieter label by overpainting.
    fig.rect(960 - 28 - 112, 26, 120, 30, PAPER)
    fig.text(932, 46, "atlas", size=14, fill=MUTED, anchor="end", kind="bold")

    cards = [
        (
            True,
            "MVP-0",
            "det = 0 is the theorem, not a boson",
            [
                "An event is a 2-plane. An edge has det = 0.",
                "The four edges sum to 0.",
            ],
            "Lean: plucker_relation, pairing_graph, the two edge theorems",
        ),
        (
            True,
            "MVP-1",
            "Orthant coefficient",
            [
                "The positive gauge lands in the orthant.",
                "1/(xyzw) equals 1 over the adjacent product.",
            ],
            "Proved in Lean. A 4-form and a cross section are not.",
        ),
        (
            True,
            "MVP-2",
            "Algebraic face residue",
            [
                "Denominator zero iff an adjacent minor is.",
                "Dropping one coordinate leaves 1 over the other three.",
            ],
            "Proved in Lean. Not a cross section, and not a mutation.",
        ),
        (
            False,
            "MVP-3",
            "One measured mass in, one ratio out",
            [
                "No GeV inside the conformal geometry.",
                "At most one external mass. The ratio is unknown.",
            ],
            "A second scale or a fit voids the milestone.",
        ),
        (
            False,
            "MVP-4",
            "Helicity from the two SL(2)s",
            [
                "The outer product and the rescaling are proved.",
                "The helicity weight is not.",
            ],
            "Lemma only. This card stays a contract.",
        ),
    ]
    top = 100
    for i, (proved, name, title, body, meta) in enumerate(cards):
        y = top + i * 168
        bg = GREEN_BG if proved else AMBER_BG
        edge = GREEN if proved else AMBER
        fig.rect(72, y, 620, 152, bg, stroke=edge, sw=1.5, rx=12)
        fig.circle(44, y + 76, 8, edge)
        if i < len(cards) - 1:
            fig.line(44, y + 88, 44, y + 168, RULE, 2)
        fig.text(92, y + 32, name, size=13, fill=edge, kind="bold")
        fig.text(168, y + 32, title, size=18, fill=INK, kind="serif")
        fig.text(92, y + 68, body[0], size=14, fill=INK)
        fig.text(92, y + 90, body[1], size=14, fill=INK)
        fig.text(92, y + 122, meta, size=13, fill=MUTED)

    fig.rect(712, 100, 220, 392, RED_BG, stroke=RED, sw=1.5, rx=12)
    fig.text(724, 128, "Not a theorem", size=14, fill=RED, kind="bold")
    refused = [
        "Hessian of sum log|det|",
        "that scalar as a metric",
        "the lambda column update",
        "calling that update a mutation",
        "any W, Z, or Higgs mass",
        "sin^2 of the weak angle",
        "a GeV from this geometry",
    ]
    for i, line in enumerate(refused):
        fig.text(724, 162 + i * 28, line, size=13, fill=INK)
    fig.rect(712, 512, 220, 150, BLUE_BG, stroke=BLUE, sw=1.5, rx=12)
    fig.text(724, 540, "Only comparison", size=14, fill=BLUE, kind="bold")
    fig.text(724, 572, "Mass from det is 0.", size=13, fill=INK)
    fig.text(724, 596, "Compared, not fitted,", size=13, fill=INK)
    fig.text(724, 620, "to the PDG photon", size=13, fill=INK)
    fig.text(724, 644, "bound. See EMPIRICAL.", size=13, fill=INK)
    footer(fig, 1010, False, "green is proved, amber is not")
    fig.save("mvp-ladder")


def draw_klein(s: dict):
    fig = Fig(960, 720)
    frame(
        fig,
        True,
        "MVP-0  ·  one 2-plane, three pictures",
        "Same witness as positiveExample in UOPG0.Basic. Numbers below are computed, then checked.",
    )
    panels = [
        (28, "2-plane", GREEN),
        (340, "Plucker point", GREEN),
        (652, "Affine event", GREEN),
    ]
    for x, title, col in panels:
        fig.rect(x, 100, 292, 500, WHITE, stroke=RULE, sw=1.4, rx=12)
        fig.text(x + 18, 132, title, size=16, fill=col, kind="bold")
    fig.arrow(312, 330, 338, 330, GREEN, sw=1.6, head=8)
    fig.arrow(624, 330, 650, 330, GREEN, sw=1.6, head=8)

    # Panel 1: a plane spanned by two arrows, then the matrix.
    ox, oy = 118, 250
    v = (108, -18)
    w = (36, -78)
    quad = [
        (ox, oy),
        (ox + v[0], oy + v[1]),
        (ox + v[0] + w[0], oy + v[1] + w[1]),
        (ox + w[0], oy + w[1]),
    ]
    fig.poly(quad, GREEN_BG, GREEN, 1.6)
    fig.arrow(ox, oy, ox + v[0], oy + v[1], BLUE, sw=2.2, head=9)
    fig.arrow(ox, oy, ox + w[0], oy + w[1], RED, sw=2.2, head=9)
    fig.text(ox + v[0] - 8, oy + v[1] + 22, "row 0", size=13, fill=BLUE, kind="bold")
    fig.text(ox + w[0] - 36, oy + w[1] - 8, "row 1", size=13, fill=RED, kind="bold")
    fig.text(46, 390, "Witness, the Lean point", size=13, fill=MUTED)
    fig.text(46, 418, "|  1   1   1   1  |", size=16, fill=INK, kind="mono")
    fig.text(46, 442, "|  0   1   2   3  |", size=16, fill=INK, kind="mono")
    fig.text(46, 478, "Rows span one plane in k^4.", size=13, fill=INK)
    fig.text(46, 502, "Not a metric. Not a mass.", size=13, fill=INK)
    fig.text(46, 536, "dim k(n-k) = 4 is why this", size=13, fill=MUTED)
    fig.text(46, 558, "can be a spacetime. That", size=13, fill=MUTED)
    fig.text(46, 580, "count is not itself a theorem.", size=13, fill=MUTED)

    # Panel 2: six minors and the quadratic.
    fig.text(358, 168, "Six ordered minors", size=13, fill=MUTED)
    for i, ij in enumerate(PAIRS):
        lean, phys = PAIR_NAME[ij]
        fig.text(358, 200 + i * 28, f"{lean}  {phys}", size=15, fill=INK, kind="mono")
        fig.text(560, 200 + i * 28, q(s["P"][ij]), size=15, fill=GREEN, anchor="end", kind="mono")
    fig.rect(358, 372, 250, 78, GREEN_BG, rx=8)
    fig.text(372, 398, "P01 P23 - P02 P13 + P03 P12", size=12, fill=INK, kind="mono")
    fig.text(372, 426, f"= {q(s['residual'])}    for this point", size=14, fill=GREEN, kind="bold")
    fig.text(358, 478, "The same quadratic is 0 for", size=13, fill=INK)
    fig.text(358, 500, "every 2x4 matrix. That is", size=13, fill=INK)
    fig.text(358, 522, "plucker_relation, not a fit.", size=13, fill=INK)
    fig.text(358, 556, "All six minors are positive.", size=13, fill=GREEN, kind="bold")
    fig.text(358, 578, "positiveExample_minors_pos", size=12, fill=MUTED, kind="mono")

    # Panel 3: graph and null separation.
    fig.text(670, 168, "Graph of a 2x2 map x", size=13, fill=MUTED)
    fig.text(670, 200, "| 1  0  |  x00  x10 |", size=13, fill=INK, kind="mono")
    fig.text(670, 222, "| 0  1  |  x01  x11 |", size=13, fill=INK, kind="mono")
    fig.text(670, 258, "Plucker bilinear of two", size=13, fill=INK)
    fig.text(670, 278, "graphs equals det(x - y).", size=13, fill=INK)
    fig.rect(670, 304, 250, 64, GREEN_BG, rx=8)
    fig.text(684, 330, "pairing = 0", size=15, fill=GREEN, kind="bold")
    fig.text(684, 352, "exactly when det(x-y) = 0", size=13, fill=INK)
    fig.text(670, 394, "Over a field, det = 0 means", size=13, fill=INK)
    fig.text(670, 416, "the two events share a", size=13, fill=INK)
    fig.text(670, 438, "nonzero direction.", size=13, fill=INK)
    fig.text(670, 472, "nullSeparation_iff", size=12, fill=MUTED, kind="mono")
    fig.text(670, 492, "singular_iff_exists_kernel", size=12, fill=MUTED, kind="mono")
    fig.text(670, 528, "On a diagonal matrix,", size=13, fill=MUTED)
    fig.text(670, 550, "det = u v. Set u = t+x,", size=13, fill=MUTED)
    fig.text(670, 572, "v = t-x. Then det = t^2-x^2.", size=13, fill=MUTED)
    footer(fig, 692, True)
    fig.save("mvp0-klein")


def draw_polygon(s: dict):
    fig = Fig(960, 760)
    frame(
        fig,
        True,
        "MVP-0  ·  four events, four null edges",
        "Reconstructed from four twistors by the same formula as regionMatrix. Nothing is fitted.",
    )
    # Plot rectangle.
    L, T, W, H = 36, 108, 500, 500
    fig.rect(L, T, W, H, WHITE, stroke=RULE, sw=1.2, rx=12)
    # Data window: x in [-1.7, 1.7], t in [-0.45, 2.55]
    xmin, xmax = -1.75, 1.75
    tmin, tmax = -0.45, 2.55

    def xy(x, t):
        px = L + 28 + (x - xmin) / (xmax - xmin) * (W - 56)
        py = T + 24 + (tmax - t) / (tmax - tmin) * (H - 56)
        return px, py

    # Axes through the origin.
    o = xy(0, 0)
    fig.arrow(*xy(xmin + 0.15, 0), *xy(xmax - 0.08, 0), MUTED, sw=1.2, head=7)
    fig.arrow(*xy(0, tmin + 0.12), *xy(0, tmax - 0.08), MUTED, sw=1.2, head=7)
    fig.text(xy(xmax - 0.08, 0)[0] - 4, xy(xmax - 0.08, 0)[1] + 18, "x", size=14, fill=MUTED, anchor="end")
    fig.text(xy(0, tmax - 0.05)[0] + 10, xy(0, tmax - 0.05)[1] + 4, "t", size=14, fill=MUTED)
    # Null lines of the origin, clipped to the axis window.
    fig.dash(*xy(-0.35, -0.35), *xy(1.55, 1.55), (186, 168, 140), sw=1.2)
    fig.dash(*xy(-1.55, 1.55), *xy(0.35, -0.35), (186, 168, 140), sw=1.2)
    # Polygon.
    pts = [xy(float(x), float(t)) for t, x in s["tx"]]
    loop = pts + [pts[0]]
    for a, b in zip(loop, loop[1:]):
        fig.line(a[0], a[1], b[0], b[1], GREEN, sw=2.6)
    for i, (px, py) in enumerate(pts):
        fig.circle(px, py, 5.5, GREEN, stroke=WHITE, sw=1.5)
        labels = [(-52, 16), (12, 6), (-8, -12), (-28, 4)]
        dx, dy = labels[i]
        fig.text(px + dx, py + dy, f"x{i}", size=14, fill=INK, kind="bold")
    # Edge names, placed by hand in data coordinates, outside the diamond.
    edge_at = [(0.78, 0.28), (0.78, 1.72), (-0.95, 1.72), (-0.95, 0.32)]
    for i, (x, t) in enumerate(edge_at):
        px, py = xy(x, t)
        fig.text(px, py, f"det p{i}=0", size=12, fill=GREEN, kind="bold")
    fig.text(*xy(-1.55, 2.35), "dashed: light lines of x0", size=12, fill=MUTED)

    # Side panel.
    fig.rect(552, 108, 380, 560, WHITE, stroke=RULE, sw=1.2, rx=12)
    fig.text(570, 138, "Reading of the matrices", size=14, fill=BLUE, kind="bold")
    fig.text(570, 162, "u = t+x,  v = t-x,  det = u v", size=13, fill=INK, kind="mono")
    fig.text(570, 182, "so det = t^2 - x^2 on this slice.", size=13, fill=MUTED)
    for i, ((t, x), ev) in enumerate(zip(s["tx"], s["events"])):
        y = 214 + i * 52
        fig.text(570, y, f"x{i}  (t, x) = ({q(t)}, {q(x)})", size=14, fill=INK, kind="bold")
        fig.text(570, y + 20, mat_str(ev), size=12, fill=MUTED, kind="mono")
    fig.text(570, 430, "Lean edge  p_i = x_i - x_{i+1}", size=13, fill=INK)
    fig.text(570, 452, "Each det is 0. The sum is 0.", size=13, fill=GREEN, kind="bold")
    fig.text(570, 482, "Twistors (lambda | mu), exact", size=13, fill=MUTED)
    for i, Z in enumerate(s["Z"]):
        lam = ",".join(q(c) for c in Z["lam"])
        mu = ",".join(q(c) for c in Z["mu"])
        fig.text(570, 506 + i * 18, f"Z{i}  ({lam})  |  ({mu})", size=12, fill=INK, kind="mono")
    fig.text(570, 590, "Angle brackets of consecutive", size=12, fill=MUTED)
    fig.text(570, 608, "lambda: " + ", ".join(q(b) for b in s["brackets"]), size=12, fill=INK, kind="mono")
    fig.text(570, 630, "Loop 0-1-2-3. Lean p_i points the other way.", size=12, fill=MUTED)
    footer(fig, 734, True)
    fig.save("mvp0-polygon")


def draw_positive(s: dict):
    fig = Fig(960, 640)
    frame(
        fig,
        True,
        "MVP-0  ·  the positive chamber, one point",
        "Left: the six minors of the Lean witness. Right: the same plane in the orthant chart.",
    )
    fig.rect(28, 104, 470, 470, WHITE, stroke=RULE, sw=1.2, rx=12)
    fig.text(46, 136, "Ordered minors, all positive", size=14, fill=GREEN, kind="bold")
    base_x, base_y = 78, 500
    bar_w, gap = 42, 28
    ymax = F(4)
    scale = 300 / float(ymax)
    fig.line(base_x - 10, base_y, base_x + 6 * (bar_w + gap), base_y, INK, 1.4)
    for i, ij in enumerate(PAIRS):
        val = s["P"][ij]
        h = float(val) * scale
        x = base_x + i * (bar_w + gap)
        fig.rect(x, base_y - h, bar_w, h, GREEN)
        fig.text(x + bar_w / 2, base_y - h - 8, q(val), size=14, fill=INK, anchor="middle", kind="bold")
        lean, phys = PAIR_NAME[ij]
        fig.text(x + bar_w / 2, base_y + 22, lean, size=12, fill=INK, anchor="middle", kind="mono")
        fig.text(x + bar_w / 2, base_y + 40, phys, size=12, fill=MUTED, anchor="middle", kind="mono")
    fig.text(46, 168, f"Plucker residual = {q(s['residual'])}", size=13, fill=GREEN, kind="bold")

    fig.rect(514, 104, 418, 470, WHITE, stroke=RULE, sw=1.2, rx=12)
    fig.text(532, 136, "Chart  x, y > 0", size=14, fill=GREEN, kind="bold")
    fig.text(532, 158, "z and w of the witness held fixed", size=13, fill=MUTED)
    # Axes box for x,y in [0, 2].
    ax, ay, aw = 590, 200, 280
    fig.rect(ax, ay, aw, aw, GREEN_BG, stroke=GREEN, sw=1.2)
    x, y, z, w = s["chart"]
    # Map [0,2] onto the square, y up.
    def pt(xc, yc):
        return ax + float(xc) / 2 * aw, ay + (1 - float(yc) / 2) * aw

    px, py = pt(x, y)
    fig.circle(px, py, 6, RED, stroke=WHITE, sw=1.5)
    fig.text(px + 12, py - 4, f"witness ({q(x)}, {q(y)})", size=13, fill=INK, kind="bold")
    fig.text(ax + 4, ay + aw - 6, "0", size=12, fill=MUTED)
    fig.text(ax + aw - 4, ay + aw - 6, "2", size=12, fill=MUTED, anchor="end")
    fig.text(ax + 8, ay + 18, "2", size=12, fill=MUTED)
    fig.text(532, 500, "square is 0 to 2 on x and on y", size=13, fill=MUTED)
    fig.text(532, 524, f"x={q(x)}   y={q(y)}   z={q(z)}   w={q(w)}", size=14, fill=INK, kind="mono")
    fig.text(532, 548, "Left GL(2) with det " + q(det2(s["g_chart"])), size=13, fill=MUTED)
    footer(fig, 614, True)
    fig.save("mvp0-positive")


def draw_gl2(s: dict):
    fig = Fig(960, 560)
    frame(
        fig,
        True,
        "MVP-0  ·  GL(2) weight, SL(2) invariance",
        "P(g C) = (det g) P(C) for every sample below. Exact integers. No Monte Carlo.",
    )
    fig.rect(28, 104, 440, 300, WHITE, stroke=GREEN, sw=1.4, rx=12)
    fig.rect(492, 104, 440, 300, WHITE, stroke=BLUE, sw=1.4, rx=12)
    fig.text(46, 136, "SL(2) sample, det = 1", size=15, fill=GREEN, kind="bold")
    fig.text(510, 136, "GL(2) sample, det = 2", size=15, fill=BLUE, kind="bold")
    fig.text(46, 164, "g = [[1, 3], [0, 1]]", size=14, fill=INK, kind="mono")
    fig.text(510, 164, "g = [[2, 0], [0, 1]]", size=14, fill=INK, kind="mono")
    fig.text(46, 200, "minor     before   after", size=13, fill=MUTED, kind="mono")
    fig.text(510, 200, "minor     before   after", size=13, fill=MUTED, kind="mono")
    for i, ij in enumerate(PAIRS):
        lean, _phys = PAIR_NAME[ij]
        y = 228 + i * 24
        fig.text(46, y, f"{lean}        {q(s['P'][ij])}        {q(s['sl_minors'][ij])}", size=14, fill=INK, kind="mono")
        fig.text(510, y, f"{lean}        {q(s['P'][ij])}        {q(s['gl_minors'][ij])}", size=14, fill=INK, kind="mono")
    fig.text(
        28,
        440,
        f"Ensemble, entries in {{-1,0,1,2}}:  {s['sl_n']} matrices with det 1, minors identical;",
        size=14,
        fill=INK,
    )
    fig.text(
        28,
        464,
        f"{s['gl_n']} other invertible matrices, every minor scaled by the determinant.",
        size=14,
        fill=INK,
    )
    fig.text(28, 500, "plucker_gl_weight_det and plucker_specialLinear_invariant.", size=13, fill=MUTED, kind="mono")
    fig.text(28, 524, "The old claim that sum log|det| is GL(2)-invariant is not this theorem, and is false.", size=13, fill=RED)
    footer(fig, 548, True)
    fig.save("mvp0-gl2")


def draw_mvp1(s: dict):
    fig = Fig(960, 720)
    frame(
        fig,
        True,
        "MVP-1  ·  the orthant coefficient",
        "Columns 0 and 2 are gauged to the identity. The rational number is proved. A 4-form is not.",
    )
    x, y, z, w = s["chart"]
    fig.rect(28, 108, 440, 430, GREEN_BG, stroke=GREEN, sw=1.5, rx=12)
    fig.text(46, 140, "Chart, all four coordinates positive", size=15, fill=GREEN, kind="bold")
    fig.text(46, 174, f"x={q(x)}   y={q(y)}   z={q(z)}   w={q(w)}", size=16, fill=INK, kind="mono")
    fig.text(46, 210, "|  1   y   0  -w |", size=16, fill=INK, kind="mono")
    fig.text(46, 234, "|  0   x   1   z |", size=16, fill=INK, kind="mono")
    fig.text(46, 270, "Ordered adjacent product", size=13, fill=MUTED)
    fig.text(46, 292, "x y z w  =  " + q(s["adjacent_chart"]), size=16, fill=INK, kind="bold")
    fig.text(46, 328, "Orthant coefficient", size=13, fill=MUTED)
    fig.text(46, 352, "1 / (x y z w)  =  " + q(s["orthant"]), size=18, fill=GREEN, kind="bold")
    fig.text(46, 390, "On the witness this is 16/3.", size=14, fill=INK)
    fig.text(46, 414, "The algebraic residue is 1.", size=14, fill=INK)
    fig.text(46, 450, "Walls: an adjacent minor is zero.", size=13, fill=MUTED)
    fig.text(46, 472, "Inside, the other two minors stay positive.", size=13, fill=MUTED)
    fig.text(46, 506, "This panel is the chart, not a 4-form.", size=13, fill=MUTED)

    fig.rect(488, 108, 444, 430, WHITE, stroke=GREEN, sw=1.5, rx=12)
    fig.text(506, 140, "Cyclic product, sign included", size=15, fill=GREEN, kind="bold")
    fig.text(506, 176, "<41>  =  - P03", size=16, fill=INK, kind="mono")
    fig.text(506, 208, "cyclic  =  <12><23><34><41>", size=15, fill=INK, kind="mono")
    fig.text(506, 236, "       =  - (x y z w)", size=15, fill=INK, kind="mono")
    fig.text(506, 278, "Parke-Taylor coefficient", size=13, fill=MUTED)
    fig.text(506, 304, "1 / cyclic  =  " + q(s["parke"]), size=18, fill=INK, kind="bold")
    fig.text(506, 340, "Equal to minus the orthant coefficient.", size=14, fill=INK)
    fig.text(506, 372, "GL(2) multiplies the adjacent", size=14, fill=INK)
    fig.text(506, 394, "product by (det g)^4.", size=14, fill=INK)
    fig.text(506, 428, "The gauge that fixes columns", size=14, fill=INK)
    fig.text(506, 450, "0 and 2 is the unique one.", size=14, fill=INK)
    fig.text(506, 490, "N=4 super Yang-Mills is the", size=13, fill=MUTED)
    fig.text(506, 512, "method copied, not the target.", size=13, fill=MUTED)

    fig.text(28, 568, "Not claimed: a de Rham 4-form, a helicity numerator, a momentum delta,", size=14, fill=RED)
    fig.text(28, 592, "a cross section, or uniqueness of the canonical form in general.", size=14, fill=RED)
    fig.text(28, 628, "Do not read the chart as a plot of a cross section, and do not read 16/3 as a mass.", size=14, fill=INK)
    footer(fig, 668, True)
    fig.save("mvp1-canonical")


def draw_mvp2(s: dict):
    fig = Fig(960, 760)
    frame(
        fig,
        True,
        "MVP-2  ·  the orthant factors onto a face",
        "The denominator vanishes on an adjacent wall. The cancellation is algebra, not a cross section.",
    )
    x, y, z, w = s["chart"]
    fig.rect(28, 108, 448, 430, GREEN_BG, stroke=GREEN, sw=1.5, rx=12)
    fig.rect(492, 108, 440, 430, WHITE, stroke=GREEN, sw=1.5, rx=12)
    fig.text(46, 142, "Where the denominator is zero", size=16, fill=GREEN, kind="bold")
    fig.text(46, 174, "x y z w = 0  iff  one of them is 0", size=14, fill=INK, kind="mono")
    fig.text(46, 198, "Those four are P01, P12, P03, P23.", size=14, fill=INK)
    fig.text(46, 222, "P13 = y z + x w is not a factor.", size=14, fill=INK)
    fig.text(46, 258, "On each face, the other three > 0,", size=14, fill=INK)
    fig.text(46, 280, "and P13 stays positive.", size=14, fill=INK)
    fig.text(46, 316, f"witness face x=0:  P13 = {q(s['face_p13'])}", size=16, fill=GREEN, kind="bold")
    fig.text(46, 348, f"chart was x={q(x)} y={q(y)} z={q(z)} w={q(w)}", size=13, fill=MUTED, kind="mono")
    fig.text(46, 384, "Off the chamber, P13 can vanish", size=14, fill=INK)
    fig.text(46, 406, "while the product does not:", size=14, fill=INK)
    fig.text(46, 434, f"(1, 1, -1, 1)  product {q(s['off_product'])}", size=14, fill=INK, kind="mono")
    fig.text(46, 470, "That point is not positive.", size=13, fill=MUTED)
    fig.text(46, 500, "No differential form is constructed.", size=13, fill=MUTED)

    fig.text(510, 142, "Cancelling one coordinate", size=16, fill=GREEN, kind="bold")
    fig.text(510, 174, "x / (x y z w) = 1 / (y z w)", size=14, fill=INK, kind="mono")
    fig.text(510, 198, "when none of the four is zero.", size=14, fill=INK)
    fig.text(510, 222, "The right-hand side ignores x.", size=14, fill=INK)
    fig.text(510, 258, f"drop x  =  {q(s['drop_x'])}", size=16, fill=INK, kind="mono")
    fig.text(510, 286, f"drop y  =  {q(s['drop_y'])}", size=16, fill=INK, kind="mono")
    fig.text(510, 314, f"drop z  =  {q(s['drop_z'])}", size=16, fill=INK, kind="mono")
    fig.text(510, 342, f"drop w  =  {q(s['drop_w'])}", size=16, fill=INK, kind="mono")
    fig.text(510, 380, "Same shape as the 3-orthant", size=14, fill=INK)
    fig.text(510, 402, "coefficient. Not a residue in", size=14, fill=INK)
    fig.text(510, 424, "de Rham cohomology, and not", size=14, fill=INK)
    fig.text(510, 446, "a factorisation of an amplitude.", size=14, fill=INK)
    fig.text(510, 490, "8/3 and 8 are not masses.", size=14, fill=RED, kind="bold")

    fig.rect(28, 556, 904, 140, RED_BG, stroke=RED, sw=1.4, rx=12)
    fig.text(46, 586, "Column shift, one point, not a mutation", size=15, fill=RED, kind="bold")
    fig.text(46, 616, "column 3  <-  column 3 + 1 * (column 1 + column 2)", size=14, fill=INK, kind="mono")
    fig.text(46, 644, "At the witness, P23 goes from 1 to " + q(s["shifted_minors"][(2, 3)]) + ". Still on the quadric.", size=14, fill=INK)
    fig.text(46, 670, "Proved for this matrix only. A general cluster algebra is not the milestone.", size=14, fill=INK)
    footer(fig, 732, True)
    fig.save("mvp2-cluster")


def draw_mvp3(_s: dict):
    fig = Fig(960, 520)
    frame(
        fig,
        False,
        "MVP-3  ·  the only way a GeV is allowed in",
        "Conformal Gr+(2,4) does not produce a mass. One declared measurement may set the unit.",
    )
    boxes = [
        (28, GREEN_BG, GREEN, "Geometry", "dimensionless", "brackets and forms", "no GeV inside"),
        (262, BLUE_BG, BLUE, "One input", "a mass, named", "before any output", "from outside"),
        (496, AMBER_BG, AMBER, "A ratio R", "unknown", "not in this repo", "no second scale"),
        (730, WHITE, RULE, "Comparison", "R times input", "against PDG", "not a fit"),
    ]
    for x, bg, edge, a, b, c, d in boxes:
        fig.rect(x, 130, 210, 200, bg, stroke=edge, sw=1.6, rx=12)
        fig.text(x + 105, 168, a, size=16, fill=INK, anchor="middle", kind="serif")
        fig.text(x + 105, 204, b, size=14, fill=INK, anchor="middle")
        fig.text(x + 105, 228, c, size=14, fill=MUTED, anchor="middle")
        fig.text(x + 105, 252, d, size=14, fill=MUTED, anchor="middle")
    fig.arrow(238, 230, 260, 230, INK, sw=1.5, head=8)
    fig.arrow(472, 230, 494, 230, INK, sw=1.5, head=8)
    fig.arrow(706, 230, 728, 230, INK, sw=1.5, head=8)
    fig.rect(28, 360, 904, 100, RED_BG, stroke=RED, sw=1.4, rx=12)
    fig.text(48, 396, "R is blank on purpose. Writing a number here would be a fit, or a guess.", size=16, fill=RED, kind="bold")
    fig.text(48, 428, "A regulator, a Planck suppression, or a second measured mass ends the milestone.", size=14, fill=INK)
    footer(fig, 496, False)
    fig.save("mvp3-scale")


def draw_mvp4(s: dict):
    fig = Fig(960, 640)
    frame(
        fig,
        False,
        "MVP-4  ·  rank one is a pair of spinors",
        "The outer product and the rescaling are Lean lemmas. The helicity weight is not. This card stays a contract.",
    )
    p0 = s["momenta"][0]
    u, v = s["factors"][0]
    fig.rect(28, 112, 904, 150, WHITE, stroke=RULE, sw=1.2, rx=12)
    fig.text(48, 146, "Edge p0 of the polygon. det = 0, and p0 = u v^T.", size=14, fill=MUTED)
    fig.text(48, 180, mat_str(p0), size=16, fill=INK, kind="mono")
    fig.text(48, 214, f"=  u v^T    u=({q(u[0])}, {q(u[1])})    v=({q(v[0])}, {q(v[1])})", size=15, fill=INK, kind="mono")
    fig.text(48, 242, "Proved: det2_eq_zero_iff_exists_outer, and polygon_edge_outer for all four edges.", size=14, fill=GREEN)

    fig.rect(28, 284, 280, 230, BLUE_BG, stroke=BLUE, sw=1.4, rx=12)
    fig.rect(328, 284, 280, 230, BLUE_BG, stroke=BLUE, sw=1.4, rx=12)
    fig.rect(628, 284, 304, 230, AMBER_BG, stroke=AMBER, sw=1.4, rx=12)
    fig.text(48, 318, "SL(2) on lambda", size=15, fill=BLUE, kind="bold")
    fig.text(48, 350, "Lorentz, undotted", size=14, fill=INK)
    fig.text(48, 376, "Would act on the column u.", size=14, fill=INK)
    fig.text(48, 412, "Not a Lean action", size=13, fill=MUTED)
    fig.text(48, 434, "in this repository.", size=13, fill=MUTED)
    fig.text(348, 318, "SL(2) on lambda~", size=15, fill=BLUE, kind="bold")
    fig.text(348, 350, "Lorentz, dotted", size=14, fill=INK)
    fig.text(348, 376, "Would act on the row v.", size=14, fill=INK)
    fig.text(348, 412, "The two copies are the", size=13, fill=MUTED)
    fig.text(348, 434, "dictionary, not a theorem.", size=13, fill=MUTED)
    fig.text(648, 318, "Rescaling, not helicity", size=15, fill=AMBER, kind="bold")
    fig.text(648, 350, "u -> t u,   v -> v / t", size=14, fill=INK, kind="mono")
    fig.text(648, 378, "Proved for every t != 0.", size=14, fill=GREEN)
    fig.text(648, 400, "The polygon checks t = 2.", size=14, fill=INK)
    fig.text(648, 434, "Helicity h: a wavefunction", size=13, fill=AMBER)
    fig.text(648, 456, "weight t^(-2h). Not proved.", size=13, fill=AMBER)
    fig.text(28, 548, "A massless boson would be a weight that this geometry forces.", size=15, fill=INK)
    fig.text(28, 574, "The lemma does not derive it. MVP-4 stays amber.", size=15, fill=INK)
    footer(fig, 618, False)
    fig.save("mvp4-helicity")


def draw_sweep(s: dict):
    """Picture of the face residue. y, z, w fixed. Not a new theorem."""
    fig = Fig(960, 720)
    frame(
        fig,
        True,
        "Face sweep  ·  the residue, drawn",
        "y, z, w fixed at the witness. Seven positive rationals for x. Exact arithmetic, then the picture.",
    )
    y, z, w = s["chart"][1], s["chart"][2], s["chart"][3]

    def panel(x0, title, ylabel):
        fig.rect(x0, 108, 440, 360, WHITE, stroke=RULE, sw=1.2, rx=12)
        fig.text(x0 + 20, 136, title, size=15, fill=INK, kind="serif")
        fig.text(x0 + 20, 158, ylabel, size=12, fill=MUTED)

    panel(28, "x times the coefficient", "stays 8/3 off the wall")
    panel(492, "P13 = y z + x w", "stays positive, including the wall")

    samples = s["sweep"]
    xs_vals = [row[0] for row in samples]
    xmin, xmax = F(0), max(xs_vals)

    def xpix(x0, xv):
        return x0 + 48 + float((xv - xmin) / (xmax - xmin)) * 340

    # Left axis: residue is constant, so the scale is just that line.
    y_top, y_bot = 196, 420
    residue = samples[0][3]
    fig.line(xpix(28, xmin), y_bot, xpix(28, xmax), y_bot, RULE, 1)
    fig.line(xpix(28, F(0)), y_top, xpix(28, F(0)), y_bot, RULE, 1)
    yres = (y_top + y_bot) / 2
    fig.dash(xpix(28, xmin), yres, xpix(28, xmax), yres, GREEN, 1.5)
    fig.circle(xpix(28, F(0)), y_bot, 5, RED)
    fig.text(xpix(28, F(0)) + 8, y_bot - 8, "x=0 pole", size=12, fill=RED)
    for xs, _prod, _coeff, res, _p13s in samples:
        fig.circle(xpix(28, xs), yres, 4.5, GREEN)
        if res != residue:
            raise RuntimeError("sweep plot saw a residue that is not constant")
    fig.text(xpix(28, xmax) - 4, yres - 16, q(residue), size=14, fill=GREEN, anchor="end", kind="bold")
    fig.text(76, 448, "x", size=12, fill=MUTED)
    fig.text(40, y_bot + 16, "0", size=12, fill=MUTED)
    fig.text(xpix(28, s["chart"][0]) - 10, y_bot + 16, "1/2", size=12, fill=MUTED)
    fig.text(xpix(28, xmax) - 8, y_bot + 16, q(xmax), size=12, fill=MUTED)

    # Right axis: P13 from the wall value up through the last sample.
    p13_wall = s["face_p13"]
    p13_vals = [p13_wall] + [row[4] for row in samples]
    pmin, pmax = min(p13_vals), max(p13_vals)

    def ypix(pv):
        return y_bot - float((pv - pmin) / (pmax - pmin)) * (y_bot - y_top)

    fig.line(xpix(492, xmin), y_bot, xpix(492, xmax), y_bot, RULE, 1)
    fig.line(xpix(492, F(0)), y_top, xpix(492, F(0)), y_bot, RULE, 1)
    pts = [(xpix(492, F(0)), ypix(p13_wall))] + [
        (xpix(492, row[0]), ypix(row[4])) for row in samples
    ]
    for a, b in zip(pts, pts[1:]):
        fig.line(a[0], a[1], b[0], b[1], GREEN, 1.6)
    fig.circle(pts[0][0], pts[0][1], 5, AMBER)
    fig.text(pts[0][0] + 8, pts[0][1] + 16, "3/4 at the wall", size=12, fill=AMBER)
    for (px, py), row in zip(pts[1:], samples):
        fig.circle(px, py, 4.5, GREEN)
        if row[4] <= 0:
            raise RuntimeError("sweep plot saw a non-positive P13")
    fig.text(xpix(492, xmax) - 4, pts[-1][1] - 14, q(samples[-1][4]), size=13, fill=GREEN, anchor="end")
    fig.text(540, 448, "x", size=12, fill=MUTED)

    fig.rect(28, 488, 904, 168, GREEN_BG, stroke=GREEN, sw=1.2, rx=12)
    fig.text(
        46,
        516,
        "Three of the seven samples. y=%s  z=%s  w=%s. The shadow lists the rest."
        % (q(y), q(z), q(w)),
        size=14,
        fill=GREEN,
        kind="bold",
    )
    headers = (46, 150, 280, 460, 680)
    for xh, label in zip(headers, ("x", "product", "1/(xyzw)", "x/(xyzw)", "P13")):
        fig.text(xh, 544, label, size=13, fill=MUTED, kind="mono")
    show = [samples[0], samples[2], samples[-1]]
    for i, (xs, prod, coeff, residue, p13s) in enumerate(show):
        vals = (q(xs), q(prod), q(coeff), q(residue), q(p13s))
        for xh, val in zip(headers, vals):
            fig.text(xh, 572 + i * 22, val, size=14, fill=INK, kind="mono")
    footer(fig, 692, True, "picture of a proved identity, not a fit")
    fig.save("face-sweep")


def write_all(s: dict):
    text = shadow_text(s)
    if "80.4" in text:
        raise RuntimeError("shadow text contains a fitted mass")
    FIG.mkdir(parents=True, exist_ok=True)
    (FIG / "shadow.txt").write_text(text, encoding="utf-8")
    draw_ladder(s)
    draw_klein(s)
    draw_polygon(s)
    draw_positive(s)
    draw_gl2(s)
    draw_mvp1(s)
    draw_mvp2(s)
    draw_mvp3(s)
    draw_mvp4(s)
    draw_sweep(s)
    for svg in FIG.glob("*.svg"):
        raw = svg.read_text(encoding="utf-8")
        if "80.4" in raw:
            raise RuntimeError(f"{svg.name} contains a fitted mass")


def check_committed(s: dict):
    text = shadow_text(s)
    path = FIG / "shadow.txt"
    if path.exists() and path.read_text(encoding="utf-8") != text:
        raise RuntimeError("docs/figures/shadow.txt is stale; rerun with --write")
    print(text, end="")
    print(
        f"shadow ok  ·  SL(2) samples {s['sl_n']}  ·  GL(2) samples {s['gl_n']}",
        file=sys.stderr,
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute identities only")
    parser.add_argument("--write", action="store_true", help="rewrite docs/figures")
    args = parser.parse_args(argv)
    do_check = args.check or not args.write
    do_write = args.write or not args.check
    shadow = build_shadow()
    if do_write:
        write_all(shadow)
    if do_check:
        check_committed(shadow)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except RuntimeError as exc:
        print(f"geometry shadow failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
