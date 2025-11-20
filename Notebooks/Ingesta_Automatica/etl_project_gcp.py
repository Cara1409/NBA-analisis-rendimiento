import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from google.cloud import storage
from io import BytesIO

# ============================================
# CONFIGURACIÓN DE GOOGLE CLOUD STORAGE
# ============================================
# Configurar credenciales de GCP
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')  # Nombre de tu bucket en GCS

# Inicializar cliente de GCS
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

def upload_to_gcs(dataframe, blob_name):
    """
    Sube un DataFrame a Google Cloud Storage como CSV
    
    Args:
        dataframe: DataFrame de pandas
        blob_name: ruta del archivo en el bucket (ej: 'nba_data/player_cleaned.csv')
    """
    try:
        blob = bucket.blob(blob_name)
        # Convertir DataFrame a CSV en memoria
        csv_buffer = BytesIO()
        dataframe.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        # Subir a GCS
        blob.upload_from_file(csv_buffer, content_type='text/csv')
        print(f"✅ Archivo subido a GCS: gs://{BUCKET_NAME}/{blob_name}")
    except Exception as e:
        print(f"❌ Error al subir {blob_name}: {e}")

print("✅ Cliente de Google Cloud Storage inicializado\n")

# ============================================
# CONFIGURACIÓN DE KAGGLE API
# ============================================
kaggle_username = os.getenv('KAGGLE_USERNAME')
kaggle_key = os.getenv('KAGGLE_KEY')

os.environ['KAGGLE_USERNAME'] = kaggle_username
os.environ['KAGGLE_KEY'] = kaggle_key

print("✅ Credenciales de Kaggle cargadas correctamente desde .env")
print(f"   Usuario: {kaggle_username}\n")

from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()
print("✅ Autenticación exitosa con Kaggle API\n")

# ============================================
# DIRECTORIOS DE DESCARGA LOCALES (temporal)
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

print("="*60)
print("🔄 INICIANDO PROCESO ETL Y CARGA A GCS")
print("="*60 + "\n")

# ===========================================
# ETL 1: PLAYER
# ===========================================
print("📊 Procesando: player.csv")
df_player = pd.read_csv(basketball_dir / "csv" / "player.csv")
df_player = df_player.rename(columns={
    "full_name": "player_name",
    "id": "player_id"
})
upload_to_gcs(df_player, "nba_data/cleaned/player_cleaned.csv")
print()

# ===========================================
# ETL 2: GAME
# ===========================================
print("📊 Procesando: game.csv")
df_game = pd.read_csv(basketball_dir / "csv" / "game.csv")
df_game["game_date"] = pd.to_datetime(df_game["game_date"], errors="coerce")

# Filtrar desde octubre de 1996
fecha_corte = pd.to_datetime("1996-10-01")
df_game = df_game[df_game["game_date"] >= fecha_corte]

# Imputación de valores nulos
df_game['ft_pct_home'].fillna(df_game['ft_pct_home'].median(), inplace=True)
df_game['ft_pct_away'].fillna(df_game['ft_pct_away'].median(), inplace=True)
df_game['fg3_pct_home'].fillna(df_game['fg3_pct_home'].median(), inplace=True)
df_game['wl_home'].fillna(df_game['wl_home'].mode()[0], inplace=True)
df_game['wl_away'].fillna(df_game['wl_away'].mode()[0], inplace=True)

# Eliminar duplicados
df_game = df_game.drop_duplicates(subset=["game_id","team_id_home","team_id_away"], keep="first")

# Transformación: separar home y away
cols_comunes = ['season_id', 'game_id', 'game_date', 'season_type']
cols_home = [col for col in df_game.columns if '_home' in col]
cols_away = [col for col in df_game.columns if '_away' in col]

df_home = df_game[cols_comunes + cols_home].copy()
df_away = df_game[cols_comunes + cols_away].copy()

df_home.columns = cols_comunes + [col.replace('_home', '') for col in cols_home]
df_away.columns = cols_comunes + [col.replace('_away', '') for col in cols_away]

df_home['team_side'] = 'home'
df_away['team_side'] = 'away'

df_game_cleaned = pd.concat([df_home, df_away], ignore_index=True)
upload_to_gcs(df_game_cleaned, "nba_data/cleaned/game_cleaned.csv")
print()

# ===========================================
# ETL 3: TEAM
# ===========================================
print("📊 Procesando: team.csv")
df_team = pd.read_csv(basketball_dir / "csv" / "team.csv")
df_team = df_team.rename(columns={
    'id': 'team_id',
    'full_name': 'team_name',
    'abbreviation': 'team_abbreviation'
})
upload_to_gcs(df_team, "nba_data/cleaned/team_cleaned.csv")
print()

# ===========================================
# ETL 4: LINE SCORE
# ===========================================
print("📊 Procesando: line_score.csv")
df_line_score = pd.read_csv(basketball_dir / "csv" / "line_score.csv")
df_line_score["game_date_est"] = pd.to_datetime(df_line_score["game_date_est"], errors="coerce")
df_line_score = df_line_score.rename(columns={'game_date_est':'game_date'})

# Filtrar desde octubre de 1996
df_line_score = df_line_score[df_line_score["game_date"] >= fecha_corte]

# Imputar valores nulos en overtime
ot_cols = [col for col in df_line_score.columns if "pts_ot" in col]
df_line_score[ot_cols] = df_line_score[ot_cols].fillna(0)

# Eliminar duplicados
df_line_score = df_line_score.drop_duplicates(subset=["game_id","team_id_home","team_id_away"], keep="first")

# Crear tablas separadas para home y away
home_cols = [
    "game_date","game_id","team_id_home","team_abbreviation_home",
    "team_city_name_home","team_nickname_home","team_wins_losses_home",
    "pts_qtr1_home","pts_qtr2_home","pts_qtr3_home","pts_qtr4_home",
    "pts_ot1_home","pts_ot2_home","pts_ot3_home","pts_ot4_home",
    "pts_ot5_home","pts_ot6_home","pts_ot7_home","pts_ot8_home",
    "pts_ot9_home","pts_ot10_home","pts_home"
]

away_cols = [
    "game_date","game_id","team_id_away","team_abbreviation_away",
    "team_city_name_away","team_nickname_away","team_wins_losses_away",
    "pts_qtr1_away","pts_qtr2_away","pts_qtr3_away","pts_qtr4_away",
    "pts_ot1_away","pts_ot2_away","pts_ot3_away","pts_ot4_away",
    "pts_ot5_away","pts_ot6_away","pts_ot7_away","pts_ot8_away",
    "pts_ot9_away","pts_ot10_away","pts_away"
]

df_home_line_score = df_line_score[home_cols].copy()
df_home_line_score = df_home_line_score.rename(columns=lambda x: x.replace("_home",""))
df_home_line_score["local_visitante"] = "home"

df_away_line_score = df_line_score[away_cols].copy()
df_away_line_score = df_away_line_score.rename(columns=lambda x: x.replace("_away",""))
df_away_line_score["local_visitante"] = "away"

df_line_score_cleaned = pd.concat([df_home_line_score, df_away_line_score], ignore_index=True)
upload_to_gcs(df_line_score_cleaned, "nba_data/cleaned/line_score_cleaned.csv")
print()

# ===========================================
# ETL 5: ALL SEASONS
# ===========================================
print("📊 Procesando: all_seasons.csv")
df_all_seasons = pd.read_csv(nba_players_dir / "all_seasons.csv")
df_all_seasons = df_all_seasons.drop(columns=["Unnamed: 0"])
df_all_seasons["college"] = df_all_seasons["college"].fillna("No College")

# Limpiar y estandarizar abreviaciones
df_all_seasons["team_abbreviation"] = (
    df_all_seasons["team_abbreviation"]
    .str.strip()
    .str.upper()
)

# Correcciones históricas
correcciones = {
    "VAN": "MEM",
    "CHH": "CHA",
    "SEA": "OKC",
    "NJN": "BKN",
    "NOH": "NOP",
    "NOK": "NOP",
    "CHO": "CHA"
}

df_all_seasons["team_abbreviation"] = df_all_seasons["team_abbreviation"].replace(correcciones)
df_all_seasons = df_all_seasons.drop(columns=["team_id", "team_name"], errors="ignore")

# Merge con team data
df_all_seasons = pd.merge(
    df_all_seasons,
    df_team[["team_id", "team_name", "team_abbreviation"]],
    on="team_abbreviation",
    how="left"
)
upload_to_gcs(df_all_seasons, "nba_data/cleaned/all_seasons_cleaned.csv")
print()

print("="*60)
print("✅ PROCESO ETL COMPLETADO")
print("="*60)
print(f"\n📦 Todos los archivos fueron cargados a: gs://{BUCKET_NAME}/nba_data/cleaned/")
print("\n💡 Archivos generados:")
print("   - player_cleaned.csv")
print("   - game_cleaned.csv")
print("   - team_cleaned.csv")
print("   - line_score_cleaned.csv")
print("   - all_seasons_cleaned.csv")