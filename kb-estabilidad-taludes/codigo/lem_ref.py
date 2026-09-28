"""Solver de referencia de equilibrio límite 2D (método de dovelas).

Sirve para VALIDAR la base teórica, no es un producto. Implementa, sobre una única
recurrencia de fuerzas entre dovelas (teoria/03-marco-comun-dovelas.md):
  - Bishop simplificado   : momento (círculo), X = 0
  - Janbu simplificado    : fuerza horizontal, X = 0          (= F_f(λ=0) de GLE)
  - Janbu corregido       : f0 · Janbu simplificado
  - Spencer               : fuerza + momento, X/E = λ constante (f(x)=1)
  - Morgenstern-Price/GLE : fuerza + momento, X/E = λ·f(x)
y una búsqueda circular (malla + radios + Nelder-Mead) y una optimización poligonal.

Convención: el talud mira a la izquierda (pie a la izquierda, corona a la derecha) y la
masa desliza hacia -x. Para un talud que mira a la derecha use espejo() antes.
Unidades coherentes cualesquiera (SI: kN, m, kPa, gw=9.81 | imperial: lb, ft, psf, gw=62.4).
"""
from dataclasses import dataclass, field
import numpy as np
from scipy.optimize import brentq, minimize

np.seterr(divide='ignore', invalid='ignore')


def yint(linea, x):
    """y(x) de una polilínea [(x, y), ...]; nan fuera de su rango."""
    p = np.asarray(linea, float)
    return np.interp(x, p[:, 0], p[:, 1], left=np.nan, right=np.nan)


def espejo(linea, x0=0.0):
    """Refleja una polilínea respecto de x = x0 (para taludes que miran a la derecha)."""
    return [(2 * x0 - x, y) for x, y in reversed(linea)]


@dataclass
class Capa:
    techo: list      # polilínea superior del material; se extiende hasta el techo de la capa siguiente
    g: float         # peso unitario total
    c: float         # cohesión efectiva (o Su si phi = 0)
    phi: float       # ángulo de fricción [°]


@dataclass
class Modelo:
    capas: list                      # de arriba hacia abajo; capas[0].techo = superficie del terreno
    piezo: list = None               # línea piezométrica -> u = gw·(y_p - y_base)
    ru: float = 0.0                  # alternativa: u = ru·sigma_v
    kh: float = 0.0                  # coeficiente sísmico horizontal (actúa hacia -x)
    gw: float = 9.81
    q: list = field(default_factory=list)   # sobrecargas verticales [(x1, x2, q)]

    @property
    def terreno(self):
        return self.capas[0].techo


def dovelas(m, ybase, xa, xb, n=50, extra=()):
    """Discretiza la masa entre xa y xb. ybase(x) vectorizada. Devuelve dict de arrays o None."""
    lineas = [c.techo for c in m.capas] + ([m.piezo] if m.piezo else [])
    xs = np.unique(np.r_[xa, xb, [x for L in lineas for x, _ in L], list(extra)])
    xs = xs[(xs >= xa) & (xs <= xb)]
    bordes = [xa]
    for x0, x1 in zip(xs[:-1], xs[1:]):              # ninguna dovela cruza un quiebre
        if x1 - x0 > 1e-9:
            bordes += list(np.linspace(x0, x1, max(1, round(n * (x1 - x0) / (xb - xa))) + 1)[1:])
    xl, xr = np.array(bordes[:-1]), np.array(bordes[1:])
    xm, b = (xl + xr) / 2, xr - xl
    ybl, ybr = ybase(xl), ybase(xr)
    yb, a = (ybl + ybr) / 2, np.arctan2(ybr - ybl, b)
    yt = yint(m.terreno, xm)
    if not np.all(np.isfinite(yt)) or np.any(yt - yb <= 1e-9):
        return None                                  # superficie fuera del terreno
    techos = np.minimum.accumulate([np.minimum(yint(c.techo, xm), yt) for c in m.capas])
    pisos = np.vstack([techos[1:], np.full(len(xm), -np.inf)])
    t = np.clip(np.minimum(techos, yt) - np.maximum(pisos, yb), 0, None)       # espesores por capa
    g = np.array([c.g for c in m.capas])[:, None]
    sv = (g * t).sum(0)                                                         # tensión vertical
    k = np.argmax((pisos < yb + 1e-6) & (techos >= yb + 1e-6), axis=0)          # capa en la base
    c = np.array([m.capas[i].c for i in k]); phi = np.radians([m.capas[i].phi for i in k])
    u = m.ru * sv if m.piezo is None else m.gw * np.clip(yint(m.piezo, xm) - yb, 0, None)
    Q = sum(qq * np.clip(np.minimum(xr, x2) - np.maximum(xl, x1), 0, None) for x1, x2, qq in m.q)
    yg = (g * t * (np.minimum(techos, yt) + np.maximum(pisos, yb)) / 2).sum(0) / np.where(sv > 0, sv, 1)
    return dict(xl=xl, xr=xr, xm=xm, b=b, yb=yb, a=a, l=b / np.cos(a), W=b * sv, yg=yg, yt=yt,
                c=c, phi=phi, u=np.nan_to_num(u), Q=Q + 0 * b, kW=m.kh * b * sv, ybase=ybase(bordes))


def marcha(d, F, t):
    """Equilibrio horizontal + vertical dovela a dovela, desde el pie (E0 = 0).
    t = tan(theta) en los n+1 bordes. Devuelve N (normal total), E (n+1) y S movilizada."""
    ca, sa, tp = np.cos(d['a']), np.sin(d['a']), np.tan(d['phi'])
    A, s0, V, kW = tp / F, (d['c'] - d['u'] * tp) * d['l'] / F, d['W'] + d['Q'], d['kW']
    if not np.any(t):                                # X = 0: forma cerrada (Bishop/Janbu)
        N = (V - s0 * sa) / (ca + A * sa)
        E = np.r_[0, np.cumsum(N * (A * ca - sa) + s0 * ca - kW)]
        return N, E, s0 + A * N
    N, E = np.empty(len(ca)), np.zeros(len(ca) + 1)
    for i in range(len(ca)):
        N[i] = (V[i] - s0[i] * sa[i] + t[i + 1] * (s0[i] * ca[i] - kW[i]) + E[i] * (t[i + 1] - t[i])) \
            / (ca[i] + A[i] * sa[i] + t[i + 1] * (sa[i] - A[i] * ca[i]))
        E[i + 1] = E[i] + N[i] * (A[i] * ca[i] - sa[i]) + s0[i] * ca[i] - kW[i]
    return N, E, s0 + A * N


def momento(d, N, S, xo, yo):
    """Momento (antihorario +) de W, kW, N, S y Q respecto de (xo, yo)."""
    ca, sa, dx = np.cos(d['a']), np.sin(d['a']), d['xm'] - xo
    return np.sum(-dx * (d['W'] + d['Q']) + (d['yg'] - yo) * d['kW']
                  + dx * (N * ca + S * sa) + (d['yb'] - yo) * (N * sa - S * ca))


def malfa_ok(d, F, lim=0.2):
    """Admisibilidad de Whitman & Bailey (1967): m_alpha >= 0.2 en todas las dovelas."""
    return np.min(np.cos(d['a']) + np.sin(d['a']) * np.tan(d['phi']) / F) >= lim


def raiz(fun, hi=20.0, lo=0.05, k=50, tol=1e-6, ok=lambda r: True):
    """Primera raíz bajando desde F alto. Descarta los cambios de signo que son polos
    (denominador de N -> 0, típico de m_alpha a F pequeño): exige |fun(raíz)| < tol y ok(raíz)."""
    xs = np.geomspace(hi, lo, k); y0 = fun(xs[0])
    for x0, x1 in zip(xs[:-1], xs[1:]):
        y1 = fun(x1)
        if np.isfinite(y0) and np.isfinite(y1) and y0 * y1 <= 0:
            try:
                r = brentq(fun, x1, x0, xtol=1e-12)
                if abs(fun(r)) < tol and ok(r): return r
            except ValueError:
                pass
        y0 = y1
    return np.nan


def f_x(d, tipo='semiseno'):
    """Función entre dovelas f(x) en los n+1 bordes (x normalizado 0..1)."""
    x = np.r_[d['xl'], d['xr'][-1]]; s = (x - x[0]) / (x[-1] - x[0])
    if callable(tipo): return tipo(s)
    return {'constante': np.ones_like(s), 'semiseno': np.sin(np.pi * s),
            'trapecio': np.clip(np.minimum(s, 1 - s) / 0.25, 0, 1)}[tipo]


def janbu(d, corregido=False, b1=(0.69, 0.50, 0.31)):
    Wt = d['W'].sum()
    F = raiz(lambda F: marcha(d, F, 0 * d['ybase'])[1][-1] / Wt, ok=lambda F: malfa_ok(d, F))
    if not corregido: return dict(F=F)
    xb = np.r_[d['xl'], d['xr'][-1]]; p0, p1 = np.array([xb[0], d['ybase'][0]]), np.array([xb[-1], d['ybase'][-1]])
    L = np.linalg.norm(p1 - p0)
    dist = np.abs(np.cross(p1 - p0, np.c_[xb, d['ybase']] - p0)) / L
    r = min(dist.max() / L, 1 / 2.8)                     # el ajuste polinómico vale hasta su máximo
    solo_c, solo_phi = np.all(d['phi'] == 0), np.all(d['c'] == 0)
    bb = b1[0] if solo_c else b1[2] if solo_phi else b1[1]
    f0 = 1 + bb * (r - 1.4 * r * r)
    return dict(F=f0 * F, F_simple=F, f0=f0, d_L=dist.max() / L, b1=bb)


def bishop(d, xo, yo):
    return dict(F=raiz(lambda F: momento(d, *marcha(d, F, 0 * d['ybase'])[::2], xo, yo) / d['W'].sum(),
                       ok=lambda F: malfa_ok(d, F)))


def gle(d, xo, yo, fx='semiseno', lams=np.linspace(-1.0, 1.0, 21)):
    """Morgenstern-Price / GLE (fx='constante' -> Spencer). Resuelve F_f(λ) y h(λ)=M(F_f(λ),λ)=0."""
    f, Wt = f_x(d, fx), d['W'].sum(); Lr = d['xr'][-1] - d['xl'][0]
    def ff(lam): return raiz(lambda F: marcha(d, F, lam * f)[1][-1] / Wt, ok=lambda F: malfa_ok(d, F))
    def h(lam):
        F = ff(lam)
        if not np.isfinite(F): return np.nan
        N, E, S = marcha(d, F, lam * f); return momento(d, N, S, xo, yo) / (Wt * Lr)
    hs = [h(l) for l in lams]; sols = []
    for l0, l1, h0, h1 in zip(lams[:-1], lams[1:], hs[:-1], hs[1:]):
        if np.isfinite(h0) and np.isfinite(h1) and h0 * h1 <= 0:
            try: lam = brentq(h, l0, l1, xtol=1e-10)
            except ValueError: continue                   # tramo con λ sin solución F_f (polo)
            F = ff(lam); E = marcha(d, F, lam * f)[1][1:-1]
            if not (np.isfinite(F) and abs(h(lam)) < 1e-6): continue
            sols.append((np.mean(E < 0) > 0.25, abs(lam), dict(F=F, lam=lam, tension=float(np.mean(E < 0)),
                         theta=np.degrees(np.arctan(lam)) if fx == 'constante' else None)))
    return min(sols, key=lambda s: s[:2])[2] if sols else dict(F=np.nan)


def spencer(d, xo, yo): return gle(d, xo, yo, 'constante')


# ---------------------------------------------------------------- superficies
def circulo(m, xc, yc, R, n=50):
    """Dovelas de un círculo: extremos = intersecciones del arco inferior con el terreno."""
    xi = []
    for (x0, y0), (x1, y1) in zip(m.terreno[:-1], m.terreno[1:]):
        dx, dy = x1 - x0, y1 - y0; fx, fy = x0 - xc, y0 - yc
        A, B, C = dx * dx + dy * dy, 2 * (fx * dx + fy * dy), fx * fx + fy * fy - R * R
        disc = B * B - 4 * A * C
        if disc < 0: continue
        for s in ((-B - disc ** .5) / (2 * A), (-B + disc ** .5) / (2 * A)):
            if 0 <= s <= 1 and y0 + s * dy < yc: xi.append(x0 + s * dx)
    if len(xi) < 2: return None
    return dovelas(m, lambda x: yc - np.sqrt(np.clip(R * R - (np.asarray(x) - xc) ** 2, 0, None)), min(xi), max(xi), n)


def poligonal(m, pts, n=50):
    pts = sorted(pts); return dovelas(m, lambda x: yint(pts, x), pts[0][0], pts[-1][0], n, [x for x, _ in pts])


def resolver(d, metodo, xo=None, yo=None):
    """Punto de momentos: centro del círculo si existe; en GLE/Spencer da igual (ΣF = 0)."""
    if xo is None: xo, yo = d['xm'].mean(), d['yt'].max() + (d['xr'][-1] - d['xl'][0])
    return {'bishop': lambda: bishop(d, xo, yo), 'janbu': lambda: janbu(d),
            'janbu_corregido': lambda: janbu(d, True), 'spencer': lambda: spencer(d, xo, yo),
            'mp': lambda: gle(d, xo, yo)}[metodo]()


def buscar_circular(m, metodo='bishop', caja=None, nx=20, ny=20, nr=10, n=40):
    """Malla de centros × radios (regla tipo Slide2: radios entre la distancia al terreno y al
    límite más cercano) y refinamiento local Nelder-Mead de (xc, yc, R)."""
    T = np.asarray(m.terreno, float); H = np.ptp(T[:, 1])
    if caja is None:                                 # caja automática sobre la cara del talud
        x0 = T[T[:, 1] == T[:, 1].min(), 0].max(); x1 = T[T[:, 1] == T[:, 1].max(), 0].min()   # pie, corona
        caja = (x0 - 0.5 * H, x1 + H, T[:, 1].max() + 0.1 * H, T[:, 1].max() + 2 * H)
    def dmin(xc, yc):  # distancia del centro a la polilínea del terreno
        P, D = T[:-1], np.diff(T, axis=0); s = np.clip(((np.array([xc, yc]) - P) * D).sum(1) / (D * D).sum(1), 0, 1)
        return np.min(np.hypot(*(P + s[:, None] * D - [xc, yc]).T))
    def fs(p):
        d = circulo(m, *p, n=n)
        if d is None: return 1e9
        F = resolver(d, metodo, p[0], p[1])['F']; return F if np.isfinite(F) and F > 0 else 1e9
    mejor = (1e9, None)
    for xc in np.linspace(caja[0], caja[1], nx + 1):
        for yc in np.linspace(caja[2], caja[3], ny + 1):
            r0, r1 = dmin(xc, yc), min(np.hypot(*(T[0] - [xc, yc])), np.hypot(*(T[-1] - [xc, yc])))
            for R in np.linspace(r0 + 0.05 * (r1 - r0), r1 - 0.05 * (r1 - r0), nr + 1):
                F = fs((xc, yc, R)); mejor = min(mejor, (F, (xc, yc, R)), key=lambda z: z[0])
    res = minimize(fs, mejor[1], method='Nelder-Mead', options=dict(xatol=1e-3, fatol=1e-5, maxiter=400))
    return (res.fun, tuple(res.x)) if res.fun < mejor[0] else mejor


def optimizar_poligonal(m, pts0, metodo='spencer', n=40):
    """Optimización local de una poligonal: x de los extremos (sobre el terreno) e y de los vértices
    interiores (x equiespaciados). Equivale al 'Optimize Surfaces' / movimiento de vértices de GEO5."""
    pts0 = sorted(pts0); k = len(pts0)
    def armar(v):
        xa, xb = v[0], v[1]; xs = np.linspace(xa, xb, k)
        return list(zip(xs, np.r_[yint(m.terreno, xa), v[2:], yint(m.terreno, xb)]))
    def fs(v):
        if not v[0] < v[1]: return 1e9
        d = poligonal(m, armar(v), n)
        if d is None: return 1e9
        F = resolver(d, metodo)['F']; return F if np.isfinite(F) and F > 0 else 1e9
    v0 = np.r_[pts0[0][0], pts0[-1][0], [y for _, y in pts0[1:-1]]]
    res = minimize(fs, v0, method='Nelder-Mead', options=dict(xatol=1e-3, fatol=1e-5, maxiter=3000, adaptive=True))
    return res.fun, armar(res.x)
