"""Grafo de conocimiento de la base (fuente única de verdad del grafo).

  python3 grafo.py              -> regenera grafo.json y grafo.md (Mermaid)
  python3 grafo.py ruta spencer -> prerrequisitos ordenados para implementar/entender un nodo
  python3 grafo.py pendientes   -> nodos cuyo estado es 'pendiente' (tareas de la fase siguiente)

Nodo: (id, nombre, tipo, nivel, doc, estado). Estados: verificado (reproducido numéricamente en
codigo/), documentado (fuente accesible leída), pendiente (falta fuente primaria o implementación).
Relaciones: parte_de, requiere, caso_de, corrige, resuelve, usa, valida_con, fuente, implementado_en.
"""
import json, sys
from pathlib import Path

T, P, M, B, S = 'teoria/', 'practica/', 'teoria/03-marco-comun-dovelas.md', 'practica/11-verificacion.md', 'fuentes/fuentes.md'
N = [  # id, nombre, tipo, nivel, doc, estado
    ('kb', 'Estabilidad de taludes 2D por equilibrio límite (clon Slide2)', 'dominio', 0, 'README.md', 'documentado'),
    # L1 áreas
    ('fisica', 'Fundamentos físicos', 'area', 1, T + '01-fundamentos-fisicos.md', 'documentado'),
    ('matematica', 'Fundamentos matemáticos y numéricos', 'area', 1, T + '02-fundamentos-matematicos.md', 'documentado'),
    ('lem', 'Métodos de equilibrio límite (dovelas)', 'area', 1, M, 'verificado'),
    ('busqueda', 'Búsqueda de la superficie crítica', 'area', 1, T + '08-busqueda-superficie-critica.md', 'verificado'),
    ('slide2_funciones', 'Mapa funcional de Slide2 (backlog)', 'area', 1, T + '09-mapa-funciones-slide2.md', 'documentado'),
    ('practica', 'Práctica: arquitectura, verificación, trampas', 'area', 1, P + '10-arquitectura-clon-agentico.md', 'documentado'),
    ('fuentes', 'Fuentes accesibles / no accesibles', 'area', 1, S, 'documentado'),
    # L2 física
    ('equilibrio_limite', 'Equilibrio límite 2D (rígido-plástico)', 'concepto', 2, T + '01-fundamentos-fisicos.md#1-equilibrio-límite-y-factor-de-seguridad', 'documentado'),
    ('factor_seguridad', 'F por reducción uniforme de resistencia', 'concepto', 2, T + '01-fundamentos-fisicos.md#1-equilibrio-límite-y-factor-de-seguridad', 'documentado'),
    ('tensiones_efectivas', 'Tensiones efectivas / totales', 'concepto', 2, T + '01-fundamentos-fisicos.md#2-tensiones-efectivas-y-totales', 'documentado'),
    ('presion_poros', 'Presión de poros (piezo, Hu, ru, malla, EF)', 'concepto', 2, T + '01-fundamentos-fisicos.md#3-presión-de-poros-opciones-de-slide2-y-equivalentes', 'verificado'),
    ('resistencia_mc', 'Mohr-Coulomb y no drenado', 'concepto', 2, T + '01-fundamentos-fisicos.md#4-modelos-de-resistencia-catálogo-de-slide2', 'verificado'),
    ('resistencia_no_lineal', 'Hoek-Brown, potencia, Barton-Bandis, anisotropía', 'concepto', 2, T + '01-fundamentos-fisicos.md#4-modelos-de-resistencia-catálogo-de-slide2', 'documentado'),
    ('cargas', 'Cargas distribuidas, lineales, agua libre', 'concepto', 2, T + '01-fundamentos-fisicos.md#5-cargas', 'documentado'),
    ('sismo', 'Sismo pseudoestático kh/kv, Newmark', 'concepto', 2, T + '01-fundamentos-fisicos.md#5-cargas', 'documentado'),
    ('soportes', 'Soportes activos/pasivos', 'concepto', 2, T + '01-fundamentos-fisicos.md#6-refuerzos-y-soportes-catálogo-de-slide2', 'documentado'),
    ('grieta', 'Grieta de tracción', 'concepto', 2, T + '01-fundamentos-fisicos.md#3-presión-de-poros-opciones-de-slide2-y-equivalentes', 'documentado'),
    ('desembalse', 'Desembalse rápido (Corps, L-K, DWW)', 'concepto', 2, T + '01-fundamentos-fisicos.md#3-presión-de-poros-opciones-de-slide2-y-equivalentes', 'pendiente'),
    # L2 matemática
    ('geometria', 'Geometría computacional (polilíneas, círculos, recortes)', 'concepto', 2, T + '02-fundamentos-matematicos.md#1-geometría-computacional-lo-que-más-código-consume-en-un-clon', 'verificado'),
    ('dovelado', 'Dovelado con quiebres obligatorios', 'concepto', 2, T + '02-fundamentos-matematicos.md#1-geometría-computacional-lo-que-más-código-consume-en-un-clon', 'verificado'),
    ('recurrencia', 'Recurrencia de fuerzas entre dovelas', 'concepto', 2, T + '02-fundamentos-matematicos.md#2-álgebra-lineal-y-recurrencias', 'verificado'),
    ('raices', 'Raíces no lineales (punto fijo, Brent, polos)', 'concepto', 2, T + '02-fundamentos-matematicos.md#3-ecuaciones-no-lineales', 'verificado'),
    ('newton_2d', 'Newton 2D en (F, λ)', 'concepto', 2, T + '05-spencer.md#2-formulación-q-utexas-s-g-wright--la-más-directa-de-programar', 'documentado'),
    ('optimizacion', 'Optimización directa y metaheurísticas', 'concepto', 2, T + '02-fundamentos-matematicos.md#4-optimización-búsqueda-de-la-superficie-crítica', 'verificado'),
    ('probabilidad', 'Monte Carlo, LHS, Pf, índice β', 'concepto', 2, T + '02-fundamentos-matematicos.md#5-probabilidad-y-confiabilidad-módulo-probabilístico-de-slide2', 'documentado'),
    # L2 LEM
    ('incognitas', 'Balance de incógnitas (6n-2 vs 4n)', 'concepto', 2, M + '#3-balance-de-incógnitas-por-qué-hacen-falta-hipótesis', 'documentado'),
    ('marco_dovelas', 'Equilibrio de una dovela (ecuación madre)', 'ecuacion', 2, M + '#4-equilibrio-de-una-dovela-derivación-usada-en-el-código', 'verificado'),
    ('equilibrio_global', 'F_f (fuerzas) y F_m (momentos)', 'ecuacion', 2, M + '#5-equilibrio-global', 'verificado'),
    ('gle', 'GLE: X = λ f(x) E', 'metodo', 2, M + '#6-la-familia-gle-cada-método-es-un-caso-particular', 'verificado'),
    ('funcion_entre_dovelas', 'Función entre dovelas f(x)', 'concepto', 2, T + '06-morgenstern-price-gle.md#4-función-entre-dovelas-fx', 'verificado'),
    ('admisibilidad', 'Admisibilidad (mα≥0.2, N\'≥0, E>0, empujes)', 'concepto', 2, M + '#8-controles-de-admisibilidad-obligatorios-antes-de-reportar-f', 'verificado'),
    # L3 métodos
    ('ordinario', 'Ordinario / Fellenius', 'metodo', 3, T + '07-otros-metodos.md', 'documentado'),
    ('bishop', 'Bishop simplificado', 'metodo', 3, T + '07-otros-metodos.md', 'verificado'),
    ('janbu_simplificado', 'Janbu simplificado', 'metodo', 3, T + '04-janbu.md#2-janbu-simplificado', 'verificado'),
    ('janbu_corregido', 'Janbu corregido (f0)', 'metodo', 3, T + '04-janbu.md#3-janbu-corregido', 'verificado'),
    ('janbu_generalizado', 'Janbu generalizado (GPS, "Janbu" de GEO5)', 'metodo', 3, T + '04-janbu.md#4-janbu-generalizado-gps--base-para-clonar-geo5', 'pendiente'),
    ('corps_lk', 'Corps #1/#2 y Lowe-Karafiath', 'metodo', 3, T + '07-otros-metodos.md', 'documentado'),
    ('spencer', 'Spencer', 'metodo', 3, T + '05-spencer.md', 'verificado'),
    ('morgenstern_price', 'Morgenstern-Price', 'metodo', 3, T + '06-morgenstern-price-gle.md', 'verificado'),
    ('mp_1965_continuo', 'M-P 1965 formulación diferencial original', 'ecuacion', 3, T + '06-morgenstern-price-gle.md#2-formulación-continua-original-1965--estructura', 'pendiente'),
    ('zhu_2005', 'Algoritmo conciso de Zhu et al. (2005)', 'algoritmo', 3, T + '06-morgenstern-price-gle.md#5-algoritmo-conciso-de-zhu-lee-qian--chen-2005', 'pendiente'),
    ('sarma', 'Sarma (dovelas inclinadas, Kc)', 'metodo', 3, T + '07-otros-metodos.md', 'pendiente'),
    ('itfm', 'ITFM / Shahunyants (GEO5)', 'metodo', 3, T + '07-otros-metodos.md', 'pendiente'),
    # L3 búsqueda
    ('filtros', 'Filtros y límites de superficie', 'concepto', 2, T + '08-busqueda-superficie-critica.md#1-planteamiento', 'documentado'),
    ('grid_search', 'Grid Search (centros × radios)', 'algoritmo', 3, T + '08-busqueda-superficie-critica.md#21-grid-search-malla-de-centros--radios', 'verificado'),
    ('slope_search', 'Slope Search', 'algoritmo', 3, T + '08-busqueda-superficie-critica.md#22-slope-search', 'documentado'),
    ('auto_refine', 'Auto Refine (circular y no circular)', 'algoritmo', 3, T + '08-busqueda-superficie-critica.md#23-auto-refine-search-circular', 'documentado'),
    ('block_search', 'Block Search', 'algoritmo', 3, T + '08-busqueda-superficie-critica.md#31-block-search-bloques-activocentralpasivo', 'documentado'),
    ('path_search', 'Path Search (XSTABL)', 'algoritmo', 3, T + '08-busqueda-superficie-critica.md#32-path-search-xstabl-irregular-surface-search', 'documentado'),
    ('simulated_annealing', 'Recocido simulado híbrido (Su 2009)', 'algoritmo', 3, T + '08-busqueda-superficie-critica.md#33-simulated-annealing-híbrido-slide2-su-2009-u-waterloo', 'documentado'),
    ('particle_swarm', 'Enjambre de partículas (uni/multimodal)', 'algoritmo', 3, T + '08-busqueda-superficie-critica.md#34-particle-swarm-slide2', 'documentado'),
    ('cuckoo_search', 'Búsqueda cuco (Lévy)', 'algoritmo', 3, T + '08-busqueda-superficie-critica.md#35-cuckoo-search-slide2-yang--deb-2009-gandomi-et-al', 'pendiente'),
    ('optimize_surfaces', 'Optimize Surfaces (Greco) / GEO5 vértices', 'algoritmo', 3, T + '08-busqueda-superficie-critica.md#37-optimize-surfaces-slide2-y-optimización-de-geo5', 'verificado'),
    # L4 práctica
    ('arquitectura', 'Arquitectura del clon + MCP para agentes', 'practica', 4, P + '10-arquitectura-clon-agentico.md', 'documentado'),
    ('verificacion', 'Estrategia y resultados de verificación', 'practica', 4, B, 'verificado'),
    ('trampas', 'Trampas de implementación medidas', 'practica', 4, P + '12-trampas-de-implementacion.md', 'documentado'),
    ('lem_ref', 'Solver de referencia (este repo)', 'implementacion', 4, 'codigo/lem_ref.py', 'verificado'),
    ('xslope', 'xslope (Apache-2.0)', 'implementacion', 4, S, 'documentado'),
    ('ogr', 'OGR-Slip2D (AGPL-3.0, MCP)', 'implementacion', 4, S, 'documentado'),
    # benchmarks
    ('bm_fk1977', 'Fredlund & Krahn 1977 = Slide2 VP#21', 'benchmark', 4, B, 'verificado'),
    ('bm_acads1a', 'ACADS 1(a) = Slide2 VP#1', 'benchmark', 4, B, 'verificado'),
    ('bm_slide2', 'Manual de verificación Slide2 (111 VP)', 'benchmark', 4, B, 'documentado'),
    ('bm_talbingo', 'Talbingo VP#6 (raíz espuria)', 'benchmark', 4, B, 'documentado'),
    # fuentes primarias (estado = acceso)
    ('src_mp1965', 'Morgenstern & Price 1965 (abierto, red bloqueada)', 'fuente', 4, S, 'pendiente'),
    ('src_fk1977', 'Fredlund & Krahn 1977 (abierto, red bloqueada)', 'fuente', 4, S, 'pendiente'),
    ('src_spencer1967', 'Spencer 1967 (pago)', 'fuente', 4, S, 'pendiente'),
    ('src_janbu1973', 'Janbu 1973 (pago)', 'fuente', 4, S, 'pendiente'),
    ('src_zhu2005', 'Zhu et al. 2005 (abierto, red bloqueada)', 'fuente', 4, S, 'pendiente'),
    ('src_utexas', 'UTEXAS2 App. A Wright (vía xslope)', 'fuente', 4, S, 'documentado'),
    ('src_su2009', 'Su 2009 HSA (vía OGR)', 'fuente', 4, S, 'documentado'),
    ('src_geo5', 'Ayuda GEO5 (ecuaciones en imagen)', 'fuente', 4, S, 'pendiente'),
    ('src_slide2_help', 'Ayuda Slide2 (vía OGR/xslope)', 'fuente', 4, S, 'documentado'),
]
E = [  # origen, relación, destino
    *[(h, 'parte_de', 'kb') for h in ('fisica', 'matematica', 'lem', 'busqueda', 'slide2_funciones', 'practica', 'fuentes')],
    *[(h, 'parte_de', 'fisica') for h in ('equilibrio_limite', 'factor_seguridad', 'tensiones_efectivas', 'presion_poros', 'resistencia_mc', 'resistencia_no_lineal', 'cargas', 'sismo', 'soportes', 'grieta', 'desembalse')],
    *[(h, 'parte_de', 'matematica') for h in ('geometria', 'dovelado', 'recurrencia', 'raices', 'newton_2d', 'optimizacion', 'probabilidad')],
    *[(h, 'parte_de', 'lem') for h in ('incognitas', 'marco_dovelas', 'equilibrio_global', 'gle', 'funcion_entre_dovelas', 'admisibilidad', 'ordinario', 'bishop', 'janbu_simplificado', 'janbu_corregido', 'janbu_generalizado', 'corps_lk', 'spencer', 'morgenstern_price', 'mp_1965_continuo', 'zhu_2005', 'sarma', 'itfm')],
    *[(h, 'parte_de', 'busqueda') for h in ('filtros', 'grid_search', 'slope_search', 'auto_refine', 'block_search', 'path_search', 'simulated_annealing', 'particle_swarm', 'cuckoo_search', 'optimize_surfaces')],
    *[(h, 'parte_de', 'practica') for h in ('arquitectura', 'verificacion', 'trampas', 'lem_ref', 'xslope', 'ogr', 'bm_fk1977', 'bm_acads1a', 'bm_slide2', 'bm_talbingo')],
    *[(h, 'parte_de', 'fuentes') for h in ('src_mp1965', 'src_fk1977', 'src_spencer1967', 'src_janbu1973', 'src_zhu2005', 'src_utexas', 'src_su2009', 'src_geo5', 'src_slide2_help')],
    # prerrequisitos
    ('factor_seguridad', 'requiere', 'equilibrio_limite'), ('resistencia_mc', 'requiere', 'tensiones_efectivas'),
    ('tensiones_efectivas', 'requiere', 'presion_poros'), ('dovelado', 'requiere', 'geometria'),
    ('marco_dovelas', 'requiere', 'dovelado'), ('marco_dovelas', 'requiere', 'factor_seguridad'),
    ('marco_dovelas', 'requiere', 'resistencia_mc'), ('marco_dovelas', 'requiere', 'cargas'),
    ('marco_dovelas', 'requiere', 'sismo'), ('marco_dovelas', 'requiere', 'incognitas'),
    ('marco_dovelas', 'requiere', 'recurrencia'), ('equilibrio_global', 'requiere', 'marco_dovelas'),
    ('gle', 'requiere', 'equilibrio_global'), ('gle', 'requiere', 'funcion_entre_dovelas'),
    ('gle', 'requiere', 'raices'), ('gle', 'requiere', 'admisibilidad'),
    ('janbu_simplificado', 'requiere', 'equilibrio_global'), ('janbu_simplificado', 'requiere', 'raices'),
    ('janbu_simplificado', 'requiere', 'admisibilidad'), ('bishop', 'requiere', 'equilibrio_global'),
    ('janbu_generalizado', 'requiere', 'janbu_simplificado'), ('spencer', 'requiere', 'newton_2d'),
    ('morgenstern_price', 'requiere', 'gle'), ('spencer', 'requiere', 'gle'),
    ('resistencia_no_lineal', 'requiere', 'resistencia_mc'), ('soportes', 'requiere', 'cargas'),
    ('grid_search', 'requiere', 'filtros'), ('grid_search', 'requiere', 'geometria'),
    ('optimize_surfaces', 'requiere', 'optimizacion'), ('simulated_annealing', 'requiere', 'optimizacion'),
    ('particle_swarm', 'requiere', 'optimizacion'), ('cuckoo_search', 'requiere', 'optimizacion'),
    ('block_search', 'requiere', 'filtros'), ('path_search', 'requiere', 'filtros'), ('auto_refine', 'requiere', 'grid_search'),
    ('arquitectura', 'requiere', 'verificacion'), ('verificacion', 'requiere', 'trampas'),
    ('desembalse', 'requiere', 'presion_poros'), ('probabilidad', 'requiere', 'grid_search'),
    # casos particulares y relaciones entre métodos
    ('janbu_simplificado', 'caso_de', 'gle'), ('bishop', 'caso_de', 'gle'), ('spencer', 'caso_de', 'morgenstern_price'),
    ('corps_lk', 'caso_de', 'gle'), ('janbu_corregido', 'corrige', 'janbu_simplificado'),
    ('zhu_2005', 'resuelve', 'morgenstern_price'), ('mp_1965_continuo', 'resuelve', 'morgenstern_price'),
    ('newton_2d', 'resuelve', 'spencer'),
    *[(a, 'usa', m) for a in ('grid_search', 'slope_search', 'auto_refine', 'block_search', 'path_search', 'simulated_annealing', 'particle_swarm', 'cuckoo_search', 'optimize_surfaces') for m in ('janbu_corregido', 'spencer', 'morgenstern_price')],
    # verificación, fuentes, implementaciones
    *[(m, 'valida_con', 'bm_fk1977') for m in ('bishop', 'janbu_simplificado', 'janbu_corregido', 'spencer', 'morgenstern_price')],
    ('grid_search', 'valida_con', 'bm_acads1a'), ('optimize_surfaces', 'valida_con', 'bm_acads1a'),
    ('admisibilidad', 'valida_con', 'bm_talbingo'), ('arquitectura', 'valida_con', 'bm_slide2'),
    ('morgenstern_price', 'fuente', 'src_mp1965'), ('mp_1965_continuo', 'fuente', 'src_mp1965'), ('gle', 'fuente', 'src_fk1977'),
    ('spencer', 'fuente', 'src_spencer1967'), ('spencer', 'fuente', 'src_utexas'), ('janbu_corregido', 'fuente', 'src_janbu1973'),
    ('janbu_generalizado', 'fuente', 'src_janbu1973'), ('janbu_generalizado', 'fuente', 'src_geo5'),
    ('zhu_2005', 'fuente', 'src_zhu2005'), ('simulated_annealing', 'fuente', 'src_su2009'),
    *[(a, 'fuente', 'src_slide2_help') for a in ('grid_search', 'slope_search', 'auto_refine', 'block_search', 'path_search', 'particle_swarm', 'cuckoo_search', 'optimize_surfaces', 'soportes', 'funcion_entre_dovelas')],
    *[(m, 'implementado_en', 'lem_ref') for m in ('bishop', 'janbu_simplificado', 'janbu_corregido', 'spencer', 'morgenstern_price', 'grid_search', 'optimize_surfaces')],
    *[(m, 'implementado_en', 'xslope') for m in ('bishop', 'janbu_corregido', 'spencer', 'morgenstern_price', 'corps_lk', 'grid_search', 'desembalse', 'probabilidad')],
    *[(m, 'implementado_en', 'ogr') for m in ('bishop', 'janbu_corregido', 'spencer', 'morgenstern_price', 'corps_lk', 'grid_search', 'slope_search', 'auto_refine', 'block_search', 'path_search', 'simulated_annealing', 'particle_swarm', 'optimize_surfaces', 'soportes', 'probabilidad', 'desembalse')],
]
ID = {n[0]: n for n in N}
assert all(a in ID and b in ID for a, _, b in E), [e for e in E if e[0] not in ID or e[2] not in ID]


def ruta(objetivo):
    """Prerrequisitos (requiere / caso_de / corrige / parte_de hacia conceptos) en orden topológico."""
    visto, orden = set(), []
    def dfs(v):
        if v in visto: return
        visto.add(v)
        for a, r, b in E:
            if a == v and r in ('requiere', 'caso_de', 'corrige'): dfs(b)
        orden.append(v)
    dfs(objetivo); return [ID[v] for v in orden]


def mermaid():
    color = {'verificado': 'fill:#d4f4dd,stroke:#2e7d32', 'documentado': 'fill:#e3eefc,stroke:#1565c0', 'pendiente': 'fill:#fde2e1,stroke:#c62828'}
    areas = [n for n in N if n[3] == 1]
    L = ['```mermaid', 'flowchart LR']
    for a in areas:
        hijos = [b for b, r, p in E if r == 'parte_de' and p == a[0] and ID[b][2] not in ('fuente', 'benchmark', 'implementacion')]
        if not hijos: continue
        L.append(f'  subgraph {a[0]}["{a[1]}"]')
        L += [f'    {h}["{ID[h][1].replace(chr(34), chr(39))}"]:::{ID[h][5]}' for h in hijos]
        L.append('  end')
    etiqueta = {'requiere': '-->', 'caso_de': '-. caso de .->', 'corrige': '== corrige ==>', 'resuelve': '-. resuelve .->'}
    visibles = {h for h in ID if ID[h][2] not in ('fuente', 'benchmark', 'implementacion') and ID[h][3] >= 2}
    L += [f'  {a} {etiqueta[r]} {b}' for a, r, b in E if r in etiqueta and a in visibles and b in visibles]
    L += [f'  classDef {k} {v}' for k, v in color.items()] + ['```']
    return '\n'.join(L)


if __name__ == '__main__':
    aqui = Path(__file__).parent
    if len(sys.argv) > 2 and sys.argv[1] == 'ruta':
        for i, n in enumerate(ruta(sys.argv[2]), 1): print(f'{i:2d}. [{n[5]:11s}] {n[1]}  →  {n[4]}')
    elif len(sys.argv) > 1 and sys.argv[1] == 'pendientes':
        for n in N:
            if n[5] == 'pendiente': print(f'- {n[0]}: {n[1]}  →  {n[4]}')
    else:
        (aqui / 'grafo.json').write_text(json.dumps({
            'nodos': [dict(zip(('id', 'nombre', 'tipo', 'nivel', 'doc', 'estado'), n)) for n in N],
            'aristas': [dict(origen=a, relacion=r, destino=b) for a, r, b in E]}, ensure_ascii=False, indent=1))
        (aqui / 'grafo.md').write_text(
            '# Grafo de conocimiento — vista general\n\n'
            '> Generado por `grafo.py` (no editar a mano). Verde = verificado numéricamente, azul = '
            'documentado con fuente accesible, rojo = pendiente de fuente primaria o implementación.\n'
            '> Flechas continuas: "requiere". Fuentes, benchmarks e implementaciones están en `grafo.json`.\n\n'
            + mermaid() + '\n\n## Ruta mínima para implementar Morgenstern-Price\n\n'
            + '\n'.join(f'{i}. {n[1]} — `{n[4]}`' for i, n in enumerate(ruta('morgenstern_price'), 1)) + '\n')
        print(f'{len(N)} nodos, {len(E)} aristas -> grafo.json, grafo.md')
