# Proyecto Final [NBA-analisis-rendimiento]

![Mi Banner](/Images/Image_banner.png)

# 🏀 Decisiones Inteligentes en la NBA: Análisis de Talento y Rendimiento


## 📌 Descripción del proyecto
Este proyecto forma parte del **Proyecto Final del Bootcamp de Data Analytics**.  
El objetivo es aplicar un flujo completo de análisis de datos para ayudar a la **NBA** a comprender y mejorar el rendimiento de sus equipos, utilizando herramientas de ingeniería, análisis y visualización de datos.

La iniciativa busca **identificar los factores que influyen en el rendimiento de los equipos**, detectar **jugadores con bajo desempeño** y **predecir tendencias futuras**, integrando datos históricos desde múltiples fuentes.

---

## 🎯 Objetivos del proyecto
- Analizar el rendimiento histórico de jugadores y equipos de la NBA.
- Identificar patrones de desempeño y factores que afectan la eficiencia colectiva.
- Construir un **modelo predictivo** del rendimiento mínimo óptimo (RMO).
- Desarrollar un **pipeline ETL automatizado** y un **modelo de datos en SQL Server**.
- Crear un **dashboard interactivo en Power BI** para visualizar resultados y KPIs clave.


---

## 🧠 Contexto del caso de negocio
La **NBA** enfrenta dificultades para mantener un rendimiento consistente entre sus equipos.  
La falta de una herramienta unificada que consolide métricas de rendimiento impide detectar con precisión qué jugadores o estrategias afectan el resultado final.

Mediante este proyecto, se desarrollará una **solución analítica integral** que consolide datos, calcule indicadores clave (eficiencia ofensiva, rebotes, asistencias, etc.) y aplique modelos predictivos para respaldar decisiones de rotación, renovación o reestructuración de equipos.

---

## 🧩 Fuentes de datos

**1. Dataset principal – Basketball (Wyatt Walsh)**  
📍 [Kaggle: wyattowalsh/basketball](https://www.kaggle.com/datasets/wyattowalsh/basketball)  
Contiene información de:
- 30 equipos y más de 65.000 juegos.
- Estadísticas de más del 95% de los partidos de la historia de la NBA.
- Datos de jugadores, equipos, partidos, y acciones play-by-play.

**2. Dataset complementario – NBA Players Data (Justinas)**  
📍 [Kaggle: justinas/nba-players-data](https://www.kaggle.com/datasets/justinas/nba-players-data)  
Incluye información demográfica y estadísticas por temporada del desempeño físico de jugadores.

---

## 📁 Estructura del Repositorio

La siguiente estructura organiza el proyecto “Decisiones Inteligentes en la NBA”, facilitando la automatización del proceso ETL, la trazabilidad de los datos y la colaboración entre los integrantes del equipo.

nba_project/
│
├── data/
│   ├── raw/                   # Datos originales descargados desde Kaggle
│   └── clean/                 # Datos procesados y limpios listos para análisis y carga a SQL Server
│
├── notebooks/
│   ├── ETL/.ipynb             # Limpieza y normalización de los archivos .csv seleccionados
│   ├── EDA/.ipynb             # Análisis exploratorio de datos (EDA), visualizaciones y validaciones
│
├── dashboard/
│   ├── canva                  # Presentación del sprint 1
│   └── powerbi_reporte.pbix   # Dashboard interactivo con visualizaciones e indicadores clave
│
├── images/
│   ├── banner.png            # Imagen para presentación.
│   ├── logo.png              # Imagen del logo de la herramienta
│   └── architecture.png      # Diagrama del pipeline ETL (Kaggle → Python → GCP → SQL → Power BI)
│
├── docs/
│   ├── propuesta.pdf         # Documento con la propuesta del proyecto
│   ├── dataset.doc           # Documento que describe las tablas
│   └── lineamientos          # Documento que describe cómo replicar el proceso/trabajo realizado
│
│
└── README.md                 # Descripción general del proyecto, equipo y guía de ejecución

## ⚙️ Tecnologías utilizadas

| Área | Tecnologías |
|------|--------------|
| 🐍 **Lenguaje principal** | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40"/> **Python 3.11** |
| 📊 **Librerías de análisis** | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" width="40"/> <img src="https://matplotlib.org/stable/_static/logo_light.svg" width="40"/> <img src="https://seaborn.pydata.org/_images/logo-tall-lightbg.svg" width="40"/> |
| 🤖 **Modelado ML** | <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" width="60"/> 
| 🗄️ **Base de datos** | <img src="https://www.svgrepo.com/show/303229/microsoft-sql-server-logo.svg" width="45"/> **SQL Server** |
| 🔄 **ETL / Conexión** | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jupyter/jupyter-original.svg" width="45"/> <img src="https://www.svgrepo.com/show/303229/microsoft-sql-server-logo.svg" width="45"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/googlecloud/googlecloud-original.svg" width="45"/> |
| 📈 **Visualización** | <img src="https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg" width="50"/> **Power BI Desktop** |
| 🧩 **Control de versiones** | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="40"/> |
| 🗂️ **Gestión del proyecto** | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/trello/trello-plain.svg" width="40"/> **Trello** |


---

## 👥 Equipo de trabajo
Equipo DAFT18 – Grupo 1

| Integrante | Rol |
|-------------|------|
| Felipe Carassale | Data Analyst |
| Lucy Melo | Data Analyst |
| Melisa Rossi | Data Analyst |
| Esteban Mamani | Data Analyst |
| Camila Pineda | Data Analyst |

