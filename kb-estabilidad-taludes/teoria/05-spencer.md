# 05 · Método de Spencer

> Nodo del grafo: `spencer` · Nivel L3 · Estado: **verificado** (V1: F&K 2.073 → 2.0729; V2: identidad con M-P f=1)

## 1. Hipótesis

Todas las resultantes entre dovelas son **paralelas**: $\tan\theta = X_i/E_i = \lambda$ constante
(Spencer 1967, *Géotechnique* 17(1):11-26). Incógnitas globales: $F$ y $\theta$. Satisface
equilibrio de fuerzas (en dos direcciones) y de momentos. Vale para superficies circulares y
no circulares. Es el caso $f(x) = 1$ de Morgenstern-Price.

GEO5 añade: planos divisorios verticales, peso aplicado en el centro del segmento de base,
$N$ en ese mismo punto, inclinación $\delta$ constante salvo en los extremos ($\delta = 0$).

## 2. Formulación "Q" (UTEXAS, S. G. Wright — la más directa de programar)

Se agrupan las dos fuerzas entre dovelas en su resultante $Q_i = Z_{i} - Z_{i+1}$ (inclinada
$\theta$). Con las fuerzas conocidas de la dovela proyectadas:

$$F_h = -k_hW - V + P\sin\beta + R\cos\psi + \dots,\qquad F_v = -W - P\cos\beta + R\sin\psi + \dots$$

($P$ carga superficial de inclinación $\beta$, $R$ refuerzo con ángulo $\psi$, $V$ agua en grieta).

Equilibrio normal y tangente a la base, más Mohr-Coulomb, da:

$$Q = \frac{-F_v\sin\alpha - F_h\cos\alpha - \frac{c'}{F}\Delta x\sec\alpha + \left(F_v\cos\alpha - F_h\sin\alpha + u\,\Delta x\sec\alpha\right)\frac{\tan\phi'}{F}}
{\cos(\alpha-\theta) + \sin(\alpha-\theta)\,\frac{\tan\phi'}{F}}$$

Momento de cada dovela respecto del centro de su base → punto de aplicación de $Q$:

$$y_Q = y_b + \frac{M_o}{Q\cos\theta}$$

Equilibrio global (dos ecuaciones, dos incógnitas):

$$R_1 = \sum Q_i = 0,\qquad R_2 = \sum Q_i\,(x_b\sin\theta - y_Q\cos\theta) = 0$$

**Solución** (UTEXAS): Newton 2D en $(F, \theta)$ con
$\Delta F = \dfrac{R_1 R_{2,\theta} - R_2 R_{1,\theta}}{R_{1,\theta}R_{2,F} - R_{1,F}R_{2,\theta}}$,
$\Delta\theta = \dfrac{R_2 R_{1,F} - R_1 R_{2,F}}{R_{1,\theta}R_{2,F} - R_{1,F}R_{2,\theta}}$;
cuando los pasos bajan de $\Delta F = 0.5$, $\Delta\theta = 0.15$ rad se pasa a un Newton
"extendido" con términos de 2.º orden. Derivadas analíticas completas en xslope
`docs/lem/spencer.md` (ec. 35–50), transcritas de UTEXAS2 App. A.

## 3. Formulación GLE (Fredlund-Krahn) — la usada en este repositorio

Con $f \equiv 1$ la marcha de `03-marco-comun` da $F_f(\lambda)$; el momento global a
$F_f(\lambda)$ da $h(\lambda)$; se resuelve $h(\lambda^*) = 0$ y $\theta^* = \arctan\lambda^*$.
Alternativa clásica: barrer $\theta$, dibujar $F_f(\theta)$ (crece con θ) y $F_m(\theta)$ (poco
sensible) y tomar el cruce.

Resultado V1 (F&K seco, 49 dovelas): $F = 2.0729$, $\theta = 14.48°$; F&K publican 2.073.

## 4. Rango de θ y robustez

- El denominador $\cos(\alpha - \theta) + \sin(\alpha-\theta)\tan\phi'/F$ se anula para ciertas
  combinaciones $(\alpha, \theta, F)$ → polos y cambios de signo falsos. xslope acota θ con
  `spencer_theta_bounds` (margen de 5° respecto del polo); este repositorio rechaza raíces con
  residual grande.
- El sistema puede tener **varias raíces**; elegir la de fuerzas entre dovelas en compresión y
  $|\theta|$ más pequeño. Si ninguna es admisible, informar "sin solución" (VP#59 de Slide2:
  Spencer no tiene solución en esa superficie; Slide2/xslope reportan Janbu/Corps).
- θ típico: 5°–25° en taludes corrientes; valores cercanos a ±45° suelen indicar problemas.
- Línea de empujes: Spencer (1973) recomienda verificar que quede dentro de la dovela.

## 5. Pseudocódigo (Newton 2D, variante UTEXAS)

```
F ← F_Bishop (o 1.5); θ ← 0
repetir hasta |ΔF| < tolF y |Δθ| < tolθ:
    para cada dovela: Q_i(F,θ), yQ_i(F,θ) y sus derivadas ∂/∂F, ∂/∂θ
    R1 ← ΣQ_i ; R2 ← ΣQ_i (x_b sinθ − yQ_i cosθ)
    resolver [∂R1/∂F ∂R1/∂θ; ∂R2/∂F ∂R2/∂θ] [ΔF Δθ]ᵀ = −[R1 R2]ᵀ
    limitar pasos; F ← F+ΔF; θ ← θ+Δθ
verificar mα ≥ 0.2, N' ≥ 0, E_i > 0, línea de empujes dentro de la dovela
```

Fuentes: Spencer (1967, 1973); UTEXAS2 User's Guide App. A (Wright; DTIC ADA207044);
Fredlund & Krahn (1977); xslope `docs/lem/spencer.md`; GEO5 ayuda "Spencer".
**Pendiente**: artículo original de Spencer (1967) para contrastar signos y su ejemplo numérico.
