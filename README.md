# Dashboard KPI : Excel vers Grafana

Ce projet est une solution clé en main pour transformer un fichier de planification Excel en tableau de bord interactif sur Grafana. Tout l'environnement (ETL, Base de données, Visualisation) est conteneurisé avec Docker pour une installation facile.

**Stack Technique :**
* **Node-RED** : Pour lire l'Excel et injecter les données (ETL).
* **MariaDB** : Pour le stockage des données.
* **Grafana** : Pour la visualisation (KPIs).
* **Docker** : Pour l'orchestration.

---

## 1. Prérequis

Avant de commencer, vous devez avoir installé :
* **Docker Desktop** : [Télécharger ici](https://www.docker.com/products/docker-desktop/).
    * *Installez-le et assurez-vous qu'il est lancé (l'icône de la baleine doit être stable).*

---

## 2. Installation (Premier démarrage)

1.  **Récupérez le projet** (Ouvrez un terminal ou PowerShell et collez) :
    ```bash
    git clone [https://github.com/Brrunn/Pipeline_Excel_Grafana.git](https://github.com/Brrunn/Pipeline_Excel_Grafana.git)
    cd Pipeline_Excel_Grafana
    ```

2.  **Lancez l'application** :
    ```bash
    docker-compose up -d
    ```
    *Attendez quelques minutes que les conteneurs se téléchargent et démarrent.*

---

## 3. Configuration Initiale (À faire une seule fois)

Ces étapes sont nécessaires uniquement lors de la toute première installation sur votre machine.

### A. Configurer Node-RED (Le moteur)
1.  Ouvrez votre navigateur sur [http://localhost:1880](http://localhost:1880).
2.  Cliquez sur le **Menu (≡)** en haut à droite > **Import**.
3.  Cliquez sur **Select a file to import** et choisissez le fichier `flow_nodered.json` (qui se trouve dans le dossier du projet que vous avez téléchargé).
4.  Cliquez sur **Import**.
5.  Si une fenêtre vous demande d'installer des modules manquants, validez.
6.  Cliquez sur le bouton rouge **Deploy** en haut à droite.

### B. Connecter Grafana
1.  Ouvrez [http://localhost:3000](http://localhost:3000).
2.  Identifiants par défaut : **User** `admin` / **Password** `admin` (passez l'étape de changement de mot de passe en cliquant sur "Skip").
3.  Allez dans le menu de gauche **Connections** (ou Configuration) > **Data Sources** > **Add data source**.
4.  Sélectionnez **MySQL**.
5.  Remplissez les informations suivantes (C'est précis !) :
    * **Host :** `mariadb:3306`  *( Ne mettez pas localhost !)*
    * **Database :** `kpi_db`
    * **User :** `kpi_user`
    * **Password :** `kpi_password`
6.  Cliquez sur **Save & Test**. Un message vert doit confirmer la connexion.

---

## 4. Utilisation au quotidien

Pour mettre à jour les données du tableau de bord :

1.  Prenez votre fichier Excel de planification.
2.  **Renommez-le** impérativement : `planif.xlsx`.
3.  Déposez ce fichier dans le dossier **`input_excel`** (situé dans le dossier du projet).
4.  Allez sur Node-RED ([http://localhost:1880](http://localhost:1880)).
5.  Cliquez sur le petit bouton carré à gauche du nœud bleu **"Horodatage"**.
    * *Cela déclenche la lecture du fichier, vide l'ancienne base et insère les nouvelles données.*
6.  Allez sur Grafana ([http://localhost:3000](http://localhost:3000)) pour voir vos KPI à jour.

---



