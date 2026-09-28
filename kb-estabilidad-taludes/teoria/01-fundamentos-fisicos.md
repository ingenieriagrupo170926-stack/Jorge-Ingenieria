# 01 · Fundamentos físicos

> Nodos: `equilibrio_limite`, `factor_seguridad`, `resistencia`, `agua`, `cargas`, `soporte` · Nivel L1–L2
> Estado: **documentado** (USACE EM 1110-2-1902, xslope, OGR, ayuda Slide2/GEO5).

## 1. Equilibrio límite y factor de seguridad

- Estática en 2D: $\sum F_x = 0$, $\sum F_y = 0$, $\sum M = 0$.
- Definición de F adoptada por Slide2, GEO5, SLOPE/W: **reducción uniforme de resistencia**
  $\tau_{mov} = s/F$ ⇔ $c_d = c/F$, $\tan\phi_d = \tan\phi/F$ en toda la superficie.
- El LEM no calcula deformaciones ni garantiza compatibilidad cinemática; supone movilización
  simultánea. En arcillas rígidas fisuradas, lutitas y superficies reactivadas la falla progresiva
  invalida la resistencia pico → usar resistencia totalmente ablandada o residual (USACE).
- Complemento: reducción de resistencia por elementos finitos (SSR, RS2/PLAXIS) — el mecanismo
  emerge sin suponer superficie (Griffiths & Lane 1999; Dawson et al. 1999). No es parte de Slide2
  pero sirve de verificación cruzada.

## 2. Tensiones efectivas y totales

$$\tau_f = c' + (\sigma_n - u)\tan\phi' \quad\text{(efectivas, drenado)}\qquad \tau_f = S_u \quad(\phi = 0,\ \text{no drenado})$$

- Análisis no drenado en tensiones totales: parámetros totales y **u = 0** en el cálculo (si no,
  se descuenta dos veces el agua). El peso del agua libre sí actúa como carga.
- Nunca usar pesos sumergidos $\gamma'$ como atajo: solo es exacto sin flujo; con flujo omite las
  fuerzas de filtración (talud infinito con flujo paralelo: F cae ≈ a la mitad). Usar pesos totales
  + presiones de poros explícitas + agua libre como carga (práctica de S. G. Wright; xslope).

## 3. Presión de poros (opciones de Slide2 y equivalentes)

| Opción | Fórmula | Nota |
|---|---|---|
| Línea piezométrica | $u = \gamma_w (y_p - y)$ | carga estática completa |
| Nivel freático con corrección Hu | $u = \gamma_w (y_p - y)\cos^2\theta$ | θ = inclinación de la línea sobre el punto ("Hu = Auto" en Slide2) |
| Coeficiente $r_u$ | $u = r_u\,\sigma_v$ | $\sigma_v$ = columna de suelo (sin cargas externas) |
| Malla de presiones | interpolación (triangulación, spline, inverso de distancia) | datos medidos |
| Filtración por EF | $u$ interpolado de la solución (estacionaria o transitoria) | Slide2 Groundwater; ver 09 |
| Succión (no saturado) | $\tau = c' + (\sigma_n - u_a)\tan\phi' + (u_a - u_w)\tan\phi^b$ | Fredlund; por defecto se ignora ($u \leftarrow \max(0,u)$) |
| Exceso por carga ($B$-bar) | $\Delta u = \bar B\,\Delta\sigma_v$ | terraplenes rápidos |
| Desembalse rápido | Corps 2 etapas, Lowe-Karafiath, Duncan-Wright-Wong 3 etapas | xslope implementa DWW |

Agua en grieta de tracción: empuje horizontal $T = \tfrac12\gamma_w z_w^2$ a $z_w/3$ del fondo, en
la dovela extrema.

## 4. Modelos de resistencia (catálogo de Slide2)

| Modelo | Ecuación clave |
|---|---|
| Mohr-Coulomb | $\tau = c' + \sigma_n'\tan\phi'$ |
| No drenado | $S_u$ constante; $S_u = c + c_p\max(0, y_{ref} - y)$ (crece con profundidad/elevación) |
| Relación de tensión vertical / SHANSEP | $S_u = k\,\sigma_v'$; $S_u = \sigma_v' S\,(OCR)^m$ |
| Sin resistencia / resistencia infinita | agua/relleno blando / roca impenetrable |
| Anisotrópico lineal y general | $c, \phi$ función del ángulo de la base respecto de una dirección |
| Curva potencial | $\tau = a(\sigma_n' + d)^b + c$ |
| Hoek-Brown generalizado | $\sigma_1' = \sigma_3' + \sigma_{ci}\left(m_b\frac{\sigma_3'}{\sigma_{ci}} + s\right)^a$, con $m_b = m_i e^{(GSI-100)/(28-14D)}$, $s = e^{(GSI-100)/(9-3D)}$, $a = \tfrac12 + \tfrac16(e^{-GSI/15} - e^{-20/3})$ (Hoek et al. 2002) |
| Barton-Bandis | $\tau = \sigma_n\tan\left[\phi_r + JRC\log_{10}(JCS/\sigma_n)\right]$ |
| Función corte/normal | tabla $\tau(\sigma_n)$ del usuario |
| Hiperbólico, drenado-no drenado, corte de tracción | variantes |

Envolventes no lineales en LEM: linealizar en la tensión normal actual de cada base (tangente
instantánea $\tan\phi_i = d\tau/d\sigma_n$, $c_i = \tau - \sigma_n\tan\phi_i$), resolver, actualizar
$\sigma_n = N'/l$ y repetir hasta que F no cambie. Hoek-Brown → envolvente de Mohr por la
transformación de Balmer (1952):
$\sigma_n' = \sigma_3' + \dfrac{\sigma_1'-\sigma_3'}{\partial\sigma_1'/\partial\sigma_3' + 1}$,
$\tau = (\sigma_n'-\sigma_3')\sqrt{\partial\sigma_1'/\partial\sigma_3'}$.

## 5. Cargas

- Distribuidas (normales a la superficie o verticales), lineales/puntuales, agua libre (presión
  hidrostática normal a la superficie).
- Sísmica pseudoestática: $k_hW$ horizontal en el centroide hacia la dirección de deslizamiento;
  $k_vW$ vertical (la convención de signo debe fijarse y documentarse; OGR usa $W(1+k_v)$ con $k_v$
  positivo hacia abajo. **Pendiente**: confirmar la convención exacta de Slide2). Aceleración crítica
  $k_c$ (F = 1) y desplazamiento de Newmark como post-proceso (VP#104).

## 6. Refuerzos y soportes (catálogo de Slide2)

Tipos: End Anchored, GeoTextile, Grouted Tieback, Grouted Tieback with Friction, Soil Nail,
Micro Pile, Pile (Ito-Matsui), Helical Anchor, User Defined. Cada uno define un **diagrama de
fuerza** a lo largo de su longitud (capacidad a tracción, arrancamiento según longitud de
anclaje detrás de la superficie, placa, adherencia) y la fuerza en el punto de corte con la
superficie de falla.

Aplicación de la fuerza $T$ (Slide2, "Active/Passive Force Application"):

$$\text{Activa (anclajes tensados):}\quad F = \frac{\text{Resistencia}}{\text{Motor} - T_{\parallel}}\qquad
\text{Pasiva (clavos, geotextiles):}\quad F = \frac{\text{Resistencia} + T_{\parallel}}{\text{Motor}}$$

La pasiva siempre da F menor (la fuerza queda dividida por F). Orientación: paralela al refuerzo,
paralela a la base (tangente), bisectriz, o definida. Retro-análisis: fuerza de soporte necesaria
para un F objetivo (VP#37).

Fuentes: USACE EM 1110-2-1902 (2003); Hoek, Carranza-Torres & Corkum (2002); Balmer (1952);
Fredlund & Rahardjo (1993); Duncan, Wright & Wong (1990); ayuda Slide2 (Groundwater, Materials,
Support, Active/Passive); xslope `docs/lem/overview.md`, `reinforcement.md`, `rapid.md`.
