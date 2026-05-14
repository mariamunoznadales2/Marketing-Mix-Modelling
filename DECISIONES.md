# K-Moda · Marketing Mix Model — Cuaderno de Decisión Estratégica

`marketing_mix_DECISION.ipynb`

---

## Objetivo

Este cuaderno no reentrena el modelo. Toma los artefactos del modelo ya
entrenado en `marketing_mix.ipynb` y los convierte en un simulador de decisiones
bajo incertidumbre para dirección.

La pregunta que responde no es "¿cómo explico las ventas?", sino:

> ¿Qué debería hacer K-Moda con su presupuesto publicitario dadas distintas
> hipótesis de negocio?

---

## Prerequisitos

1. Ejecutar `marketing_mix.ipynb` completo para generar `mmm_artifacts.pkl`.
2. Tener instaladas las dependencias del entorno: `numpy`, `pandas`,
   `matplotlib`, `scikit-learn` y `scipy`.

Si `mmm_artifacts.pkl` no existe, el notebook usa valores mock calibrados a los
outputs reales y funciona de todos modos. En la ejecución actual la fuente de
datos usada fue `mmm_artifacts.pkl`.

---

## Estructura del notebook

| Sección | Contenido |
|---------|-----------|
| 1 | Carga de artefactos del modelo |
| 2 | Funciones de respuesta de canal |
| 3 | Incertidumbre: bandas de confianza |
| 4 | `simulate_scenario()` |
| 5 | Biblioteca de escenarios |
| 6 | Comparativa visual de escenarios |
| 7 | Análisis de función de pérdida, MAPE |
| 8 | Vista ejecutiva: mapa riesgo-retorno |
| 9 | Frontera de eficiencia estratégica, ROI vs ventas |

---

## Parámetros del modelo

| Métrica | Valor |
|---------|------:|
| R² | 0.885 |
| MAPE base | 7.5% |
| Ventas anuales baseline | 153.2 M€/año |
| Presupuesto actual | 11.97 M€/año |
| Uplift directo del mix óptimo en `marketing_mix.ipynb` | +3.00 M€/año |

### ROI base por canal

| Canal | Inversión actual | ROI | Incertidumbre coef. |
|-------|-----------------:|----:|--------------------:|
| Digital Performance | 4.76 M€ | 4.32x | 18% |
| Digital Awareness | 2.77 M€ | 8.29x | 25% |
| Offline | 3.85 M€ | 4.45x | 32% |
| CRM / Email | 0.59 M€ | 24.27x | 22% |

La incertidumbre es mayor en Offline y Digital Awareness porque son canales de
brand-building donde el efecto causal es más difícil de aislar estadísticamente.

---

## Calibración

El notebook verifica que las funciones de respuesta reconstruyen correctamente
el punto actual:

| Concepto | Resultado |
|----------|----------:|
| Contribución marketing @ actual | 74.9 M€/año |
| Baseline no-marketing | 78.3 M€/año |
| Total reconstruido | 153.2 M€/año |

| Canal | Δ @ m = 1 |
|-------|----------:|
| Digital Performance | +0.00 €/año |
| Digital Awareness | +0.00 €/año |
| Offline | +0.00 €/año |
| CRM / Email | +0.00 €/año |

Esto confirma que el escenario actual queda calibrado como punto de referencia:
si el multiplicador de todos los canales es `m = 1`, el delta contra el actual
es cero.

---

## Validación directa del modelo

Esta validación viene del notebook principal `marketing_mix.ipynb` y usa
`predict` directo sobre el ElasticNet final. Sirve como ancla del modelo antes
de pasar a la capa de decisión.

| Test | Resultado | Lectura |
|------|----------:|---------|
| Baseline, m = 1 | +0.00 €/año | Si no se cambia el mix, el delta contra el actual es cero. |
| Mix óptimo SLSQP | +3.00 M€/año | Reasignar el presupuesto al mix óptimo genera uplift estimado. |

### Sensibilidad aislada por canal

| Canal | Multiplicador óptimo | Δ aislado |
|-------|---------------------:|----------:|
| Digital Performance | 0.67x | -5.37 M€/año |
| Digital Awareness | 1.36x | +5.58 M€/año |
| Offline | 1.14x | +1.68 M€/año |
| CRM / Email | 1.11x | +1.12 M€/año |

Los deltas aislados muestran qué ocurre al mover cada canal por separado al
multiplicador óptimo, manteniendo el resto en baseline. No deben sumarse: la
ganancia válida del mix completo en el modelo principal es **+3.00 M€/año**.

---

## Curvas de respuesta

`decision_01_roi_curves.png`

Para cada canal se muestra:

- Línea central P50: estimación del modelo.
- Banda interior P25-P75: rango de mayor probabilidad.
- Banda exterior P10-P90: rango amplio de incertidumbre.
- Punto actual: inversión y ROI observados en el período.
- Estrella dorada: punto óptimo según el modelo.

Las bandas se generan con 800 simulaciones Monte Carlo perturbando los
coeficientes de saturación del modelo.

---

## Escenarios simulados

### Validación de `simulate_scenario()`

| Métrica | Resultado |
|---------|----------:|
| Ventas centrales | 153.2 M€ |
| Δ vs actual | +0.000 M€ |
| P10-P90 | [141.4, 166.1] M€ |
| ROI total | 12.80x |
| Riesgo | Medio, 16.1% |

### Biblioteca de escenarios

| Escenario | Lógica |
|-----------|--------|
| Actual (referencia) | Mix histórico 2020-2024 |
| Óptimo matemático | Resultado del optimizador SLSQP del modelo |
| Conservador | Proteger CRM y Performance, reducir riesgo operativo |
| Agresivo | Apostar por Awareness y Offline para volumen y marca |
| Eficiencia ROI | Maximizar retorno por euro invertido |
| Marca | Awareness + Offline sostenido para brand equity |

### Resultados centrales

| Escenario | Ventas (M€) | P10-P90 (M€) | Δ vs actual | Δ % | ROI | Riesgo |
|-----------|------------:|-------------:|------------:|----:|----:|--------|
| Actual (referencia) | 153.2 | [141.4 - 166.1] | +0.00 M€ | 0.0% | 12.80x | Medio |
| Óptimo matemático | 154.9 | [142.1 - 168.7] | +1.72 M€ | 1.1% | 12.91x | Medio |
| Conservador (CRM + Perf) | 154.4 | [142.8 - 167.0] | +1.15 M€ | 0.8% | 12.90x | Medio |
| Agresivo (Awareness + Offline) | 153.4 | [140.9 - 167.3] | +0.21 M€ | 0.1% | 12.82x | Medio |
| Eficiencia ROI | 155.9 | [143.4 - 169.5] | +2.73 M€ | 1.8% | 13.03x | Medio |
| Marca (Awareness + Offline) | 152.3 | [139.5 - 166.2] | -0.94 M€ | -0.6% | 12.72x | Medio |

### Desglose de inversión por canal

| Escenario | Digital Performance | Digital Awareness | Offline | CRM / Email | Inversión total |
|-----------|--------------------:|------------------:|--------:|------------:|----------------:|
| Actual (referencia) | 4.76 M€ | 2.77 M€ | 3.85 M€ | 0.59 M€ | 11.97 M€ |
| Óptimo matemático | 3.19 M€ | 3.77 M€ | 4.38 M€ | 0.65 M€ | 12.00 M€ |
| Conservador (CRM + Perf) | 5.40 M€ | 2.69 M€ | 3.11 M€ | 0.76 M€ | 11.97 M€ |
| Agresivo (Awareness + Offline) | 3.63 M€ | 3.74 M€ | 4.11 M€ | 0.49 M€ | 11.97 M€ |
| Eficiencia ROI | 4.16 M€ | 4.08 M€ | 3.02 M€ | 0.70 M€ | 11.97 M€ |
| Marca (Awareness + Offline) | 3.23 M€ | 3.81 M€ | 4.51 M€ | 0.42 M€ | 11.97 M€ |

Nota de reconciliación: el `BASE.md` reporta el uplift directo del modelo
principal, **+3.00 M€/año**, usando `predict_mix` sobre ElasticNet. Esta tabla
pertenece al cuaderno de decisión y aplica una capa adicional de curvas de
respuesta, incertidumbre y distancia al mix histórico; por eso el escenario
"Óptimo matemático" aparece como una estimación central más conservadora,
**+1.72 M€**.

---

## Análisis de función de pérdida

`decision_03_mape.png`

| Escenario | Desviación máx. canal | MAPE ajustado est. | Confianza |
|-----------|----------------------:|-------------------:|-----------|
| Actual (referencia) | 0% | 7.5% | Alta |
| Óptimo matemático | 36% | 8.6% | Alta |
| Conservador (CRM + Perf) | 30% | 8.4% | Alta |
| Agresivo (Awareness + Offline) | 35% | 8.6% | Alta |
| Eficiencia ROI | 47% | 9.0% | Alta |
| Marca (Awareness + Offline) | 37% | 8.7% | Alta |

El MAPE ajustado es un proxy conservador: aumenta cuanto más se aleja el
escenario del mix de entrenamiento. Todos los escenarios mantienen confianza
**Alta**, pero las desviaciones superiores al 30% requieren validación holdout
antes de reasignar presupuesto real.

---

## Vista ejecutiva

`decision_04_risk_return.png`

| Prioridad | Escenario recomendado | Ventas | ROI | Riesgo |
|-----------|----------------------|-------:|----:|--------|
| Máximas ventas | Eficiencia ROI | 155.9 M€ | 13.03x | Medio |
| Mayor ROI | Eficiencia ROI | 155.9 M€ | 13.03x | Medio |
| Equilibrio | Eficiencia ROI | 155.9 M€ | 13.03x | Medio |

El escenario **Eficiencia ROI** domina en la comparativa de escenarios simulados:
consigue la mayor venta central, el mayor ROI medio y mantiene riesgo Medio.

---

## Frontera de eficiencia estratégica

`decision_05_efficiency_frontier.png`  
`decision_06_frontier_alloc.png`

La nueva sección del notebook muestra que el trade-off ROI vs ventas no es solo
un problema de reasignación interna. También es un problema de **nivel de
presupuesto**. Bajo rendimientos decrecientes, aumentar el ROI exige invertir
menos; maximizar ventas exige aceptar un ROI menor.

### Frontera de eficiencia

| Fracción actual | Presupuesto | ROI | Ventas (M€) | P10-P90 (M€) | Δ vs actual |
|----------------:|------------:|----:|------------:|-------------:|------------:|
| 20% | 2.42 M€ | 46.1x | 111.6 | [105.1 - 118.2] | -41.65 M€ |
| 30% | 3.63 M€ | 33.3x | 120.9 | [113.2 - 128.7] | -32.28 M€ |
| 40% | 4.84 M€ | 26.6x | 128.8 | [120.0 - 137.7] | -24.43 M€ |
| 50% | 6.04 M€ | 22.4x | 135.4 | [125.7 - 145.9] | -17.78 M€ |
| 60% | 7.25 M€ | 19.5x | 141.4 | [130.8 - 151.9] | -11.80 M€ |
| 70% | 8.46 M€ | 17.4x | 147.2 | [135.7 - 158.9] | -6.03 M€ |
| 80% | 9.67 M€ | 15.7x | 152.1 | [140.0 - 164.5] | -1.12 M€ |
| 90% | 10.88 M€ | 14.3x | 156.1 | [143.0 - 168.9] | +2.87 M€ |
| 100% | 12.09 M€ | 13.3x | 161.0 | [147.6 - 174.5] | +7.77 M€ |
| 120% | 14.51 M€ | 11.6x | 168.8 | [154.4 - 183.5] | +15.56 M€ |
| 150% | 18.13 M€ | 9.9x | 179.2 | [163.0 - 195.4] | +25.96 M€ |
| 200% | 24.18 M€ | 7.9x | 191.2 | [172.8 - 209.8] | +38.00 M€ |
| 300% | 36.26 M€ | 5.9x | 213.0 | [191.6 - 234.4] | +59.80 M€ |

La fila 100% no es el mix histórico actual: es el mejor mix encontrado sobre la
frontera para un presupuesto equivalente al actual. Por eso puede superar al
escenario "Actual (referencia)".

### Objetivos ROI con presupuesto fijo

| Restricción | ROI logrado | Ventas | Δ vs actual |
|-------------|------------:|-------:|------------:|
| ROI ≥ 12.5x | 13.35x | 161.3 M€ | +8.13 M€ |
| ROI ≥ 13.0x | 13.33x | 161.1 M€ | +7.89 M€ |
| ROI ≥ 13.5x | 13.50x | 160.1 M€ | +6.89 M€ |

### Presupuesto necesario por objetivo ROI

| ROI objetivo | Budget necesario | Ajuste vs actual | Ventas |
|-------------:|-----------------:|-----------------:|-------:|
| 12.5x | 12.1 M€ (100%) | +1% | 161.0 M€ |
| 13.0x | 12.1 M€ (100%) | +1% | 161.0 M€ |
| 14.0x | 10.9 M€ (90%) | -9% | 156.1 M€ |
| 15.0x | 10.9 M€ (90%) | -9% | 156.1 M€ |
| 17.0x | 8.5 M€ (70%) | -29% | 147.2 M€ |
| 20.0x | 7.3 M€ (60%) | -39% | 141.4 M€ |

### Interpretación estratégica

| Zona de la frontera | ROI típico | Budget | Perfil estratégico |
|---------------------|-----------:|--------|--------------------|
| Alto volumen | 8-10x | >150% actual | Crecimiento, cuota de mercado |
| Equilibrio | 12-14x | 80-100% actual | Mixto, sostenible |
| Alta eficiencia | 17-20x | 50-70% actual | Margen, rentabilidad |
| Máxima eficiencia | >25x | <40% actual | Solo canales más eficientes |

Perseguir un ROI de 20x no significa simplemente optimizar el mix: implica
invertir alrededor de un 40% menos que el presupuesto actual y aceptar menos
ventas. La dirección debe elegir conscientemente dónde situarse en la curva:
crecimiento, equilibrio, eficiencia o maximización de margen.

---

## Advertencias metodológicas

- **CRM / Email:** el ROI elevado refleja el coste de plataforma registrado, no
  el coste total del equipo. El ROI real es significativamente menor.
- **Offline:** los efectos de brand equity a largo plazo no están capturados en
  este modelo. El ROI puede estar subestimado para este canal.
- **Holdout:** cualquier escenario con cambios materiales de mix debe validarse
  con holdout o experimento antes de reasignar presupuesto real.
- **Horizonte temporal:** el modelo entrena sobre 2020-2024. Cambios
  estructurales de mercado no están reflejados.

---

## Gráficas generadas

| Archivo | Contenido |
|---------|-----------|
| `decision_01_roi_curves.png` | Curvas ROI por canal con bandas P10-P90 |
| `decision_02_scenario_comparison.png` | Comparativa de escenarios: ventas, ROI, delta y mix |
| `decision_03_mape.png` | MAPE estimado por escenario |
| `decision_04_risk_return.png` | Mapa riesgo-retorno |
| `decision_05_efficiency_frontier.png` | Frontera ROI vs ventas |
| `decision_06_frontier_alloc.png` | Evolución del mix a lo largo de la frontera |

---

## Separación modelo / decisión

| Capa | Qué hace | Dónde |
|------|----------|-------|
| Modelo | Estima el efecto causal de la inversión en ventas | `marketing_mix.ipynb` |
| Decisión | Evalúa trade-offs bajo incertidumbre | `marketing_mix_DECISION.ipynb` |

El modelo no dicta la decisión: la informa y estructura. El modelo principal
valida un potencial directo de **+3.00 M€/año** para el mix óptimo; el cuaderno
de decisión traduce ese potencial a escenarios comparables bajo incertidumbre y
añade la frontera ROI-ventas para elegir el nivel de presupuesto adecuado.
