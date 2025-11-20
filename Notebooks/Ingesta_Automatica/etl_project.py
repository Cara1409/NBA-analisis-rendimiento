import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
# ============================================
# CONFIGURACIÓN DE KAGGLE API
# Configurar credenciales de Kaggle desde variables de entorno
kaggle_username = os.getenv('KAGGLE_USERNAME')
kaggle_key = os.getenv('KAGGLE_KEY')

# Establecer las variables de entorno explícitamente
os.environ['KAGGLE_USERNAME'] = kaggle_username
os.environ['KAGGLE_KEY'] = kaggle_key

print("✅ Credenciales cargadas correctamente desde .env")
print(f"   Usuario: {kaggle_username}\n")

# Ahora sí importar kaggle (después de configurar las variables)
from kaggle.api.kaggle_api_extended import KaggleApi

# Autenticar la API
api = KaggleApi()
api.authenticate()
print("✅ Autenticación exitosa con Kaggle API\n")

# ============================================
# DIRECTORIOS DE DESCARGA
# ============================================
basketball_dir = Path("data/basketball")
nba_players_dir = Path("data/nba_players")
smart_decisions_nba_dir = Path("data/smart_decisions_nba")

basketball_dir.mkdir(parents=True, exist_ok=True)
nba_players_dir.mkdir(parents=True, exist_ok=True)
smart_decisions_nba_dir.mkdir(parents=True, exist_ok=True)

print("📥 Iniciando descarga de datasets de Kaggle...\n")

# ============================================
# DATASET 1: Basketball Database
# ============================================
print("1️⃣ Descargando: Basketball Database (wyattowalsh/basketball)")
print("-" * 60)

try:
    api.dataset_download_files(
        'wyattowalsh/basketball',
        path=str(basketball_dir),
        unzip=True
    )
    print(f"✅ Descargado exitosamente en: {basketball_dir}\n")
except Exception as e:
    print(f"❌ Error al descargar: {e}\n")
# ============================================
# ============================================
# DATASET 2: NBA Players Data
# ============================================
print("2️⃣ Descargando: NBA Players Data (justinas/nba-players-data)")
print("-" * 60)

try:
    api.dataset_download_files(
        'justinas/nba-players-data',
        path=str(nba_players_dir),
        unzip=True
    )
    print(f"✅ Descargado exitosamente en: {nba_players_dir}\n")
except Exception as e:
    print(f"❌ Error al descargar: {e}\n")
    
# ===========================================
# ETL TABLAS PROYECTO NBA  
# ===========================================
df_player = pd.read_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\basketball\csv\player.csv")
df_player = df_player.rename(columns={
    "full_name": "player_name",
    "id": "player_id"
}) 
df_player.to_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\smart_decisions_nba\player_cleaned.csv", index=False) 
# ===========================================
df_game = pd.read_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\basketball\csv\game.csv")
df_game["game_date"] = pd.to_datetime(df_game["game_date"], errors="coerce")
# Definir la fecha límite (1 de octubre de 1996)
fecha_corte = pd.to_datetime("1996-10-01")

# Filtrar solo partidos desde esa fecha en adelante
df_game = df_game[df_game["game_date"] >= fecha_corte]
df_game.isnull().sum().sort_values(ascending=False) ## Verificación final de valores nulos en cada columna tras la limpieza 

## Imputar con la mediana en columnas numéricas específicas
df_game['ft_pct_home'].fillna(df_game['ft_pct_home'].median(), inplace=True)
df_game['ft_pct_away'].fillna(df_game['ft_pct_away'].median(), inplace=True)
df_game['fg3_pct_home'].fillna(df_game['fg3_pct_home'].median(), inplace=True)

## Imputar con el valor más frecuente en columnas categóricas específicas
df_game['wl_home'].fillna(df_game['wl_home'].mode()[0], inplace=True)
df_game['wl_away'].fillna(df_game['wl_away'].mode()[0], inplace=True)

df_game = df_game.drop_duplicates(subset=["game_id","team_id_home","team_id_away"], keep="first")

# Paso 1: columnas comunes
cols_comunes = ['season_id', 'game_id', 'game_date', 'season_type']

# Paso 2: columnas específicas por equipo
cols_home = [col for col in df_game.columns if '_home' in col]
cols_away = [col for col in df_game.columns if '_away' in col]

# Paso 3: renombrar columnas para unificar
df_home = df_game[cols_comunes + cols_home].copy()
df_away = df_game[cols_comunes + cols_away].copy()

df_home.columns = cols_comunes + [col.replace('_home', '') for col in cols_home]
df_away.columns = cols_comunes + [col.replace('_away', '') for col in cols_away]

# Paso 4: agregar columna de rol (local/visitante)
df_home['team_side'] = 'home'
df_away['team_side'] = 'away'

# Paso 5: unir ambos DataFrames
df_game_cleaned = pd.concat([df_home, df_away], ignore_index=True)

df_game_cleaned.to_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\smart_decisions_nba\game_cleaned.csv", index=False) 
# ===========================================
df_team = pd.read_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\basketball\csv\team.csv")

df_team = df_team.rename(columns={
    'id': 'team_id',
    'full_name': 'team_name',
    'abbreviation': 'team_abbreviation'
})

df_team.to_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\smart_decisions_nba\team_cleaned.csv", index=False)
# ===========================================
df_line_score = pd.read_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\basketball\csv\line_score.csv")

# Convertir la columna a datetime
df_line_score["game_date_est"] = pd.to_datetime(df_line_score["game_date_est"], errors="coerce")
df_line_score= df_line_score.rename(columns={
    'game_date_est':'game_date'})

# Definir la fecha límite (1 de octubre de 1996)
fecha_corte = pd.to_datetime("1996-10-01")

# Filtrar solo partidos desde esa fecha en adelante
df_line_score = df_line_score[df_line_score["game_date"] >= fecha_corte]

# Imputar valores nulos en columnas numéricas.
ot_cols = [col for col in df_line_score.columns if "pts_ot" in col]
df_line_score[ot_cols] = df_line_score[ot_cols].fillna(0)

# Eliminar duplicados
df_line_score = df_line_score.drop_duplicates(subset=["game_id","team_id_home","team_id_away"], keep="first")

# Crear tabla para equipos locales
home_cols = [
    "game_date","game_id","team_id_home","team_abbreviation_home",
    "team_city_name_home","team_nickname_home","team_wins_losses_home",
    "pts_qtr1_home","pts_qtr2_home","pts_qtr3_home","pts_qtr4_home",
    "pts_ot1_home","pts_ot2_home","pts_ot3_home","pts_ot4_home",
    "pts_ot5_home","pts_ot6_home","pts_ot7_home","pts_ot8_home",
    "pts_ot9_home","pts_ot10_home","pts_home"
]

df_home_line_score = df_line_score[home_cols].copy()
df_home_line_score = df_home_line_score.rename(columns=lambda x: x.replace("_home",""))
df_home_line_score["local_visitante"] = "home"
print(df_home_line_score.head())

# Crear tabla para equipos visitantes
away_cols = [
    "game_date","game_id","team_id_away","team_abbreviation_away",
    "team_city_name_away","team_nickname_away","team_wins_losses_away",
    "pts_qtr1_away","pts_qtr2_away","pts_qtr3_away","pts_qtr4_away",
    "pts_ot1_away","pts_ot2_away","pts_ot3_away","pts_ot4_away",
    "pts_ot5_away","pts_ot6_away","pts_ot7_away","pts_ot8_away",
    "pts_ot9_away","pts_ot10_away","pts_away"
]

df_away_line_score = df_line_score[away_cols].copy()
df_away_line_score = df_away_line_score.rename(columns=lambda x: x.replace("_away",""))
df_away_line_score["local_visitante"] = "away"
print(df_away_line_score.head())

# Unir ambas tablas
df_line_score_cleaned = pd.concat([df_home_line_score, df_away_line_score], ignore_index=True)

df_line_score_cleaned.to_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\smart_decisions_nba\line_score_cleaned.csv", index=False) 
# ===========================================   
df_all_seasons = pd.read_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\nba_players\all_seasons.csv")

df_all_seasons = df_all_seasons.drop(columns=["Unnamed: 0"])

df_all_seasons["college"] = df_all_seasons["college"].fillna("No College")

# Paso 1: limpiar y estandarizar abreviaciones
df_all_seasons["team_abbreviation"] = (
    df_all_seasons["team_abbreviation"]
    .str.strip()
    .str.upper()
)

# Paso 2: diccionario de correcciones históricas
correcciones = {
    "VAN": "MEM",  # Vancouver → Memphis
    "CHH": "CHA",  # Hornets antiguos → actuales
    "SEA": "OKC",  # Seattle → Oklahoma
    "NJN": "BKN",  # New Jersey → Brooklyn
    "NOH": "NOP",  # New Orleans Hornets → Pelicans
    "NOK": "NOP",  # Transición → Pelicans
    "CHO": "CHA"   # Estandarizar a abreviación oficial
}

# Paso 3: aplicar correcciones
df_all_seasons["team_abbreviation"] = df_all_seasons["team_abbreviation"].replace(correcciones)

# Paso 4: eliminar columnas anteriores si existen
df_all_seasons = df_all_seasons.drop(columns=["team_id", "team_name"], errors="ignore")

# Paso 5: hacer el merge con df_teams
df_all_seasons = pd.merge(
    df_all_seasons,
    df_team[["team_id", "team_name", "team_abbreviation"]],
    on="team_abbreviation",
    how="left"
)
df_all_seasons.to_csv(r"C:\Users\laram\OneDrive\Escritorio\DATA ANALYTICS HENRY\nba_project\data\smart_decisions_nba\all_seasons_cleaned.csv", index=False) 
