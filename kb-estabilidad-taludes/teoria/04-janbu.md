# 04 · Janbu: simplificado, corregido y generalizado

> Nodos del grafo: `janbu_simplificado`, `janbu_corregido`, `janbu_generalizado` · Nivel L3
> Estado: simplificado y corregido **verificados** (V1: coincide con xslope a 0.15 %);
> generalizado **documentado, no implementado** (fuente primaria Janbu 1973 no accesible).
>
> Ortografía: **Janbu** (Nilmar Janbu, NTH Trondheim), no "Jambu".

## 1. Tres métodos distintos con el mismo apellido

| Variante | Qué supone | Qué equilibra | Dónde aparece |
|---|---|---|---|
| Simplificado (Janbu 1954/1973) | $X = 0$ | fuerzas horizontales globales + vertical por dovela | Slide2 "Janbu Simplified", SLOPE/W, xslope, OGR |
| Corregido | simplificado × $f_0$ empírico | idem, corregido | Slide2 "Janbu Corrected", OGR, xslope |
| Generalizado (GPS, Janbu 1957/1973) | posición de la línea de empujes $z_i$ | fuerzas + momento de cada dovela (salvo la última) | **GEO5 "Janbu"**, SLOPE/W "Janbu Generalized" |

GEO5 llama "Janbu" al generalizado: su ayuda indica fuerzas no nulas entre bloques, arranque con
$\delta_i = 0$ y $z_i \approx 1/3$ de la altura del borde, e iteración hasta cumplir equilibrio y
admisibilidad cinemática. Un clon de Slide2 necesita simplificado + corregido; un clon de GEO5
necesita además el generalizado.

## 2. Janbu simplificado

**Hipótesis**: corte entre dovelas nulo ($X_i = 0$); se conservan las normales $E_i$.

**Normal de base** (equilibrio vertical de la dovela, igual que Bishop):

$$N = \frac{W + Q - \frac{1}{F}\left(c'l - ul\tan\phi'\right)\sin\alpha}{m_\alpha},\qquad m_\alpha = \cos\alpha + \frac{\sin\alpha\tan\phi'}{F}$$

**Factor de seguridad** (equilibrio horizontal de toda la masa, las $E$ se cancelan):

$$F_J = \frac{\sum\left[c'l + (N - ul)\tan\phi'\right]\cos\alpha}{\sum N\sin\alpha + \sum k_hW + \sum H_{ext}}$$

Forma clásica equivalente (sin cargas externas ni sismo), con $n_\alpha = \cos^2\alpha\,(1 + \tan\alpha\tan\phi'/F)$:

$$F_J = \frac{\sum \left[c'b + (W - ub)\tan\phi'\right] / n_\alpha}{\sum W\tan\alpha}$$

Es implícita en $F$: punto fijo desde $F^{(0)} = 1$ hasta $|F^{(k+1)} - F^{(k)}| < \varepsilon$
(Slide2 usa por defecto $\varepsilon = 0.005$, 50 iteraciones, 25 dovelas — valores replicados
por OGR-Slip2D). Con apoyos pasivos el mapa puede oscilar: amortiguar
$F \leftarrow \tfrac12(F + F_{nuevo})$ (xslope). En este repositorio se usa la raíz de
$E_n(F) = 0$ con Brent, que da el mismo valor (V2: diferencia < $10^{-6}$).

**Cargas externas** (xslope `janbu.md`, ec. 6–7): las componentes verticales entran en $N$;
las horizontales en el denominador con su signo. Sismo $k_hW$ y agua en grieta $T$ son
desestabilizantes; refuerzo y pilotes (aplicación activa) restan en el denominador sin dividir
por $F$; con aplicación pasiva se dividen por $F$ (ver 01 §6).

**Propiedad**: $F_J = F_f(\lambda = 0)$ de GLE. Suele ser conservador (menor) frente a métodos
rigurosos: F&K seco, Janbu 1.877 vs Spencer 2.073 (−9.4 %).

## 3. Janbu corregido

$$F_{JC} = f_0 \cdot F_J,\qquad f_0 = 1 + b_1\left[\frac{d}{L} - 1.4\left(\frac{d}{L}\right)^2\right]$$

- $L$: longitud de la **cuerda** entre los extremos de la superficie.
- $d$: máxima distancia **perpendicular** de la cuerda a la superficie (no la altura de suelo:
  usar la altura sobreestima $f_0$; OGR midió +2.9 % de error con esa lectura).
- $b_1$ según tipo de suelo en la base:

| Suelo | $b_1$ (Janbu 1973, curvas) | Nota |
|---|---|---|
| Solo cohesión ($\phi = 0$) | **0.69** | xslope y el blog citado en el MD original usan 0.67 |
| Cohesión y fricción | 0.50 | también se usa para superficies que atraviesan varios tipos (regla de Slide2 según OGR) |
| Solo fricción ($c = 0$) | 0.31 | |

- El polinomio es un ajuste a la carta de Janbu; tiene máximo en $d/L = 1/2.8 \approx 0.357$ y
  después decrece (sin sentido físico): recortar $d/L$ a ese valor (xslope).
- Incremento típico: hasta ~5 % en suelos granulares y ~12 % en análisis en tensiones totales
  (Geoengineer.org, resumen de Janbu 1973).
- Verificación: F&K, $d/L = 0.225$, $b_1 = 0.50$ → $f_0 = 1.0771$ (idéntico a xslope).

**Pendiente de fuente primaria**: la carta original de Janbu (1973) para confirmar 0.69 frente a
0.67, el dominio de $d/L$ y la regla para suelos mixtos. Ver `fuentes/fuentes.md`.

## 4. Janbu generalizado (GPS) — base para clonar GEO5

Hipótesis: se fija la **línea de empujes** (altura $z_i$ del punto de aplicación de $E_i$ sobre la
base, típicamente $\approx h_i/3$). Del equilibrio de momentos de cada dovela respecto del
centro de su base se obtiene el corte entre dovelas:

$$X_i \approx -E_i\tan\alpha_{t,i} + h_{t,i}\,\frac{dE}{dx}\Big|_i$$

($\alpha_t$ = inclinación de la línea de empujes, $h_t$ = su altura sobre la base). Luego:

1. Arranque $X_i = 0$ (equivale a Janbu simplificado) → $F$, $E_i$.
2. Con $E_i$ y la línea de empujes, calcular $X_i$ con la ecuación anterior (diferencias finitas).
3. Recalcular $N$ con $\Delta X$, luego $F$ y $E_i$; iterar hasta estabilizar $F$ y $X$.

Satisface equilibrio de fuerzas de todas las dovelas y momentos de todas salvo la última.
Es conocido por problemas de convergencia cuando la línea de empujes sale de la dovela o en
superficies muy curvas. GEO5 lo inicializa con $\delta_i = 0$ y $z_i \approx h_i/3$ y exige
admisibilidad cinemática. **Ecuaciones exactas de GEO5 no extraíbles** (están como imágenes).

## 5. Pseudocódigo mínimo (simplificado + corregido)

```
F ← 1
repetir:
    mα ← cos α + sin α · tanφ'/F
    N  ← (W + Q − (c'l − u l tanφ') sin α / F) / mα
    F' ← Σ(c'l + (N − u l) tanφ') cos α / (Σ N sin α + Σ kW + ΣH)
    si |F' − F| < ε: salir;  F ← F'
comprobar mα ≥ 0.2 y N − u l ≥ 0 en todas las dovelas
L ← |P_fin − P_ini|;  d ← max dist ⟂ de la base a la cuerda;  r ← min(d/L, 0.357)
b1 ← 0.69 (solo c) | 0.31 (solo φ) | 0.50 (otro)
F_JC ← (1 + b1 (r − 1.4 r²)) · F
```

Implementación: `codigo/lem_ref.py::janbu`. Fuentes: Janbu (1954, 1957, 1973); Abramson et al.
(2002) §5.5; xslope `docs/lem/janbu.md`; OGR `ogr_slip2d/methods/janbu.py`; GEO5 ayuda
"Janbu" (polígono y círculo).
