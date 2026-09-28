# Fuentes: a cuáles se pudo ingresar y a cuáles no

> Nodo: `fuentes` · Actualizado: 2026-09-28.
>
> **Condición de esta sesión**: la red del entorno solo permitía GitHub, GitLab y PyPI. Los PDF
> públicos de Rocscience, Seequent, GEO5, USACE, universidades, etc. **no se pudieron descargar**
> (la política de red los bloqueó) aunque son de acceso libre; de ellos solo se leyeron los
> resúmenes del buscador. Para compensar se leyeron íntegros los **clones abiertos** de Slide2
> (código y documentación), que citan y transcriben esas fuentes, y se verificó numéricamente
> lo esencial con un solver propio.
>
> No se usaron repositorios piratas (Sci-Hub, LibGen) ni copias no autorizadas (Scribd,
> Studocu, Academia) como autoridad.

## A. Leídas en texto completo y usadas (verificadas en esta sesión)

| Fuente | Acceso | Qué se obtuvo |
|---|---|---|
| **xslope** — N. L. Jones, [github.com/njones61/xslope](https://github.com/njones61/xslope) (Apache-2.0) + paquete PyPI 0.5.2 | código y docs completos; **ejecutado** | teoría de Janbu (+f0), Spencer (derivación UTEXAS con derivadas de Newton), M-P/GLE, búsqueda, cargas, agua, refuerzos; reconstrucción problema por problema del **manual de verificación de Slide2 (111 VP)**, del de SLOPE/W (47) y RS2; bibliografía con DOI; lector de archivos .sli/.slim/.slmd de Slide2 |
| **OGR-Slip2D** — S. Sáez López (UPCT), [github.com/samuelsl27/OGR-Slip2D](https://github.com/samuelsl27/OGR-Slip2D) (AGPL-3.0) | código, docs y auditorías | reimplementación de los buscadores de Slide2 (Grid, Slope, Auto Refine, Block, Path, SA de Su 2009, PSO, Optimize) con reglas **medidas** contra salidas de Slide2 (regla de radios); GLE compartida Spencer/M-P; trampas numéricas documentadas; valores por defecto; servidor MCP para agentes |
| **lythosle** — [github.com/hdaltuntas/lythosle](https://github.com/hdaltuntas/lythosle) (AGPL-3.0) | README | alcance de 8 métodos y validaciones |
| **pybimstab** — Montoya-Araque & Suárez-Burgoa (PyPI, BSD-2) | código | GLE para suelos bloque-matriz |
| SpencerLEM (GitHub, proyecto académico IIT-BHU) | clonado | no revisado en detalle |
| Documento previo del usuario (MD) | completo | punto de partida; se corrigió y amplió |

## B. Localizadas, de acceso PÚBLICO/LIBRE, pero bloqueadas por la red de este entorno

Se leyó el resumen del buscador y, cuando existe, la transcripción en xslope/OGR. Habilitando
estos dominios en la configuración de red del entorno, la siguiente fase puede leerlas directo.

| Fuente | Dónde | Lo que falta extraer |
|---|---|---|
| Morgenstern & Price (1965), *Géotechnique* 15(1):79-93 | ERA U. Alberta (PDF abierto) | ecuaciones diferenciales exactas, integración cerrada por dovela (constantes), ejemplos |
| Fredlund & Krahn (1977), *CGJ* 14(3):429-439 | scispace.com (PDF) | tablas completas (incl. Janbu simplificado y riguroso del caso de ejemplo), signos de la formulación GLE |
| Zhu, Lee, Qian & Chen (2005), *CGJ* 42(1):272-278 | HKU Scholars Hub (PDF) | ecuación exacta de λ y términos de carga externa; ejemplos |
| USACE EM 1110-2-1902 (2003) *Slope Stability* | publications.usace.army.mil | App. C (fuerzas) y App. G (ejemplo Modified Swedish con tablas por dovela) |
| UTEXAS2 User's Guide, App. A (S. G. Wright) | DTIC ADA207044 | derivación de Spencer (leída vía la transcripción de xslope) |
| *Stability Modeling with SLOPE/W* (Seequent, 2022) | files.seequent.com | GLE, funciones f(x) (seno recortado, trapecio, Fredlund-Wilson-Fan), Janbu generalizado, convergencia |
| *SLOPE/W Verification Manual* (Seequent) | files.seequent.com | 47 problemas (leídos vía xslope) |
| *Slide2 Slope Stability Verification Manual* | static.rocscience.cloud | 111 problemas (leídos vía xslope `docs/verification/rocscience.md`) |
| *Slide2 Groundwater Verification Manual* (2022) | static.rocscience.cloud | 21 problemas de filtración (vía xslope) |
| Slide "Search Methods" (PDF) | static.rocscience.cloud | detalles de Grid/Slope/Auto Refine y no circulares (resumen vía OGR) |
| "Locating General Failure Surfaces… via Cuckoo Search" | rocscience.com | parámetros y algoritmo usados en Slide2 |
| Su (2009) HSA, U. Waterloo | rocscience.com (PDF) | ecuaciones completas de VFSA + LMC (transcritas en OGR) |
| Ayuda en línea de Slide2 (métodos, función entre dovelas, búsquedas, soportes activo/pasivo, probabilístico) | rocscience.com/help/slide2 | textos completos; valores por defecto exactos |
| Ayuda en línea de GEO5 (Janbu, Spencer, M-P, optimización poligonal, ITFM, Shahunyants) | finesoftware.eu/help/geo5 | **ecuaciones (están como imágenes)**, criterio de convergencia |
| Hoek, Carranza-Torres & Corkum (2002), Hoek-Brown ed. 2002 | rocscience.com (PDF) | fórmulas ya conocidas; cotejo |
| TRB SR 176 cap. 7; notas "Theory of Slope Stability" (Portland State); GEO Report 208 (CEDD Hong Kong); FHWA NHI-10-025; Geoengineer.org (Janbu, Spencer) | sitios públicos | presentaciones didácticas y ejemplos |
| Yang & Deb (2009) "Cuckoo search via Lévy flights" | arXiv:1003.1594 | algoritmo base |

## C. De pago o sin copia legal gratuita localizada

| Fuente | Estado | Lo que falta para la base |
|---|---|---|
| Spencer (1967) *Géotechnique* 17(1):11-26 y Spencer (1973) línea de empujes | solo resumen (ICE/Emerald) | ecuaciones y ejemplo originales, contraste de signos |
| Morgenstern & Price (1967) *Computer Journal* 9(4):388-393 | solo resumen (Oxford) | Newton-Raphson original y detalles numéricos |
| Janbu (1954, 1957) y Janbu (1973) en *Embankment-Dam Engineering* (Wiley) | solo registro; copias en Scribd no usadas | **carta de f0 y b1 (0.69 vs 0.67)**, dominio de d/L, GPS completo |
| Chen & Morgenstern (1983) *CGJ* 20(1):104-119 | de pago | condiciones de extremo y restricciones sobre f(x) |
| Fredlund, Krahn & Pufahl (1981) ICSMFE Estocolmo | actas | relación formal entre métodos |
| Sarma (1973, 1979) *Géotechnique* | de pago | ecuaciones completas de Sarma |
| Lowe & Karafiath (1960); Whitman & Bailey (1967) | de pago | hipótesis y criterio $m_\alpha$ original |
| Greco (1996) *J. Geotech. Eng.* 122(7) | de pago (ASCE) | caminata aleatoria original (Optimize Surfaces) |
| Cheng et al. (2007) *Computers and Geotechnics*; Cheng (2007) *Eng. Optimization* | de pago | comparativa de 6 heurísticas; límites dinámicos |
| Duncan, Wright & Brandon (2014) *Soil Strength and Slope Stability* | libro de pago | ejercicios de verificación didácticos |
| Abramson et al. (2002) *Slope Stability and Stabilization Methods* | libro de pago | cap. 5 (métodos), §5.5 Janbu |
| Cheng & Lau, *Slope Stability Analysis and Stabilization* | libro de pago | métodos y búsqueda (autor de SLOPE 2000) |
| Donald & Giam (1989) ACADS U255 | informe no digital | enunciados originales (reconstruidos en xslope) |
| Manual teórico interno de Slide2 (ecuaciones exactas de implementación) | no publicado | tolerancias internas, casos degenerados |
| Formulación interna de GEO5 | no publicada (imágenes en ayuda) | recurrencias exactas y convergencia |

## D. Cómo conseguir legalmente lo que falta

1. **Habilitar dominios** en la red del entorno para la fase siguiente: `era.library.ualberta.ca`,
   `scispace.com`, `hub.hku.hk`, `www.publications.usace.army.mil`, `apps.dtic.mil`,
   `files.seequent.com`, `static.rocscience.cloud`, `www.rocscience.com`, `www.finesoftware.eu`,
   `onlinepubs.trb.org`, `arxiv.org`, `www.cedd.gov.hk`, `www.fhwa.dot.gov`.
2. Pago por artículo o acceso institucional: ICE Virtual Library (Spencer, Sarma), Canadian
   Science Publishing (Chen-Morgenstern), ASCE Library (Greco), Oxford (M-P 1967).
3. Pedir copia al autor (ResearchGate) o préstamo interbibliotecario (Janbu 1973, ACADS).
4. Preguntar a Rocscience/Fine por sus manuales teóricos (Rocscience publica "Verification &
   Theory"; algunos teóricos se entregan con licencia).

## Bibliografía completa con DOI

La lista alfabética de ~90 referencias con DOI (manuales de verificación, artículos de
benchmarks, anclas analíticas) está en xslope `docs/verification/references.md` (Apache-2.0).
Referencias núcleo de esta base:

- Fredlund, D.G. & Krahn, J. (1977). *CGJ* 14(3):429-439. doi:10.1139/t77-045
- Morgenstern, N.R. & Price, V.E. (1965). *Géotechnique* 15(1):79-93. doi:10.1680/geot.1965.15.1.79
- Spencer, E. (1967). *Géotechnique* 17(1):11-26. doi:10.1680/geot.1967.17.1.11
- Chen, Z.Y. & Morgenstern, N.R. (1983). *CGJ* 20(1):104-119. doi:10.1139/t83-010
- Zhu, D.Y., Lee, C.F., Qian, Q.H. & Chen, G.R. (2005). *CGJ* 42(1):272-278.
- Janbu, N. (1973). Slope stability computations. En Hirschfeld & Poulos (eds.), *Embankment-Dam Engineering*, Wiley, 47-86.
- Greco, V.R. (1996). *J. Geotech. Eng.* 122(7):517-525. doi:10.1061/(ASCE)0733-9410(1996)122:7(517)
- Arai, K. & Tagyo, K. (1985). *Soils and Foundations* 25(1):43-51. doi:10.3208/sandf1972.25.43
- Griffiths, D.V. & Lane, P.A. (1999). *Géotechnique* 49(3):387-403. doi:10.1680/geot.1999.49.3.387
- USACE (2003). EM 1110-2-1902 *Slope Stability*.
