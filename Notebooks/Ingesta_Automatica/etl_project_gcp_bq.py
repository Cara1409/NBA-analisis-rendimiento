import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from google.cloud import storage, bigquery
from google.cloud.exceptions import NotFound
from io import BytesIO

# ============================================
# CONFIGURACIÓN DE GOOGLE CLOUD
# ============================================
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
DATASET_ID = 'nba_analytics'

# Inicializar clientes
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
bq_client = bigquery.Client(project=PROJECT_ID)

print("✅ Clientes de Google Cloud Storage y BigQuery inicializados\n")

# ============================================
# FUNCIONES DE CARGA
# ============================================
def upload_to_gcs(dataframe, blob_name):
    """Sube un DataFrame a Google Cloud Storage como CSV"""
    try:
        blob = bucket.blob(blob_name)
        csv_buffer = BytesIO()
        dataframe.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        blob.upload_from_file(csv_buffer, content_type='text/csv')
        print(f"✅ GCS: gs://{BUCKET_NAME}/{blob_name}")
        return True
    except Exception as e:
        print(f"❌ Error al subir a GCS {blob_name}: {e}")
        return False

def create_dataset_if_not_exists():
    """Crea el dataset de BigQuery si no existe"""
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    try:
        bq_client.get_dataset(dataset_ref)
        print(f"✅ Dataset '{DATASET_ID}' ya existe en BigQuery\n")
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        dataset.description = "Dataset para análisis de datos de la NBA (1996-2024)"
        dataset = bq_client.create_dataset(dataset, timeout=30)
        print(f"✅ Dataset '{DATASET_ID}' creado en BigQuery\n")

def convert_float_columns_to_int(df, int_columns):
    """Convierte columnas float a int, manejando NaN"""
    for col in int_columns:
        if col in df.columns:
            # Convertir NaN a 0 o dejarlo como está, luego convertir a int
            df[col] = df[col].fillna(0).astype('Int64')  # Int64 permite NaN
    return df

def load_to_bigquery(dataframe, table_name, schema):
    """Carga un DataFrame directamente a BigQuery"""
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    
    try:
        # Limpiar DataFrame antes de cargar
        df_clean = dataframe.copy()
        
        # Identificar columnas INT64 del esquema
        int_columns = [field.name for field in schema if field.field_type == "INTEGER"]
        
        # Convertir columnas float a int
        df_clean = convert_float_columns_to_int(df_clean, int_columns)
        
        # Configurar opciones de carga - usar autodetect para mejor compatibilidad
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,  # Cambiar a True para detectar tipos automáticamente
            allow_quoted_newlines=True,
            allow_jagged_rows=False
        )
        
        # Convertir DataFrame a CSV en memoria
        csv_buffer = BytesIO()
        df_clean.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        # Cargar a BigQuery
        job = bq_client.load_table_from_file(
            csv_buffer,
            table_id,
            job_config=job_config
        )
        job.result()  # Esperar a que termine
        
        table = bq_client.get_table(table_id)
        print(f"✅ BigQuery: {table_id} ({table.num_rows:,} filas)")
        return True
    except Exception as e:
        print(f"❌ Error al cargar a BigQuery {table_name}: {e}")
        return False

# ============================================
# ESQUEMAS DE BIGQUERY
# ============================================
schema_player = [
    bigquery.SchemaField("player_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("player_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("is_active", "BOOLEAN", mode="NULLABLE"),
]

schema_team = [
    bigquery.SchemaField("team_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("team_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("team_abbreviation", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("nickname", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("city", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("state", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("year_founded", "INTEGER", mode="NULLABLE"),
]

schema_game = [
    bigquery.SchemaField("season_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("game_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("game_date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("season_type", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("team_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("team_side", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("matchup", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("wl", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("min", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("fgm", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("fga", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("fg_pct", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("fg3m", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("fg3a", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("fg3_pct", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("ftm", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("fta", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("ft_pct", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("oreb", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("dreb", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("reb", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("ast", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("stl", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("blk", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("tov", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pf", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("plus_minus", "INTEGER", mode="NULLABLE"),
]

schema_line_score = [
    bigquery.SchemaField("game_date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("game_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("team_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("team_abbreviation", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("team_city_name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("team_nickname", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("team_wins_losses", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("pts_qtr1", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_qtr2", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_qtr3", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_qtr4", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot1", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot2", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot3", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot4", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot5", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot6", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot7", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot8", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot9", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts_ot10", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("pts", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("local_visitante", "STRING", mode="REQUIRED"),
]

schema_all_seasons = [
    bigquery.SchemaField("player_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("team_abbreviation", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("player_height", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("player_weight", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("college", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("country", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("draft_year", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("draft_round", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("draft_number", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("gp", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("pts", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("reb", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("ast", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("net_rating", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("oreb_pct", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("dreb_pct", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("usg_pct", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("ts_pct", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("ast_pct", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("season", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("team_id", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("team_name", "STRING", mode="NULLABLE"),
]

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
# DIRECTORIOS DE DESCARGA
# ============================================
basketball_dir = Path("data/basketball")
nba_players_dir = Path("data/nba_players")

basketball_dir.mkdir(parents=True, exist_ok=True)
nba_players_dir.mkdir(parents=True, exist_ok=True)

print("📥 Iniciando descarga de datasets de Kaggle...\n")

# ============================================
# DESCARGAR DATASETS
# ============================================
print("1️⃣ Descargando: Basketball Database")
print("-" * 60)
try:
    api.dataset_download_files('wyattowalsh/basketball', path=str(basketball_dir), unzip=True)
    print(f"✅ Descargado exitosamente\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

print("2️⃣ Descargando: NBA Players Data")
print("-" * 60)
try:
    api.dataset_download_files('justinas/nba-players-data', path=str(nba_players_dir), unzip=True)
    print(f"✅ Descargado exitosamente\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# ============================================
# CREAR DATASET DE BIGQUERY
# ============================================
print("="*60)
print("🏀 CREANDO BASE DE DATOS EN BIGQUERY")
print("="*60 + "\n")
create_dataset_if_not_exists()

print("="*60)
print("🔄 INICIANDO PROCESO ETL")
print("="*60 + "\n")

# ===========================================
# ETL 1: PLAYER
# ===========================================
print("📊 Procesando: PLAYERS")
print("-" * 60)
df_player = pd.read_csv(basketball_dir / "csv" / "player.csv")
df_player = df_player.rename(columns={"full_name": "player_name", "id": "player_id"})

upload_to_gcs(df_player, "nba_data/cleaned/player_cleaned.csv")
load_to_bigquery(df_player, "players", schema_player)
print()

# ===========================================
# ETL 2: TEAM
# ===========================================
print("📊 Procesando: TEAMS")
print("-" * 60)
df_team = pd.read_csv(basketball_dir / "csv" / "team.csv")
df_team = df_team.rename(columns={
    'id': 'team_id',
    'full_name': 'team_name',
    'abbreviation': 'team_abbreviation'
})

# Convertir year_founded a entero
if 'year_founded' in df_team.columns:
    df_team['year_founded'] = df_team['year_founded'].fillna(0).astype(int)

upload_to_gcs(df_team, "nba_data/cleaned/team_cleaned.csv")
load_to_bigquery(df_team, "teams", schema_team)
print()

# ===========================================
# ETL 3: GAME
# ===========================================
print("📊 Procesando: GAMES")
print("-" * 60)
df_game = pd.read_csv(basketball_dir / "csv" / "game.csv")
df_game["game_date"] = pd.to_datetime(df_game["game_date"], errors="coerce")

fecha_corte = pd.to_datetime("1996-10-01")
df_game = df_game[df_game["game_date"] >= fecha_corte]

# Imputación - usar loc para evitar warnings
df_game.loc[:, 'ft_pct_home'] = df_game['ft_pct_home'].fillna(df_game['ft_pct_home'].median())
df_game.loc[:, 'ft_pct_away'] = df_game['ft_pct_away'].fillna(df_game['ft_pct_away'].median())
df_game.loc[:, 'fg3_pct_home'] = df_game['fg3_pct_home'].fillna(df_game['fg3_pct_home'].median())
df_game.loc[:, 'wl_home'] = df_game['wl_home'].fillna(df_game['wl_home'].mode()[0])
df_game.loc[:, 'wl_away'] = df_game['wl_away'].fillna(df_game['wl_away'].mode()[0])

df_game = df_game.drop_duplicates(subset=["game_id","team_id_home","team_id_away"], keep="first")

# Transformación
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

# Convertir columnas numéricas a int donde sea necesario
int_cols = ['min', 'fgm', 'fga', 'fg3m', 'fg3a', 'ftm', 'fta', 'oreb', 'dreb', 'reb', 
            'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'plus_minus']
for col in int_cols:
    if col in df_game_cleaned.columns:
        df_game_cleaned[col] = df_game_cleaned[col].fillna(0).astype(int)

upload_to_gcs(df_game_cleaned, "nba_data/cleaned/game_cleaned.csv")
load_to_bigquery(df_game_cleaned, "games", schema_game)
print()

# ===========================================
# ETL 4: LINE SCORE
# ===========================================
print("📊 Procesando: LINE_SCORE")
print("-" * 60)
df_line_score = pd.read_csv(basketball_dir / "csv" / "line_score.csv")
df_line_score["game_date_est"] = pd.to_datetime(df_line_score["game_date_est"], errors="coerce")
df_line_score = df_line_score.rename(columns={'game_date_est':'game_date'})
df_line_score = df_line_score[df_line_score["game_date"] >= fecha_corte]

ot_cols = [col for col in df_line_score.columns if "pts_ot" in col]
df_line_score[ot_cols] = df_line_score[ot_cols].fillna(0)
df_line_score = df_line_score.drop_duplicates(subset=["game_id","team_id_home","team_id_away"], keep="first")

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

# Convertir columnas de puntos a enteros
pts_cols = ['pts_qtr1', 'pts_qtr2', 'pts_qtr3', 'pts_qtr4',
            'pts_ot1', 'pts_ot2', 'pts_ot3', 'pts_ot4', 'pts_ot5',
            'pts_ot6', 'pts_ot7', 'pts_ot8', 'pts_ot9', 'pts_ot10', 'pts']
for col in pts_cols:
    if col in df_line_score_cleaned.columns:
        df_line_score_cleaned[col] = df_line_score_cleaned[col].fillna(0).astype(int)

# Convertir team_id a entero
if 'team_id' in df_line_score_cleaned.columns:
    df_line_score_cleaned['team_id'] = df_line_score_cleaned['team_id'].fillna(0).astype(int)

upload_to_gcs(df_line_score_cleaned, "nba_data/cleaned/line_score_cleaned.csv")
load_to_bigquery(df_line_score_cleaned, "line_score", schema_line_score)
print()

# ===========================================
# ETL 5: ALL SEASONS
# ===========================================
print("📊 Procesando: ALL_SEASONS")
print("-" * 60)
df_all_seasons = pd.read_csv(nba_players_dir / "all_seasons.csv")
df_all_seasons = df_all_seasons.drop(columns=["Unnamed: 0"])
df_all_seasons["college"] = df_all_seasons["college"].fillna("No College")

df_all_seasons["team_abbreviation"] = df_all_seasons["team_abbreviation"].str.strip().str.upper()

correcciones = {
    "VAN": "MEM", "CHH": "CHA", "SEA": "OKC",
    "NJN": "BKN", "NOH": "NOP", "NOK": "NOP", "CHO": "CHA"
}

df_all_seasons["team_abbreviation"] = df_all_seasons["team_abbreviation"].replace(correcciones)
df_all_seasons = df_all_seasons.drop(columns=["team_id", "team_name"], errors="ignore")

df_all_seasons = pd.merge(
    df_all_seasons,
    df_team[["team_id", "team_name", "team_abbreviation"]],
    on="team_abbreviation",
    how="left"
)

upload_to_gcs(df_all_seasons, "nba_data/cleaned/all_seasons_cleaned.csv")
load_to_bigquery(df_all_seasons, "all_seasons", schema_all_seasons)
print()

print("="*60)
print("✅ PROCESO ETL COMPLETADO")
print("="*60)
print(f"\n📦 Cloud Storage: gs://{BUCKET_NAME}/nba_data/cleaned/")
print(f"📊 BigQuery: {PROJECT_ID}.{DATASET_ID}")
print("\n💡 Tablas disponibles:")
print("   - players")
print("   - teams")
print("   - games")
print("   - line_score")
print("   - all_seasons")