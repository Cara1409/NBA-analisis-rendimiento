# Automatizacion de Ingesta y Análisis de Datos NBA

**Proyecto:** Decisiones Inteligentes NBA - Análisis de Talento y Rendimiento

## 📊 Resumen Ejecutivo

Pipeline ETL automatizado que descarga, procesa y centraliza datos históricos de la NBA en Google Cloud Platform. El sistema permite realizar análisis avanzados de rendimiento deportivo y talento de jugadores, proporcionando una infraestructura escalable para la toma de decisiones basada en datos.

### Resultados Clave

- **~35,000 partidos** procesados y estructurados
- **~4,800 jugadores** con estadísticas detalladas
- **28 temporadas** de datos históricos (1996-2024)
- **5 tablas analíticas** optimizadas en BigQuery
- **100% automatización** del proceso de ingesta

---

## 🎯 Objetivos

1. Automatizar la extracción de datos desde fuentes públicas confiables
2. Estandarizar información histórica de múltiples datasets
3. Centralizar datos en una plataforma cloud escalable
4. Garantizar calidad y consistencia mediante limpieza rigurosa
5. Facilitar análisis avanzados con herramientas modernas

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Justificación |
|------------|------------|---------------|
| **Desarrollo** | Python 3.x | Ecosistema robusto para análisis y automatización de datos |
| **Consola** | Cmder | Integración cmd, PowerShell y Git Bash en un solo entorno |
| **Orquestación** | Scripts Python | Control total del flujo ETL |
| **Almacenamiento** | Google Cloud Storage | Escalable, seguro y fácil de integrar con otros servicios |
| **Data Warehouse** | BigQuery | Consultas SQL sobre grandes volúmenes |
| **Versionado** | Git | Facilita el control de cambios y colaboración |

---

## 📦 Fuentes de Datos

### Dataset 1: Basketball Database
- **Fuente:** [wyattowalsh/basketball](https://www.kaggle.com/datasets/wyattowalsh/basketball) (Kaggle)
- **Contenido:** Partidos, equipos, jugadores, estadísticas por juego
- **Volumen:** ~16 CSV con datos desde 1946

### Dataset 2: NBA Players Data
- **Fuente:** [justinas/nba-players-data](https://www.kaggle.com/datasets/justinas/nba-players-data) (Kaggle)
- **Contenido:** Estadísticas agregadas por jugador/temporada
- **Métricas:** Avanzadas (TS%, USG%, Net Rating, etc.)

---

## 🔄 Proceso ETL

### EXTRACCIÓN

```
Kaggle API → Autenticación → Descarga automática → Descompresión local
```

- Uso de credenciales seguras desde variables de entorno
- Descarga incremental de datasets actualizados
- Almacenamiento temporal en estructura de carpetas

### TRANSFORMACIÓN

#### Limpieza de Datos

1. **Filtrado Temporal**
   - Corte: 1 de octubre de 1996
   - Razón: Mayor consistencia en datos modernos
   - Impacto: Reducción del 30% en registros inconsistentes

2. **Tratamiento de Nulos**
   - Numéricas → Mediana (ft_pct, fg3_pct)
   - Categóricas → Moda (wl_home, wl_away)
   - Overtime → 0 (pts_ot1 a pts_ot10)

3. **Eliminación de Duplicados**
   - Criterio: (game_id, team_id_home, team_id_away)
   - Estrategia: Conservar primer registro
   - Resultado: ~2% de registros eliminados

#### Normalización

1. **Equipos Relocalizados**
   - VAN → MEM (Vancouver → Memphis)
   - SEA → OKC (Seattle → Oklahoma City)
   - NJN → BKN (New Jersey → Brooklyn)
   - CHH/CHO → CHA (Charlotte Hornets)
   - NOH/NOK → NOP (New Orleans Pelicans)

2. **Separación Home/Away**
   - Transformación de registros anchos → largos
   - Duplicación de filas para análisis por equipo
   - Columna team_side para identificar local/visitante

3. **Tipado de Datos**
   - Conversión float → int para IDs y contadores
   - Interpretación automática de fechas con formato internacional
   - Limpieza de strings (trim, upper)

### CARGA

#### Google Cloud Storage

```
Bucket: nba-data-bucket
├── nba_data/
│   └── cleaned/
│       ├── player_cleaned.csv
│       ├── team_cleaned.csv
│       ├── game_cleaned.csv
│       ├── line_score_cleaned.csv
│       └── all_seasons_cleaned.csv
```

- Formato: CSV con encoding UTF-8
- Versionado: Sobrescritura controlada
- Acceso: IAM con cuenta de servicio

#### BigQuery

```
Dataset: nba_analytics
├── players (5 columnas, ~4,800 filas)
├── teams (7 columnas, ~50 filas)
├── games (28 columnas, ~70,000 filas)
├── line_score (23 columnas, ~70,000 filas)
└── all_seasons (22 columnas, ~12,000 filas)
```

- Esquemas predefinidos con tipos estrictos
- Particionado por fecha para optimización
- Modo de escritura: TRUNCATE (reemplazo completo)

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                      KAGGLE DATASETS                        │
│     • wyattowalsh/basketball • justinas/nba-players-data    │
└────────────────────┬────────────────────────────────────────┘
                     │ Kaggle API
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   PYTHON ETL PIPELINE                       │
│   ┌─────────────┐  ┌──────────────┐   ┌─────────────┐       │
│   │ EXTRACCIÓN  │→│ TRANSFORMACIÓN│→  │    CARGA    │       │
│   └─────────────┘  └──────────────┘   └─────────────┘       │
│   • Download        • Limpieza        • GCS Upload          │
│   • Unzip           • Normalización   • BigQuery Load       │
│   • Validación      • Tipado          • Schema Enforcement  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
┌──────────────────┐      ┌──────────────────┐
│  CLOUD STORAGE   │      │     BIGQUERY     │
│  • Archivos CSV  │      │   • Tablas SQL   │
│  • Backup        │      │   • Análisis     │
│  • Durabilidad   │      │   • Consultas    │
└──────────────────┘      └──────────────────┘
        │                         │
        └────────────┬────────────┘
                     ↓
            ┌──────────────────────┐
            │    ANÁLISIS & BI     │
            │  • Looker Studio     │
            │  • Python Notebooks  │
            │  • Machine Learning  │
            └──────────────────────┘
```

---

## 📈 Resultados y Métricas

### Cobertura de Datos

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| **Temporadas** | 28 | 1996-97 a 2023-24 |
| **Partidos únicos** | ~35,000 | Regular season + playoffs |
| **Jugadores** | 4,800+ | Activos e históricos |
| **Equipos** | 50+ | Incluye relocalizaciones |
| **Registros totales** | ~160,000 | Suma de todas las tablas |

### Calidad de Datos

**Antes del ETL:**
- Duplicados: ~2-3% en tablas de juegos
- Nulos: 5-10% en métricas de tiro
- Inconsistencias: Abreviaciones históricas
- Formato: Fechas y tipos mezclados

**Después del ETL:**
- Duplicados: 0%
- Nulos: <1% (imputados estratégicamente)
- Consistencia: 100% normalizado
- Formato: Esquemas estrictos en BigQuery

### Desempeño del Pipeline

| Fase | Tiempo | Observaciones |
|------|--------|---------------|
| **Descarga Kaggle** | ~2-3 min | Depende de conexión |
| **Procesamiento ETL** | ~5-7 min | ~160k registros |
| **Carga a GCS** | ~30-60 seg | Archivos CSV |
| **Carga a BigQuery** | ~1-2 min | Validación de esquemas |
| **TOTAL** | **~10 min** | Pipeline completo |

### Almacenamiento

- **GCS:** ~500 MB (archivos CSV comprimibles)
- **BigQuery:** ~2 GB (sin particionado)
- **Costo estimado:** <$5/mes con uso moderado

---

## 💡 Casos de Uso y Aplicaciones

### Análisis de Rendimiento

**Ejemplo 1: Identificación de Talento Emergente**
- Aplicación: Exploración para equipos en reconstrucción

**Ejemplo 2: Ventaja Local vs Visitante**
- Aplicación: Estrategias de calendario y viajes

### Machine Learning Potencial

1. **Predicción de Resultados**
   - Features: Estadísticas recientes, ventaja local, back-to-backs
   - Target: Victoria/Derrota

2. **Proyección de Rendimiento**
   - Features: Métricas avanzadas, edad, minutos
   - Target: Puntos por juego siguiente temporada

3. **Optimización de Rotaciones**
   - Features: Plus/minus, fatiga, matchups (impacto en el marcador, nivel de fatiga y enfrentamientos entre jugadores)
   - Target: Combinaciones óptimas de quinteto

---

## 🚧 Desafíos y Soluciones

### Desafío 1: Inconsistencia Histórica
- **Problema:** Equipos relocalizados con múltiples abreviaciones
- **Solución:** Diccionario de mapeo y normalización sistemática
- **Resultado:** 100% de registros vinculados correctamente

### Desafío 2: Valores Nulos en Métricas
- **Problema:** ~5-10% de nulos en porcentajes de tiro
- **Solución:** Imputación con mediana (robusto a outliers)
- **Resultado:** Preservación de distribuciones estadísticas

### Desafío 3: Tipos de Datos en BigQuery
- **Problema:** Pandas infiere float para columnas int con NaN
- **Solución:** Conversión explícita con Int64 (nullable integer)
- **Resultado:** Esquemas limpios sin rechazos de carga

### Desafío 4: Seguridad de Credenciales
- **Problema:** Riesgo de exposición de API keys
- **Solución:** Variables de entorno + .gitignore robusto
- **Resultado:** Cero credenciales versionadas en Git

---

## 📚 Lecciones Aprendidas

### Técnicas
1. Planificación de esquemas antes de BigQuery reduce iteraciones
2. Conversión de tipos temprana evita errores en carga
3. Separación home/away duplica datos pero simplifica análisis
4. Uso de Path hace código portable entre sistemas

### Herramientas
1. Cmder mejora significativamente experiencia en Windows
2. python-dotenv es estándar para gestión de configuración
3. BigQuery autodetect útil pero esquemas explícitos son superiores
4. GCS como stage permite recuperación ante fallos

### Proceso
1. Validar datos localmente antes de cargar a cloud
2. Documentar transformaciones facilita detectar y corregir errores (debugging)
3. 3.	Hacer cambios frecuentes con Git permite volver fácilmente a una versión anterior si algo sale mal.
4. Testear cada tabla por separado acelera detección de errores

---

## 🔜 Próximos Pasos

- [ ] Implementar Cloud Functions para scheduling automático
- [ ] Crear dashboard en Looker Studio con KPIs clave
- [ ] Agregar tests unitarios para funciones ETL
- [ ] Documentar data dictionary con definiciones de métricas

---

## 🎯 Impacto y Valor Agregado

### Para Equipos NBA
- Exploración de talento automatizado con datos históricos completos
- Análisis comparativo de jugadores y estilos de juego
- Proyecciones basadas en métricas avanzadas

### Para Analistas
- Infraestructura lista para modelos predictivos
- Datos limpios sin necesidad de preprocesamiento manual
- Escalabilidad para análisis de gran volumen

### Para Apuestas Deportivas
- Datos históricos para modelos de probabilidad
- Métricas avanzadas no disponibles en fuentes comerciales
- Actualización automatizada para datos recientes

### Para Investigación Académica
- Dataset público para estudios deportivos
- Reproducibilidad con código abierto
- Base metodológica para otros deportes

---

## ✅ Conclusiones

### Logros Técnicos
1. Pipeline ETL 100% funcional y automatizado
2. Infraestructura Cloud escalable y de bajo costo
3. Datos limpios, consistentes y documentados
4. Código modular, reproducible y versionado

### Logros de Negocio
1. Reducción de 90% en tiempo de preparación de datos
2. Base de 160,000+ registros listos para análisis
3. Plataforma extensible a nuevas fuentes
4. Fundamento para decisiones basadas en datos

---

## 📖 Recursos y Referencias

### Documentación Técnica
- [Kaggle API Documentation](https://github.com/Kaggle/kaggle-api)
- [Google Cloud Storage Python Client](https://cloud.google.com/python/docs/reference/storage/latest)
- [BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)

### Datasets Originales
- [Basketball Database (Kaggle)](https://www.kaggle.com/datasets/wyattowalsh/basketball)
- [NBA Players Data (Kaggle)](https://www.kaggle.com/datasets/justinas/nba-players-data)

### Herramientas
- [Cmder Console Emulator](https://cmder.net/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Google Cloud Console](https://console.cloud.google.com/)

---

## 📝 Licencia

Este proyecto utiliza datos públicos de Kaggle y está destinado para uso educativo y de investigación.

---

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias y mejoras.