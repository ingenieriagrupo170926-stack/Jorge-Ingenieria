# Grafo de conocimiento — vista general

> Generado por `grafo.py` (no editar a mano). Verde = verificado numéricamente, azul = documentado con fuente accesible, rojo = pendiente de fuente primaria o implementación.
> Flechas continuas: "requiere". Fuentes, benchmarks e implementaciones están en `grafo.json`.

```mermaid
flowchart LR
  subgraph fisica["Fundamentos físicos"]
    equilibrio_limite["Equilibrio límite 2D (rígido-plástico)"]:::documentado
    factor_seguridad["F por reducción uniforme de resistencia"]:::documentado
    tensiones_efectivas["Tensiones efectivas / totales"]:::documentado
    presion_poros["Presión de poros (piezo, Hu, ru, malla, EF)"]:::verificado
    resistencia_mc["Mohr-Coulomb y no drenado"]:::verificado
    resistencia_no_lineal["Hoek-Brown, potencia, Barton-Bandis, anisotropía"]:::documentado
    cargas["Cargas distribuidas, lineales, agua libre"]:::documentado
    sismo["Sismo pseudoestático kh/kv, Newmark"]:::documentado
    soportes["Soportes activos/pasivos"]:::documentado
    grieta["Grieta de tracción"]:::documentado
    desembalse["Desembalse rápido (Corps, L-K, DWW)"]:::pendiente
  end
  subgraph matematica["Fundamentos matemáticos y numéricos"]
    geometria["Geometría computacional (polilíneas, círculos, recortes)"]:::verificado
    dovelado["Dovelado con quiebres obligatorios"]:::verificado
    recurrencia["Recurrencia de fuerzas entre dovelas"]:::verificado
    raices["Raíces no lineales (punto fijo, Brent, polos)"]:::verificado
    newton_2d["Newton 2D en (F, λ)"]:::documentado
    optimizacion["Optimización directa y metaheurísticas"]:::verificado
    probabilidad["Monte Carlo, LHS, Pf, índice β"]:::documentado
  end
  subgraph lem["Métodos de equilibrio límite (dovelas)"]
    incognitas["Balance de incógnitas (6n-2 vs 4n)"]:::documentado
    marco_dovelas["Equilibrio de una dovela (ecuación madre)"]:::verificado
    equilibrio_global["F_f (fuerzas) y F_m (momentos)"]:::verificado
    gle["GLE: X = λ f(x) E"]:::verificado
    funcion_entre_dovelas["Función entre dovelas f(x)"]:::verificado
    admisibilidad["Admisibilidad (mα≥0.2, N'≥0, E>0, empujes)"]:::verificado
    ordinario["Ordinario / Fellenius"]:::documentado
    bishop["Bishop simplificado"]:::verificado
    janbu_simplificado["Janbu simplificado"]:::verificado
    janbu_corregido["Janbu corregido (f0)"]:::verificado
    janbu_generalizado["Janbu generalizado (GPS, 'Janbu' de GEO5)"]:::pendiente
    corps_lk["Corps #1/#2 y Lowe-Karafiath"]:::documentado
    spencer["Spencer"]:::verificado
    morgenstern_price["Morgenstern-Price"]:::verificado
    mp_1965_continuo["M-P 1965 formulación diferencial original"]:::pendiente
    zhu_2005["Algoritmo conciso de Zhu et al. (2005)"]:::pendiente
    sarma["Sarma (dovelas inclinadas, Kc)"]:::pendiente
    itfm["ITFM / Shahunyants (GEO5)"]:::pendiente
  end
  subgraph busqueda["Búsqueda de la superficie crítica"]
    filtros["Filtros y límites de superficie"]:::documentado
    grid_search["Grid Search (centros × radios)"]:::verificado
    slope_search["Slope Search"]:::documentado
    auto_refine["Auto Refine (circular y no circular)"]:::documentado
    block_search["Block Search"]:::documentado
    path_search["Path Search (XSTABL)"]:::documentado
    simulated_annealing["Recocido simulado híbrido (Su 2009)"]:::documentado
    particle_swarm["Enjambre de partículas (uni/multimodal)"]:::documentado
    cuckoo_search["Búsqueda cuco (Lévy)"]:::pendiente
    optimize_surfaces["Optimize Surfaces (Greco) / GEO5 vértices"]:::verificado
  end
  subgraph practica["Práctica: arquitectura, verificación, trampas"]
    arquitectura["Arquitectura del clon + MCP para agentes"]:::documentado
    verificacion["Estrategia y resultados de verificación"]:::verificado
    trampas["Trampas de implementación medidas"]:::documentado
  end
  factor_seguridad --> equilibrio_limite
  resistencia_mc --> tensiones_efectivas
  tensiones_efectivas --> presion_poros
  dovelado --> geometria
  marco_dovelas --> dovelado
  marco_dovelas --> factor_seguridad
  marco_dovelas --> resistencia_mc
  marco_dovelas --> cargas
  marco_dovelas --> sismo
  marco_dovelas --> incognitas
  marco_dovelas --> recurrencia
  equilibrio_global --> marco_dovelas
  gle --> equilibrio_global
  gle --> funcion_entre_dovelas
  gle --> raices
  gle --> admisibilidad
  janbu_simplificado --> equilibrio_global
  janbu_simplificado --> raices
  janbu_simplificado --> admisibilidad
  bishop --> equilibrio_global
  janbu_generalizado --> janbu_simplificado
  spencer --> newton_2d
  morgenstern_price --> gle
  spencer --> gle
  resistencia_no_lineal --> resistencia_mc
  soportes --> cargas
  grid_search --> filtros
  grid_search --> geometria
  optimize_surfaces --> optimizacion
  simulated_annealing --> optimizacion
  particle_swarm --> optimizacion
  cuckoo_search --> optimizacion
  block_search --> filtros
  path_search --> filtros
  auto_refine --> grid_search
  arquitectura --> verificacion
  verificacion --> trampas
  desembalse --> presion_poros
  probabilidad --> grid_search
  janbu_simplificado -. caso de .-> gle
  bishop -. caso de .-> gle
  spencer -. caso de .-> morgenstern_price
  corps_lk -. caso de .-> gle
  janbu_corregido == corrige ==> janbu_simplificado
  zhu_2005 -. resuelve .-> morgenstern_price
  mp_1965_continuo -. resuelve .-> morgenstern_price
  newton_2d -. resuelve .-> spencer
  classDef verificado fill:#d4f4dd,stroke:#2e7d32
  classDef documentado fill:#e3eefc,stroke:#1565c0
  classDef pendiente fill:#fde2e1,stroke:#c62828
```

## Ruta mínima para implementar Morgenstern-Price

1. Geometría computacional (polilíneas, círculos, recortes) — `teoria/02-fundamentos-matematicos.md#1-geometría-computacional-lo-que-más-código-consume-en-un-clon`
2. Dovelado con quiebres obligatorios — `teoria/02-fundamentos-matematicos.md#1-geometría-computacional-lo-que-más-código-consume-en-un-clon`
3. Equilibrio límite 2D (rígido-plástico) — `teoria/01-fundamentos-fisicos.md#1-equilibrio-límite-y-factor-de-seguridad`
4. F por reducción uniforme de resistencia — `teoria/01-fundamentos-fisicos.md#1-equilibrio-límite-y-factor-de-seguridad`
5. Presión de poros (piezo, Hu, ru, malla, EF) — `teoria/01-fundamentos-fisicos.md#3-presión-de-poros-opciones-de-slide2-y-equivalentes`
6. Tensiones efectivas / totales — `teoria/01-fundamentos-fisicos.md#2-tensiones-efectivas-y-totales`
7. Mohr-Coulomb y no drenado — `teoria/01-fundamentos-fisicos.md#4-modelos-de-resistencia-catálogo-de-slide2`
8. Cargas distribuidas, lineales, agua libre — `teoria/01-fundamentos-fisicos.md#5-cargas`
9. Sismo pseudoestático kh/kv, Newmark — `teoria/01-fundamentos-fisicos.md#5-cargas`
10. Balance de incógnitas (6n-2 vs 4n) — `teoria/03-marco-comun-dovelas.md#3-balance-de-incógnitas-por-qué-hacen-falta-hipótesis`
11. Recurrencia de fuerzas entre dovelas — `teoria/02-fundamentos-matematicos.md#2-álgebra-lineal-y-recurrencias`
12. Equilibrio de una dovela (ecuación madre) — `teoria/03-marco-comun-dovelas.md#4-equilibrio-de-una-dovela-derivación-usada-en-el-código`
13. F_f (fuerzas) y F_m (momentos) — `teoria/03-marco-comun-dovelas.md#5-equilibrio-global`
14. Función entre dovelas f(x) — `teoria/06-morgenstern-price-gle.md#4-función-entre-dovelas-fx`
15. Raíces no lineales (punto fijo, Brent, polos) — `teoria/02-fundamentos-matematicos.md#3-ecuaciones-no-lineales`
16. Admisibilidad (mα≥0.2, N'≥0, E>0, empujes) — `teoria/03-marco-comun-dovelas.md#8-controles-de-admisibilidad-obligatorios-antes-de-reportar-f`
17. GLE: X = λ f(x) E — `teoria/03-marco-comun-dovelas.md#6-la-familia-gle-cada-método-es-un-caso-particular`
18. Morgenstern-Price — `teoria/06-morgenstern-price-gle.md`
