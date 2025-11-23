<!-- ====================== PORTADA ====================== -->

# 📘 **PROYECTO FINAL — Decisiones Inteligentes en la NBA**
## 🧠 *Análisis de Talento y Rendimiento (1996–2023)*  
### 🏫 Henry | Cohorte DA_FT18 | Año 2025  

**Equipo de Analítica:**  
👩‍💻 Lucy Melo  
👩‍💻 Melisa Rossi  
👨‍💻 Felipe Carassale  
👩‍💻 Camila Pineda  
👨‍💻 Esteban Mamani  

---

<p align="center">
  <img src="../Images/informe/image_1.png" width="90%">
</p>

---

<!-- ====================== ÍNDICE PREMIUM ====================== -->

# 📑 **ÍNDICE NAVEGABLE**  
*(Click para ir a cada sección)*  

### 🏁 INTRODUCCIÓN  
- [📘 Portada](#-proyecto-final--decisiones-inteligentes-en-la-nba)  
- [📄 Resumen](#-resumen)  
- [🎯 Objetivo del Proyecto](#-objetivo-del-proyecto)

### 🔬 DATOS Y MÉTODOS  
- [🧪 Datos y Metodología](#-datos-y-metodología)  
  - [📚 Origen de los Datos](#-origen-de-los-datos)  
  - [🧹 Limpieza y Transformación](#-limpieza-y-transformación-de-datos)  
  - [📊 Análisis Estadístico](#-análisis-estadístico)

### 🔎 ANÁLISIS EXPLORATORIO  
- [🔎 EDA: Exploración Inicial](#-análisis-exploratorio-de-datos-eda)  
- [🏀 Contexto Histórico](#-contexto-histórico-de-la-liga)  
- [🧍‍♂️ Evolución de Jugadores](#-evolución-de-la-cantidad-de-jugadores-por-temporada)  
- [📈 Distribuciones y Tendencias](#-distribución-general-del-rendimiento-por-jugador-y-temporada)

### 🧩 INDICADORES PERSONALIZADOS  
- [📦 Global Score](#-análisis-de-rendimiento-colectivo)  
- [🎚️ Vara (P10)](#-evolución-del-percentil-10-vara-por-equipo)  
- [🏅 RMO (P75)](#-indicadores-personalizados-rmo-rendimiento-más-óptimo)  
- [🏆 Top 10 Élites](#-top-10-jugadores-con-rendimiento-superior-al-rmo)

### 🤖 MODELO PREDICTIVO  
- [🤖 Predicción de Rendimiento](#-modelo-predictivo-de-rendimiento-global)  
- [📊 Importancia de Variables](#-importancia-de-variables-en-el-modelo)

### 🧬 CLUSTERING  
- [🧬 K-Means](#-segmentación-por-clustering-k-means)  
- [📋 Comparación por Clúster](#-tabla-comparativa-de-métricas-por-clúster)  
- [🔵 Interpretación](#-interpretación-de-los-clústeres)

### 📊 DASHBOARD & INSIGHTS  
- [📊 Dashboard Interactivo](#-dashboard-interactivo-de-la-nba)  
- [⚠️ Limitaciones](#-limitaciones-del-análisis)  
- [🧠 Conclusiones](#-conclusiones-finales)  
- [🧭 Recomendaciones](#-recomendaciones-estratégicas)

### 📁 ANEXOS  
- [🧩 Archivos](#-anexos)  
- [🏁 Cierre](#-cierre)

---

<!-- ====================== RESUMEN ====================== -->

# 📄 **RESUMEN**

El presente informe ofrece un análisis integral del rendimiento de jugadores y equipos de la **NBA** durante 26 temporadas (1996–2022).  
Se aplicaron metodologías de:

- Limpieza de datos  
- Métricas avanzadas  
- Modelado predictivo  
- Clustering  
- Dashboards interactivos  

El análisis revela:

- Patrones estables de rendimiento histórico  
- Relación entre eficiencia, uso ofensivo y rebotes  
- Factores determinantes en desempeño colectivo  
- Talento oculto en jugadores poco reconocidos  
- Un modelo predictivo con **R² = 0.8613**  
- Cuatro perfiles de jugador vía clustering  
- Umbrales estratégicos mediante RMO (P75) y VARA (P10)

Este informe permite fortalecer decisiones sobre:

✔️ Renovación de contratos  
✔️ Transferencias  
✔️ Roles de jugadores  
✔️ Construcción de plantillas  
✔️ Scouting basado en datos  

---

<!-- ====================== OBJETIVOS ====================== -->

# 🎯 **OBJETIVO DEL PROYECTO**

Desarrollar una herramienta analítica integral que permita:

- Identificar talento subvalorado  
- Analizar eficiencia ofensiva/defensiva  
- Predecir rendimiento por jugador  
- Comprender patrones históricos  
- Mejorar decisiones deportivas y financieras  

---

<!-- ====================== DATOS Y MÉTODOS ====================== -->

# 🧪 **DATOS Y METODOLOGÍA**

## 📚 **Origen de los datos**

Los datos fueron obtenidos desde **Kaggle** e incluyen:

| Archivo | Contenido |
|--------|-----------|
| 📄 `all_seasons.csv` | Estadísticas históricas por jugador |
| 🧍‍♂️ `player.csv` | Datos físicos y biográficos |
| 🏀 `game.csv` | Partidos y resultados |
| 📊 `line_score.csv` | Estadísticas por encuentro |
| 🏆 `team.csv` | Rendimiento agregado por equipo |

---

## 🧹 **Limpieza y Transformación de Datos**

Incluyó:

- Normalización de valores  
- Unificación de temporadas y equipos  
- Imputación por mediana  
- Eliminación de duplicados  
- Estandarización Z-Score  
- Creación de métricas nuevas:
  - global_score  
  - net_rating_score  
  - vara  
  - rmo  

---

## 📊 **Análisis Estadístico**

Se aplicaron:

- Estadística descriptiva  
- Correlaciones  
- Identificación de outliers  
- Tendencias históricas  
- Clustering  
- Regresión lineal  

---

<!-- ========================================================= -->
# 🔎 **ANÁLISIS EXPLORATORIO DE DATOS (EDA)**
<!-- ========================================================= -->

El EDA permitió explorar tendencias históricas, variaciones por temporada y patrones de rendimiento global en la NBA.  
Las visualizaciones fueron desarrolladas en Python y posteriormente integradas al dashboard interactivo.

---

# 🏀 **Contexto Histórico de la Liga**

<p align="center">
  <img src="../Images/informe/image_2.png" width="85%">
</p>

### 📌 *Hallazgos clave*
- Caídas notables en temporadas *lockout*: **1998–99** y **2011–12**.  
- Disminución severa en **2020–21** debido a COVID-19.  
- Anomalía en **2012**, atribuida al dataset original.  
- Periodo estable entre 2000 y 2010.

---

# 📅 **Eventos que explican la variación por temporada**

| Año | 🛈 Evento | ⚙️ Causa | 📉 Efecto |
|-----|-----------|---------|-----------|
| 1998–99 | Lockout | Disputa laboral | Solo 50 juegos |
| 2011–12 | Lockout | Negociaciones laborales | 66 juegos |
| 2012 | Anomalía | Error de dataset | Registro irreal |
| 2019–21 | COVID-19 | Crisis sanitaria | Calendario reducido |

---

# 🧍‍♂️ **Evolución del número de jugadores por temporada**

<p align="center">
  <img src="../Images/informe/image_3.png" width="85%">
</p>

### 📌 *Interpretación*
- Fuerte crecimiento desde 2010.  
- Aumento brusco entre 2017-2019.  
- Variabilidad histórica por falta de registros en años iniciales.  
- Más jugadores → mayor dispersión estadística.

---

# 📊 **Distribución general del rendimiento por jugador**

<p align="center">
  <img src="../Images/informe/image_4.png" width="85%">
</p>

### 📌 *Hallazgos relevantes*
- **Puntos**: mayoría en rango bajo (≈5 PTS).  
- **Asistencias**: concentración entre 0–3.  
- **Rebotes**: pico cerca de 2.  

➡️ Confirma **alta especialización por rol** en la NBA moderna.

---

# 🏅 **Top 10 jugadores por eficiencia (Net Rating)**

<p align="center">
  <img src="../Images/informe/image_5.png" width="85%">
</p>

### 📌 *Insights*
- **Ahmad Caver** encabeza la lista.  
- Varios jugadores no son figuras mediáticas.  
- El Net Rating captura impacto real más allá de la fama.

---

# 📈 **Tendencia histórica de eficiencia promedio**

<p align="center">
  <img src="../Images/informe/image_6.png" width="85%">
</p>

### 📌 *Interpretación*
- Caída en **2021–22**, efecto post-pandemia.  
- Recuperación inmediata en 2022–23.  
- Promedio ligeramente negativo → normal por naturaleza relativa del Net Rating.

---

# 🧩 **Correlación entre métricas clave**

<p align="center">
  <img src="../Images/informe/image_7.png" width="85%">
</p>

### 📌 *Conclusiones de correlaciones*
- **Pts ↔ Ast (0.66)**: relación sólida → roles polivalentes.  
- **Pts ↔ Reb (0.62)**: jugadores completos ofensivamente.  
- **Ast ↔ Reb (0.25)**: especialización fuerte por posición.  
- **Net Rating** tiene baja correlación → depende de múltiples factores.

---

# 🏀 **Conclusiones preliminares del EDA**

- La NBA muestra **estabilidad competitiva** a través del tiempo.  
- Existen **tendencias claras de evolución ofensiva** desde 2010.  
- Factores externos (lockouts, pandemia) tienen impacto real en los datos.  
- Roles más eficientes se distribuyen de forma desigual por temporada.  
- Se observa **talento subvalorado** en métricas avanzadas.

---

<!-- ========================================================= -->
# 🧩 **INDICADORES PERSONALIZADOS DE RENDIMIENTO**
<!-- ========================================================= -->

Esta sección presenta métricas avanzadas creadas para evaluar rendimiento individual y colectivo en la NBA:

- **VARA (P10)** → Filtro de desempeño mínimo  
- **RMO (P75)** → Rendimiento Más Óptimo  
- **Global Score** → Indicador estandarizado  
- **Top 10 Élites** → Jugadores excepcionales según datos  

Cada métrica aporta una capa de análisis clave para scouting, renovación y estrategias deportivas.

---

# 📦 **Distribución del Global Score por Temporada**

<p align="center">
  <img src="../Images/informe/image_8.png" width="85%">
</p>

### 📌 *Insights clave*
- Mediana estable → equilibrio competitivo.  
- Altura similar en cajas → dispersión uniforme.  
- Outliers en todos los años → jugadores excepcionales o bajo desempeño extremo.  
- Es una métrica muy útil para comparar temporadas completas.

---

# 🎚️ **Vara (Percentil 10) por Equipo**

La **VARA** representa el valor mínimo que el 10% de los jugadores de un equipo no logra superar.  
Es un indicador de **profundidad del roster**.

<p align="center">
  <img src="../Images/informe/image_9.png" width="85%">
</p>

### 📌 *Interpretación estratégica*
- Tendencias ascendentes → equipos con banca sólida.  
- Variaciones bruscas → lesiones, reconstrucciones o relocalizaciones.  
- SAS, BOS, MIA → estabilidad histórica.  
- SEA, VAN, NOK → discontinuidad por cambios de franquicia.

---

# 🧮 **RMO — Rendimiento Más Óptimo (Percentil 75)**

El **RMO** define el *umbral de excelencia* en cuatro métricas principales:

| Métrica | Umbral RMO (P75) | 🔍 Significado |
|--------|------------------|----------------|
| **Puntos** | 11.5 | Anotadores top |
| **Asistencias** | 2.4 | Generadores clave |
| **Rebotes** | 4.7 | Interiores dominantes |
| **Net Rating** | 3.2 | Impacto positivo real |

➡️ Un jugador es considerado **élite** si supera estos criterios.

---

# 🧩 **Clasificación de Jugadores según su RMO**

Se establecieron tres categorías:

### 🟢 **1. Alto rendimiento**
Cumplen:  
✔️ Puntos > RMO  
✔️ Eficiencia > RMO  

### 🟡 **2. Rendimiento aceptable**
Cumplen:  
✔️ Net Rating ≥ 85% del RMO  

### 🔴 **3. Bajo rendimiento**
No cumplen los criterios anteriores.

---

## 📊 **Resumen global por categoría**

| Categoría | Jugadores | % del total |
|-----------|-----------|--------------|
| 🔴 Bajo rendimiento | **9,478** | **72%** |
| 🟡 Aceptable | **2,325** | **18%** |
| 🟢 Alto rendimiento | **1,194** | **10%** |

👉 Solo **1 de cada 10 jugadores** es realmente élite estadística.

---

# 📈 **Distribución de Eficiencia vs. Umbral RMO**

<p align="center">
  <img src="../Images/informe/image_10.png" width="85%">
</p>

### 📌 Conclusiones
- La mayoría de jugadores se concentra cerca de **Net Rating = 0**.  
- Valores positivos altos son muy escasos → verdadera élite.  
- El umbral **RMO = 3.20** es una frontera clara de excelencia.

---

# 🏆 **Top 10 Jugadores con Rendimiento Superior al RMO**

<p align="center">
  <img src="../Images/informe/image_11.png" width="85%">
</p>

### 📌 Observaciones clave
- **RJ Hunter** lidera el ranking.  
- Solo **Draymond Green** es figura mediática.  
- Otros jugadores tienen carreras cortas pero métricas potentes.  
- Indica **talento oculto** en jugadores fuera del spotlight.

---

## 📘 **Revisión de Trayectorias**

| Jugador | ¿Famoso? | Nota |
|--------|-----------|-------|
| Draymond Green | ⭐ Sí | Campeón, All-Star, referente defensivo |
| RJ Hunter | ❌ No | Ritmo alto, carrera corta |
| Mac McClung | ⚡ No | Figura G-League, campeón de mates |
| Ndudi Ebi | ❌ No | Carrera internacional extensa |
| Randy Livingston | ❌ No | Rol marginal |
| Delonte West | 🟡 Parcial | Conocido por temas externos |
| Kidd-Gilchrist | 🟡 Parcial | 2ª selección del Draft |
| Andre Ingram | ❌ No | Leyenda de la G-League |
| Elijah Bryant | ❌ No | Campeón con Bucks (1 juego) |
| Kevin Martin | ⭐ Parcial | 17.4 PPG en carrera |

### 🎯 *Conclusión general*:
La eficiencia avanzada no necesariamente coincide con la popularidad.  
➡️ Oportunidad excelente para **scouting basado en datos**.

---

<!-- ========================================================= -->
# 🧠 **Conclusiones estratégicas del Bloque 3**
<!-- ========================================================= -->

- El **RMO** define claramente a la élite de la liga.  
- La **VARA** permite medir profundidad real del equipo.  
- El **Global Score** estandariza rendimientos entre décadas.  
- La lista élite revela **talento oculto** fuera del radar mediático.  
- Las métricas avanzadas dan ventaja competitiva en scouting.  

---

<!-- ========================================================= -->
# 🤖 **MODELO PREDICTIVO — Rendimiento Global**
<!-- ========================================================= -->

El objetivo fue predecir el **global_score** (desempeño estandarizado) utilizando estadísticas físicas y avanzadas.  
El modelo elegido: **Regresión Lineal Múltiple**, validado con métricas estándar.

---

## 🧮 **Resultados del Modelo**

| Métrica | Valor |
|--------|--------|
| 🔢 **MAE** | **0.1456** |
| 📈 **R²** | **0.8613** |

### 📌 *Interpretación*
- **Error promedio (MAE)** de solo **0.15** → excelente precisión.  
- **R² = 0.8613** → el modelo explica el **86%** del rendimiento.  
- Robustez adecuada para comparaciones y predicciones generales.

---

# 📊 **Importancia de Variables**

<p align="center">
  <img src="../Images/informe/image_12.png" width="85%">
</p>

La importancia relativa revela qué factores influyen más en el rendimiento.

---

## 🔝 **TOP 4 variables más influyentes**

| Variable | Importancia | Interpretación |
|---------|-------------|----------------|
| ⭐ **ts_pct_score** | 36.15% | Calidad del tiro |
| 🔥 **usg_pct_score** | 26.42% | Volumen de uso ofensivo |
| 🧱 **dreb_pct_score** | 15.86% | Rebote defensivo |
| 🎯 **ast_pct_score** | 12.64% | Capacidad de generar juego |

### 📌 Insight fundamental:
**La eficiencia y el uso ofensivo pesan 20 veces más que la edad, estatura y peso juntos.**  
➡️ Hoy la NBA es *estrategia*, no tanto *biología*.

---

# 🧬 **CLUSTERING K-MEANS — Segmentación de Jugadores**
El clustering permite clasificar jugadores según su estilo, impacto y estadística avanzada.

<p align="center">
  <img src="../Images/informe/image_13.png" width="85%">
</p>

Se evaluaron múltiples configuraciones y **K=4** produjo la mejor separación de perfiles.

---

## 🗂️ **Descripción general de los clústeres**

| Clúster | Perfil Estratégico | Descripción |
|---------|--------------------|-------------|
| 🔵 **0** | Rol Secundario | Bajo impacto, poco uso |
| 🔴 **1** | Anotador de Volumen | Alto puntaje, uso ofensivo alto |
| 🟢 **2** | Interior Defensivo | Altura/peso altos, rebote fuerte |
| 🟣 **3** | Playmaker | Más asistencias, impacto creativo |

---

## 📋 **Tabla Completa por Clúster**

| Cluster | Edad | Altura | Peso | Partidos | Puntos | Rebotes | Asistencias | Net Rating | Global Score | Vara |
|--------|------|--------|------|----------|--------|----------|--------------|-------------|---------------|------|
| 🔵 **0** | 27.32 | 199.41 | 97.74 | 46.79 | 5.73 | 2.27 | 1.16 | -4.25 | -0.40 | -0.54 |
| 🔴 **1** | 26.84 | 206.76 | 108.80 | 57.84 | 12.80 | 5.70 | 1.73 | -0.94 | 0.41 | -0.51 |
| 🟢 **2** | 27.09 | 208.52 | 111.00 | 51.00 | 5.49 | 4.70 | 0.72 | -1.41 | 0.05 | -0.51 |
| 🟣 **3** | 27.35 | 190.60 | 88.24 | 56.99 | 10.96 | 2.70 | 3.90 | -0.74 | 0.22 | -0.51 |

---

# 🔍 **Interpretación Estratégica de los Clústeres**

---

## 🔵 **Clúster 0 — Roles secundarios / fondo de plantilla**
- Métricas bajas en todo.  
- Net Rating muy negativo.  
- Frecuentes en equipos en reconstrucción.  

➡️ *Estrategia:* Desarrollo, minutos limitados o reemplazo.

---

## 🔴 **Clúster 1 — Anotadores de volumen**
- Puntos y uso ofensivo altos.  
- Eficiencia no tan elevada.  
- Requieren sistemas que maximicen spacing.  

➡️ *Estrategia:* Ideal para equipos que necesitan anotación primaria.

---

## 🟢 **Clúster 2 — Interiores defensivos**
- Altura/peso superiores al promedio.  
- Rebores defensivos y ofensivos altos.  
- Bajo scoring pero alto impacto táctico.  

➡️ *Estrategia:* Clave para equipos que priorizan defensa y rebote.

---

## 🟣 **Clúster 3 — Playmakers**
- Más asistencias.  
- Perfil bajo en puntaje, alto en creación.  
- Importantes para sistemas basados en pase.  

➡️ *Estrategia:* Complemento perfecto para anotadores del Clúster 1.

---

# 📌 **Variable Dominante en cada Clúster**

| Clúster | Métrica dominante | Significado |
|---------|--------------------|-------------|
| 🔵 0 | net_rating_score | Eficiencia baja general |
| 🔴 1 | usg_pct_score | Carga ofensiva |
| 🟢 2 | oreb_pct_score | Fortaleza interior |
| 🟣 3 | ast_pct_score | Generación de juego |

---

# 🧠 **Conclusiones Estratégicas del Clustering**

- La NBA tiene **perfiles consistentes** a través del tiempo.  
- Identificar el clúster ayuda a definir rol ideal del jugador.  
- Clúster 1 + Clúster 3 → combinaciones ofensivas óptimas.  
- Clúster 2 → pieza clave defensiva.  
- Clúster 0 → jugadores prescindibles o de desarrollo.  
- El clustering es una herramienta poderosa para *scouting*.

---

<!-- ========================================================= -->
# 📊 **DASHBOARD INTERACTIVO – Análisis Visual NBA**
<!-- ========================================================= -->

El dashboard fue diseñado para ofrecer una experiencia interactiva y amigable, permitiendo analizar:

- Tendencias históricas  
- Eficiencia por jugador  
- RMO (Rendimiento Más Óptimo)  
- Clústeres de jugadores  
- Comparaciones entre temporadas  

<p align="center">
  <img src="../Images/informe/image_14.png" width="85%">
</p>

---

# 🗂️ **Estructura del Dashboard**

---

## 1️⃣ **Página Principal – Vista General**

Incluye las métricas clave:

- Jugadores por temporada  
- Distribución de puntos, rebotes y asistencias  
- Evolución de equipos  
- Indicadores rápidos  

👉 *Ideal para análisis inicial.*

---

## 2️⃣ **Net Rating – Eficiencia Global**

<p align="center">
  <img src="../Images/informe/image_15.png" width="85%">
</p>

Contiene:

- Top 10 de eficiencia  
- Tendencias del Net Rating  
- Distribución general  

📌 **Insight:**  
La eficiencia muestra alta variabilidad anual, afectada por cambios en estilo de juego y eventos históricos.

---

## 3️⃣ **RMO – Rendimiento Más Óptimo**

<p align="center">
  <img src="../Images/informe/image_16.png" width="85%">
</p>

El dashboard calcula:

- Percentil 75 (umbral élite)  
- Jugadores que superan el RMO  
- Clasificación automática (alto, aceptable, bajo)  

📌 **Insight:**  
Solo **1 de cada 10 jugadores** alcanza rendimiento élite.

---

## 4️⃣ **Clustering – Segmentación de Estilos de Juego**

<p align="center">
  <img src="../Images/informe/image_17.png" width="85%">
</p>

Incluye:

- Visualización 2D de grupos  
- Explicación de perfiles  
- Métricas agregadas por clúster  
- Cambios a lo largo del tiempo  

📌 **Insight:**  
Los cuatro perfiles identificados son estables y altamente útiles para *scouting*.

---

<!-- ========================================================= -->
# ⚠️ **LIMITACIONES DEL ANÁLISIS**
<!-- ========================================================= -->

A pesar del rigor, el análisis presenta algunas restricciones:

---

### 🧩 **1. Dataset incompleto**
- Falta información completa para todas las temporadas.  
- Algunas estadísticas avanzadas solo existen para años recientes.

---

### 🏥 **2. No incluye variables de contexto**
- Lesiones  
- Minutos jugados  
- Rol real en el equipo  
- Entrenadores  
- Estilo de ofensiva/defensa  

---

### 🎯 **3. Net Rating no es completamente individual**
Depende del contexto del equipo → alineaciones, rivales, ritmo de juego.

---

### 🧪 **4. Modelo predictivo sin factores tácticos**
Una regresión lineal no captura interacciones complejas entre variables.

---

<!-- ========================================================= -->
# 🧠 **CONCLUSIONES FINALES**
<!-- ========================================================= -->

---

## ✔️ **1. La eficiencia es la variable más determinante**
El **ts_pct_score** domina la predicción del rendimiento.  
La NBA moderna prioriza la *calidad del tiro*.

---

## ✔️ **2. Existen patrones claros de jugadores**
El clustering detecta perfiles consistentes:

- Anotadores  
- Playmakers  
- Interiores defensivos  
- Roles secundarios  

---

## ✔️ **3. Gran presencia de talento oculto**
Muchos jugadores con rendimiento élite **no son mediáticamente famosos**.  
Esto permite identificar *gemas escondidas*.

---

## ✔️ **4. Modelo predictivo robusto**
Un **R² = 0.8613** confirma su utilidad para análisis de rendimiento.

---

## ✔️ **5. El RMO aporta objetividad**
Permite clasificar jugadores de manera transparente con métricas estadísticas.

---

<!-- ========================================================= -->
# 🧭 **RECOMENDACIONES ESTRATÉGICAS**
<!-- ========================================================= -->

---

## 🏀 **Para entrenadores**
- Priorizar jugadas que aumenten eficiencia (spacing, pick and roll).  
- Optimizar minutos de jugadores con ts_pct_score alto.  

---

## 📊 **Para analistas**
- Incorporar datos adicionales: lesiones, ritmo de juego, salarios.  
- Probar modelos como XGBoost, Random Forest o Redes Neuronales.  

---

## 🏢 **Para gerentes deportivos**
- Identificar talento oculto (alto RMO con baja popularidad).  
- Armar plantillas balanceadas:  
  Anotador (C1) + Playmaker (C3) + Interior sólido (C2).  

---

<!-- ========================================================= -->
# 🏁 **CIERRE**
<!-- ========================================================= -->

Este proyecto demuestra que un enfoque basado en *analítica avanzada*, *estadística descriptiva*, *modelado predictivo* y *visualización interactiva* permite:

- Descubrir patrones ocultos  
- Elaborar perfiles de jugadores  
- Optimizar decisiones deportivas  
- Mejorar estrategias de scouting  

La NBA es un ecosistema complejo y en constante evolución.  
Con datos, es posible obtener **ventaja competitiva real** en scouting, planificación y toma de decisiones.

---

<p align="center">
  <b>🏀 Data + Estrategia = Decisiones Más Inteligentes</b>
</p>


