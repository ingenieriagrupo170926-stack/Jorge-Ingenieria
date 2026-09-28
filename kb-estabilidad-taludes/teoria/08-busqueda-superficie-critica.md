# 08 · Búsqueda de la superficie crítica

> Nodos: `busqueda`, `grid_search`, `slope_search`, `auto_refine`, `block_search`, `path_search`,
> `simulated_annealing`, `particle_swarm`, `cuckoo_search`, `optimize_surfaces`, `geo5_optimizacion`
> Nivel L3 · Estado: malla + Nelder-Mead y optimización poligonal **verificados** (V3–V4);
> algoritmos de Slide2 **documentados** (ayuda Slide2 + reimplementación medida de OGR-Slip2D).

## 1. Planteamiento

$$\Gamma_{cr} = \arg\min_{\Gamma\in\mathcal A} F(\Gamma)$$

$F(\Gamma)$ es la salida de un método LEM (03–06) y es **no convexa, no diferenciable y con
mesetas**: hay varios mínimos locales (talud con bermas, estratos débiles, pie vs. cuerpo). Por eso
Slide2 recomienda usar **al menos dos métodos de búsqueda** y GEO5 recomienda varios arranques.

$\mathcal A$ (superficies admisibles) se define con filtros; en Slide2 los "Slope Limits" filtran
**siempre**, cualquiera sea el tipo de superficie o el buscador:

| Filtro | Efecto |
|---|---|
| Límites de talud (1 o 2 ventanas) | entrada/salida dentro de los límites |
| Profundidad mínima / área mínima / peso mínimo | evita "rebanadas" superficiales ($c' = 0$ → mínimo trivial talud infinito) |
| Elevación mínima | ningún vértice por debajo |
| Solo convexas | rechaza vértices reflexos (búsquedas no circulares) |
| $m_\alpha \ge 0.2$, $N' \ge 0$, tracción | admisibilidad del cálculo (ver 03 §8) |
| Superficies compuestas | círculo truncado en material impenetrable: $y = \max(y_{circ}, y_{piso})$ |
| Foco (punto/línea/tangente) | pre-filtra círculos antes de evaluarlos |

## 2. Superficies circulares

### 2.1 Grid Search (malla de centros × radios)
1. Rectángulo de centros con $n_x \times n_y$ intervalos → $(n_x+1)(n_y+1)$ centros (Auto Grid o manual).
2. Para cada centro, radios entre un mínimo y un máximo "según la distancia del centro a la
   superficie del talud". **Radius Increment** = número de intervalos → $r_{inc}+1$ círculos por centro.
3. Total por defecto: $21 \times 21 \times 11 = 4851$ círculos. Se conserva el mínimo por centro
   (contornos de F sobre la malla).

Regla de radios **medida** por OGR-Slip2D sobre salidas de Slide2 (no está escrita en la ayuda):
$d_{min}$ = distancia del centro a la superficie del talud entre límites, $d_{max} = \min(|C-P_L|, |C-P_R|)$,
$\delta = 0.05(d_{max}-d_{min})$, radios equiespaciados en $[d_{min}+\delta,\ d_{max}-\delta]$
(error < $10^{-7}$ en 441 centros de dos modelos de referencia). Si el mínimo cae en el borde de la
malla hay que moverla/agrandarla.

### 2.2 Slope Search
Dos puntos aleatorios sobre el terreno (uno hacia el pie, otro hacia la corona, dentro de los
límites) + un **ángulo inicial en el pie** aleatorio dentro de una ventana. El centro es la
intersección de la mediatriz de los dos puntos con la normal a la tangente en el pie. Todos los
círculos generados "afloran" en el talud.

### 2.3 Auto Refine Search (circular)
1. Dividir la superficie del talud (entre límites) en $D$ divisiones medidas **a lo largo** de la
   polilínea.
2. Para cada **par** de divisiones, $c$ círculos por los puntos medios (sobre el terreno) con
   tangente barrida desde la pendiente de la recta que los une hasta la vertical en el punto
   superior → $\binom{D}{2}c$ círculos por iteración.
3. Clasificar divisiones por su F (la ayuda dice promedio; OGR usa el **mínimo** porque el
   promedio no converge hacia mínimos en los extremos — decisión documentada y medida).
4. Conservar la fracción con menor F como nueva zona de búsqueda (tramos contiguos); repetir las
   iteraciones indicadas (sin corte por convergencia).
Suele encontrar F menores que Grid/Slope con el mismo número de superficies.

## 3. Superficies no circulares

### 3.1 Block Search (bloques activo–central–pasivo)
Un punto aleatorio por cada objeto "Block Search" (ventana, línea, polilínea o punto) dibujado
por el usuario; se ordenan por $x$; desde los extremos se proyecta hacia el terreno con ángulos
izquierdo/derecho (por defecto 135° y 45°, antihorario desde +x, o rangos aleatorios). Se descarta
si no aflora dentro de los límites. Opción "solo convexas". Ideal para estratos débiles.

### 3.2 Path Search (XSTABL "Irregular Surface Search")
Punto de inicio aleatorio en la mitad del talud del lado del pie; primer segmento con ángulo
inicial aleatorio en $[-45°, \beta - 5°]$; segmentos siguientes de longitud fija (≈0.3·H) con
dirección aleatoria que **solo puede girar hacia arriba** (cóncava, cinemáticamente admisible);
termina al aflorar; se descarta si sale de los límites o baja de la elevación mínima.

### 3.3 Simulated Annealing híbrido (Slide2; Su 2009, U. Waterloo)
HSA = VFSA (global) + LMC (local, Greco 1996). Variables: $x_2..x_{N-1}$, $y_2..y_{N-1}$
normalizadas a [0,1]; extremos sobre el terreno.
- Generación de Cauchy: $r = \mathrm{sgn}(u - 0.5)\,T\left[(1 + 1/T)^{|2u-1|} - 1\right]$
- Aceptación: $P = 1/\left(1 + e^{\Delta E/T_{acc}}\right)$
- Enfriamiento: $T_k = T_0\,e^{-c\,k^{1/n}}$, $c \approx 8$ (1–10 adecuado)
- Control de razón aceptados/rechazados: >2 → $T_{acc}/2$; <0.5 → $2T_{acc}$
- Límites dinámicos de $y$ según vértices vecinos (Cheng 2007) para evitar autointersecciones.
- LMC: 8 movimientos por vértice $(\pm1, 0, \pm1)^2$; repetir la dirección exitosa; si ninguna
  mejora, reducir el paso de ese vértice por $(1-\varepsilon)$, $\varepsilon = 0.75$; los extremos
  se mueven solo en $x$ sobre el terreno.

### 3.4 Particle Swarm (Slide2)
Forma documentada por Slide2 (sin inercia): $S_{i+1} = S_i + V_i$,
unimodal $V_i = r_1(S_G - S_i) + r_2(S_B - S_i)$; multimodal $V_i = r_1(N_1 - S_i) + r_2(N_2 - S_i)$
($S_G$ mejor global, $S_B$ mejor propio, $N_1, N_2$ vecinos más cercanos → varios mínimos
locales; Qu, Suganthan & Das 2013). Canon: Kennedy & Eberhart (1995).

### 3.5 Cuckoo Search (Slide2; Yang & Deb 2009; Gandomi et al.)
Nidos = superficies; nuevas soluciones por **vuelos de Lévy** (paso con distribución de cola
pesada, algoritmo de Mantegna), abandono de una fracción $p_a$ de los peores nidos. Rocscience
publica una nota técnica ("Locating General Failure Surfaces in Slope Analysis via Cuckoo
Search"). **Pendiente**: parámetros por defecto de Slide2.

### 3.6 Auto Refine no circular
Mismos círculos que 2.3, convertidos a poligonales de $k$ vértices (por defecto 12) sobre las que
se calcula F; optimización activada por defecto. Solo métodos de equilibrio completo (Spencer/GLE)
convergen limpiamente al refinar vértices (OGR midió +0.29 % → +0.01 % de 8 a 64 vértices).

### 3.7 Optimize Surfaces (Slide2) y optimización de GEO5
- Slide2 "Surface Altering Optimization": caminata aleatoria tipo Monte Carlo (Greco 1996) sobre
  los vértices de las mejores superficies; acepta si baja F; el paso se reduce por el
  "Step Reduction Factor"; opción de reaplicar filtros de profundidad/elevación/concavidad.
- GEO5: mueve cada vértice interior en horizontal y vertical y los extremos sobre el terreno;
  paso inicial = 1/10 de la menor distancia entre nodos, se reduce a la mitad por ciclo; advierte
  mínimos locales → varios arranques, incluso desde el círculo crítico.

## 4. Estrategia recomendada para el clon (y para un agente)

```
1. Preflight: geometría cerrada, capas continuas, agua definida, unidades coherentes.
2. Círculo: Grid Search (auto grid) + Auto Refine; revisar que el mínimo no esté en el borde.
3. Refinar localmente el mejor círculo (Nelder-Mead en (xc, yc, R)).
4. No circular: convertir el círculo crítico a poligonal (8–12 vértices) + optimizar
   (GEO5/Greco/Nelder-Mead) y, en paralelo, Block Search si hay estrato débil y SA/PSO/Cuckoo.
5. Recalcular el crítico con Spencer y GLE (y Janbu corregido si se exige).
6. Reportar F, método, geometría, λ/θ, residuales, número de superficies válidas/descartadas.
7. Sensibilidad: nº de dovelas, tolerancia, f(x), semillas aleatorias (≥3), límites.
```

En este repositorio: `buscar_circular` (malla con la regla de radios anterior + Nelder-Mead) y
`optimizar_poligonal` (extremos sobre el terreno + vértices interiores, Nelder-Mead adaptativo).

Fuentes: ayuda Slide2 (Grid/Slope/Auto Refine/Block/Path/SA/PSO/Cuckoo/Optimize); Slide
"Search Methods" (PDF Rocscience); Su (2009); Greco (1996); Cheng (2007); Cheng et al. (2007)
"Performance studies on six heuristic global optimization methods"; Kennedy & Eberhart (1995);
Yang & Deb (2009); GEO5 "Optimization of polygonal slip surface"; OGR `ogr_slip2d/search.py`,
`optimize.py`, `particle_swarm.py`; xslope `search.py`, `docs/lem/search.md`.
