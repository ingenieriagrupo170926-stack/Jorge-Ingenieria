# 06 · Morgenstern-Price y GLE (Equilibrio Límite General)

> Nodos: `morgenstern_price`, `gle`, `funcion_entre_dovelas`, `zhu_2005` · Nivel L3
> Estado: formulación GLE **verificada** (V1: F&K 2.076 → 2.0724 con semiseno);
> ecuaciones diferenciales originales (1965) y algoritmo de Zhu (2005) **documentados, pendientes
> de cotejo con la fuente primaria** (bloqueadas por la red de este entorno, ambas de acceso libre).

## 1. Hipótesis

$$X(x) = \lambda\, f(x)\, E(x)$$

$f(x)$ la elige el usuario (forma), $\lambda$ es incógnita (escala). Se buscan $F$ y $\lambda$ que
satisfagan fuerzas y momentos con $E = 0$ y $M = 0$ en ambos extremos (Morgenstern & Price 1965,
*Géotechnique* 15(1):79-93). Superficies de forma arbitraria.

En Slide2, "GLE/Morgenstern-Price" es un mismo método; la función por defecto es la
**media senoide** y $f = 1$ reproduce Spencer. GEO5: planos verticales, peso y $N$ en el centro
del segmento de base, inclinación $\delta_i$ distinta en cada borde y $\delta = 0$ en los extremos.

## 2. Formulación continua original (1965) — estructura

Para una rebanada infinitesimal entre $x$ y $x+dx$, con $y(x)$ la superficie de falla e $y_t(x)$ la
línea de empujes:

- **Momento** respecto de la base: $X = \dfrac{d}{dx}\left(E\,y_t\right) - y\,\dfrac{dE}{dx}$
  (más términos de presiones de agua en las caras si se trabaja con fuerzas efectivas).
- **Fuerzas** normal y tangente a la base combinadas con Mohr-Coulomb → una ecuación diferencial
  de primer orden en $E$ que contiene $dW/dx$, $dX/dx$, $\tan\alpha = dy/dx$, $c'$, $\tan\phi'/F$ y $r_u$.

Discretización de M-P: en cada dovela suponen $y = Ax + B$, $dW/dx = px + q$ y $f = kx + m$
lineales; integran en forma cerrada $E$ y el momento al final de cada dovela y exigen
$E_n = 0$, $M_n = 0$ en el extremo. El sistema no lineal en $(F, \lambda)$ se resuelve por
Newton-Raphson (Morgenstern & Price 1967, *Computer Journal* 9(4):388-393).

**Pendiente**: transcribir las ecuaciones exactas y las constantes de integración del artículo
(el PDF está en el repositorio abierto ERA de la Universidad de Alberta; no se pudo abrir aquí).

## 3. Formulación discreta GLE (Fredlund & Krahn 1977) — la estándar en software

Normal de base incluyendo la diferencia de cortes entre dovelas:

$$N = \frac{W + Q + (X_{R} - X_{L})\,s - \frac{1}{F}\left(c'l - ul\tan\phi'\right)\sin\alpha}{m_\alpha}$$

(el signo $s$ del término $X_R - X_L$ depende de la convención; en la de este repositorio el
término sale de la marcha automáticamente: ver `03-marco-comun-dovelas.md` §4).

$$F_m = \frac{\sum\left[c'l R + (N - ul)R\tan\phi'\right]}{\sum W x - \sum N f + \sum k_hW e \pm \sum D d \pm \sum A a}$$

$$F_f = \frac{\sum\left[c'l\cos\alpha + (N-ul)\tan\phi'\cos\alpha\right]}{\sum N\sin\alpha + \sum k_hW - \sum D\cos\omega \pm \sum A}$$

($x, f, e, d, a$: brazos de palanca de $W$, $N$, sismo, cargas puntuales $D$ y agua $A$.)

**Tres errores que invalidan una implementación** (medidos en las auditorías de OGR-Slip2D):
1. Omitir $X_R - X_L$ en $N$ → $F_m$ no depende de $\lambda$ y el "cruce" siempre da Bishop.
2. Compartir un solo iterado $F = (F_f + F_m)/2$ entre las dos ramas → $F_m(0)$ 2–4 % por
   debajo de Bishop. Cada rama debe converger a **su propio** punto fijo.
3. Proyectar mal en $F_f$ (usar $S\cos\alpha$ donde corresponde $S\sec\alpha$ en la forma con
   $\tan\alpha$) → hasta un factor 2 en taludes de 45°–64°.

## 4. Función entre dovelas f(x)

| Función | Definición ($s = (x - x_{ini})/(x_{fin} - x_{ini})$) | Uso |
|---|---|---|
| Constante | $f = 1$ | = Spencer |
| Media senoide | $f = \sin(\pi s)$ | por defecto en Slide2, SLOPE/W, OGR, este repo |
| Seno recortado | $f = \max(f_{min}, \sin(\pi s))$ o seno escalado con valores de extremo dados | Slide2, SLOPE/W |
| Trapezoidal | rampas lineales en los extremos y meseta central | Slide2, SLOPE/W |
| Definida por puntos | tabla $(s, f)$ del usuario | Slide2 "Data Point Specified" |
| Fredlund-Wilson-Fan | derivada de tensiones elásticas por EF | SLOPE/W |

Solo importa la **forma** (escalar $f$ reescala $\lambda$). El $F$ suele ser poco sensible a $f(x)$
(V1: constante 2.0729 vs semiseno 2.0724), pero $\lambda$ y la distribución de fuerzas sí cambian.
Chen & Morgenstern (1983) muestran que las condiciones en los extremos restringen $f(x)$
(inclinación de la resultante en los bordes compatible con el estado tensional del borde).
**Pendiente**: fórmula exacta del seno recortado y del trapecio en Slide2 (parámetros por defecto).

## 5. Algoritmo "conciso" de Zhu, Lee, Qian & Chen (2005)

*Can. Geotech. J.* 42(1):272-278. Útil por ser explícito y rápido. Con fuerzas efectivas:

$$R_i = \left[W_i\cos\alpha_i - k_cW_i\sin\alpha_i + Q_i\cos(\omega_i-\alpha_i) - U_i\right]\tan\phi_i' + c_i'b_i\sec\alpha_i$$
$$T_i = W_i\sin\alpha_i + k_cW_i\cos\alpha_i - Q_i\sin(\omega_i-\alpha_i)$$
$$\Phi_i = (\sin\alpha_i - \lambda f_i\cos\alpha_i)\tan\phi_i' + (\cos\alpha_i + \lambda f_i\sin\alpha_i)F_s$$
$$\Psi_{i-1} = \frac{(\sin\alpha_i - \lambda f_{i-1}\cos\alpha_i)\tan\phi_i' + (\cos\alpha_i + \lambda f_{i-1}\sin\alpha_i)F_s}{\Phi_{i-1}}$$
$$E_i\Phi_i = \Psi_{i-1}E_{i-1}\Phi_{i-1} + F_sT_i - R_i$$

Con $E_0 = E_n = 0$ la recurrencia da $F_s$ en forma casi explícita:

$$F_s = \frac{\sum_{i=1}^{n-1}\left(R_i\prod_{j=i}^{n-1}\Psi_j\right) + R_n}{\sum_{i=1}^{n-1}\left(T_i\prod_{j=i}^{n-1}\Psi_j\right) + T_n}$$

y el equilibrio de momentos da $\lambda$ explícito como cociente
$\lambda = \dfrac{\sum\left[b_i(E_i + E_{i-1})\tan\alpha_i + \text{(términos de sismo y cargas)}\right]}{\sum b_i\,(f_iE_i + f_{i-1}E_{i-1})}$.
Iteración: $F_s = 1$, $\lambda = 0$ → actualizar $F_s$ → calcular $E_i$ → actualizar $\lambda$ →
repetir; exige $\Phi_i > 0$. Los autores reportan < 10 iteraciones con tolerancia $10^{-4}$ en sus
ejemplos (no es garantía general). Slide2 incluye un problema de verificación de Zhu (VP#51,
Spencer 1.293).

**Pendiente**: signos exactos del término $Q_i$ y los términos de carga del cociente de $\lambda$
(verificar contra el PDF de HKU Scholars Hub, acceso libre, bloqueado aquí).

## 6. Estrategias de solución y cuál usar

| Estrategia | Pros | Contras |
|---|---|---|
| Barrido de $\lambda$ + cruce $F_f = F_m$ (F&K, SLOPE/W) | diagnóstico visual (gráfico F vs λ) | lento; interpolación |
| Newton 2D en $(F,\lambda)$ (M-P 1967, UTEXAS) | cuadrático cerca de la solución | diverge con mal arranque; polos |
| $h(\lambda) = M(F_f(\lambda),\lambda)$ + Brent (xslope "approach A", este repo) | robusto, una variable | más evaluaciones |
| Zhu 2005 punto fijo | explícito, pocas líneas | exige $\Phi_i>0$; convergencia no garantizada |

Recomendación para el clon: Newton 2D como vía rápida y $h(\lambda)$ + Brent como respaldo
(así lo hace xslope: "approach B" → si falla, "approach A"). Siempre filtrar raíces espurias
(fuerzas entre dovelas en tracción) y elegir la de $|\lambda|$ mínimo.

## 7. Resultados de control (V1, 49 dovelas)

| Caso F&K (1977) | M-P semiseno (este repo) | λ | F&K publicado | xslope |
|---|---|---|---|---|
| Seco | 2.0724 | 0.324 | 2.076 | 2.0706 |
| $r_u = 0.25$ | 1.7576 | 0.314 | 1.764 | 1.7559 |
| Línea piezométrica | 1.8278 | 0.299 | 1.832 | 1.8261 |

Fuentes: Morgenstern & Price (1965, 1967); Fredlund & Krahn (1977); Fredlund, Krahn & Pufahl
(1981); Chen & Morgenstern (1983); Zhu et al. (2005); SLOPE/W *Stability Modeling* (Seequent
2022); Slide2 ayuda "Interslice Force Function"; GEO5 ayuda "Morgenstern-Price"; xslope
`docs/lem/mprice.md`; OGR `ogr_slip2d/interslice.py`.
