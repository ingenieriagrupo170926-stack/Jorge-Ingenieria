# Base académica de estabilidad de taludes: Janbu, Spencer y Morgenstern–Price

## Objetivo y alcance

Los métodos de Janbu, Spencer y Morgenstern–Price no “encuentran” por sí solos la superficie crítica: calculan el factor de seguridad de una superficie candidata. Un algoritmo geométrico externo genera o modifica círculos y poligonales, vuelve a calcular el factor de seguridad y busca su mínimo. Slide2 y GEO5 separan expresamente el método de equilibrio del tipo y algoritmo de búsqueda de superficies.[^1][^2]

El problema completo es:

\[
F(\Gamma)=\text{factor de seguridad de la superficie candidata }\Gamma
\]

\[
\Gamma_{cr}=\underset{\Gamma\in\mathcal A}{\operatorname{argmin}}\;F(\Gamma)
\tag{1}
\]

Aquí, \(\mathcal A\) es el conjunto de superficies admisibles. Este documento es una base para delegar después la derivación y programación profunda; no pretende reproducir algoritmos propietarios no publicados.

> El apellido correcto es **Janbu**, no “Jambu”. Asimismo, Janbu simplificado, Janbu corregido y Janbu riguroso/generalizado son formulaciones diferentes.

## Base física necesaria

### Equilibrio límite

La masa potencialmente deslizante se idealiza en 2D, en deformación plana, y se divide en dovelas. Se supone una superficie de falla, una ley de resistencia basal y un factor de seguridad uniforme; el método no calcula directamente deformaciones ni garantiza compatibilidad cinemática.[^3]

Debe dominarse:

- Estática: \(\sum F_x=0\), \(\sum F_y=0\), \(\sum M=0\).
- Esfuerzos totales y efectivos.
- Presión de poros, filtración y fuerzas de agua externas.
- Resistencia pico, totalmente ablandada y residual.
- Carga drenada, no drenada y pseudoestática.
- Anisotropía, estratos débiles, grietas de tracción y sobrecargas.

USACE advierte que el ablandamiento y la falla progresiva pueden invalidar la hipótesis de movilización simultánea de resistencia pico; en arcillas rígidas, lutitas y superficies reactivadas puede requerirse resistencia totalmente ablandada o residual.[^3]

### Resistencia basal

Para esfuerzos efectivos:

\[
\tau_f=c'+\sigma_n'\tan\phi',\qquad \sigma_n'=\sigma_n-u
\tag{2}
\]

Para la dovela \(i\):

\[
S_i=\frac{c_i'l_i+(N_i-U_i)\tan\phi_i'}{F}
\tag{3}
\]

con \(l_i=b_i\sec\alpha_i\) y \(U_i=u_il_i\). Si se trabaja con la normal efectiva \(N_i'\):

\[
S_i=\frac{c_i'l_i+N_i'\tan\phi_i'}{F}
\tag{4}
\]

No deben mezclarse ambas convenciones. Zhu et al. formulan explícitamente el problema con normal efectiva, agua, sismo y cargas externas.[^4]

En un análisis no drenado en tensiones totales deben usarse parámetros totales coherentes y asignarse \(u=0\) dentro del cálculo; de lo contrario se descontaría dos veces el efecto de la presión de poros.[^3]

## Base matemática necesaria

- Geometría analítica y trigonometría: círculos, poligonales, intersecciones y brazos de momento.
- Integración y geometría computacional: áreas parciales por estrato y pesos.
- Álgebra lineal y recurrencias: transmisión de fuerzas entre dovelas.
- Ecuaciones no lineales: \(F\), \(\theta\) y \(\lambda\).
- Métodos numéricos: punto fijo, bisección, secante y Newton–Raphson.
- Optimización: malla, refinamiento local y metaheurísticas.
- Control numérico: tolerancias, singularidades, normales negativas y sensibilidad al número de dovelas.

Para una superficie circular inferior:

\[
y_b(x)=y_c-\sqrt{R^2-(x-x_c)^2}
\tag{5}
\]

Para una superficie no circular se utilizan vértices \((x_j,y_j)\) unidos por segmentos. Cada dovela debe cortarse además en cambios de material, nivel freático, cargas y quiebres geométricos. Su peso es:

\[
W_i=\sum_k\gamma_kA_{ik}
\tag{6}
\]

## Fuerzas por dovela

| Símbolo | Definición |
|---|---|
| \(b_i,l_i,\alpha_i\) | Ancho, longitud e inclinación de la base |
| \(W_i\) | Peso total de la dovela |
| \(N_i,N_i'\) | Fuerza normal basal total o efectiva |
| \(S_i\) | Corte basal movilizado |
| \(E_{i-1},E_i\) | Normales entre dovelas |
| \(X_{i-1},X_i\) | Cortantes entre dovelas |
| \(U_i\) | Resultante de presión de poros basal |
| \(Q_i\) | Carga externa equivalente |
| \(k_hW_i\) | Fuerza pseudoestática horizontal |

Existen más incógnitas que ecuaciones de estática; cada método se distingue por la hipótesis usada para relacionar \(E\), \(X\) o la línea de empujes.[^3]

## Janbu simplificado

Janbu simplificado satisface el equilibrio global de fuerzas, pero no el equilibrio completo de momentos. En el cálculo básico se omite el cortante entre dovelas.[^5][^3]

Sin cargas externas ni sismo, una forma usual es:

\[
F_J=\frac{\displaystyle\sum_{i=1}^{n}
\frac{c_i'b_i+(W_i-u_ib_i)\tan\phi_i'}
{\cos\alpha_i+\dfrac{\sin\alpha_i\tan\phi_i'}{F_J}}}
{\displaystyle\sum_{i=1}^{n}W_i\tan\alpha_i}
\tag{7}
\]

Es implícita en \(F_J\). Se asume \(F_J^{(0)}\), se evalúa el lado derecho y se itera hasta cumplir \(|F_J^{(k+1)}-F_J^{(k)}|<\varepsilon_F\). En presencia de sismo, agua externa, sobrecargas o refuerzo, las componentes deben derivarse con un único convenio de signos, no agregarse empíricamente.

## Janbu corregido

La versión corregida multiplica el valor simplificado por un factor empírico:

\[
F_{JC}=f_0F_J
\tag{8}
\]

Una aproximación difundida a la carta de Janbu es:

\[
f_0=1+b_1\left[\frac dL-1.4\left(\frac dL\right)^2\right]
\tag{9}
\]

Aquí, \(d\) es la máxima distancia entre superficie y cuerda y \(L\) la longitud de la cuerda. Una implementación abierta usa \(b_1=0.67\) para suelo cohesivo, 0.50 para suelo \(c-\phi\) y 0.31 para suelo friccional.[^6]

Existe una discrepancia secundaria de 0.67 frente a 0.69 para suelo cohesivo; antes de buscar coincidencia al tercer decimal debe consultarse la edición exacta de Janbu y la convención del software.[^7][^6]

| Variante | Equilibrio/hipótesis | Observación |
|---|---|---|
| Janbu simplificado | Equilibrio de fuerzas; cortante inter-dovela omitido | Produce \(F_J\) |
| Janbu corregido | \(F_J\) multiplicado por \(f_0\) | Sigue siendo una corrección empírica |
| Janbu riguroso | Fuerzas inter-dovela y línea de empujes | No equivale a \(f_0F_J\) |

Slide2 lista Janbu Simplified y Janbu Corrected por separado. GEO5 denomina su opción “Janbu”, pero describe fuerzas no nulas entre bloques e iteración de sus inclinaciones, más próxima a una formulación generalizada que a la sola corrección \(f_0\).[^8][^9]

## Método de Spencer

Spencer supone resultantes inter-dovela paralelas:

\[
\frac{X_i}{E_i}=\tan\theta
\tag{10}
\]

El ángulo \(\theta\) y \(F\) se determinan simultáneamente para satisfacer equilibrio global de fuerzas y momentos. La publicación original declara dos ecuaciones de equilibrio, una de fuerzas y otra de momentos.[^10]

Para cada \(\theta\) se obtienen dos soluciones: \(F_F(\theta)\), por fuerzas, y \(F_M(\theta)\), por momentos. La solución rigurosa satisface:

\[
F_F(\theta^*)=F_M(\theta^*)=F^*
\tag{11}
\]

Fredlund y Krahn expresan el equilibrio de fuerzas, para el caso general con cargas, como:

\[
F_F=
\frac{\sum_i\left[c_i'l_i\cos\alpha_i+(N_i-U_i)\tan\phi_i'\cos\alpha_i\right]}
{\sum_iN_i\sin\alpha_i+\sum_i k_hW_i+A-L\cos\omega}
\tag{12}
\]

El equilibrio de momentos puede escribirse:

\[
F_M=
\frac{\sum_i c_i'l_iR_i+
\sum_i(N_i-U_i)R_i\tan\phi_i'}
{\sum_iW_ix_i-\sum_iN_if_i+\sum_i k_hW_ie_i+Aa+Ld}
\tag{13}
\]

Los símbolos geométricos son brazos respecto al centro real o ficticio elegido. En Spencer debe resolverse la raíz \(g(\theta)=F_F-F_M=0\), preferiblemente con bisección o secante acotada. La comparación unificada de Fredlund y Krahn proporciona las ecuaciones, supuestos y ejemplos numéricos completos.[^3]

Spencer equivale a Morgenstern–Price con función inter-dovela constante. Slide2 lo confirma: en GLE, usar \(f(x)=1\) equivale a Spencer.[^11]

## Morgenstern–Price

### Hipótesis central

Morgenstern–Price permite que la razón entre cortante y normal inter-dovela varíe:

\[
X(x)=\lambda f(x)E(x)
\tag{14}
\]

\(f(x)\) se especifica y \(\lambda\) escala su magnitud. Se buscan simultáneamente \(F\) y \(\lambda\), satisfaciendo todas las ecuaciones de equilibrio y las condiciones de frontera. El artículo original desarrolla la formulación para superficies arbitrarias y establece fuerzas laterales nulas en los extremos.[^12]

Las formas habituales de \(f(x)\) son constante, media senoide, seno recortado, trapezoidal o definida por el usuario. En Slide2 la media senoide es la opción GLE predeterminada y la constante reproduce Spencer.[^11]

### Formulación computacional legible

Zhu et al. presentan un algoritmo abierto y directamente programable. Definen:

\[
R_i=\left[W_i\cos\alpha_i-k_hW_i\sin\alpha_i-Q_i\cos(\omega_i-\alpha_i)-U_i\right]	an\phi_i'
+c_i'b_i\sec\alpha_i
\tag{15}
\]

\[
T_i=W_i\sin\alpha_i+k_hW_i\cos\alpha_i-Q_i\sin(\omega_i-\alpha_i)
\tag{16}
\]

La recurrencia de empujes es:

\[
E_i\Phi_i=E_{i-1}\Phi_{i-1}\psi_{i-1}+F_sT_i-R_i
\tag{17}
\]

con

\[
\Phi_i=(\sin\alpha_i-\lambda f_i\cos\alpha_i)\tan\phi_i'
+F_s(\cos\alpha_i+\lambda f_i\sin\alpha_i)
\tag{18}
\]

Las condiciones de frontera son \(E_0=E_n=0\). De ellas se obtiene una ecuación implícita para \(F_s\); el equilibrio de momentos proporciona una expresión explícita para \(\lambda\). Zhu et al. recomiendan iniciar con \(F_s=1\), \(\lambda=0\), actualizar \(F_s\), calcular los \(E_i\), actualizar \(\lambda\) y repetir hasta cumplir ambas tolerancias.[^4]

También exigen transmisión físicamente válida:

\[
\Phi_i>0
\tag{19}
\]

El artículo reporta convergencia en menos de diez iteraciones con tolerancia de 0.0001 para sus ejemplos, pero ello es una verificación de esos casos, no garantía universal.[^4]

## Búsqueda de superficie crítica

### Superficies circulares

Slide2 ofrece Grid Search, Slope Search y Auto Refine para círculos. En Grid Search cada centro genera una serie de radios y se conserva el menor \(F\); una malla de 20 por 20 intervalos produce 441 centros.[^13][^14][^15]

Flujo mínimo reproducible:

1. Definir centros \((x_c,y_c)\) y radios admisibles.
2. Intersectar cada círculo con el terreno.
3. Descartar superficies por profundidad, área y límites.
4. Discretizar y resolver \(F\).
5. Refinar alrededor de los mejores centros y radios.
6. Repetir hasta que geometría y \(F\) se estabilicen.

### Superficies no circulares

Slide2 ofrece Block, Path, Simulated Annealing, Particle Swarm, Auto Refine y Cuckoo Search; recomienda después optimización local de superficies.[^16][^17]

GEO5 mueve sucesivamente los vértices internos en horizontal y vertical, desplaza los extremos sobre el terreno, inicia el paso con un décimo de la menor separación entre nodos y lo reduce a la mitad en cada ciclo. Su propia documentación advierte que esta búsqueda puede quedar atrapada en un mínimo local y recomienda varios arranques, incluso partir del círculo crítico.[^18]

Así, un resultado serio debe usar múltiples semillas, restricciones geológicas, refinamiento local y comparación circular/no circular. Un único inicio no demuestra mínimo global.

## GEO5 y Slide2

| Tema | GEO5 | Slide2 |
|---|---|---|
| Superficies | Circulares y poligonales | Circulares, no circulares y definidas por usuario |
| Métodos relevantes | Janbu, Spencer, Morgenstern–Price | Janbu Simplified/Corrected, Spencer, GLE/M–P |
| Circular | Malla u optimización | Grid, Slope, Auto Refine |
| No circular | Movimiento iterativo de vértices | Seis buscadores y optimización local |
| Riesgo reconocido | Mínimo local | Dependencia del buscador y filtros |
| Verificación pública | Ayuda teórica cualitativa | Manual extenso con benchmarks |

GEO5 indica que Spencer, Janbu y Morgenstern–Price funcionan tanto en superficies circulares como poligonales. Slide2 publica un manual amplio de verificación con resultados de Janbu, Spencer y GLE/M–P frente a fuentes como Arai–Tagyo, Fredlund–Krahn y Zhu.[^2][^19][^20]

## Plan para cálculo profundo

1. Fijar un convenio único de signos y dibujar la dovela.
2. Implementar geometría y pesos con pruebas unitarias.
3. Implementar Janbu simplificado y luego \(f_0\).
4. Implementar Spencer como intersección \(F_F(\theta)=F_M(\theta)\).
5. Implementar Morgenstern–Price con Zhu et al. y funciones constante/media senoide.
6. Validar primero una superficie fija; no activar todavía la búsqueda.
7. Reproducir casos de Fredlund–Krahn y Zhu.
8. Comparar contra el manual de verificación de Slide2.[^20][^4][^3]
9. Añadir búsqueda circular exhaustiva y refinada.
10. Añadir búsqueda poligonal multiarranque y restricciones.
11. Ejecutar sensibilidad a dovelas, tolerancia, \(f(x)\), presión de poros y semillas.
12. Documentar balance residual de \(F_x\), \(F_y\), momentos y condiciones de frontera.

## Fuentes accesibles

| Fuente | Estado | Contenido legible |
|---|---|---|
| Morgenstern & Price (1965), *The Analysis of the Stability of General Slip Surfaces* | Acceso completo localizado | Ecuaciones diferenciales, \(X=\lambda f(x)E\), fronteras y ejemplos.[^12] |
| Fredlund & Krahn (1977) | Acceso completo localizado | Comparación unificada, ecuaciones de Janbu, Spencer y M–P, tablas benchmark.[^3] |
| Zhu et al. (2005) | Acceso completo institucional | Algoritmo programable, ecuaciones [^21]–[^22], iteración y ejemplos.[^4] |
| USACE EM 1110-2-1902 | Acceso público oficial | Hipótesis, limitaciones, selección de resistencia y procedimiento de análisis.[^3] |
| Documentación GEO5 | Acceso público | Métodos disponibles, naturaleza del Janbu implementado y optimización poligonal.[^18][^2][^9][^23] |
| Documentación Slide2 | Acceso público | Tipos de superficie, búsquedas, funciones inter-dovela y filtros.[^13][^16][^11] |
| Manual de verificación Slide2 | PDF público | Benchmarks y factores de seguridad de Janbu, Spencer y GLE/M–P.[^20] |
| Spencer (1967), artículo original | Resumen editorial accesible; texto íntegro no recuperado de forma fiable | Alcance original y planteamiento fuerza–momento.[^10] |

## Fuentes no accesibles o incompletas

| Fuente | Limitación encontrada | Información pendiente |
|---|---|---|
| Morgenstern & Price (1967), *A Numerical Method...* | Página de Oxford indica falta de acceso al artículo completo.[^12] | Implementación Newton–Raphson original y detalles numéricos completos. |
| Janbu (1973), *Slope Stability Computations* | Registro y vistas secundarias localizadas; no se obtuvo una copia primaria autorizada completa.[^24][^25] | Derivación original, carta \(f_0\), definición exacta de \(d/L\) y coeficientes. |
| Spencer (1967), texto íntegro | Editorial muestra resumen; algunas copias comunitarias no ofrecieron transcripción íntegra verificable.[^10] | Ecuaciones originales, numeración y ejemplos del autor. |
| Duncan, Wright & Brandon (2014), *Soil Strength and Slope Stability* | Página editorial y capítulo de muestra, libro completo de pago.[^26] | Presentación didáctica completa y ejercicios de verificación. |
| Abramson et al. (2001), *Slope Stability and Stabilization Methods* | Catálogo/editorial y vistas no oficiales; libro completo no obtenido legalmente.[^27][^28] | Capítulo integral de equilibrio límite y tablas comparativas. |
| Manual teórico interno completo de Slide2 | La web afirma que existen manuales teóricos, pero el material recuperado se concentró en ayuda y verificación.[^29] | Ecuaciones exactas de implementación, tolerancias y tratamiento de casos degenerados. |
| Formulación matemática completa de GEO5 | Ayuda accesible cualitativa, pero varias páginas renderizan ecuaciones como imágenes no extraíbles.[^19][^23] | Recurrencias exactas y criterio interno de convergencia. |

No se emplearon ni se recomiendan repositorios piratas. Se priorizaron PDFs públicos, repositorios institucionales, documentación oficial y vistas autorizadas; Scribd y foros solo sirvieron para localizar referencias, no como autoridad matemática.

## Vacíos de investigación

- Verificar en fuente primaria los coeficientes exactos de \(f_0\) de Janbu y su dominio geométrico.
- Recuperar legalmente Spencer (1967) completo y contrastar signos con Fredlund–Krahn.
- Establecer si GEO5 usa Janbu generalizado, una variante propietaria o una combinación con corrección.
- Documentar las tolerancias, límites de \(\lambda\) y manejo de normales negativas en GEO5 y Slide2.
- Reproducir al menos tres benchmarks: seco circular, estrato débil no circular y nivel freático.
- Comparar no solo \(F\), sino también \(\lambda\), \(\theta\), línea de empujes, residuales de equilibrio y geometría crítica.

## Entregable sugerido para la siguiente fase

La siguiente investigación debería producir un cuaderno de cálculo o código con cuatro módulos: geometría, solucionadores LEM, buscador de superficies y verificación. El criterio de éxito debe ser reproducir superficies fijas de Fredlund–Krahn y Zhu antes de comparar mínimos globales con GEO5 o Slide2; solo después conviene añadir cargas sísmicas, refuerzo, anisotropía y resistencia no lineal.

---

## References

1. [Slip Surfaces - Slide2 Documentation](https://www.rocscience.com/help/slide2/documentation/slide-model/slip-surfaces) - In most cases, a Slide2 analysis will involve a critical surface search, in order to attempt to find...

2. [Analysis | Program Slope Stability | Online Help | GEO5](https://www.finesoftware.eu/help/geo5/en/analysis-05/) - In the combo list the analysis type is selected: Standard; Optimization (for circular or polygonal s...

3. [scispace.com › pdf › comparison-of-slope-stability-methods-of-analysis-2jipg28fncComparison of slope stability methods of analysis1](https://scispace.com/pdf/comparison-of-slope-stability-methods-of-analysis-2jipg28fnc.pdf) - The two methods of solution were compared using the University of Alberta computer program (Krahn et...

4. [[PDF] A concise algorithm for computing the factor of safety using the ...](https://hub.hku.hk/bitstream/10722/42061/1/102322.pdf) - Abstract: A concise algorithm is proposed in this paper for the calculation of the factor of safety ...

5. [[PDF] METHODS OF STABILITY ANALYSIS](https://onlinepubs.trb.org/onlinepubs/sr/sr176/176-007.pdf) - If 0 is set equal to zero and substituted into. Equation 7.30, the equation governing Bishop's simpl...

6. [Janbu Method - XSLOPE](https://xslope.org/en/stable/lem/janbu/) - Free, open-source slope stability and seepage analysis software: seven limit equilibrium methods, fi...

7. [Janbu Slope Stability - My Thoughts](https://blog.ervivekshah.com.np/p/janbu-method-slope-stability.html) - m_a = cos(a) * [ 1 + tan(a)*tan(phi') / FS ] f0 = 1 + A * (d/L - 1.4*(d/L)^2) -- Berger & Fellenius ...

8. [Technical Specifications - Slide2 Overview](https://www.rocscience.com/help/slide2/overview/technical-specifications) - Janbu Corrected; Janbu Simplified; Lowe-Karafiath; Ordinary/Fellenius; Sarma ... Calculate excess po...

9. [Janbu | Circular Slip Surface | Online Help | GEO5](https://www.finesoftware.eu/help/geo5/en/janbu-02/) - Janbu method assumes non-zero forces between blocks. Method satisfies the force equations of equilib...

10. [www.emerald.com › 17/1/11 › 392344A Method of analysis of the Stability of Embankments Assuming...](https://www.emerald.com/jgeot/article/17/1/11/392344/A-Method-of-analysis-of-the-Stability-of) - A method of analysis is described for determining the factor of safety of an embankment against fail...

11. [Interslice Force Function - Slide2 Documentation](https://www.rocscience.com/help/slide2/documentation/slide-model/project-settings/methods/interslice-force-function) - Interslice Force Functions are specified as a function of normalized X-coordinates, ranging between ...

12. [academic.oup.com › comjnl › article-abstractA Numerical Method for Solving the Equations of Stability of...](https://academic.oup.com/comjnl/article-abstract/9/4/388/390321) - A practical method of solving the equations of statical equilibrium to obtain the factor of safety o...

13. [Grid Search - Slide2 Documentation](https://www.rocscience.com/help/slide2/documentation/slide-model/slip-surfaces/circular-surfaces/grid-search) - Grid Search. A Grid Search is one of the Search Methods available in Slide2 for locating the Global ...

14. [Overview of Circular Surfaces - Slide2 Documentation](https://www.rocscience.com/help/slide2/documentation/slide-model/slip-surfaces/circular-surfaces/overview-of-circular-surfaces) - There are THREE different Search Methods available in Slide2 for locating critical CIRCULAR slip sur...

15. [Auto Grid - Slide2 Documentation](https://www.rocscience.com/help/slide2/documentation/slide-model/slip-surfaces/circular-surfaces/auto-grid) - Auto Grid. A slip center grid is used to generate the slip circles used in the critical surface sear...

16. [Non-Circular Surfaces - Slide2 Documentation](https://www.rocscience.com/help/slide2/documentation/slide-model/slip-surfaces/non-circular-surfaces) - A critical surface search to attempt to find the slip surface with the overall minimum safety factor...

17. [Slide2 Documentation | Optimize Surfaces](https://www.rocscience.com/help/slide2/documentation/slide-model/slip-surfaces/non-circular-surfaces/optimize-surfaces) - The Surface Altering Optimization (SA) option is a local search method which uses the results of the...

18. [Optimization of Polygonal Slip Surface](https://www.finesoftware.eu/help/geo5/en/optimization-of-polygonal-slip-surface-01/) - The endpoints of the optimized slip surface are moved on the ground surface, internal points are mov...

19. [Program Slope Stability | Online Help | GEO5](https://www.finesoftware.eu/help/geo5/en/slopestability/) - This program is used to perform slope stability analysis (embankments, earth cuts, anchored retainin...

20. [[PDF] Slide2 - Slope Stability - Rocscience](https://static.rocscience.cloud/assets/verification-and-theory/Slide2/Slide_SlopeStabilityVerification.pdf) - This document contains a series of verification slope stability problems that have been analyzed usi...

21. [Quiero que busques bajo que principios, metodos, calculos utiliza el programa SLIDE 2, el cual es un programa de estabilización de taludes. A partir de eso quiero que ejecutes un ejemplo simple aplicativo con alguno de los metodos que encontraste. De...

...abilidad de taludes similar o igual al que usa el programa. Quiero que investigues, para popsteriormente apliques en un ejemplo y de razones y aprendas. Posteriormente saca conclusiones para ver que tan fiable es lo que encontraste y las limitaciones](https://www.perplexity.ai/search/c6e83bfc-d3e6-495b-84b3-765737ecd58d) - SLIDE 2 es un potente programa de análisis de estabilidad de taludes que emplea principalmente métod...

22. [www.scribd.com › document › 333578279Nilmar Janbu - Stability Analysis of Slopes With Dimensionless...](https://www.scribd.com/document/333578279/Nilmar-Janbu-Stability-Analysis-of-Slopes-With-Dimensionless-Parameters) - Nilmar Janbu - Stability Analysis of Slopes With Dimensionless Parameters - Free download as PDF Fil...

23. [Morgenstern-Price | Circular Slip Surface | Online Help](https://www.finesoftware.eu/help/geo5/en/morgenstern-price-02/) - ... function). Morgenstern-Price is a rigorous method in the sense that it satisfies all three equat...

24. [Slope stability computations : In Embankment-dam Engineering. Textbook. Eds. R.C. Hirschfeld and S.J. Poulos. JOHN WILEY AND SONS INC., PUB., NY, 1973, 40P](https://linkinghub.elsevier.com/retrieve/pii/0148906275901394)

25. [scispace.com › papers › slope-stability-computations-5aloc90hex(Open Access) Slope stability computations (1973) | Nilmar Janbu...](https://scispace.com/papers/slope-stability-computations-5aloc90hex) - The general applicability of the proposed method for solving slope stability, earth pressure, and be...

26. [www.wiley-vch.de › soil-strength-and-slope-stability-978/1/118-65165-0Wiley-VCH - Soil Strength and Slope Stability](https://www.wiley-vch.de/en/areas-interest/engineering/civil-engineering-construction-10ce/soil-10ce2/soil-strength-and-slope-stability-978-1-118-65165-0) - Soil Strength and Slope Stability, Second Edition presents the latest thinking and techniques in the...

27. [Slope Stability and Stabilization Methods (2nd Edition)](https://tagasoft.com/publications/slope-stability-and-stabilization-methods-abramson-2001/) - The second edition adds material on shallow failures and landfill slopes and remains a go-to manual ...

28. [Slope Stability and Stabilization Methods de Lee W. Abramson](https://www.leslibraires.ca/livres/slope-stability-and-stabilization-methods-9780471384939) - ... Slope Stability and Stabilization, Second Edition assembles the background information, theory, ...

29. [Slide2 Overview | Documentation and Theory Overview - Rocscience](https://www.rocscience.com/help/slide2/overview/documentation-and-theory-overview) - Slide2 is a 2D limit equilibrium slope stability program for evaluating the safety factor or probabi...

