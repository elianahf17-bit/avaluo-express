# Genera ilustraciones ficticias (SVG) para las propiedades. Ejecutar una vez: python gen_images.py
import os
os.makedirs("static/img", exist_ok=True)
P = {"lote-escazu": ("terreno", "#fde68a", "#86efac"), "local-desamparados": ("local", "#bae6fd", "#d4d4d8"),
     "casa-atenas": ("casa", "#bbf7d0", "#a3e635"), "finca-santacruz": ("finca", "#fed7aa", "#bef264"),
     "lote-puntarenas": ("mar", "#a5f3fc", "#fcd34d"), "casa-cartago": ("casa", "#e0e7ff", "#86efac")}
def casa():
    return ('<rect x="200" y="190" width="200" height="120" fill="#fff" stroke="#065f46" stroke-width="4"/>'
            '<polygon points="180,195 300,110 420,195" fill="#b91c1c"/><rect x="280" y="240" width="45" height="70" fill="#92400e"/>'
            '<rect x="220" y="215" width="40" height="35" fill="#7dd3fc"/><rect x="345" y="215" width="40" height="35" fill="#7dd3fc"/>')
def local():
    return ('<rect x="170" y="150" width="260" height="160" fill="#fff" stroke="#1f2937" stroke-width="4"/>'
            '<rect x="170" y="150" width="260" height="30" fill="#065f46"/><path d="M170 180h260l-15 25h-230z" fill="#dc2626"/>'
            '<rect x="205" y="225" width="100" height="85" fill="#7dd3fc"/><rect x="335" y="225" width="55" height="85" fill="#92400e"/>')
def finca():
    return ('<rect x="330" y="170" width="150" height="130" fill="#b91c1c"/><polygon points="320,175 405,120 490,175" fill="#7f1d1d"/>'
            '<rect x="385" y="230" width="40" height="70" fill="#fff"/>' +
            ''.join(f'<rect x="{60+i*40}" y="270" width="6" height="45" fill="#78350f"/>' for i in range(7)) +
            '<rect x="60" y="282" width="246" height="6" fill="#78350f"/><rect x="60" y="298" width="246" height="6" fill="#78350f"/>')
def terreno():
    return ('<polygon points="120,320 480,320 440,250 160,250" fill="#4ade80" stroke="#166534" stroke-width="3"/>'
            '<rect x="290" y="190" width="8" height="70" fill="#78350f"/><rect x="250" y="170" width="100" height="35" fill="#fff" stroke="#065f46" stroke-width="3"/>'
            '<text x="300" y="194" font-size="18" font-family="Arial" font-weight="bold" fill="#065f46" text-anchor="middle">SE VENDE</text>')
def mar():
    return '<rect y="190" width="600" height="70" fill="#38bdf8"/>' + terreno()
F = {"casa": casa, "local": local, "finca": finca, "terreno": terreno, "mar": mar}
for n, (k, sky, gr) in P.items():
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{sky}"/><stop offset="1" stop-color="#fff"/></linearGradient></defs>'
         f'<rect width="600" height="400" fill="url(#g)"/><circle cx="500" cy="80" r="38" fill="#fbbf24"/>'
         f'<path d="M0 290 Q150 230 300 285 T600 270 V400 H0Z" fill="{gr}"/>{F[k]()}</svg>')
    open(f"static/img/{n}.svg", "w", encoding="utf-8").write(s)
