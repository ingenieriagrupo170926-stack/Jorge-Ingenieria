# 12 · Trampas de implementación (medidas, no teóricas)

> Nodo: `trampas` · Nivel L4. Cada punto tiene origen verificable: auditorías de OGR-Slip2D
> (`docs/audits/*.md` y docstrings), documentación de xslope, o este repositorio (V1–V4).
> Úsese como lista de revisión de código y como prompt de revisión para agentes.

## Formulación

1. **$F_f$ mal proyectado.** En la forma $\sum S\sec\alpha / \sum(W+\Delta X)\tan\alpha$, escribir
   $S\cos\alpha$ reduce F en $\cos^2\alpha$ por dovela: factor ~2 en taludes de 45°–64°. Prueba:
   $F_f(\lambda=0)$ debe igualar a Janbu simplificado término a término (OGR v0.1.106).
2. **Ramas con un iterado compartido.** $F_f$ y $F_m$ son puntos fijos independientes; iterar
   $F = (F_f+F_m)/2$ deja $F_m(0)$ 2–4 % bajo Bishop (OGR).
3. **Normal sin $X_R - X_L$.** Entonces $F_m$ no depende de λ y "Spencer/GLE" devuelven Bishop
   siempre (le pasó a OGR durante 80 versiones).
4. **Signo de la marcha.** Marchar desde el extremo equivocado da el mismo F (la suma telescopa)
   pero invierte el signo de todas las $E$ → falsas tracciones y rechazos (OGR, VP#26 Prandtl).
5. **Janbu $f_0$ fuera de dominio.** El polinomio decrece para $d/L > 0.357$: recortar. $d$ se mide
   perpendicular a la cuerda, no como altura de suelo (+2.9 % de error en OGR v0.1.19).
6. **$b_1$ en suelos mixtos.** Usar 0.50 cuando las bases atraviesan varios tipos (regla de Slide2
   según OGR; mejoró 7 filas del banco y empeoró 1). 0.69 vs 0.67 para $\phi=0$: sin resolver.
7. **Ordinario con agua.** $W\cos\alpha - ul$ (F&K) ≠ $(W-ub)\cos\alpha$; en bases horizontales la
   diferencia llega a 7.5 % (VP#22).
8. **Bishop en superficies no circulares** depende del eje elegido (OGR D47): no usarlo como
   "riguroso" fuera del círculo.
9. **Apoyos activos vs pasivos.** Pasivo divide por F (siempre da menor F); confundirlos cambia
   mucho el resultado en taludes reforzados (VP#85 con anclajes: Slide2 publica 1.324 en pasivo).

## Numérica

10. **Polos.** $m_\alpha$ y el denominador de la marcha se anulan para F pequeños o θ grandes;
    un buscador de horquilla ve un cambio de signo falso. Verificar $|r(F^*)| < tol$ (este repo)
    o acotar θ con margen (xslope `spencer_theta_bounds`). Bajar desde F alto.
11. **Raíces múltiples de $F_f - F_m$.** Talbingo (VP#6): λ = −0.979 → F = 1.68 (16 de 24 bordes
    en tracción, uno a −63 000 kN/m) frente a λ = +0.419 → F = 2.29 correcto. Preferir compresión
    y |λ| mínimo; si ninguna raíz es admisible, repetir sin el filtro y **decirlo**. El veredicto
    de admisibilidad es sensible: en VP#85 un cambio de signo de la resultante de empujes movió
    el F reportado por la búsqueda un 37 % con superficies casi idénticas (OGR D155) → publicar
    el margen de empuje, no solo un sí/no.
12. **Convergencia aparente.** Un punto fijo que "no mejora" no es uno que converge: exigir
    contracción además de paso < tol (OGR D116); con apoyos pasivos amortiguar (xslope).
13. **Fuerzas no nulas en el extremo.** Comprobar $E_n/\Sigma W$ y $M/(\Sigma W L)$ al final (V2).
14. **Métodos de θ prescrita con φ > 55°** (Hoek-Brown a bajo confinamiento) no convergen: usar
    Spencer/GLE.

## Geometría y agua

15. Dovelas que cruzan quiebres de terreno, capas o piezométrica → pesos y α erróneos.
16. Pesos sumergidos con flujo → omiten fuerzas de filtración (F puede duplicarse).
17. Freático inclinado tomado como piezométrico → sobreestima $u$ ($\cos^2\theta$; 12 % a 20°).
18. Tensiones totales con $u \neq 0$ → doble descuento del agua.
19. Muestrear una piezométrica fuera de su extensión → $u = 0$ silencioso (xslope lo prohíbe).
20. Círculos por debajo de la roca: o se rechazan o se truncan (superficie compuesta); elegir
    explícitamente.

## Búsqueda

21. **Mínimo trivial**: con $c' = 0$ el mínimo es una "rebanada" superficial (talud infinito).
    Filtro de profundidad mínima.
22. **Mínimo en el borde de la malla**: ampliar/mover la malla.
23. **Un solo buscador / una sola semilla** no demuestra mínimo global (Slide2 y GEO5 lo advierten).
24. Promedio vs mínimo al refinar divisiones en Auto Refine (OGR v0.1.150: el promedio no lleva
    a mínimos en los extremos del talud).
25. Configuraciones "muertas": opciones que se guardan pero ningún cálculo lee (OGR D08, D32).
    Cada opción del modelo necesita una prueba que demuestre que cambia el resultado.

## Validación

26. Validar contra **referencias externas** (artículos, manuales de verificación), no contra
    instantáneas de la propia salida: una instantánea congela el error.
27. Comparar mismo método con mismo método; búsquedas distintas pueden hallar mecanismos
    distintos (xslope puntúa solo pares del mismo método).
28. La tolerancia depende de la fuente: un valor leído de una figura no merece 0.1 %.
