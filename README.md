## 🏗 Architecture

| Service | Rôle | Accès |
| :--- | :--- | :--- |
| **MariaDB** | Base de données SQL (Stockage) | `localhost:3306` |
| **Importer (Python)** | Script automatique qui lit les CSV et remplit la BDD | *Interne uniquement* |
| **Grafana** | Outils de création de Dashboards et KPIs | `http://localhost:3000` |
| **Node-RED** | (Optionnel) Flux d'automatisation | `http://localhost:1880` |

---

## 🚀 Installation & Démarrage (5 min)

### 1. Pré-requis

- Avoir **Docker Desktop** installé et lancé sur votre machine.
- Avoir **Git** installé.

### 2. Récupérer le projet

Clonez ce dépôt sur votre ordinateur (ouvrir un terminal VsCode) :

```bash
git clone <https://github.com/Brrunn/Pipeline_Excel_Grafana>
cd Pipeline_Safran
```

### 3. Préparer les données

Déposez vos fichiers CSV sources dans le dossier /input_csv situé à la racine.

**⚠️ IMPORTANT** : Les fichiers doivent être nommés exactement comme ci-dessous pour être reconnus par le script d'importation :
- ShopActivityRecent.csv
- ShopActivityHistorical.csv
- Reference_WorkCenter.csv
- Reference_Employee.csv
- Reference_DIPlan.csv
- Reference_Department.csv
- OrderOperation.csv
- OrderHeader.csv
- DIActivity.csv

### 4. Lancer le pipeline

Ouvrez un terminal dans le dossier du projet et lancez :

```bash
docker-compose up --build -d
```

**Ce qui va se passer :** 
- MariaDB démarre.
- Le script Python attend que la BDD soit prête, puis charge vos CSV un par un (cela peut prendre quelques minutes selon la taille des fichiers).
- Une fois terminé, les données sont persistantes (même si vous éteignez Docker).


## Comment explorer les données (SQL)

Pour vérifier les données, faire des requêtes SQL complexes ou voir le schéma, nous recommandons l'outil gratuit **DBeaver** (ou l'extension "Database Client" sur VS Code).

**Paramètres de connexion (depuis votre ordinateur) :**

| Paramètre | Valeur |
| :--- | :--- |
| **Type de BDD** | MariaDB / MySQL |
| **Server Host** | `localhost` |
| **Port** | `3306` |
| **Database** | `kpi_db` |
| **Username** | `kpi_user` |
| **Password** | `kpi_password` |

---

## Comment visualiser les KPIs (Grafana)

Ouvrez votre navigateur sur : [http://localhost:3000](http://localhost:3000)

**Identifiants par défaut :**
* **User :** `admin`
* **Password :** `admin` (changez-le lors de la première connexion ou pas dailleurs, plus facile à retenir)

### Connecter la base de données à Grafana
Lors de la première utilisation, vous devez dire à Grafana où chercher les données :

1. Allez dans **Connections** (menu gauche) -> **Data Sources** -> **Add new data source**.
2. Sélectionnez **MySQL** (MariaDB est compatible MySQL).
3. Configurez **EXACTEMENT** comme ceci (Attention au Host !) :

| Champ | Valeur | Note importante |
| :--- | :--- | :--- |
| **Host** | `mariadb:3306` | ⚠️ Ne mettez pas "localhost", car on est dans le réseau Docker ! |
| **Database** | `kpi_db` | |
| **User** | `kpi_user` | |
| **Password** | `kpi_password` | |

4. Cliquez sur **Save & Test**. Vous devriez voir un message vert "Database Connection OK".
5. Vous pouvez maintenant créer des Dashboards !

---
