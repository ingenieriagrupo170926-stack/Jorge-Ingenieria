"""Validación del solver de referencia contra casos publicados.

  python3 validar.py            -> imprime tablas y guarda resultados_validacion.md

Casos:
  V1  Fredlund & Krahn (1977) = Slide2 VP#21: círculo fijo, seco / ru=0.25 / línea piezométrica.
  V2  Identidades internas: Spencer == M-P con f=1; momento independiente del punto; Janbu == F_f(0).
  V3  ACADS 1(a) (Donald & Giam 1989) = Slide2 VP#1: búsqueda del círculo crítico.
  V4  Optimización poligonal a partir del círculo crítico de V3.
"""
import time
import numpy as np
from lem_ref import Modelo, Capa, circulo, poligonal, resolver, marcha, momento, gle, janbu, espejo, \
    buscar_circular, optimizar_poligonal

out = []
def p(s=''): print(s); out.append(s)

# ---------------------------------------------------------------- V1 Fredlund & Krahn (1977)
# Terreno original (mira a la derecha): (0,60) (60,60) (140,20) (180,20); c'=600 psf, phi'=20°, g=120 pcf,
# círculo centro (120,90) R=80. Se refleja respecto de x=90 para que mire a la izquierda.
T = espejo([(0, 60), (60, 60), (140, 20), (180, 20)], 90)
PZ = espejo([(0, 40), (140, 20), (180, 20)], 90)
xc, yc, R = 180 - 120, 90, 80
ref = {  # F&K (1977) publicados | xslope 0.5.2 con 50 dovelas (ejecutado en esta sesión)
    'seco':  dict(bishop=(2.080, 2.0749), janbu=(None, 1.8747), spencer=(2.073, 2.0710), mp=(2.076, 2.0706)),
    'ru':    dict(bishop=(1.766, 1.7585), janbu=(None, 1.5865), spencer=(1.761, 1.7565), mp=(1.764, 1.7559)),
    'freat': dict(bishop=(1.834, 1.8283), janbu=(None, 1.6755), spencer=(1.830, 1.8268), mp=(1.832, 1.8261)),
}
casos = {'seco': Modelo([Capa(T, 120, 600, 20)], gw=62.4),
         'ru': Modelo([Capa(T, 120, 600, 20)], ru=0.25, gw=62.4),
         'freat': Modelo([Capa(T, 120, 600, 20)], piezo=PZ, gw=62.4)}
p('## V1 — Fredlund & Krahn (1977) / Slide2 VP#21 — círculo fijo (120, 90), R = 80 ft, 50 dovelas\n')
p('| Caso | Método | Este solver | F&K 1977 | Δ vs F&K | xslope | Δ vs xslope | extra |')
p('|---|---|---|---|---|---|---|---|')
for nombre, m in casos.items():
    d = circulo(m, xc, yc, R, n=50)
    for met in ('bishop', 'janbu', 'janbu_corregido', 'spencer', 'mp'):
        r = resolver(d, met, xc, yc); fk, xs = ref[nombre].get(met, (None, None))
        extra = (f"f0={r['f0']:.4f}, d/L={r['d_L']:.3f}, b1={r['b1']}" if met == 'janbu_corregido' else
                 f"θ={r['theta']:.2f}°" if met == 'spencer' else f"λ={r['lam']:.3f} (semiseno)" if met == 'mp' else '')
        pct = lambda a, b: f'{100 * (a - b) / b:+.2f} %' if b else '—'
        p(f"| {nombre} | {met} | {r['F']:.4f} | {fk or '—'} | {pct(r['F'], fk)} | {xs or '—'} | {pct(r['F'], xs)} | {extra} |")

# ---------------------------------------------------------------- V2 identidades
p('\n## V2 — Identidades internas (caso F&K seco)\n')
d = circulo(casos['seco'], xc, yc, R, n=50)
s1, s2 = gle(d, xc, yc, 'constante'), gle(d, 300.0, 500.0, 'constante')
m1 = gle(d, xc, yc, lambda s: np.ones_like(s))
p(f"- Spencer con punto de momentos en el centro vs en (300, 500): {s1['F']:.6f} vs {s2['F']:.6f} "
  f"(|Δ| = {abs(s1['F'] - s2['F']):.1e}) → el resultado riguroso no depende del punto de momentos.")
p(f"- M-P con f(x)=1 (función de usuario) vs Spencer: {m1['F']:.6f} vs {s1['F']:.6f} (λ = {m1['lam']:.5f} = tanθ).")
Fj = janbu(d)['F']; N, E, S = marcha(d, Fj, 0 * d['ybase'])
Fcl = np.sum(S * Fj * np.cos(d['a'])) / np.sum(N * np.sin(d['a']))
p(f"- Janbu simplificado por recurrencia (E_n = 0) vs fórmula cerrada ΣS·cosα / ΣN·sinα: {Fj:.6f} vs {Fcl:.6f}.")
p(f"- Equilibrio residual en la solución Spencer: E_n/ΣW = "
  f"{marcha(d, s1['F'], s1['lam'] * np.ones(len(d['ybase'])))[1][-1] / d['W'].sum():.1e}, "
  f"M/(ΣW·L) = {momento(d, *marcha(d, s1['F'], s1['lam'] * np.ones(len(d['ybase'])))[::2], xc, yc) / (d['W'].sum() * 80):.1e}")

# ---------------------------------------------------------------- V3 ACADS 1(a)
p('\n## V3 — ACADS 1(a) / Slide2 VP#1 — búsqueda circular (c\'=3 kPa, φ\'=19.6°, γ=20 kN/m³)\n')
A = Modelo([Capa([(0, 25), (30, 25), (50, 35), (90, 35)], 20, 3, 19.6)])
p('| Método | F mínimo | Círculo crítico (xc, yc, R) | ACADS (consenso) | Slide2 | xslope | tiempo |')
p('|---|---|---|---|---|---|---|')
refs = {"bishop": ("1.00", "0.987", "0.985"), "janbu_corregido": ("1.00", "—", "0.986 ('Janbu' de xslope, con f0)"), "spencer": ("1.00", "—", "0.984")}
crit = {}
for met, nx in (('bishop', 20), ('janbu_corregido', 20), ('spencer', 6)):
    t0 = time.time(); F, cir = buscar_circular(A, met, nx=nx, ny=nx, nr=10, n=40); crit[met] = cir
    p(f"| {met} | {F:.4f} | ({cir[0]:.2f}, {cir[1]:.2f}, {cir[2]:.2f}) | {refs[met][0]} | {refs[met][1]} | {refs[met][2]} | {time.time() - t0:.0f} s |")

# ---------------------------------------------------------------- V4 poligonal
p('\n## V4 — Optimización poligonal (8 vértices) desde el círculo crítico Spencer de V3\n')
xc3, yc3, R3 = crit['spencer']; dc = circulo(A, xc3, yc3, R3, n=40)
xs = np.linspace(dc['xl'][0], dc['xr'][-1], 8); pts = list(zip(xs, yc3 - np.sqrt(np.clip(R3 ** 2 - (xs - xc3) ** 2, 0, None))))
F0 = resolver(poligonal(A, pts, 40), 'spencer')['F']
t0 = time.time(); F1, pts1 = optimizar_poligonal(A, pts, 'spencer', n=40)
p(f"- Spencer sobre la poligonal inscrita en el círculo: {F0:.4f}; tras optimizar: {F1:.4f} ({time.time() - t0:.0f} s).")
p(f"- Vértices optimizados: {[(round(float(x), 2), round(float(y), 2)) for x, y in pts1]}")

open('resultados_validacion.md', 'w').write('# Resultados de validación (generado por validar.py)\n\n' + '\n'.join(out) + '\n')
