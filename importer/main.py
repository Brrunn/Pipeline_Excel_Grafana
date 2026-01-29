import os
import time
import pandas as pd
from sqlalchemy import create_engine, text

# Configuration
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'kpi_mariadb')
DB_NAME = os.getenv('MYSQL_DATABASE')
DATA_FOLDER = '/data'

# Liste des fichiers attendus et leur mapping vers le nom de table final
# Format : "NomDuFichierCSV.csv": "NomDeLaTableSQL"
FILES_MAPPING = {
    "ShopActivityRecent.csv": "ShopActivityRecent",
    "ShopActivityHistorical.csv": "ShopActivityHistorical",
    "Reference_WorkCenter.csv": "Reference_WorkCenter",
    "Reference_Employee.csv": "Reference_Employee",
    "Reference_DIPlan.csv": "Reference_DIPlan",
    "Reference_Department.csv": "Reference_Department",
    "OrderOperation.csv": "OrderOperation",
    "OrderHeader.csv": "OrderHeader",
    "DIActivity.csv": "DIActivity"
}

def wait_for_db():
    """Attend que MariaDB soit prête"""
    connection_str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(connection_str)
    
    retries = 30
    while retries > 0:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Connexion à MariaDB réussie !")
            return engine
        except Exception as e:
            print(f"⏳ Attente de MariaDB... ({retries} essais restants)")
            time.sleep(2)
            retries -= 1
    raise Exception("Impossible de se connecter à MariaDB")

def import_csvs(engine):
    for csv_file, table_name in FILES_MAPPING.items():
        file_path = os.path.join(DATA_FOLDER, csv_file)
        
        if not os.path.exists(file_path):
            print(f"⚠️ Fichier ignoré (introuvable) : {csv_file}")
            continue

        print(f"🚀 Traitement de {csv_file} -> Table: {table_name}...")
        
        try:
            # Chunksize est CRUCIAL pour les gros fichiers de +150Mo (ShopActivityRecent)
            # Cela évite de saturer la RAM en envoyant par paquets de 10 000 lignes
            chunk_size = 10000 
            
            # On lit le CSV. 
            # sep=',' assume que tes CSV sont séparés par des virgules.
            # Si c'est des points-virgules, change par sep=';'
            # encoding='utf-8' ou 'latin1' selon ton export SQL Server
            iterator = pd.read_csv(file_path, chunksize=chunk_size, encoding='utf-8', low_memory=False)
            
            first_chunk = True
            for chunk in iterator:
                # Mode 'replace' pour le premier morceau (recrée la table), 'append' pour les suivants
                mode = 'replace' if first_chunk else 'append'
                
                chunk.to_sql(
                    name=table_name,
                    con=engine,
                    if_exists=mode,
                    index=False
                )
                first_chunk = False
                print(f"   ... paquet importé.")
                
            print(f"✅ {table_name} importée avec succès.")

        except Exception as e:
            print(f"❌ Erreur sur {csv_file} : {e}")

if __name__ == "__main__":
    print("--- Démarrage de l'ETL Python ---")
    engine = wait_for_db()
    import_csvs(engine)
    print("--- Importation terminée. Mise en veille. ---")