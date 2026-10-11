"""Gera as aulas em Markdown e os PDFs.

Uso:  python3 tools/build.py      (depois: node tools/print.js)
Requer: reportlab (QR codes) e pandoc (Markdown -> HTML).
"""
import html
import re
import subprocess
from pathlib import Path

from reportlab.graphics import renderSVG
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing

import content as C
import diagrams

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
AULAS = ROOT / "plano" / "iniciante" / "aulas"
BUILD = ROOT / "tools" / "_build"
PHASE_NAME = {1: "Fase 1 — Fundação", 2: "Fase 2 — Arsenal", 3: "Fase 3 — Integração"}
ROUND_FMT = {1: "2 min / 1 min", 2: "2:30 → 3 min / 1 min", 3: "3 min / 1 min"}


def esc(s):
    return html.escape(s, quote=False)


def qr_svg(url, size=78):
    w = QrCodeWidget(url)
    w.barBorder = 1
    b = w.getBounds()
    bw, bh = b[2] - b[0], b[3] - b[1]
    d = Drawing(size, size, transform=[size / bw, 0, 0, size / bh, 0, 0])
    d.add(w)
    s = renderSVG.drawToString(d)
    return s[s.index("<svg"):]


def strength_lines(s):
    if s.get("strength_override"):
        return "", [s["strength_override"]]
    t, lines = C.STRENGTH[s["phase"]]
    return t, lines


# ---------------------------------------------------------------- Markdown das aulas
def session_md(s):
    o = [f"# Aula {s['id']} — {s['title']}", "",
         f"**Semana {s['week']} · {PHASE_NAME[s['phase']]} · Sessão solo de 60 min**", "",
         f"**Objetivo:** {s['goal']}", ""]
    if s["pre"]:
        o += ["## Antes da aula: assistir", ""]
        o += [f"- [{C.V[v][0]}]({C.V[v][3]}) — {C.V[v][1]} ({C.V[v][2]})" for v in s["pre"]] + [""]
    o += ["## A. Aquecimento (10 min)", ""] + [f"- {x}" for x in C.WARMUP[s["phase"]]] + [""]
    o += ["## B. Técnica", ""]
    for name, mins, how, cues, diag, vids in s["tech"]:
        o += [f"### {name} ({mins} min)", ""] + [f"{i}. {x}" for i, x in enumerate(how, 1)] + [""]
        if cues:
            o += ["**Pontos-chave:** " + " · ".join(cues), ""]
        if diag:
            o += [f"![{name}](../../../img/{diag}.svg)", ""]
    for extra in s.get("diagrams_extra", []):
        o += [f"![diagrama](../../../img/{extra}.svg)", ""]
    if s["shadow"]:
        fmt, rounds = s["shadow"]
        o += [f"## C. Shadowboxing ({fmt})", ""] + [f"- {r}" for r in rounds] + [""]
    t, lines = strength_lines(s)
    o += ["## D. Força e condicionamento (12 min)", ""] + ([f"*{t}*", ""] if t else []) + [f"- {x}" for x in lines] + [""]
    o += ["## E. " + C.COOLDOWN, "", "## Foco para levar à aula em grupo", "", f"> {s['focus']}", ""]
    o += ["---", "[← índice das aulas](README.md)", ""]
    return "\n".join(o)


def write_md():
    AULAS.mkdir(parents=True, exist_ok=True)
    idx = ["# Guia aula a aula — Nível Iniciante", "",
           "As 24 sessões solo, uma por arquivo. Também em PDF: [`pdf/02-guia-aula-a-aula-iniciante.pdf`](../../../pdf/02-guia-aula-a-aula-iniciante.pdf).", "",
           "Gerado por `tools/build.py` a partir de `tools/content.py`. Para editar, mude o `content.py` e rode de novo.", "",
           "| Aula | Semana | Fase | Tema |", "|---|---|---|---|"]
    for s in C.S:
        (AULAS / f"{s['id']}.md").write_text(session_md(s), encoding="utf-8")
        idx.append(f"| [{s['id']}]({s['id']}.md) | {s['week']} | {s['phase']} | {s['title']} |")
    (AULAS / "README.md").write_text("\n".join(idx) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- HTML / CSS
CSS = """
@page { size: A4; margin: 14mm 14mm 16mm 14mm; }
* { box-sizing: border-box; }
body { font-family: Helvetica, Arial, sans-serif; color:#111827; font-size: 10.5pt; line-height: 1.38; }
h1 { font-size: 20pt; margin: 0 0 4mm; color:#111827; }
h2 { break-after: avoid; page-break-after: avoid; font-size: 13pt; margin: 5mm 0 2mm; padding-bottom: 1mm; border-bottom: 2px solid #dc2626; }
h3 { font-size: 11pt; margin: 3mm 0 1mm; }
p, li { margin: 0 0 1.2mm; }
ul, ol { margin: 0 0 2mm 5mm; padding-left: 3mm; }
a { color:#1d4ed8; text-decoration:none; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 3mm; font-size: 9.5pt; page-break-inside: avoid; }
th, td { border: 1px solid #d1d5db; padding: 1.2mm 2mm; vertical-align: top; text-align: left; }
th { background:#f3f4f6; }
blockquote { margin: 2mm 0; padding: 2mm 3mm; background:#fef2f2; border-left: 4px solid #dc2626; }
img { max-width: 100%; max-height: 85mm; width: auto; height: auto; display:block; margin: 2mm auto; page-break-inside: avoid; }
code { background:#f3f4f6; padding: 0 1mm; border-radius: 2px; font-size: 9pt; }
pre { background:#f3f4f6; padding: 2mm; font-size: 8.5pt; white-space: pre-wrap; }
.page { page-break-after: always; }
.cover { height: 260mm; display:flex; flex-direction:column; justify-content:center; text-align:center; }
.cover h1 { font-size: 34pt; margin-bottom: 6mm; }
.cover .sub { font-size: 14pt; color:#4b5563; }
.cover .tag { margin-top: 14mm; font-size: 11pt; color:#6b7280; }
.belt { height: 6mm; background: linear-gradient(90deg,#dc2626,#111827); margin: 8mm 30mm; border-radius: 3mm; }
.hdr { display:flex; justify-content:space-between; align-items:baseline; border-bottom: 3px solid #111827; padding-bottom: 1.5mm; margin-bottom: 2mm; }
.hdr .id { font-size: 22pt; font-weight: bold; color:#dc2626; }
.hdr .meta { font-size: 9.5pt; color:#4b5563; text-align:right; }
.goal { background:#eff6ff; border-left: 4px solid #2563eb; padding: 2mm 3mm; margin: 2mm 0 3mm; }
.timeline { display:flex; gap: 1mm; margin: 2mm 0 3mm; font-size: 8.5pt; }
.timeline div { flex: var(--w); padding: 1.2mm 1.5mm; color:#fff; border-radius: 1.5mm; text-align:center; }
.drill { border: 1px solid #e5e7eb; border-radius: 2mm; padding: 2mm 3mm; margin: 2mm 0; page-break-inside: avoid; }
.drill h3 { margin-top: 0; }
.drill h3 span { color:#6b7280; font-weight: normal; }
.cues { font-size: 9.5pt; color:#065f46; background:#ecfdf5; padding: 1mm 2mm; border-radius: 1.5mm; margin-top: 1mm; }
.videos { display:flex; flex-wrap: wrap; gap: 3mm; margin: 1mm 0 2mm; }
.vid { display:flex; gap: 2mm; align-items:center; width: 57mm; border: 1px solid #e5e7eb; border-radius: 2mm; padding: 1.5mm; page-break-inside: avoid; }
.vid svg { width: 18mm; height: 18mm; flex: none; }
.drill svg { max-height: 52mm; width: auto !important; }
.vid .t { font-size: 8.8pt; line-height: 1.25; }
.vid .w { color:#6b7280; font-size: 8pt; }
.check { display:grid; grid-template-columns: 1fr 1fr; gap: 1mm 6mm; font-size: 9.5pt; }
.box { border: 1px dashed #9ca3af; border-radius: 2mm; padding: 2mm 3mm; margin-top: 2mm; font-size: 9.5pt; }
.line { border-bottom: 1px solid #d1d5db; height: 6mm; }
.small { font-size: 8.5pt; color:#6b7280; }
.focus { background:#111827; color:#fff; padding: 2mm 3mm; border-radius: 2mm; margin-top: 2mm; }
.focus b { color:#fca5a5; }
"""


def page(title, body):
    return f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>{esc(title)}</title><style>{CSS}</style></head><body>{body}</body></html>"


def img_inline(name):
    return (IMG / f"{name}.svg").read_text(encoding="utf-8").replace("<svg ", "<svg style='max-width:100%;height:auto;display:block;margin:2mm auto' ", 1)


def vid_card(v):
    t, who, cred, url = C.V[v]
    return f"<div class='vid'>{qr_svg(url)}<div class='t'><b>{esc(t)}</b><br><span class='w'>{esc(who)} · {esc(cred)}</span><br><a href='{url}'>abrir vídeo</a></div></div>"


def session_html(s):
    b = [f"<div class='page'><div class='hdr'><div><span class='id'>Aula {s['id']}</span> &nbsp;<b style='font-size:15pt'>{esc(s['title'])}</b></div>"
         f"<div class='meta'>Semana {s['week']} · {PHASE_NAME[s['phase']]}<br>Sessão solo · 60 min</div></div>"]
    b.append(f"<div class='goal'><b>Objetivo:</b> {esc(s['goal'])}</div>")
    tech_min = sum(d[1] for d in s["tech"])
    blocks = [("A · Aquecimento", 10, "#6b7280"), ("B · Técnica", tech_min if s["shadow"] else tech_min, "#2563eb")]
    if s["shadow"]:
        blocks.append(("C · Shadow", 15, "#7c3aed"))
    blocks += [("D · Força", 12 if not s.get("strength_override") else 5, "#dc2626"), ("E", 3, "#111827")]
    b.append("<div class='timeline'>" + "".join(f"<div style='--w:{m};background:{c}'>{esc(n)} · {m}′</div>" for n, m, c in blocks) + "</div>")
    if s["pre"]:
        b.append("<h2>Antes da aula: assistir (aponte a câmera do celular para o QR)</h2><div class='videos'>" + "".join(vid_card(v) for v in s["pre"]) + "</div>")
    b.append("<h2>A · Aquecimento (10 min)</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in C.WARMUP[s["phase"]]) + "</ul>")
    b.append(f"<h2>B · Técnica ({tech_min} min) — no espelho, filmando</h2>")
    for name, mins, how, cues, diag, vids in s["tech"]:
        d = f"<div class='drill'><h3>{esc(name)} <span>· {mins} min</span></h3><ol>" + "".join(f"<li>{esc(x)}</li>" for x in how) + "</ol>"
        if cues:
            d += "<div class='cues'>✔ " + " · ".join(esc(c) for c in cues) + "</div>"
        if diag:
            d += img_inline(diag)
        b.append(d + "</div>")
    for extra in s.get("diagrams_extra", []):
        b.append(img_inline(extra))
    if s["shadow"]:
        fmt, rounds = s["shadow"]
        b.append(f"<h2>C · Shadowboxing — {esc(fmt)}</h2><ul>" + "".join(f"<li>{esc(r)}</li>" for r in rounds) + "</ul>"
                 "<p class='small'>Regras: adversário imaginário com altura e estilo · tema por round · volta à guarda depois de cada golpe · respire em cada golpe.</p>")
    t, lines = strength_lines(s)
    b.append("<h2>D · Força e condicionamento</h2>" + (f"<p><i>{esc(t)}</i></p>" if t else "") + "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in lines) + "</ul>")
    b.append(f"<h2>E · Volta à calma e registro</h2><p>{esc(C.COOLDOWN)}</p>")
    b.append(f"<div class='focus'><b>FOCO NA AULA EM GRUPO DESTA SEMANA:</b> {esc(s['focus'])}</div>")
    b.append("<div class='box'><b>Registro</b> · data: ______ · esforço (1–10): ___ · ombro E antes/depois: ___ / ___ · completo ( ) parcial ( )"
             "<br>Melhor coisa: <div class='line'></div>Erro principal visto no vídeo: <div class='line'></div></div>")
    b.append("</div>")
    return "".join(b)


def md_to_html(md_paths):
    """Converte Markdown em HTML com pandoc, ajustando caminhos de imagem."""
    out = []
    for p in md_paths:
        r = subprocess.run(["pandoc", "-f", "gfm", "-t", "html", str(p)], capture_output=True, text=True, check=True)
        h = r.stdout

        def fix(m):
            src = (p.parent / m.group(1)).resolve()
            return f'src="file://{src}"'
        h = re.sub(r'src="([^"]+\.svg)"', fix, h)
        out.append(f"<div class='page'>{h}</div>")
    return "".join(out)


def cover(title, sub, extra=""):
    return (f"<div class='page cover'><div style='font-size:46pt'>🥊</div><h1>{esc(title)}</h1><div class='belt'></div>"
            f"<div class='sub'>{sub}</div><div class='tag'>{extra}</div></div>")


def build_html():
    BUILD.mkdir(exist_ok=True)
    who = "Atleta: 26 anos · 1,80 m · 70 kg · ortodoxo · objetivo: estreia amadora em abril/2027"
    # 00 — resumo e metodologia
    h = cover("Pesquisa, Metodologia e Plano de 6 Meses", "Boxe — do zero à elite", who)
    h += md_to_html([ROOT / "docs/03-pesquisa-e-metodologia.md", ROOT / "plano/6-meses.md", ROOT / "docs/00-metodo-e-regras.md"])
    (BUILD / "00-resumo-pesquisa-metodologia.html").write_text(page("Pesquisa e Metodologia", h), encoding="utf-8")

    # 01 — manual técnico
    h = cover("Manual Técnico", "Fundamentos, referências de campeões e biblioteca", who)
    h += md_to_html([ROOT / f for f in ["fundamentos/01-base-e-guarda.md", "fundamentos/02-footwork.md", "fundamentos/03-golpes.md",
                                         "fundamentos/04-defesa.md", "fundamentos/05-combinacoes-e-shadowboxing.md",
                                         "fundamentos/06-forca-e-condicionamento.md", "fundamentos/07-ombro.md",
                                         "docs/01-referencias-campeoes.md", "docs/02-biblioteca.md"]])
    (BUILD / "01-manual-tecnico.html").write_text(page("Manual Técnico", h), encoding="utf-8")

    # 02 — guia aula a aula
    h = cover("Guia Aula a Aula — Nível Iniciante", "12 semanas · 24 sessões solo · diagramas · QR codes dos vídeos", who)
    rows = "".join(f"<tr><td><b>{s['id']}</b></td><td>{s['week']}</td><td>{PHASE_NAME[s['phase']]}</td><td>{esc(s['title'])}</td><td style='width:14mm'>☐</td></tr>" for s in C.S)
    h += ("<div class='page'><h1>Como usar este guia</h1>"
          "<ul><li>Cada página é <b>uma sessão solo de 60 min</b>. <b>A</b> = 1º solo da semana (técnica nova, prioridade). <b>B</b> = 2º solo.</li>"
          "<li>Com só 1 solo na semana, faça o <b>A</b>.</li>"
          "<li>Antes da aula, assista os vídeos (QR code). Durante a aula, celular filmando e espelho.</li>"
          "<li>O plano avança por <b>critério</b>: avaliações nas aulas 04B, 08B e 12B.</li>"
          "<li><b>Ombro esquerdo:</b> o protocolo do aquecimento é obrigatório. Dor ≥ 5/10, pontada ou estalo com dor: pare e avise.</li>"
          "<li>Diagramas: vista de cima, adversário para o topo; pé esquerdo azul (E), direito vermelho (D).</li></ul>"
          "<h2>Semana-tipo</h2><table><tr><th>Seg</th><th>Ter</th><th>Qua</th><th>Qui</th><th>Sex</th><th>Sáb</th><th>Dom</th></tr>"
          "<tr><td>Aula</td><td><b>Solo A</b></td><td>Aula</td><td>descanso / corrida leve</td><td>Aula</td><td><b>Solo B</b></td><td>descanso</td></tr></table>"
          "<h2>Índice e checklist</h2><table><tr><th>Aula</th><th>Sem.</th><th>Fase</th><th>Tema</th><th>Feito</th></tr>" + rows + "</table></div>")
    h += "<div class='page'><h1>Numeração dos golpes e base</h1><table><tr><th>1</th><td>Jab</td><th>2</th><td>Direto</td><th>3</th><td>Gancho E</td></tr><tr><th>4</th><td>Gancho D</td><th>5</th><td>Uppercut E</td><th>6</th><td>Uppercut D</td></tr><tr><th>b</th><td colspan='5'>sufixo = no corpo (ex.: 3b)</td></tr></table>"
    h += img_inline("base") + img_inline("cadeia-cinetica") + img_inline("trajetorias") + "</div>"
    h += "".join(session_html(s) for s in C.S)
    h += md_to_html([ROOT / "avaliacoes/avaliacao-iniciante.md"])
    (BUILD / "02-guia-aula-a-aula-iniciante.html").write_text(page("Guia Aula a Aula", h), encoding="utf-8")


if __name__ == "__main__":
    for name, fn in diagrams.ALL.items():
        (IMG / f"{name}.svg").write_text(fn(), encoding="utf-8")
    write_md()
    build_html()
    print("ok")
