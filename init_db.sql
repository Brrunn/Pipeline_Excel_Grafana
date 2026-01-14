CREATE TABLE IF NOT EXISTS planif (
    id INT AUTO_INCREMENT PRIMARY KEY,
    takt VARCHAR(50),
    heure_debut VARCHAR(20),
    heure_fin VARCHAR(20),
    interrompu VARCHAR(10),
    poste_8 VARCHAR(50),
    poste_7 VARCHAR(50),
    poste_6 VARCHAR(50),
    poste_5 VARCHAR(50),
    poste_4 VARCHAR(50),
    poste_3 VARCHAR(50),
    poste_2 VARCHAR(50),
    poste_1 VARCHAR(50),
    date_import TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 

