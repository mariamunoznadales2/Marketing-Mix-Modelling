# K-Moda · Marketing Mix Modeling

Trabajo de Marketing Mix Modeling para estimar el impacto incremental de la inversión publicitaria de K-Moda sobre las ventas, optimizar la asignación del presupuesto anual y traducir el modelo en una decisión ejecutiva entre crecimiento y eficiencia.

El proyecto combina análisis exploratorio, construcción de una serie semanal nacional, modelado econométrico con Elastic Net, optimización presupuestaria con SLSQP, simulación de escenarios bajo incertidumbre y una app ejecutiva en Streamlit.

## Objetivo del trabajo

El objetivo principal es responder a una pregunta de negocio:

> ¿Cómo debe reasignar K-Moda su presupuesto de marketing para maximizar el valor generado sin perder de vista el riesgo, la saturación de canales y el trade-off entre ventas y ROI?

El análisis parte de datos históricos de 2020 a 2024 y evalúa un presupuesto base cercano a 12 millones de euros anuales.

## Resultados principales

| Indicador | Resultado |
|---|---:|
| Período analizado | 2020-2024 |
| Serie modelada | 260 semanas |
| Ventas totales modeladas | 766 M€ aprox. |
| R² del modelo | 0,885 |
| MAPE | 7,5% aprox. |
| Presupuesto anual base | 12 M€ |
| Uplift validado del mix óptimo | +3,00 M€/año |
| Contribución atribuida a marketing | 48,9% de las ventas |

La recomendación base es mantener un enfoque de equilibrio: no aumentar necesariamente el presupuesto total, sino reasignar inversión desde Digital Performance hacia canales con mejor recorrido marginal, especialmente Digital Awareness, Offline y CRM / Email.

## Metodología

El trabajo sigue estas fases:

1. **EDA y validación de integridad**
   - Revisión de tablas, fechas, granularidades y claves.
   - Identificación de la diferencia de frecuencia entre ventas/tráfico diarios e inversión semanal.

2. **Construcción de la variable dependiente**
   - Rollup de `ventas_lineas` a ventas netas.
   - Construcción de un panel fecha x ciudad.
   - Uso de `LEFT JOIN` para evitar sesgos por pérdida de filas.
   - Agregación semanal para obtener `Yt`.

3. **Construcción de variables independientes**
   - Inversión por canal.
   - Tráfico web.
   - Variables de calendario, clima, turismo, promociones y tendencia.
   - Transformaciones de adstock y saturación.

4. **Modelado**
   - Modelo ElasticNetCV con coeficientes positivos.
   - Validación con `TimeSeriesSplit`.
   - Controles de base, tendencia y estacionalidad.
   - Agrupación de canales para reducir multicolinealidad.

5. **Atribución y ROI**
   - Descomposición de ventas entre base estructural y marketing.
   - Cálculo de ventas atribuidas por grupo de canal.
   - Cálculo de ROI incremental.

6. **Optimización**
   - Optimización SLSQP con presupuesto fijo.
   - Bounds realistas por canal.
   - Penalización de suavidad para evitar soluciones extremas.
   - Validación directa con `predict` sobre el ElasticNet final.

7. **Decisión estratégica**
   - Simulación de escenarios.
   - Bandas de incertidumbre P10-P90.
   - Frontera ROI vs ventas.
   - Lectura ejecutiva de crecimiento, equilibrio y eficiencia.

## Estructura del repositorio

```text
.
├── app_mmm.py                         # Dashboard ejecutivo en Streamlit
├── marketing_mix.ipynb                # Notebook principal de MMM
├── marketing_mix_DECISION.ipynb       # Notebook de escenarios y decisión estratégica
├── DECISIONES.md                      # Resumen metodológico y ejecutivo del cuaderno de decisión
├── ROI_VS_VENTAS.md                   # Documento sobre la frontera ROI vs ventas
├── requirements.txt                   # Dependencias Python
├── mmm_artifacts.pkl                  # Artefactos exportados del modelo principal
├── Presentación.pptx                 # Presentación final
├── ENTREGA/
│   ├── Presentación.pptx             # Copia de entrega
│   └── link_app.txt                   # Link o referencia de la app
├── out_csv_final/
│   ├── calendario_ciudad.csv
│   ├── clientes.csv
│   ├── inversion_medios_semanal.csv
│   ├── pedidos.csv
│   ├── productos.csv
│   ├── trafico_tienda_web_diario.csv
│   ├── ventas_lineas.csv
│   └── CASOMAT_MM_07_VENTAS_LINEAS.pkl
└── graficas_styled/
    ├── graficas_base/                 # Gráficas del modelo base
    └── graficas_decision/             # Gráficas de escenarios y frontera
```

## Datos utilizados

Los datos procesados se encuentran en `out_csv_final/`.

| Archivo | Contenido |
|---|---|
| `ventas_lineas.csv` | Líneas de venta, fuente granular principal para construir `Yt` |
| `pedidos.csv` | Información de pedidos |
| `clientes.csv` | Información de clientes |
| `productos.csv` | Catálogo de productos |
| `calendario_ciudad.csv` | Calendario por ciudad con variables externas |
| `trafico_tienda_web_diario.csv` | Tráfico web y variables diarias por ciudad |
| `inversion_medios_semanal.csv` | Inversión semanal por canal y ciudad |
| `CASOMAT_MM_07_VENTAS_LINEAS.pkl` | Caché local para acelerar la lectura de ventas |

Los archivos de ventas y pedidos son grandes, por lo que el notebook usa caché en pickle para acelerar la ejecución local.

## Canales modelados

El modelo agrupa la inversión en cuatro bloques:

| Canal | Lectura |
|---|---|
| Digital Performance | Canal de respuesta directa, con señales de saturación relativa |
| Digital Awareness | Canal con mayor recorrido marginal en el mix óptimo |
| Offline | Canal relevante para volumen y marca, con mayor incertidumbre |
| CRM / Email | Canal con ROI elevado, aunque condicionado por el coste registrado |

## Hallazgos por canal

| Canal | Inversión actual | ROI base | Lectura |
|---|---:|---:|---|
| Digital Performance | 4,76 M€ | 4,32x | Canal con mayor peso presupuestario y menor eficiencia relativa |
| Digital Awareness | 2,77 M€ | 8,29x | Canal recomendado para refuerzo |
| Offline | 3,85 M€ | 4,45x | Impacto relevante, aunque con incertidumbre y posible efecto a largo plazo no capturado |
| CRM / Email | 0,59 M€ | 24,27x | Muy eficiente, pero el ROI puede estar sobreestimado si no incluye coste total de equipo |

## Escenarios estratégicos

El cuaderno de decisión compara distintos escenarios:

| Escenario | Lectura |
|---|---|
| Actual | Punto de referencia histórico |
| Óptimo matemático | Reasignación optimizada con restricciones |
| Conservador | Protege CRM y Performance, reduce riesgo operativo |
| Agresivo | Refuerza Awareness y Offline para volumen y marca |
| Eficiencia ROI | Busca el mayor retorno por euro invertido |
| Marca | Prioriza Awareness y Offline con foco en brand equity |

La comparativa de escenarios muestra que el modelo no debe leerse como una única respuesta automática. Su valor está en mostrar las consecuencias de cada decisión.

## Frontera ROI vs ventas

Una conclusión central del trabajo es que no existe un ROI óptimo único.

La frontera de eficiencia muestra una relación clara:

- Más presupuesto implica más ventas y menor ROI.
- Menos presupuesto implica mayor ROI y menos ventas.
- Subir el ROI no significa necesariamente optimizar mejor el mix; muchas veces significa reducir el nivel total de inversión.

Ejemplos documentados:

| Objetivo | Presupuesto aprox. | Ventas aprox. | Lectura |
|---|---:|---:|---|
| ROI 13x | 12,1 M€ | 161,0 M€ | Equilibrio |
| ROI 17x | 8,5 M€ | 147,2 M€ | Alta eficiencia |
| ROI 20x | 7,3 M€ | 141,4 M€ | Eficiencia extrema con sacrificio de ventas |

Por tanto, la decisión final es estratégica:

> K-Moda debe elegir dónde situarse entre crecimiento, equilibrio y eficiencia.

## Gráficas generadas

Las gráficas principales están en `graficas_styled/`.

### Gráficas base

| Archivo | Contenido |
|---|---|
| `01_serie_yt_y_estacionalidad.png` | Serie temporal de ventas y estacionalidad |
| `02_distribucion_inversion.png` | Distribución de inversión |
| `03_yt_vs_inversion_total.png` | Ventas frente a inversión total |
| `04_trafico_web_vs_ventas.png` | Tráfico web frente a ventas |
| `05_heatmap_correlaciones.png` | Correlaciones entre variables |
| `06_estacionalidad_por_semana.png` | Estacionalidad semanal |
| `07_curva_mape_alpha.png` | Selección de regularización |
| `fase6_curvas_respuesta.png` | Curvas de respuesta |
| `fase6_escenarios.png` | Escenarios de inversión |
| `economic_waterfall_sales_decomposition.png` | Descomposición económica de ventas |
| `economic_attributed_sales_by_channel.png` | Ventas atribuidas por canal |
| `economic_current_vs_optimal_investment.png` | Inversión actual vs óptima |
| `economic_marketing_vs_base_share_over_time.png` | Peso de marketing vs base en el tiempo |

### Gráficas de decisión

| Archivo | Contenido |
|---|---|
| `decision_01_roi_curves.png` | Curvas ROI por canal con bandas de incertidumbre |
| `decision_04_risk_return.png` | Mapa riesgo-retorno |
| `decision_05_efficiency_frontier.png` | Frontera ROI vs ventas |
| `decision_06_frontier_alloc.png` | Evolución del mix a lo largo de la frontera |

## Cómo ejecutar el proyecto

### 1. Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el notebook principal

Abrir y ejecutar:

```text
marketing_mix.ipynb
```

Este notebook construye el dataset modelado, entrena el MMM, calcula contribuciones y exporta `mmm_artifacts.pkl`.

### 4. Ejecutar el cuaderno de decisión

Abrir y ejecutar:

```text
marketing_mix_DECISION.ipynb
```

Este notebook toma los artefactos del modelo y genera escenarios, bandas de incertidumbre y la frontera ROI vs ventas.

### 5. Lanzar la app Streamlit

```bash
streamlit run app_mmm.py
```

La app presenta el trabajo en formato ejecutivo: resumen, diagnóstico del mix, saturación, frontera estratégica, simulador, escenarios y biblioteca visual.

## Dependencias

El archivo `requirements.txt` fija las siguientes librerías principales:

```text
streamlit==1.56.0
pandas==3.0.2
numpy==2.4.4
matplotlib==3.10.8
scipy==1.17.1
seaborn==0.13.2
scikit-learn==1.8.0
```

## Entregables

| Entregable | Archivo |
|---|---|
| Notebook principal | `marketing_mix.ipynb` |
| Notebook de decisión | `marketing_mix_DECISION.ipynb` |
| Dashboard ejecutivo | `app_mmm.py` |
| Presentación | `Presentación.pptx` |
| Documentación de decisión | `DECISIONES.md` |
| Análisis ROI vs ventas | `ROI_VS_VENTAS.md` |
| Gráficas finales | `graficas_styled/` |
| Datos procesados | `out_csv_final/` |

## Advertencias metodológicas

- El modelo estima efectos incrementales agregados, no conversiones individuales.
- La multicolinealidad entre canales obliga a interpretar los resultados por bloques, no como causalidad perfecta canal a canal.
- CRM / Email muestra un ROI muy alto porque el coste registrado parece corresponder principalmente a plataforma; si se imputan costes de equipo, el ROI real bajaría.
- Offline puede estar infraestimado porque los efectos de marca a largo plazo no se capturan completamente.
- Escenarios alejados del mix histórico deben validarse con holdout, experimentos o pilotos antes de reasignar presupuesto real.
- Un ROI más alto no siempre significa mejor negocio: puede venir de reducir inversión y aceptar menos ventas.

## Conclusión ejecutiva

El modelo valida que el marketing tiene un peso relevante en las ventas de K-Moda y que existe una oportunidad de mejora por reasignación del presupuesto.

La recomendación base es una posición de equilibrio:

- Mantener el presupuesto cercano a 12 M€.
- Reducir peso en Digital Performance.
- Reforzar Digital Awareness, Offline y CRM / Email.
- Usar la frontera ROI vs ventas para decidir si la prioridad del ejercicio es crecer, proteger margen o maximizar eficiencia.

El modelo no sustituye la decisión de dirección: la estructura, la cuantifica y muestra sus consecuencias.
