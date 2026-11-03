#!/usr/bin/env python3
"""Wrap Lean source lines over WIDTH columns at ', ' separators inside brackets.

Only breaks where bracket depth > 0 (list/tuple/vector literals, simp/rw lists), so the
term is unchanged; continuation lines are indented 4 spaces past the line's indent.
Comment lines and lines inside block comments are left alone. Used by the generators
(sims/jord1/emit_lean.py) and for hand-written files. Usage: lean_wrap.py FILE...
"""
import sys

WIDTH = 100


def wrap_line(line, width=WIDTH):
    if len(line) <= width or line.lstrip().startswith(('--', '/-', '-/')):
        return [line]
    ind = len(line) - len(line.lstrip())
    cont = ' ' * (ind + 4)
    out, cur, prefix, depth0 = [], line, '', 0
    while len(prefix + cur) > width:
        depth, cut, instr, cutdepth = depth0, -1, False, depth0
        limit = width - len(prefix)
        for i, ch in enumerate(cur):
            if ch == '"': instr = not instr
            if instr: continue
            if ch in '([{⟨': depth += 1
            elif ch in ')]}⟩': depth -= 1
            elif ch == ',' and depth > 0 and i + 1 < len(cur) and cur[i + 1] == ' ' and i + 1 <= limit:
                cut, cutdepth = i + 1, depth
        if cut <= 0: break
        out.append((prefix + cur[:cut]).rstrip())
        cur, prefix, depth0 = cur[cut:].lstrip(), cont, cutdepth
    out.append(prefix + cur)
    return out


def wrap_text(text, width=WIDTH):
    res, in_block = [], 0
    for line in text.split('\n'):
        s = line.strip()
        opens, closes = line.count('/-'), line.count('-/')
        if in_block or s.startswith('--') or '/-' in line:
            res.append(line)
        else:
            res += wrap_line(line, width)
        in_block = max(0, in_block + opens - closes)
    return '\n'.join(res)


if __name__ == '__main__':
    for f in sys.argv[1:]:
        t = open(f).read(); w = wrap_text(t)
        if w != t: open(f, 'w').write(w)
