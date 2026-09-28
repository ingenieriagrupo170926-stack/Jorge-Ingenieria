# 11 · Verificación: estrategia, casos y resultados

> Nodos: `verificacion`, `bm_fk1977`, `bm_acads1a`, `bm_slide2`, `bm_talbingo` · Nivel L4
> Resultados completos y reproducibles: [`codigo/resultados_validacion.md`](../codigo/resultados_validacion.md)
> (`cd codigo && python3 validar.py`).

## 1. Estrategia en tres niveles

1. **Anclas analíticas** (error solo de discretización): talud infinito
   ($F = \tan\phi'/\tan\beta$ seco; $\approx(\gamma'/\gamma_{sat})\tan\phi'/\tan\beta$ con flujo paralelo),
   cuña plana de Culmann (todos los métodos coinciden en un plano: VP#43, VP#53), capacidad
   portante de Prandtl (VP#25–26), cartas de Taylor, $k_c$ con F = 1 (VP#62).
2. **Casos publicados** con geometría completa: Fredlund & Krahn (1977), ACADS (Donald & Giam
   1989), Arai & Tagyo (1985), Yamagami & Ueta (1988), Baker (1980), Zhu (2005), Low (1989),
   Chen & Shao (1988), Duncan & Wright.
3. **Manuales de verificación de software**: Slide2 (111 problemas), SLOPE/W (47), RS2. Sus
   geometrías, parámetros y valores están reconstruidos en xslope
   (`docs/verification/rocscience.md`, `geostudio.md`) con archivos de entrada.

Reglas: comparar **mismo método con mismo método**; superficie fija antes que búsqueda; la
tolerancia depende de la precisión de la fuente; nunca validar contra salidas propias archivadas.

## 2. Resultados de este repositorio

### V1 — Fredlund & Krahn (1977) = Slide2 VP#21, círculo fijo, 49 dovelas

| Caso | Bishop | Janbu simp. | Janbu corr. | Spencer (θ) | M-P semiseno (λ) |
|---|---|---|---|---|---|
| Seco — este repo | 2.0767 | 1.8772 | 2.0218 | 2.0729 (14.48°) | 2.0724 (0.324) |
| Seco — F&K 1977 | 2.080 | — | — | 2.073 | 2.076 |
| Seco — xslope 0.5.2 (50 dov.) | 2.0749 | 1.8747 | 2.0192 | 2.0710 | 2.0706 |
| $r_u$ = 0.25 — este repo | 1.7602 | 1.5888 | 1.7112 | 1.7583 (14.04°) | 1.7576 (0.314) |
| $r_u$ = 0.25 — F&K 1977 | 1.766 | — | — | 1.761 | 1.764 |
| Piezométrica — este repo | 1.8301 | 1.6779 | 1.8072 | 1.8286 (13.50°) | 1.8278 (0.299) |
| Piezométrica — F&K 1977 | 1.834 | — | — | 1.830 | 1.832 |

Diferencias frente a F&K: −0.01 % a −0.36 %; frente a xslope: +0.09 % a +0.14 % (efecto del
número y reparto de dovelas). $f_0 = 1.0771$ idéntico a xslope.

### V2 — Identidades (deben cumplirse a precisión de máquina)

- Spencer con el punto de momentos en el centro o en (300, 500): mismo F (Δ = 0).
- M-P con $f(x) = 1$ = Spencer; $\lambda = \tan\theta$.
- Janbu por recurrencia = fórmula cerrada de Janbu.
- Residuales en la solución: $E_n/\Sigma W \sim 10^{-17}$, $M/(\Sigma W L) \sim 10^{-15}$.

### V3 — ACADS 1(a) = Slide2 VP#1, búsqueda circular

| Método | Este repo | ACADS (consenso) | Slide2 | xslope |
|---|---|---|---|---|
| Bishop | 0.985 | 1.00 | 0.987 | 0.985 |
| Janbu corregido | 0.986 | 1.00 | — | 0.986 |
| Spencer | 0.984 | 1.00 | — | 0.984 |

Lección registrada durante la validación: sin el control $m_\alpha \ge 0.2$ la búsqueda devolvía
F ≈ 0.05 (raíces por debajo de los polos de $m_\alpha$). Con el control, 0.985. Es la trampa n.º 10
de `12-trampas-de-implementacion.md` ocurriendo en vivo.

### V4 — Optimización poligonal desde el círculo crítico

Poligonal de 8 vértices inscrita en el círculo crítico Spencer: 0.9881 (la cuerda recorta el
arco); tras optimizar extremos y vértices (Nelder-Mead, 57 s): **0.9852**, todavía 0.1 % sobre el
círculo (0.9843). Con 8 vértices la poligonal no alcanza al círculo en un talud homogéneo: hace
falta más vértices (OGR midió la convergencia de Spencer con 8→64 vértices) o arrancar de más
semillas. Es el comportamiento esperado de una optimización local, no un error del método.

## 3. Batería recomendada para el clon (por hito)

| Hito | Casos (VP# de Slide2) | Qué ejercitan |
|---|---|---|
| H1 | 21 (F&K), 6 (Talbingo, raíz espuria), 43 y 53 (plano), 26 (Prandtl) | métodos sobre superficie fija |
| H2 | 2, 3, 4, 10, 27, 51, 55–56 | capas, agua, sismo, grieta |
| H3 | 1, 14–17, 23–24 | búsqueda circular |
| H4 | 7–9, 18–20, 22, 57, 61 | no circular, capa débil, compuestas |
| H5 | 30–32, 37, 47–50, 54, 58–60, 85–94, 106 | soportes |
| H6 | 28–29, 33–36, 40 | probabilístico y sensibilidad |
| H8 | 38, 46, 71–77, 95–104; manual Groundwater | filtración, desembalse, Newmark |

Valores objetivo por problema: xslope `docs/verification/rocscience.md` (con enlace a los
archivos de entrada `.xlsx` de cada caso).
