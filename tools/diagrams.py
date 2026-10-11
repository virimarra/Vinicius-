"""Gera os diagramas SVG dos drills em img/.

Convenções: vista de cima, adversário para o topo da imagem.
Pé esquerdo (E) em azul, pé direito (D) em vermelho. Base ortodoxa.
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "img"
BLUE, RED, GRAY, INK, GREEN, ORANGE = "#2563eb", "#dc2626", "#9ca3af", "#111827", "#16a34a", "#ea580c"
FONT = "font-family:Helvetica,Arial,sans-serif"


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<title>{title}</title><rect width="{w}" height="{h}" fill="#ffffff"/>'
            '<defs>'
            f'<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
            f'<marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
            f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>'
            f'<marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker>'
            f'<marker id="ao" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ORANGE}"/></marker>'
            '</defs>' + body + '</svg>')


def text(x, y, s, size=12, color=INK, anchor="middle", weight="normal"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}" style="{FONT}">{s}</text>'


def foot(x, y, ang, color, label=None, op=1.0):
    g = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang})" opacity="{op}">'
         f'<ellipse cx="0" cy="0" rx="10" ry="22" fill="{color}" fill-opacity="0.85" stroke="{INK}" stroke-width="1"/>'
         f'<circle cx="0" cy="-15" r="4" fill="#fff" fill-opacity="0.8"/></g>')
    if label:
        g += text(x, y + 4, label, 11, "#fff", weight="bold") if op > 0.5 else ""
    return g


def arrow(x1, y1, x2, y2, color=INK, marker="a", dash=False, width=2):
    d = ' stroke-dasharray="5,4"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}" marker-end="url(#{marker})"{d}/>'


def opponent_marker(x, y):
    return text(x, y, "▲ adversário", 11, GRAY)


def cross(x, y, s=14):
    return (f'<line x1="{x-s}" y1="{y-s}" x2="{x+s}" y2="{y+s}" stroke="{RED}" stroke-width="4"/>'
            f'<line x1="{x-s}" y1="{y+s}" x2="{x+s}" y2="{y-s}" stroke="{RED}" stroke-width="4"/>')


def check(x, y):
    return f'<path d="M{x-12},{y} l8,9 l16,-18" stroke="{GREEN}" stroke-width="4" fill="none"/>'


# ---------------------------------------------------------------- base
def base():
    b = ""
    # painel certo
    cx = 140
    b += text(cx, 24, "CERTO — base ortodoxa", 14, GREEN, weight="bold") + opponent_marker(cx, 44)
    b += f'<line x1="{cx-28}" y1="60" x2="{cx-28}" y2="235" stroke="{GRAY}" stroke-dasharray="6,5"/>'
    b += f'<line x1="{cx+28}" y1="60" x2="{cx+28}" y2="235" stroke="{GRAY}" stroke-dasharray="6,5"/>'
    b += foot(cx - 28, 105, 25, BLUE, "E") + foot(cx + 28, 185, 55, RED, "D")
    b += f'<line x1="{cx-50}" y1="127" x2="{cx+50}" y2="127" stroke="{ORANGE}" stroke-dasharray="3,3"/>'
    b += text(cx + 54, 131, "calcanhar E", 9, ORANGE, "start")
    b += text(cx, 252, "um pé em cada \"trilho\"", 11) + text(cx, 266, "largura ≥ ombros · calcanhar D levantado", 10, GRAY)
    b += check(cx + 118, 50)
    # errado 1
    cx = 400
    b += text(cx, 24, "ERRADO — corda bamba", 14, RED, weight="bold") + opponent_marker(cx, 44)
    b += f'<line x1="{cx}" y1="60" x2="{cx}" y2="235" stroke="{GRAY}" stroke-dasharray="6,5"/>'
    b += foot(cx, 105, 15, BLUE, "E") + foot(cx, 185, 45, RED, "D")
    b += text(cx, 252, "pés na mesma linha:", 11) + text(cx, 266, "cai com um empurrão lateral", 10, GRAY)
    b += cross(cx + 105, 50)
    # errado 2
    cx = 660
    b += text(cx, 24, "ERRADO — de frente", 14, RED, weight="bold") + opponent_marker(cx, 44)
    b += foot(cx - 40, 145, 0, BLUE, "E") + foot(cx + 40, 145, 0, RED, "D")
    b += text(cx, 252, "pés lado a lado:", 11) + text(cx, 266, "cai com um empurrão de frente", 10, GRAY)
    b += cross(cx + 105, 50)
    return svg(800, 280, b, "Base ortodoxa: certo e errado")


# ---------------------------------------------------------------- step-drag
def step_drag():
    b = ""
    panels = [("FRENTE", (0, -1), "E"), ("TRÁS", (0, 1), "D"), ("ESQUERDA", (-1, 0), "E"), ("DIREITA", (1, 0), "D")]
    for i, (name, (dx, dy), first) in enumerate(panels):
        cx, cy = 100 + i * 200, 150
        b += text(cx, 24, name, 14, weight="bold") + opponent_marker(cx, 42)
        L0, R0 = (cx - 22, cy - 35), (cx + 22, cy + 35)
        s = 34
        L1, R1 = (L0[0] + dx * s, L0[1] + dy * s), (R0[0] + dx * s, R0[1] + dy * s)
        b += foot(*L0, 25, BLUE, op=0.22) + foot(*R0, 55, RED, op=0.22)
        b += foot(*L1, 25, BLUE, "E") + foot(*R1, 55, RED, "D")
        order = {"E": 1, "D": 2} if first == "E" else {"E": 2, "D": 1}
        for (p0, p1, col, mk, lab) in [(L0, L1, BLUE, "ab", "E"), (R0, R1, RED, "ar", "D")]:
            ox, oy = (16, 0) if dx == 0 else (0, 30)
            b += arrow(p0[0] + ox, p0[1] + oy, p1[0] + ox - dx * 6, p1[1] + oy - dy * 6, col, mk)
            b += f'<circle cx="{(p0[0]+p1[0])/2+ox+12:.1f}" cy="{(p0[1]+p1[1])/2+oy:.1f}" r="9" fill="{col}"/>'
            b += text((p0[0] + p1[0]) / 2 + ox + 12, (p0[1] + p1[1]) / 2 + oy + 4, str(order[lab]), 11, "#fff", weight="bold")
        b += text(cx, 262, f"sai primeiro: pé {'esquerdo' if first == 'E' else 'direito'}", 11)
    b += text(400, 284, "transparente = posição inicial · número = ordem do pé · a base nunca muda de formato", 11, GRAY)
    return svg(800, 295, b, "Step-drag nas 4 direções")


# ---------------------------------------------------------------- pivô
def pivot():
    b = text(200, 24, "PIVÔ NO PÉ DA FRENTE", 14, weight="bold") + opponent_marker(200, 42)
    L = (200, 120)
    v = (40, 72)
    b += foot(*L, 25, BLUE, "E")
    r = math.hypot(*v)
    for th, col in [(45, ORANGE), (-45, GREEN)]:
        t = math.radians(th)
        x = L[0] + v[0] * math.cos(t) - v[1] * math.sin(t)
        y = L[1] + v[0] * math.sin(t) + v[1] * math.cos(t)
        sweep = 1 if th > 0 else 0
        b += (f'<path d="M{L[0]+v[0]:.1f},{L[1]+v[1]:.1f} A{r:.1f},{r:.1f} 0 0,{sweep} {x:.1f},{y:.1f}" '
              f'fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#{"ao" if col == ORANGE else "ag"})"/>')
        b += foot(x, y, 55 + th, RED, op=0.45)
        b += text(x + (-38 if th > 0 else 38), y + 4, "sentido " + ("A" if th > 0 else "B"), 11, col, weight="bold")
    b += foot(L[0] + v[0], L[1] + v[1], 55, RED, "D")
    b += f'<circle cx="{L[0]}" cy="{L[1]}" r="30" fill="none" stroke="{BLUE}" stroke-dasharray="2,3"/>'
    b += text(200, 268, "gire na planta do pé E · o pé D desenha um arco de 45–90°", 11)
    b += text(200, 284, "o corpo gira junto e a base continua intacta · treine os 2 sentidos", 11, GRAY)
    return svg(400, 295, b, "Pivô no pé da frente")


# ---------------------------------------------------------------- caixa
def box_drill():
    b = text(200, 24, "DRILL DA CAIXA (fita no chão)", 14, weight="bold") + opponent_marker(200, 42)
    x0, y0, s = 120, 70, 160
    b += f'<rect x="{x0}" y="{y0}" width="{s}" height="{s}" fill="none" stroke="#f59e0b" stroke-width="6" stroke-opacity="0.6"/>'
    pts = [(x0, y0 + s), (x0, y0), (x0 + s, y0), (x0 + s, y0 + s)]
    labels = ["1 · frente", "2 · direita", "3 · trás", "4 · esquerda"]
    for i in range(4):
        a, c = pts[i], pts[(i + 1) % 4]
        b += arrow(a[0] + (c[0] - a[0]) * .15, a[1] + (c[1] - a[1]) * .15, a[0] + (c[0] - a[0]) * .85, a[1] + (c[1] - a[1]) * .85, INK)
    b += text(x0 - 12, y0 + s / 2, labels[0], 12, anchor="end") + text(x0 + s / 2, y0 - 10, labels[1], 12)
    b += text(x0 + s + 12, y0 + s / 2, labels[2], 12, anchor="start") + text(x0 + s / 2, y0 + s + 22, labels[3], 12)
    b += text(200, 280, "2–4 passos curtos em cada lado · volte sempre ao canto inicial", 11, GRAY)
    return svg(400, 292, b, "Drill da caixa")


# ---------------------------------------------------------------- X
def x_drill():
    b = text(200, 24, "DRILL DO \"X\" — saídas em ângulo", 14, weight="bold") + opponent_marker(200, 42)
    c = (200, 160)
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        b += f'<line x1="{c[0]}" y1="{c[1]}" x2="{c[0]+dx*95}" y2="{c[1]+dy*95}" stroke="#f59e0b" stroke-width="6" stroke-opacity="0.6"/>'
    b += f'<circle cx="{c[0]}" cy="{c[1]}" r="16" fill="{INK}"/>' + text(c[0], c[1] + 4, "você", 10, "#fff")
    outs = [((-1, -1), "frente-esquerda"), ((1, -1), "frente-direita"), ((-1, 1), "trás-esquerda"), ((1, 1), "trás-direita")]
    for (dx, dy), lab in outs:
        b += arrow(c[0] + dx * 22, c[1] + dy * 22, c[0] + dx * 80, c[1] + dy * 80, GREEN, "ag")
        b += text(c[0] + dx * 100, c[1] + dy * 100 + (14 if dy > 0 else -6), lab, 11, anchor="middle")
    b += text(200, 290, "combo no centro → saia em diagonal por um braço do X → volte", 11, GRAY)
    return svg(400, 300, b, "Drill do X")


# ---------------------------------------------------------------- slip
def slip():
    b = ""
    for i, (title, side, lab2) in enumerate([("SLIP DO JAB", 1, "cabeça para a SUA DIREITA"), ("SLIP DO DIRETO", -1, "cabeça para a SUA ESQUERDA")]):
        cx = 150 + i * 300
        b += text(cx, 24, title, 14, weight="bold") + text(cx, 42, "como você se vê no espelho", 10, GRAY)
        # linha do golpe
        b += f'<line x1="{cx}" y1="55" x2="{cx}" y2="250" stroke="{RED}" stroke-dasharray="6,4"/>'
        b += text(cx, 262, "linha do golpe", 10, RED)
        # corpo
        b += f'<path d="M{cx-60},240 Q{cx-55},170 {cx},165 Q{cx+55},170 {cx+60},240" fill="#e5e7eb" stroke="{INK}"/>'
        b += f'<circle cx="{cx}" cy="130" r="26" fill="none" stroke="{GRAY}" stroke-dasharray="4,3"/>'
        hx = cx + side * 34  # deslocamento ~10-15 cm
        b += f'<circle cx="{hx}" cy="140" r="26" fill="#fde68a" stroke="{INK}" stroke-width="1.5"/>'
        b += arrow(cx + side * 8, 112, hx + side * 6, 118, INK)
        b += text(cx, 284, lab2, 12, weight="bold") + text(cx, 299, "joelho do mesmo lado dobra · olhos no alvo · só 10–15 cm", 10, GRAY)
    return svg(600, 310, b, "Slip do jab e do direto")


# ---------------------------------------------------------------- bob and weave
def bob_weave():
    b = text(300, 24, "ROLL / BOB AND WEAVE com corda esticada", 14, weight="bold")
    b += f'<line x1="20" y1="110" x2="580" y2="110" stroke="#a16207" stroke-width="4"/>' + text(300, 100, "corda (altura do ombro)", 10, "#a16207")
    path = "M110,80 C130,200 470,200 490,80"
    b += f'<path d="{path}" fill="none" stroke="{GREEN}" stroke-width="3" stroke-dasharray="8,5" marker-end="url(#ag)"/>'
    for x, y, op in [(110, 80, .35), (300, 175, 1), (490, 80, .35)]:
        b += f'<g opacity="{op}"><circle cx="{x}" cy="{y}" r="20" fill="#fde68a" stroke="{INK}"/>'
        b += f'<rect x="{x-28}" y="{y+18}" width="18" height="16" rx="5" fill="{BLUE}"/><rect x="{x+10}" y="{y+18}" width="18" height="16" rx="5" fill="{RED}"/></g>'
    b += text(110, 150, "começa de um lado", 11) + text(300, 235, "desce DOBRANDO OS JOELHOS (\"U\")", 12, weight="bold")
    b += text(300, 252, "coluna reta · guarda colada · olhos à frente", 11, GRAY) + text(490, 150, "sobe do outro lado", 11)
    return svg(600, 265, b, "Bob and weave com corda")


# ---------------------------------------------------------------- trajetórias
def punches():
    b = text(200, 22, "TRAJETÓRIAS (vista de cima)", 14, weight="bold")
    b += f'<circle cx="200" cy="70" r="24" fill="#fde68a" stroke="{INK}"/>' + text(200, 74, "alvo", 10)
    b += f'<ellipse cx="200" cy="250" rx="70" ry="22" fill="#e5e7eb" stroke="{INK}"/>' + text(200, 285, "você (ombros)", 10, GRAY)
    b += arrow(160, 240, 192, 96, BLUE, "ab", width=3) + text(160, 170, "1", 16, BLUE, weight="bold")
    b += arrow(245, 245, 208, 96, RED, "ar", width=3) + text(238, 170, "2", 16, RED, weight="bold")
    b += f'<path d="M135,245 Q85,90 175,72" fill="none" stroke="{GREEN}" stroke-width="3" marker-end="url(#ag)"/>' + text(88, 150, "3", 16, GREEN, weight="bold")
    b += f'<path d="M268,248 Q320,90 225,72" fill="none" stroke="{ORANGE}" stroke-width="3" marker-end="url(#ao)"/>' + text(318, 150, "4", 16, ORANGE, weight="bold")
    # lateral uppercut
    ox = 400
    b += text(ox + 150, 22, "UPPERCUT 5/6 (vista lateral)", 14, weight="bold")
    b += f'<circle cx="{ox+200}" cy="80" r="24" fill="#fde68a" stroke="{INK}"/>' + text(ox + 200, 84, "queixo", 10)
    b += f'<path d="M{ox+110},250 Q{ox+150},235 {ox+170},200 Q{ox+190},150 {ox+190},110" fill="none" stroke="{GREEN}" stroke-width="3" marker-end="url(#ag)"/>'
    b += text(ox + 95, 175, "joelho flexiona", 11, anchor="start") + text(ox + 95, 190, "→ perna e quadril sobem", 11, anchor="start")
    b += text(ox + 150, 270, "curto · cotovelo ~90° · não \"pescar\" lá de baixo", 11, GRAY)
    return svg(800, 295, b, "Trajetórias dos golpes")


# ---------------------------------------------------------------- cadeia cinética
def kinetic():
    steps = ["Pé empurra o chão", "Joelho/quadril giram", "Tronco gira", "Ombro", "Braço estende", "Punho gira no fim"]
    b = text(400, 22, "O SOCO COMEÇA NO CHÃO (cadeia cinética)", 14, weight="bold")
    w = 118
    for i, s in enumerate(steps):
        x = 12 + i * (w + 14)
        b += f'<rect x="{x}" y="40" width="{w}" height="46" rx="8" fill="#eff6ff" stroke="{BLUE}"/>'
        words = s.split(" ")
        mid = (len(words) + 1) // 2
        b += text(x + w / 2, 60, " ".join(words[:mid]), 12) + text(x + w / 2, 76, " ".join(words[mid:]), 12)
        if i < len(steps) - 1:
            b += arrow(x + w + 1, 63, x + w + 13, 63)
    b += text(400, 108, "braço sozinho = soco fraco e lento · impacto com os 2 primeiros nós dos dedos · expire em cada golpe", 11, GRAY)
    return svg(800, 118, b, "Cadeia cinética do soco")


# ---------------------------------------------------------------- cortar o ringue
def cut_ring():
    b = text(200, 22, "CORTAR O RINGUE (pressão)", 14, weight="bold")
    b += f'<rect x="60" y="40" width="280" height="220" fill="none" stroke="{INK}" stroke-width="3"/>'
    b += f'<circle cx="300" cy="90" r="16" fill="{RED}"/>' + text(300, 94, "A", 11, "#fff", weight="bold")
    b += f'<path d="M300,110 L300,200" stroke="{RED}" stroke-dasharray="5,4" fill="none" marker-end="url(#ar)"/>' + text(318, 160, "fuga", 10, RED, "start")
    b += f'<circle cx="190" cy="170" r="16" fill="{BLUE}"/>' + text(190, 174, "você", 9, "#fff", weight="bold")
    b += arrow(206, 175, 262, 200, BLUE, "ab") + text(200, 215, "passo lateral", 10, BLUE)
    b += f'<path d="M150,170 L120,110" stroke="{GRAY}" stroke-dasharray="4,4" marker-end="url(#a)"/>' + text(110, 100, "NÃO siga atrás", 10, GRAY)
    b += text(200, 280, "vá para onde ele VAI, não para onde ele está · jab fecha a saída", 11, GRAY)
    return svg(400, 292, b, "Cortar o ringue")


ALL = {
    "base": base, "step-drag": step_drag, "pivo": pivot, "caixa": box_drill, "x-drill": x_drill,
    "slip": slip, "bob-weave": bob_weave, "trajetorias": punches, "cadeia-cinetica": kinetic, "cortar-ringue": cut_ring,
}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, fn in ALL.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("ok", name)
