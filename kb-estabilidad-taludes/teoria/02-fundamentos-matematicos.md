# 02 · Fundamentos matemáticos y numéricos

> Nodos: `geometria_computacional`, `dovelado`, `raices_no_lineales`, `optimizacion`, `probabilidad` · Nivel L1–L2
> Estado: geometría, raíces y optimización local **verificadas** en `codigo/lem_ref.py`; estadística **documentada**.

## 1. Geometría computacional (lo que más código consume en un clon)

| Operación | Fórmula / algoritmo | Uso |
|---|---|---|
| Interpolación en polilínea | lineal por tramos, $y(x)$ | terreno, capas, piezométrica, base poligonal |
| Círculo ∩ segmento | $P = P_0 + s\,D$; $\lvert D\rvert^2 s^2 + 2(F\!\cdot\!D)s + \lvert F\rvert^2 - R^2 = 0$, $F = P_0 - C$, $0 \le s \le 1$ | extremos de la superficie circular |
| Arco inferior | $y_b(x) = y_c - \sqrt{R^2 - (x-x_c)^2}$ | base circular |
| Distancia punto–segmento | proyección $s = \mathrm{clip}\left(\frac{(P-P_0)\cdot D}{D\cdot D}, 0, 1\right)$ | regla de radios, $d$ de Janbu |
| Área y centroide de polígono | fórmula del cordón (*shoelace*) | peso y centroide de dovela por material |
| Recorte de polígonos | Sutherland-Hodgman / Weiler-Atherton (o `shapely`) | dovela ∩ región de material |
| Punto en polígono | *ray casting* | material en la base, cargas |
| Momento de una fuerza | $M = (x - x_o)F_y - (y - y_o)F_x$ | equilibrio global |
| Superficie compuesta | $y(x) = \max[y_{circ}(x), y_{piso}(x)]$ | círculo truncado en roca |

**Dovelado** (reglas que usan Slide2/xslope/OGR):
- Bordes de dovela obligatorios en: extremos, vértices del terreno, de capas, de la piezométrica,
  de la superficie poligonal, cruces arco–piso (superficies compuestas) y límites de cargas.
  Ninguna base debe cruzar un quiebre.
- Repartir las $n$ dovelas proporcionalmente a la longitud de cada tramo (xslope, este repo) o de
  ancho uniforme (Slide2 por defecto: 25 dovelas; los problemas de verificación suelen usar 50).
- Base = cuerda entre los puntos de borde; $\alpha = \mathrm{atan2}(\Delta y, \Delta x)$, $l = b/\cos\alpha$.
- $W = \sum_k \gamma_k A_k$; para capas descritas por líneas de techo continuas basta
  $A_k = b\,t_k(x_m)$ (exacto si techo y base son rectos dentro de la dovela).
- Sensibilidad: repetir con 25/50/100 dovelas; la diferencia debe ser < 0.5 %.

## 2. Álgebra lineal y recurrencias

- Cada dovela: sistema 2×2 en $(N_i, E_{i+1})$ (03 §4). La marcha completa es una recurrencia
  afín $E_{i+1} = p_i + q_iE_i$ → forma cerrada con productos acumulados (xslope la vectoriza con
  `cumprod`/`cumsum`; cae a bucle escalar si aparecen no finitos).
- Zhu (2005) usa la misma idea con coeficientes de transmisión $\Psi$ (06 §5).
- Newton 2D: jacobiano 2×2 analítico (UTEXAS) o por diferencias finitas.

## 3. Ecuaciones no lineales

| Técnica | Dónde | Cuidado |
|---|---|---|
| Punto fijo $F \leftarrow g(F)$ | Bishop, Janbu | puede oscilar → amortiguar $\tfrac12(F + g(F))$ |
| Bisección / Brent con horquilla | $F_f(\lambda)$, $h(\lambda)$ | los **polos** ($m_\alpha \to 0$) producen cambios de signo falsos: verificar $\lvert r(F^*)\rvert$ |
| Secante | $\lambda$ en GLE (OGR) | requiere buen arranque |
| Newton 2D | Spencer (UTEXAS), M-P (1967) | pasos limitados; Newton "extendido" de 2.º orden cerca de la solución |
| Raíces múltiples | $F_f - F_m$ | elegir la admisible (compresión) más cercana a $\lambda = 0$ |

Arranques recomendados: $F^{(0)}$ = Bishop o Janbu; $\lambda^{(0)} = 0$. Tolerancias habituales:
$\Delta F < 0.005$ (Slide2 por defecto), $10^{-4}$–$10^{-6}$ en verificación.

## 4. Optimización (búsqueda de la superficie crítica)

- Exhaustiva estructurada: malla de centros × radios (Grid Search).
- Directa sin derivadas: Nelder-Mead, búsqueda de patrones, movimiento de vértices (GEO5).
- Monte Carlo local: caminata aleatoria de Greco (1996) — "Optimize Surfaces".
- Metaheurísticas: recocido simulado (VFSA de Ingber + LMC; Su 2009), enjambre de partículas
  (Kennedy & Eberhart 1995), búsqueda cuco con vuelos de Lévy (Yang & Deb 2009), genéticos,
  evolución diferencial, colonia de hormigas. Comparativa: Cheng et al. (2007), *Computers and
  Geotechnics* — "six heuristic global optimization methods".
- Multimodal: PSO con vecinos más cercanos (Qu et al. 2013) → varios mecanismos a la vez.
- Parametrización física de superficies (arXiv 2412.01598, 2024): alternativa eficiente reciente.

## 5. Probabilidad y confiabilidad (módulo probabilístico de Slide2)

- Variables aleatorias por material ($c, \phi, \gamma$, $S_u$…), cargas, nivel freático, $k_h$.
- Distribuciones: normal, lognormal, uniforme, triangular, beta, exponencial, gamma; truncamiento
  por mínimos/máximos **relativos** a la media.
- Muestreo: Monte Carlo y Latin Hypercube; correlación $c$–$\phi$ (coeficiente $\rho$).
- Tipos de análisis: *Global Minimum* (N cálculos sobre la superficie crítica determinista) y
  *Overall Slope* (N búsquedas completas; da mayor probabilidad de falla, más representativa).
- $P_f = \#(F < 1)/N$. Índice de confiabilidad:
  normal $\beta = (\mu_F - 1)/\sigma_F$; lognormal
  $\beta_{LN} = \dfrac{\ln\left(\mu_F/\sqrt{1+V^2}\right)}{\sqrt{\ln(1+V^2)}}$, $V = \sigma_F/\mu_F$.
- Alternativas: FOSM/series de Taylor (USACE), estimaciones puntuales (Rosenblueth),
  superficie de respuesta; búsqueda de mínimo índice de confiabilidad (Hassan & Wolff 1999).
- Sensibilidad: barrido de una variable entre mín. y máx. manteniendo el resto en su media.

Fuentes: USACE EM 1110-2-1902; Greco (1996); Su (2009); Cheng et al. (2007); Kennedy & Eberhart
(1995); Yang & Deb (2009); Hassan & Wolff (1999); Duncan (2000); ayuda Slide2 (Probabilistic
Analysis, Sensitivity); OGR `ogr_core/statistics/probabilistic.py`; xslope `reliability.py`.
