# Base de conocimientos: superficies de falla en taludes 2D (Janbu, Janbu corregido, Spencer, Morgenstern-Price)

Base teórica y práctica, organizada como **grafo de conocimiento**, para construir un clon de
Slide2 (Rocscience, 2D) y GEO5 Estabilidad de Taludes, automatizable por agentes. Es la
primera etapa de la investigación: todo lo que dice está citado, verificado con un cálculo
propio o marcado explícitamente como pendiente.

## Qué hay y en qué orden leerlo

```
kb-estabilidad-taludes/
├── README.md                     ← este índice
├── siguiente-fase.md             ← encargo para la investigación profunda (Opus)
├── grafo/
│   ├── grafo.py                  ← fuente del grafo; consultas "ruta" y "pendientes"
│   ├── grafo.json                ← 73 nodos · 206 relaciones (legible por agentes)
│   ├── grafo.md                  ← vista Mermaid (se ve en GitHub)
│   └── grafo.png                 ← la misma vista renderizada
├── teoria/
│   ├── 01-fundamentos-fisicos.md         L1 equilibrio límite, agua, resistencia, cargas, soportes
│   ├── 02-fundamentos-matematicos.md     L1 geometría, dovelado, raíces, optimización, probabilidad
│   ├── 03-marco-comun-dovelas.md         L2 ★ la ecuación madre: todos los métodos salen de aquí
│   ├── 04-janbu.md                       L3 simplificado, corregido (f0) y generalizado (GEO5)
│   ├── 05-spencer.md                     L3
│   ├── 06-morgenstern-price-gle.md       L3 M-P 1965, GLE, f(x), Zhu 2005
│   ├── 07-otros-metodos.md               L3 Fellenius, Bishop, Corps, L-K, Sarma, ITFM
│   ├── 08-busqueda-superficie-critica.md L3 los 9 buscadores de Slide2 + GEO5
│   └── 09-mapa-funciones-slide2.md       L1 todas las funciones de Slide2 → teoría → prioridad → VP#
├── practica/
│   ├── 10-arquitectura-clon-agentico.md  L4 capas, esquema JSON, herramientas MCP, hoja de ruta, licencias
│   ├── 11-verificacion.md                L4 estrategia y resultados
│   └── 12-trampas-de-implementacion.md   L4 28 errores medidos en implementaciones reales
├── codigo/
│   ├── lem_ref.py                ← solver de referencia (Bishop, Janbu S/C, Spencer, M-P, búsqueda)
│   ├── validar.py                ← reproduce los casos publicados
│   └── resultados_validacion.md  ← salida de validar.py
└── fuentes/fuentes.md            ← a qué fuentes se pudo ingresar y a cuáles no, y qué falta de cada una
```

Jerarquía del grafo: **L0** dominio → **L1** áreas → **L2** conceptos y ecuaciones →
**L3** métodos y algoritmos → **L4** implementación, verificación y fuentes. Estados:
🟢 verificado numéricamente aquí · 🔵 documentado con fuente accesible · 🔴 pendiente.

## Hallazgos principales

1. **Un método LEM no busca la superficie.** Calcula $F(\Gamma)$ de una superficie dada; el
   buscador (malla, Auto Refine, Block, Path, recocido, enjambre, cuco, optimización) minimiza
   $F$. Son dos módulos separados en Slide2, GEO5 y en cualquier clon.
2. **Los cuatro métodos pedidos son una sola ecuación.** Con la marcha dovela a dovela de
   `teoria/03` y la hipótesis $X = \lambda f(x)E$: Janbu simplificado = $F_f(\lambda = 0)$;
   Janbu corregido = $f_0 \cdot F_f(0)$; Spencer = $f = 1$; Morgenstern-Price = $f(x)$ cualquiera;
   Bishop = $F_m(0)$. Implementarla bien una vez da todos.
3. **Ya existen clones abiertos de Slide2** que se estudiaron a fondo: **xslope** (Apache-2.0,
   800+ casos verificados contra los manuales de Slide2/SLOPE/W/RS2, lee archivos de Slide2) y
   **OGR-Slip2D** (AGPL-3.0, réplica de los 6 buscadores de Slide2 con reglas medidas y un
   **servidor MCP de 74 herramientas para agentes**). Para un producto cerrado conviene partir
   de xslope; el código AGPL obliga a publicar el propio.
4. **Verificación propia**: el solver de `codigo/` reproduce Fredlund & Krahn (1977) con error
   ≤ 0.36 % en Bishop, Spencer y M-P, a xslope con ≤ 0.14 %, y la búsqueda del ACADS 1(a) da
   0.985 (Slide2 0.987).
5. **Las trampas son numéricas, no teóricas**: polos de $m_\alpha$, raíces espurias de
   $F_f - F_m$ con fuerzas en tracción, proyecciones erróneas, filtros de búsqueda. Están
   catalogadas con su evidencia en `practica/12`.
6. **"Janbu" no es un solo método**: Slide2 ofrece simplificado y corregido; GEO5 llama "Janbu"
   al generalizado (línea de empujes). El apellido es Janbu, no "Jambu".

## Correcciones al documento previo

- $b_1$ para suelo cohesivo: 0.69 según las curvas de Janbu (OGR) y 0.67 según xslope y
  otras fuentes secundarias. Sigue abierto hasta leer Janbu (1973).
- $d$ es la distancia **perpendicular** máxima de la cuerda a la superficie; el polinomio de
  $f_0$ debe recortarse en $d/L = 0.357$.
- El Janbu de GEO5 es el generalizado (arranca con $\delta_i = 0$, $z_i \approx h/3$), no la
  corrección $f_0$.
- Parte de lo que el MD daba como "acceso completo localizado" (F&K 1977, M-P 1965, Zhu 2005)
  **no se pudo abrir desde este entorno** (bloqueo de red): ver `fuentes/fuentes.md`.

## Uso rápido

```bash
pip install numpy scipy
cd codigo && python3 validar.py                 # ~10 min; escribe resultados_validacion.md
python3 ../grafo/grafo.py ruta spencer          # qué hay que saber para implementar Spencer
python3 ../grafo/grafo.py pendientes            # qué falta investigar
```

```python
from lem_ref import Modelo, Capa, circulo, resolver
m = Modelo([Capa([(0, 25), (30, 25), (50, 35), (90, 35)], g=20, c=3, phi=19.6)])
d = circulo(m, 29.63, 53.45, 28.45, n=50)
print({k: round(resolver(d, k, 29.63, 53.45)['F'], 3) for k in ('bishop', 'janbu_corregido', 'spencer', 'mp')})
```

## Para agentes

- Punto de entrada: `grafo/grafo.json` (nodos con `doc` = archivo#sección y `estado`).
- Antes de implementar un nodo: `grafo.py ruta <id>` da los prerrequisitos en orden.
- Antes de reportar un F: aplicar `teoria/03` §8 (admisibilidad) y `practica/10` §5 (barandillas).
