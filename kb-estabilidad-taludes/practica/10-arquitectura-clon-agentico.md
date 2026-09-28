# 10 · Arquitectura de un clon de Slide2 automatizable por agentes

> Nodo: `arquitectura` · Nivel L4 · Estado: **propuesta** basada en xslope, OGR-Slip2D y este repo.

## 1. Decisión previa: construir, reutilizar o bifurcar

Ya existen tres clones abiertos que resuelven gran parte del problema. Leerlos ahorra meses.

| Proyecto | Licencia | Qué aporta | Implicación |
|---|---|---|---|
| **xslope** (N. L. Jones) | Apache-2.0 | 7 métodos LEM, búsqueda, EF de filtración y SSR, confiabilidad, **lector de archivos Slide2** (.sli/.slim/.slmd), 800+ casos verificados contra Slide2/SLOPE/W/RS2 | Se puede reutilizar/modificar en software cerrado conservando el aviso de licencia |
| **OGR-Slip2D** (S. Sáez López, UPCT) | AGPL-3.0 | réplica funcional de Slide2: 9 métodos, 6 buscadores + optimización, 18 modelos de resistencia, 7 soportes, probabilístico, EC7, **servidor MCP con 74 herramientas** | Copyleft fuerte: si se usa su código, incluso como servicio web, hay que publicar el código propio bajo AGPL |
| **lythosle** | AGPL-3.0 | 8 métodos sin dependencias, interfaz web | igual que OGR |
| pybimstab | BSD-2 | GLE + superficies en suelos bloque-matriz | permisiva |

Recomendación: estudiar ambos, **tomar xslope como base de código** si el producto será cerrado,
y usar OGR/lythosle solo como referencia de comportamiento (ideas y valores, no código). Para
uso interno sin distribución la AGPL no obliga a publicar, pero un servicio accesible por red sí.

## 2. Capas

```
┌────────────── agentes (Claude u otros) ──────────────┐
│  MCP server  ·  CLI  ·  API Python  ·  (GUI opcional) │
└───────────────┬──────────────────────────────────────┘
                ▼
  modelo (JSON, fuente de verdad, versionable)
                ▼
  núcleo: geometría → materiales → agua → cargas/soportes → dovelado
                ▼
  solvers LEM (registro de plugins: bishop, janbu, janbu_c, spencer, gle, corps, lk, sarma)
                ▼
  búsqueda (grid, slope, auto-refine, block, path, SA, PSO, cuckoo, optimize)
                ▼
  post-proceso (dovelas, fuerzas, línea de empujes, residuales) · probabilístico · informe
```

Reglas de OGR que conviene copiar: núcleo sin dependencias de GUI; un solo "dovelador" como
puente geométrico; todos los métodos consumen el mismo objeto de dovelas y devuelven el mismo
resultado; unidades SI internas y conversión solo en la frontera; validar contra referencias
externas, **nunca** contra instantáneas de la propia salida.

## 3. Esquema de modelo (propuesta mínima)

```json
{
  "unidades": "SI", "direccion_falla": "derecha_a_izquierda",
  "geometria": {"terreno": [[0,25],[30,25],[50,35],[90,35]],
                "capas": [{"id": "arcilla", "techo": [[0,25],[30,25],[50,35],[90,35]]}]},
  "materiales": {"arcilla": {"modelo": "mohr_coulomb", "gamma": 20, "c": 3, "phi": 19.6,
                             "agua": "ninguna"}},
  "agua": {"piezometricas": [], "ru": 0.0, "gamma_w": 9.81},
  "cargas": {"distribuidas": [], "sismo": {"kh": 0.0, "kv": 0.0}},
  "soportes": [],
  "analisis": {"metodos": ["spencer", "gle", "janbu_corregido"], "dovelas": 50,
               "tolerancia": 1e-4, "gle_funcion": "semiseno"},
  "busqueda": {"tipo": "grid", "no_circular": ["optimize"], "limites": [20, 70],
               "profundidad_min": 0.5, "semilla": 1}
}
```

## 4. Herramientas para agentes (MCP) — mínimo útil

| Herramienta | Entrada | Salida |
|---|---|---|
| `modelo_crear` / `modelo_validar` | JSON | errores de preflight (capas abiertas, agua fuera de rango, unidades) |
| `superficie_evaluar` | modelo + superficie + métodos | F por método, λ/θ, residuales, avisos de admisibilidad |
| `busqueda_ejecutar` | modelo + estrategia + semilla | superficie crítica, F, nº de superficies válidas/rechazadas |
| `sensibilidad` | variable, rango | curva F(variable) |
| `probabilistico` | distribuciones, N, tipo | $P_f$, β, histograma |
| `dovelas_tabla` | resultado | W, α, N, S, E, X, u por dovela |
| `figura` | resultado | PNG de la sección con la superficie |
| `informe` | resultado | Markdown/PDF trazable |

OGR-Slip2D ya implementa este patrón (74 herramientas, perfiles "compact" para modelos locales,
transporte stdio/HTTP con token): ver `docs/mcp/` de su repositorio.

## 5. Flujo de trabajo del agente y barandillas

1. **Preflight** antes de calcular (geometría, materiales, agua, unidades, límites).
2. Búsqueda con **≥ 2 buscadores** y ≥ 3 semillas en los aleatorios; circular y no circular.
3. Recalcular la superficie crítica con Spencer **y** GLE; reportar diferencia.
4. Rechazar resultados con $m_\alpha < 0.2$, $N' < 0$ extendido, fuerzas entre dovelas en
   tracción o residuales > tolerancia; decir por qué (no devolver un número "silencioso").
5. Sensibilidad mínima: nº de dovelas (25/50/100), $f(x)$, nivel freático.
6. Informe con trazabilidad: versión del motor, método, parámetros, superficie, F, λ/θ, residuales.
7. Nunca inventar parámetros geotécnicos: si faltan, preguntar o marcar supuestos.

## 6. Hoja de ruta con criterios de aceptación

| Hito | Contenido | Criterio de aceptación |
|---|---|---|
| H1 | dovelado + Bishop/Janbu/Spencer/GLE en superficie fija | F&K (VP#21) los tres casos ± 0.5 %; identidades V2 |
| H2 | capas, agua, cargas, sismo, grieta | VP#2, 3, 4, 10, 27, 51 ± 1 % |
| H3 | Grid + Auto Refine + filtros | VP#1, 14–17 ± 1 % (mismo centro/radio que Slide2) |
| H4 | no circular (Block, Path, SA, Optimize) | VP#8, 9, 18–20 dentro de la banda publicada |
| H5 | soportes activos/pasivos | VP#30–32, 47–50, 58–60 ± 2 % |
| H6 | probabilístico y sensibilidad | VP#28–29, 33–36, 40 |
| H7 | MCP + informe | agente reproduce H1–H3 sin intervención |
| H8 | filtración EF, desembalse, Newmark, EC7 | manual Groundwater; VP#46, 96–104 |
