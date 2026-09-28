# 09 · Mapa funcional de Slide2 → teoría → prioridad de clonado

> Nodo: `slide2_funciones` · Nivel L1 · Sirve como **backlog** del clon. Prioridad: **P0** = MVP que
> ya cubre Janbu/Spencer/M-P; **P1** = paridad práctica con Slide2; **P2** = avanzado.
> "VP#" = problema del *Slide2 Slope Stability Verification Manual* (111 problemas) con el que se
> valida; los valores de referencia y la geometría están reconstruidos en xslope
> `docs/verification/rocscience.md`.

| Módulo Slide2 | Qué hace | Teoría (este repo) | Prioridad | Referencias abiertas | Validar con |
|---|---|---|---|---|---|
| Unidades, dirección de falla | SI/imperial; izquierda→derecha / derecha→izquierda | 03 §2 (espejo) | P0 | xslope, OGR | VP#1, VP#21 |
| Geometría: contorno externo, límites de materiales | polígonos/regiones | 02 §1 | P0 | OGR `ogr_core/geometry` | todos |
| Importar DXF / formatos .sli/.slim/.slmd | CAD y archivos de Slide2 | — | P1 | xslope `slide2.py` (lector de .sli/.slim/.slmd), `cad.py`; OGR DXF | — |
| Materiales Mohr-Coulomb, no drenado, $S_u$(prof.) | resistencia | 01 §4 | P0 | ambos | VP#1–4, 23–24 |
| Hoek-Brown, potencia, Barton-Bandis, anisotrópicos, SHANSEP, función τ(σ) | resistencia no lineal | 01 §4 | P1–P2 | OGR (18 modelos), xslope (pow, HB) | VP#44–45, 61, 105 |
| Agua: nivel freático, piezométricas, $H_u$, $r_u$ | presión de poros | 01 §3 | P0 | ambos | VP#16, 21, 27, 55 |
| Mallas de presión, filtración EF estacionaria/transitoria | presión de poros | 01 §3 | P2 | xslope `seep.py`, OGR `ogr_fem2d` | VP#10, 38, 71–77; manual Groundwater (21 problemas) |
| Agua libre embalsada | carga hidrostática | 01 §5 | P0 | ambos | VP#10, 42, 65–70 |
| Grieta de tracción (seca/con agua) | geometría + empuje | 01 §3 | P1 | ambos | VP#2, 27, 51–52, 56 |
| Cargas distribuidas y lineales | fuerzas externas | 01 §5, 03 §4 | P0 | ambos | VP#9, 25, 47 |
| Sismo pseudoestático $k_h$, $k_v$ | fuerzas de inercia | 01 §5 | P0 | ambos | VP#4, 51, 62–63 |
| Newmark / $k_y$ | post-proceso | 01 §5 | P2 | OGR `newmark.py` | VP#104 |
| Soportes (anclajes, geotextil, clavos, micropilotes, pilotes Ito-Matsui, helicoidal, usuario) | fuerzas de refuerzo activas/pasivas | 01 §6 | P1 | OGR (7 tipos), xslope (`reinforcement.md`, `piles.md`) | VP#30–32, 37, 47–50, 54, 58–60, 85–94, 106 |
| Métodos LEM (Fellenius, Bishop, Janbu S/C, Spencer, Corps #1/#2, L-K, GLE/M-P, Sarma) | F de una superficie | 03–07 | P0 (Janbu, Spencer, M-P, Bishop) / P1 resto | ambos | VP#1, 6, 8, 21–22, 43, 53 |
| Función entre dovelas GLE | f(x) | 06 §4 | P0 | ambos | VP#7–8, 22 |
| Superficies circulares: Grid, Slope, Auto Refine, Focus | búsqueda | 08 §2 | P0 (Grid) / P1 | OGR `search.py`, xslope `search.py` | VP#1, 14–17, 19 |
| Superficies no circulares: Block, Path, SA, PSO, Cuckoo, Auto Refine NC, Optimize | búsqueda | 08 §3 | P1 | OGR (6 buscadores + optimización), xslope | VP#9, 18–20, 63 |
| Superficies compuestas / capa débil | geometría | 02 §1 | P1 | ambos | VP#22, 57, 61 |
| Superficies definidas por el usuario | F de superficie fija | 03 | P0 | ambos | VP#6, 8, 25–26, 43 |
| Filtros (límites, prof. mín., área, peso, $m_\alpha$, tracción) | admisibilidad | 03 §8, 08 §1 | P0 | ambos | VP#17, 52 |
| Optimización multimodal (MMO) | varios mínimos | 08 §3.4 | P2 | OGR `particle_swarm.py` | VP#103–105 |
| Probabilístico (MC, LHS, Global Min., Overall Slope, $P_f$, β) | confiabilidad | 02 §5 | P1 | OGR `probabilistic.py`, xslope `reliability.py` | VP#28–29, 33–36 |
| Sensibilidad | barrido de variables | 02 §5 | P1 | ambos | VP#40 |
| Retro-análisis (fuerza de soporte requerida) | inversión | 01 §6 | P2 | OGR `back_analysis.py` | VP#37 |
| Desembalse rápido (Corps, L-K, DWW 3 etapas, $\bar B$) | agua transitoria | 01 §3 | P2 | xslope `rapid.md`, OGR `rapid_drawdown.py` | VP#46, 95–102 |
| Normas de diseño (Eurocódigo 7 DA1/DA2/DA3, LRFD) | factores parciales | — | P2 | OGR (EC7) | — |
| Interpretación: datos por dovela, diagramas de fuerza, línea de empujes, contornos de F, informe | post-proceso | 03 §8 | P1 | ambos | — |

## Parámetros por defecto a replicar (según OGR-Slip2D, que dice reproducir los de Slide2)

- 25 dovelas, tolerancia 0.005, 50 iteraciones, métodos por defecto Bishop + Janbu simplificado,
  función GLE semiseno, $m_\alpha$ límite 0.2, Grid 20×20 intervalos y *Radius Increment* 10.
- **Pendiente**: confirmar con el manual de Slide2 (valores de "Project Settings" y "Surface Options").

## Lo que Slide2 NO hace (y un clon no necesita para paridad)

Reducción de resistencia por EF (eso es RS2), análisis 3D (Slide3), deformaciones.
