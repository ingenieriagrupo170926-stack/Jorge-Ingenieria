# Encargo para la fase siguiente (cálculo profundo)

> Para el agente que continúe (p. ej. Claude Opus 5.5). Lee primero `README.md` y
> `grafo/grafo.json`; `python3 grafo/grafo.py pendientes` lista lo abierto.

## Contexto que ya está resuelto (no rehacer)

- La formulación común por dovela y la familia GLE están derivadas y **verificadas**
  (`teoria/03`, `codigo/lem_ref.py`, `practica/11`): Bishop, Janbu simplificado/corregido,
  Spencer y M-P reproducen Fredlund & Krahn (1977) a ≤ 0.36 % y xslope a ≤ 0.14 %.
- Existen clones abiertos de Slide2 que deben leerse antes de escribir código:
  xslope (Apache-2.0) y OGR-Slip2D (AGPL-3.0). Ver `practica/10` para la decisión de licencia.

## Requisito de entorno

Habilitar en la red del entorno los dominios de `fuentes/fuentes.md` §D. Sin ellos no se pueden
leer las fuentes primarias abiertas (M-P 1965, F&K 1977, Zhu 2005, USACE, SLOPE/W, Slide2, GEO5).

## Tareas (en orden) y criterio de terminado

| # | Tarea | Hecho cuando |
|---|---|---|
| 1 | Leer M-P (1965) y transcribir las ecuaciones diferenciales y la integración cerrada por dovela | `teoria/06` §2 sin "pendiente"; implementación opcional que reproduzca el ejemplo del artículo |
| 2 | Leer F&K (1977): tablas completas (incl. Janbu simplificado y riguroso), signos GLE | V1 ampliado con esas columnas; diferencias < 0.5 % |
| 3 | Leer Zhu et al. (2005): ecuación exacta de λ y términos de carga | `lem_ref.zhu()` que reproduzca sus ejemplos y VP#51 (1.293) |
| 4 | Confirmar $b_1$ (0.69 vs 0.67), dominio de $d/L$ y regla para suelos mixtos (Janbu 1973 o Abramson §5.5) | `teoria/04` §3 sin "pendiente" |
| 5 | Implementar Janbu generalizado (GPS) y compararlo con GEO5 si hay acceso a un caso | nodo `janbu_generalizado` en verde |
| 6 | Añadir al solver: capas con polígonos, cargas inclinadas, agua libre, grieta con agua, soportes activos/pasivos | VP#2, 3, 4, 10, 27, 51 ± 1 % |
| 7 | Grid Search con la regla de radios medida + Auto Refine + filtros | VP#1, 14–17 con el mismo centro/radio que Slide2 |
| 8 | No circulares: Block, Path, HSA (Su 2009), Optimize (Greco) | VP#8, 9, 18–20 dentro de la banda publicada |
| 9 | Sarma, ITFM, Shahunyants (si se clona también GEO5) | casos propios o de la ayuda de GEO5 |
| 10 | Probabilístico (MC/LHS, Global Minimum/Overall Slope, β normal/lognormal) | VP#28–29, 33–36 |
| 11 | Servidor MCP mínimo (`practica/10` §4) y flujo del agente con barandillas (§5) | un agente reproduce H1–H3 sin intervención |

## Reglas

- Cada número nuevo en la base debe citar su fuente (autor, año, página/tabla/ecuación) o un
  cálculo reproducible en `codigo/`.
- Actualizar el estado del nodo en `grafo/grafo.py` y regenerar (`python3 grafo/grafo.py`).
- Leer `practica/12-trampas-de-implementacion.md` antes de tocar los solvers.
- No usar copias piratas; si una fuente es de pago, registrarla en `fuentes/fuentes.md` §C.
