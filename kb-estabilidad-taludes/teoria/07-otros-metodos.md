# 07 · Otros métodos que ofrece Slide2 / GEO5 (para un clon completo)

> Nodo: `otros_metodos` · Nivel L3 · Estado: Bishop **verificado** (V1); el resto **documentado**.

| Método | Equilibrio | Hipótesis entre dovelas | Superficie | Slide2 | GEO5 |
|---|---|---|---|---|---|
| Ordinario / Fellenius / Petterson | momento | se ignoran (resultante ∥ base) | circular | ✔ | ✔ |
| Bishop simplificado | momento + vertical | $X = 0$ | circular | ✔ | ✔ |
| Janbu simplificado / corregido | fuerzas | $X = 0$ (+ $f_0$) | cualquiera | ✔ | — |
| Janbu generalizado | fuerzas + momento por dovela | línea de empujes | cualquiera | — | ✔ ("Janbu") |
| Cuerpo de Ingenieros #1 | fuerzas | θ = pendiente de la recta entrada–salida | cualquiera | ✔ | — |
| Cuerpo de Ingenieros #2 | fuerzas | θ = pendiente del terreno sobre cada dovela | cualquiera | ✔ | — |
| Lowe-Karafiath | fuerzas | θ = (α + β)/2 (base y terreno) | cualquiera | ✔ | — |
| Spencer | completo | θ constante | cualquiera | ✔ | ✔ |
| GLE / Morgenstern-Price | completo | $X = \lambda f(x)E$ | cualquiera | ✔ | ✔ |
| Sarma (dovelas verticales o inclinadas) | completo | resistencia movilizada en caras entre dovelas; aceleración crítica $K_c$ | poligonal | ✔ | ✔ (poligonal) |
| Shahunyants | completo (método ruso) | — | ambos | — | ✔ |
| ITFM (empuje desequilibrado, norma china) | fuerzas | resultante ∥ base de la dovela anterior | ambos | — | ✔ |

## Fórmulas mínimas

**Ordinario (Fellenius)** — sin iteración:
$$F = \frac{\sum\left[c'l + (W\cos\alpha - ul)\tan\phi'\right]}{\sum W\sin\alpha}$$
Ojo: con presión de poros existen dos variantes ($W\cos\alpha - ul$ de F&K frente a
$(W - ub)\cos\alpha$); difieren mucho en bases casi horizontales (VP#22: 1.037 vs 1.121).

**Bishop simplificado** (círculo, momento respecto del centro):
$$F = \frac{\sum \left[c'b + (W - ub)\tan\phi'\right]/m_\alpha}{\sum W\sin\alpha},\qquad m_\alpha = \cos\alpha + \frac{\sin\alpha\tan\phi'}{F}$$
En este repositorio: raíz de $M(F, \lambda = 0)$ respecto del centro (V1: F&K 2.080 → 2.0767).
Para superficies no circulares Slide2 calcula Bishop respecto de un eje; es un método de
momentos y su valor **depende del eje** (OGR, anomalía D47): usar solo con círculos.

**Métodos de fuerzas con θ prescrita** (Corps #1, #2, Lowe-Karafiath): la marcha de 03 §4 con
$t_j = \tan\theta_j$ fijo y $E_n(F) = 0$. Se decide si θ se aplica a la resultante total o a la
efectiva (fuerzas de agua en las caras). Fallan a converger con $\phi$ muy altos (> 55°, típico
de Hoek-Brown a bajo confinamiento): preferir Spencer/GLE en roca.

**ITFM** (coeficiente de transmisión, forma implícita):
$$P_i = W_i\sin\alpha_i - \frac{c_il_i + W_i\cos\alpha_i\tan\phi_i}{F} + \psi_{i-1}P_{i-1},\qquad
\psi_{i-1} = \cos(\alpha_{i-1}-\alpha_i) - \sin(\alpha_{i-1}-\alpha_i)\frac{\tan\phi_i}{F}$$
con $P_n = 0$. **Pendiente**: verificar contra la ayuda de GEO5 (ecuaciones en imagen).

**Sarma (1973, 1979)**: plantea el equilibrio con la resistencia movilizada también en las caras
entre dovelas (que pueden ser inclinadas) y resuelve la aceleración horizontal crítica $K_c$
que lleva la masa al equilibrio límite; F estático = factor que reduce la resistencia hasta
$K_c = 0$. **Pendiente**: ecuaciones completas (artículos de *Géotechnique* de pago).

**Shahunyants**: incluido en GEO5; ecuaciones no revisadas (pendiente).

Fuentes: Fellenius (1936); Bishop (1955); USACE EM 1110-2-1902 (App. C, métodos de fuerzas);
Lowe & Karafiath (1960); Sarma (1973, 1979); ayuda GEO5 (lista de métodos por tipo de
superficie); ayuda Slide2 "Analysis Methods"; xslope `docs/lem/force_eq.md`, `oms.md`, `bishop.md`.
