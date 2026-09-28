# 03 · Marco común del método de dovelas (la "ecuación madre")

> Nodo del grafo: `marco_dovelas` · Nivel L2 · Estado: **verificado numéricamente** (`codigo/lem_ref.py`, V1–V2)
>
> Todos los métodos que pide el proyecto (Janbu simplificado, Janbu corregido, Spencer,
> Morgenstern-Price) salen de **una sola** formulación de equilibrio por dovela. Lo único que
> cambia entre ellos es la hipótesis sobre las fuerzas entre dovelas y qué ecuación global se
> impone. Si esto se implementa una vez y bien, los cuatro métodos salen casi gratis.

## 1. Idealización

- Problema 2D en deformación plana, espesor unitario (fuerzas por metro lineal).
- La masa sobre la superficie candidata $\Gamma$ es un cuerpo rígido-plástico.
- Se moviliza la **misma fracción** de la resistencia en todo $\Gamma$:
  $\tau_{mov} = s / F$ (definición de F por reducción de resistencia).
- Mohr-Coulomb en la base de cada dovela (u otra envolvente linealizada, ver 01).
- La masa se divide en $n$ dovelas verticales (Sarma usa dovelas inclinadas, ver 07).

## 2. Geometría y notación de una dovela

Convención de este repositorio (la misma de `lem_ref.py`): **el talud mira a la izquierda**
(pie a la izquierda, corona a la derecha) y la masa desliza hacia $-x$. Un talud que mira a la
derecha se refleja ($x \to -x$) antes de calcular.

```
            x_l            x_r
             |<---- b ---->|
             |   Q (sobrecarga)
             |     ↓       |
   E_i, X_i →|             |← E_{i+1}, X_{i+1}     (E: normal horizontal, X: corte vertical)
             |   W ↓  kW ← |                       (kW: sismo pseudoestático hacia -x)
             |_____________|
            /  base: largo l = b/cos α, inclinación α (α>0 cuando sube hacia la corona)
      N ↑ (normal a la base)   S ↗ (corte resistente, a lo largo de la base)
```

| Símbolo | Significado |
|---|---|
| $b, l, \alpha$ | ancho, largo de base ($l = b\sec\alpha$), inclinación de la base |
| $W$ | peso total ($\sum_k \gamma_k A_k$, todas las capas cortadas por la dovela) |
| $N$ | normal **total** en la base; $N' = N - u\,l$ es la efectiva |
| $S$ | corte movilizado en la base: $S = \dfrac{c'l + (N - ul)\tan\phi'}{F}$ |
| $u$ | presión de poros en el punto medio de la base |
| $E_i, X_i$ | normal y corte entre dovelas en el borde $i$ ($i = 0..n$); $E_0=E_n=0$ en extremos libres |
| $\theta_i$ | inclinación de la resultante entre dovelas: $\tan\theta_i = X_i/E_i$ |
| $k_h W$ | fuerza sísmica pseudoestática en el centroide |
| $Q$ | sobrecarga vertical sobre la dovela |

## 3. Balance de incógnitas (por qué hacen falta hipótesis)

| Incógnitas | Cantidad |
|---|---|
| Factor de seguridad $F$ | 1 |
| Normales $N_i$ | $n$ |
| Cortes $S_i$ | $n$ |
| Posición de $N_i$ en la base | $n$ |
| Normales entre dovelas $E_i$ | $n-1$ |
| Cortes entre dovelas $X_i$ | $n-1$ |
| Posición de $E_i$ (línea de empujes) | $n-1$ |
| **Total** | $6n-2$ |

Ecuaciones: $3n$ de equilibrio + $n$ de Mohr-Coulomb = $4n$. Faltan $2n-2$. Suponer que $N$
actúa en el centro de la base (dovelas delgadas) elimina $n$ → faltan $n-2$. Cada método
"cierra" el problema con una hipótesis sobre $X$, $\theta$ o la línea de empujes
(Fredlund & Krahn 1977; Duncan & Wright 2005; USACE EM 1110-2-1902).

## 4. Equilibrio de una dovela (derivación usada en el código)

Con $A = \tan\phi'/F$ y $s_0 = (c' - u\tan\phi')\,l/F$, el corte es $S = s_0 + A\,N$.
Las fuerzas sobre la dovela $i$ son:

- peso $(0,-W)$, sobrecarga $(0,-Q)$, sismo $(-k_hW, 0)$;
- normal de base $N(-\sin\alpha, \cos\alpha)$ y corte $S(\cos\alpha, \sin\alpha)$;
- cara izquierda $(+E_i, +X_i)$, cara derecha $(-E_{i+1}, -X_{i+1})$, con $X_j = t_j E_j$, $t_j=\tan\theta_j$.

$$\Sigma F_x:\; -N\sin\alpha + S\cos\alpha - k_hW + E_i - E_{i+1} = 0$$
$$\Sigma F_y:\; N\cos\alpha + S\sin\alpha - W - Q + t_iE_i - t_{i+1}E_{i+1} = 0$$

Despejando (sistema lineal 2×2 en $N$ y $E_{i+1}$):

$$\boxed{N_i = \frac{W + Q - s_0\sin\alpha + t_{i+1}(s_0\cos\alpha - k_hW) + E_i\,(t_{i+1} - t_i)}
{\cos\alpha + A\sin\alpha + t_{i+1}(\sin\alpha - A\cos\alpha)}}$$

$$\boxed{E_{i+1} = E_i + N_i\,(A\cos\alpha - \sin\alpha) + s_0\cos\alpha - k_hW}$$

Se "marcha" desde el pie con $E_0 = 0$. Para un $F$ y un juego de $\theta_j$ dados, la marcha
entrega todos los $N_i$ y $E_i$. **Residual de fuerzas**: $E_n(F,\theta)$ (debe ser 0).

Caso $t\equiv 0$ (sin corte entre dovelas): $N = \dfrac{W + Q - (c'l - ul\tan\phi')\sin\alpha/F}{m_\alpha}$
con $m_\alpha = \cos\alpha + \sin\alpha\tan\phi'/F$ — la normal de Bishop/Janbu.

## 5. Equilibrio global

**Fuerzas horizontales** (sumando $\Sigma F_x$ sobre todas las dovelas, $E_0=E_n=0$):

$$F_f = \frac{\sum \left[c'l + (N-ul)\tan\phi'\right]\cos\alpha}{\sum N\sin\alpha + \sum k_hW}$$

Forma equivalente de Fredlund-Krahn / SLOPE/W: $F_f = \dfrac{\sum S_{disp}\sec\alpha}{\sum (W+\Delta X)\tan\alpha + \sum H}$
(son idénticas; usar $S\cos\alpha$ en el numerador de la segunda forma es un error clásico que
reduce $F$ en $\cos^2\alpha$ por dovela — ver `practica/12-trampas.md`).

**Momentos** respecto de un punto $(x_o, y_o)$ (antihorario positivo):

$$M = \sum\Big[-(x_m-x_o)(W+Q) + (y_g-y_o)k_hW + (x_m-x_o)(N\cos\alpha + S\sin\alpha) + (y_b-y_o)(N\sin\alpha - S\cos\alpha)\Big]$$

En un círculo con el punto en el centro, $N$ no da momento y $S$ tiene brazo $R$:
$F_m = \dfrac{\sum [c'l + (N-ul)\tan\phi']R}{\sum W x - \sum N f + \sum k_hW e}$ (forma F&K con brazos
generales $x, f, e$). **Si el equilibrio de fuerzas se cumple, el momento no depende del punto
elegido** — propiedad usada como prueba (V2) y que libera a Spencer/M-P de necesitar un centro.

## 6. La familia GLE: cada método es un caso particular

Hipótesis general (Morgenstern-Price 1965, generalizada por Fredlund & Krahn 1977 como GLE):

$$X_i = \lambda\, f(x_i)\, E_i \qquad (\tan\theta_i = \lambda f_i)$$

Para cada $\lambda$ se obtienen dos factores: $F_f(\lambda)$ (fuerzas) y $F_m(\lambda)$ (momentos).
La solución rigurosa es el cruce $F_f(\lambda^*) = F_m(\lambda^*)$.

| Método | Hipótesis entre dovelas | Equilibrio impuesto | Posición en GLE |
|---|---|---|---|
| Ordinario/Fellenius | resultante entre dovelas ∥ base (se ignoran) | momento | — (no es caso exacto) |
| Bishop simplificado | $X = 0$ | momento + vertical por dovela | $F_m(\lambda = 0)$ |
| **Janbu simplificado** | $X = 0$ | fuerzas | $F_f(\lambda = 0)$ |
| **Janbu corregido** | $X = 0$ + factor empírico $f_0$ | fuerzas | $f_0 \cdot F_f(0)$ |
| Janbu generalizado | línea de empujes supuesta | fuerzas + momento por dovela | fuera de GLE (usa $z$, no $\lambda$) |
| Cuerpo de Ingenieros #1/#2 | $\theta$ = pendiente fija | fuerzas | $F_f$ con $f$ geométrica |
| Lowe-Karafiath | $\theta = (\alpha + \beta)/2$ | fuerzas | $F_f$ con $f$ geométrica |
| **Spencer** | $\theta$ constante | fuerzas + momento | $f(x) = 1$ |
| **Morgenstern-Price** | $X/E = \lambda f(x)$ | fuerzas + momento | $f(x)$ cualquiera |

Consecuencias prácticas verificadas en V2:
- Spencer ≡ M-P con $f=1$ (diferencia < $10^{-6}$ en este solver).
- Janbu simplificado por la recurrencia = fórmula cerrada de Janbu.
- Bishop = raíz de $M(F, \lambda=0)$ respecto del centro del círculo.

## 7. Cómo se resuelve (tres estrategias equivalentes)

1. **Cruce de curvas** (Fredlund-Krahn, SLOPE/W): barrer $\lambda$, calcular $F_f(\lambda)$ y $F_m(\lambda)$
   por punto fijo cada uno con su propio $F$, interpolar el cruce.
2. **Newton 2D en $(F, \lambda)$** (M-P 1967, UTEXAS/Wright para Spencer): residuales
   $R_1 = E_n$, $R_2 = M_n$, derivadas analíticas o numéricas; rápido pero sensible al arranque.
3. **Reducción a una variable** (este repositorio y xslope): $F_f(\lambda)$ = raíz de $E_n$;
   $h(\lambda) = M(F_f(\lambda), \lambda)$; se busca $h(\lambda)=0$ con Brent. Robusto porque
   $F_f(\lambda)$ es suave y univaluado.

Pseudocódigo (el de `lem_ref.gle`):

```
para λ en malla [-1, 1]:
    F_f(λ) ← raíz de E_n(F; λ f) bajando desde F alto y rechazando polos
    h(λ)   ← M(F_f(λ), λ) / (ΣW · L)
para cada cambio de signo de h: λ* ← Brent; comprobar |h(λ*)| < tol
elegir la raíz con fuerzas entre dovelas en compresión y |λ| mínimo
devolver F = F_f(λ*), λ*, θ* = atan(λ*) (Spencer), E_i, X_i, N_i
```

## 8. Controles de admisibilidad (obligatorios antes de reportar F)

- $m_\alpha > 0$ en todas las dovelas; criterio práctico $m_\alpha \ge 0.2$ (Whitman & Bailey 1967),
  aplicado a Bishop, Janbu, Spencer y GLE en Slide2 y replicado por OGR-Slip2D (`checks.M_ALPHA_LIMIT`).
- $N' \ge 0$: normales efectivas en tracción → grieta de tracción o superficie inválida.
- $E_i > 0$ (compresión) en la mayoría de los bordes interiores; raíces con tracción
  generalizada son **soluciones espurias** del sistema (ej. Talbingo, VP#6: λ = −0.979 da 1.68
  frente al correcto 2.29 con λ = +0.419).
- Línea de empujes dentro de la dovela (recomendación Spencer 1973; Chen & Morgenstern 1983).
- Residuales finales: $E_n/\Sigma W$ y $M/(\Sigma W\cdot L)$ del orden de la tolerancia (V2 los imprime).

Fuentes: Fredlund & Krahn (1977); Fredlund, Krahn & Pufahl (1981); Spencer (1967);
Morgenstern & Price (1965); UTEXAS2 App. A (Wright, DTIC ADA207044); documentación de xslope
(`docs/lem/*.md`) y OGR-Slip2D (`ogr_slip2d/interslice.py`). Ver `fuentes/fuentes.md`.
