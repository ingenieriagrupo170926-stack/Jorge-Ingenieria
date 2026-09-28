# Resultados de validación (generado por validar.py)

## V1 — Fredlund & Krahn (1977) / Slide2 VP#21 — círculo fijo (120, 90), R = 80 ft, 50 dovelas

| Caso | Método | Este solver | F&K 1977 | Δ vs F&K | xslope | Δ vs xslope | extra |
|---|---|---|---|---|---|---|---|
| seco | bishop | 2.0767 | 2.08 | -0.16 % | 2.0749 | +0.09 % |  |
| seco | janbu | 1.8772 | — | — | 1.8747 | +0.13 % |  |
| seco | janbu_corregido | 2.0218 | — | — | — | — | f0=1.0771, d/L=0.225, b1=0.5 |
| seco | spencer | 2.0729 | 2.073 | -0.01 % | 2.071 | +0.09 % | θ=14.48° |
| seco | mp | 2.0724 | 2.076 | -0.17 % | 2.0706 | +0.09 % | λ=0.324 (semiseno) |
| ru | bishop | 1.7602 | 1.766 | -0.33 % | 1.7585 | +0.10 % |  |
| ru | janbu | 1.5888 | — | — | 1.5865 | +0.14 % |  |
| ru | janbu_corregido | 1.7112 | — | — | — | — | f0=1.0771, d/L=0.225, b1=0.5 |
| ru | spencer | 1.7583 | 1.761 | -0.15 % | 1.7565 | +0.10 % | θ=14.04° |
| ru | mp | 1.7576 | 1.764 | -0.36 % | 1.7559 | +0.10 % | λ=0.314 (semiseno) |
| freat | bishop | 1.8301 | 1.834 | -0.21 % | 1.8283 | +0.10 % |  |
| freat | janbu | 1.6779 | — | — | 1.6755 | +0.14 % |  |
| freat | janbu_corregido | 1.8072 | — | — | — | — | f0=1.0771, d/L=0.225, b1=0.5 |
| freat | spencer | 1.8286 | 1.83 | -0.08 % | 1.8268 | +0.10 % | θ=13.50° |
| freat | mp | 1.8278 | 1.832 | -0.23 % | 1.8261 | +0.09 % | λ=0.299 (semiseno) |

## V2 — Identidades internas (caso F&K seco)

- Spencer con punto de momentos en el centro vs en (300, 500): 2.072854 vs 2.072854 (|Δ| = 0.0e+00) → el resultado riguroso no depende del punto de momentos.
- M-P con f(x)=1 (función de usuario) vs Spencer: 2.072854 vs 2.072854 (λ = 0.25821 = tanθ).
- Janbu simplificado por recurrencia (E_n = 0) vs fórmula cerrada ΣS·cosα / ΣN·sinα: 1.877171 vs 1.877171.
- Equilibrio residual en la solución Spencer: E_n/ΣW = 7.2e-17, M/(ΣW·L) = 3.3e-15

## V3 — ACADS 1(a) / Slide2 VP#1 — búsqueda circular (c'=3 kPa, φ'=19.6°, γ=20 kN/m³)

| Método | F mínimo | Círculo crítico (xc, yc, R) | ACADS (consenso) | Slide2 | xslope | tiempo |
|---|---|---|---|---|---|---|
| bishop | 0.9852 | (29.63, 53.45, 28.45) | 1.00 | 0.987 | 0.985 | 7 s |
| janbu_corregido | 0.9856 | (31.09, 49.98, 25.00) | 1.00 | — | 0.986 ('Janbu' de xslope, con f0) | 6 s |
| spencer | 0.9843 | (29.70, 53.35, 28.35) | 1.00 | — | 0.984 | 277 s |

## V4 — Optimización poligonal (8 vértices) desde el círculo crítico Spencer de V3

- Spencer sobre la poligonal inscrita en el círculo: 0.9881; tras optimizar: 0.9852 (57 s).
- Vértices optimizados: [(30.0, 25.0), (33.05, 25.03), (36.1, 25.7), (39.15, 26.72), (42.2, 28.04), (45.25, 29.71), (48.3, 31.85), (51.35, 35.0)]
