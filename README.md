# RAPPORT DE TEST D’INTRUSION

### Mediroza — Projet de fin de stage — Version publique

**SEMAINE 4  |  CYBERSECURITY  |  NETWORKWALKS**

**Rapport formaté :** [PDF](docs/Rapport_Public_Mardochee_BONOU_B084.pdf) | [DOCX modifiable](docs/Rapport_Public_Mardochee_BONOU_B084.docx)

| Champ | Information |
|---|---|
| Pentester | Mardochée BONOU |
| Programme / Batch | B084 — Networkwalks |
| Travaux documentés | 22–25 novembre 2026 |
| Jalons | M1 : accès initial ; M2 : ouverture des PDF ; M3 : analyse de données ; M4 : rapport |
| Client / cible | Hôpital de démonstration — mediroza.example |
| Phases couvertes | Reconnaissance, énumération, validation d’impact, analyse des preuves et rapport |
| Classification | Public — version anonymisée ; données de démonstration |
| Profil GitHub | https://github.com/Mardoch45 |

# 1. Cadre d’autorisation et responsabilité

Les activités présentées concernent un projet pédagogique Networkwalks dont le cahier des charges annonce une autorisation écrite. Le périmètre est limité au domaine cible ; l’ingénierie sociale, le déni de service et les tests hors périmètre sont exclus. Les techniques décrites s’appliquent uniquement à des environnements autorisés.

Cette version de portfolio présente la méthode et les résultats à un niveau anonymisé. Les rapports patients, les noms d’employés et d’actionnaires, les salaires individuels, les identifiants, les mots de passe, les empreintes et les captures originales sont conservés dans le livrable confidentiel. Le domaine .example et le jeu SQL public sont des éléments de démonstration.

# 2. Introduction et résumé exécutif

Ce rapport documente mon projet de fin de stage, réalisé dans le cadre de la semaine 4 de mon parcours Cybersecurity & Ethical Hacking chez Networkwalks. Il prolonge la reconnaissance par la récupération de documents, l’analyse des protections de PDF et l’examen d’une sauvegarde SQL exposée.

Le déroulement suit les quatre jalons : obtenir trois rapports patients, ouvrir les trois PDF, analyser l’exposition des données des employés et des actionnaires, puis rédiger un rapport professionnel avec preuves, impact et recommandations.

L’accès initial par SQLi est confirmé par le stagiaire avec des captures de saisie et de la page des rapports, mais la requête HTTP brute n’est pas conservée. L’ouverture des trois PDF et l’analyse des deux tables du SQL sont vérifiées localement. Le risque global proposé est Élevé pour la confidentialité ; aucune modification de base ni interruption de service n’est démontrée.

| Jalon | Résultat | Statut |
| --- | --- | --- |
| M1 | Trois rapports récupérés via le portail patient | Rapporté par le stagiaire ; captures disponibles |
| M2 | Trois mots de passe retrouvés et contenus lus | Vérifié sur les originaux |
| M3 | 30 employés et 10 actionnaires dans la sauvegarde | Extraction complète et contrôles réalisés |
| M4 | Rapport et dossier de portfolio | Préparés pour relecture |

# 3. Périmètre et méthodologie

Participant : Mardochée BONOU, Batch B084. Le sujet fourni porte la référence B083, tandis que mon identité de participant est B084, confirmée pour ce rapport. La durée prévue dans le sujet est de cinq jours ; les preuves disponibles documentent des travaux du 22 au 25 novembre 2026.

La méthode comprend WHOIS, résolution DNS, identification web, énumération de chemins, analyse du portail, récupération des PDF, essais de mots de passe hors ligne, lecture des métadonnées puis analyse locale du SQL. Les parties d’analyse et de préparation des documents ont été réalisées avec une assistance technique ; les sources et les limites sont distinguées des interprétations.

Les contrôles portent sur les trois PDF et sur tous les enregistrements des deux tables du fichier fourni. Les preuves réseau ont été réalisées par le stagiaire ; elles n’ont pas été rejouées pour préparer ce document. Une adresse IP d’hébergement, un port ouvert ou un nom de technologie ne constitue pas à lui seul une vulnérabilité.

# 4. Outils utilisés

| Outil | Rôle |
| --- | --- |
| Kali Linux | Environnement de travail utilisé dans la VM du stagiaire |
| WHOIS, nslookup et DNSRecon | Reconnaissance des informations de domaine et des enregistrements DNS |
| WhatWeb, Gobuster et Nmap | Identification web, énumération des chemins et repérage des services |
| Client FTP | Compréhension du service et d’une tentative d’authentification refusée |
| pdf2john et John the Ripper | Extraction des données de vérification et essais de mots de passe locaux |
| ExifTool et Poppler | Ouverture, lecture du texte et examen des métadonnées originales |
| curl | Conservation de la réponse HTTP et du contenu de la sauvegarde |
| Python et SQLite | Extraction structurée, agrégations, rapprochements et contrôles d’intégrité |

# 5. Activités réalisées et résultats

## 5.1 Reconnaissance et énumération

```text
whois mediroza.example
nslookup mediroza.example
whatweb mediroza.example
dnsrecon -d mediroza.example
```

Les commandes ci-dessus illustrent la démarche avec un domaine réservé. Les adresses réelles, les journaux DNS et les captures d’infrastructure sont retirés de la version publique. Les outils de reconnaissance ont servi à cartographier le contexte, pas à attribuer une vulnérabilité à chaque service découvert.

La tentative FTP anonyme a été refusée. Le code 331 demandait la poursuite de l’authentification ; le code 530 indiquait le refus. Aucun accès FTP réussi n’est revendiqué. Les résultats DNS et les variations de réponses HTTP restent des observations dont la cause n’est pas extrapolée.

## 5.2 M1 — Accès initial aux rapports

Le stagiaire rapporte avoir utilisé une valeur d’injection dans le champ Username du portail patient et obtenu les liens des trois rapports. La capture de saisie et celle de la page des rapports sont disponibles dans le dossier confidentiel. La route exacte, les paramètres complets et la réponse HTTP après soumission ne sont pas archivés.

Dans une requête vulnérable construite par concaténation, une apostrophe peut terminer une chaîne et un commentaire SQL peut neutraliser une condition placée ensuite. Ce mécanisme explique l’hypothèse de contournement ; il ne représente pas du code serveur récupéré. Un accès administratif complet, une écriture dans la base et une compromission du système ne sont pas démontrés.

## 5.3 M2 — Ouverture des PDF

Les trois documents utilisent le gestionnaire PDF Standard, révision 3, avec RC4 et une clé de 128 bits. Les mots de passe ont été retrouvés par dictionnaire, puis chaque original a été réellement ouvert et son texte extrait. Le test démontre la faiblesse des mots de passe utilisés, et non une récupération directe de la clé indépendante du secret.

Les mots de passe et leurs empreintes ne sont pas publiés. La méthode consiste à extraire les données de vérification de chaque PDF, sélectionner un dictionnaire pertinent, lancer les essais hors ligne puis vérifier l’ouverture réelle. Les protections du portail ne limitent pas des essais effectués sur un fichier déjà téléchargé.

## 5.4 Métadonnées et piste vers la sauvegarde

Les métadonnées utiles étaient chiffrées avec le document. Sans mot de passe, ExifTool signalait que le PDF était protégé. Après ouverture, un commentaire opérationnel indiquait un répertoire historique de sauvegarde. Les copies réexportées permettent de lire le rapport, mais perdent ces champs ; les originaux restent la référence pour leur analyse.

## 5.5 M3 — Récupération et analyse du SQL

Le fichier contient les tables staff et shareholders. CREATE TABLE décrit les colonnes ; INSERT INTO indique l’ordre des valeurs. L’analyse importe uniquement ces blocs dans SQLite local, sans exécuter les commandes MySQL SET, DROP ou LOCK et sans se connecter à la base du serveur.

Dans staff, monthly_salary_zar désigne le salaire mensuel en rands sud-africains. Dans shareholders, share_percent et shares_held indiquent le pourcentage de participation et le nombre de parts. COUNT, SUM et JOIN permettent de vérifier les effectifs, les totaux et les correspondances entre les tables.

| Résultat de l’audit | Présentation publique |
| --- | --- |
| 30 employés et 10 actionnaires | Effectifs publiés sans identité individuelle |
| Salaires et participations | Valeurs réelles conservées dans le rapport confidentiel |
| Contrôles de cohérence | Totaux, nombres de lignes et correspondances vérifiés |
| Jeu SQL du dépôt | 30 employés et 10 actionnaires entièrement fictifs |

Un refus de liste du répertoire n’établit pas que ses fichiers sont protégés. L’énumération a reçu 403 sur le répertoire historique, tandis que la récupération directe du fichier a renvoyé 200. La vulnérabilité est l’exposition HTTP d’une sauvegarde interne ; son contenu sert à démontrer l’impact.

## 5.6 Cohérence et limites des données

L’en-tête du dump annonce le 27 août 2019, mais trois dates d’embauche lui sont postérieures. Cette incohérence empêche d’attribuer une période fiable aux montants. Le champ HTTP Last-Modified ne date pas les salaires. Le rapport décrit les enregistrements du fichier, sans garantir leur actualité ni l’effectif actuel de l’hôpital.

# 6. Analyse des risques et impact

| ID | Constat | Preuve / observation | Impact | Niveau |
| --- | --- | --- | --- | --- |
| F-01 | SQLi du portail rapportée | Valeur confirmée et captures ; requête brute absente | Accès rapporté aux documents médicaux | Élevé, provisoire |
| F-02 | Mots de passe PDF prévisibles | Trois ouvertures vérifiées après essais locaux | Lecture de documents confidentiels | Élevé |
| F-03 | Informations internes dans les métadonnées | Commentaire opérationnel lu sur un original | Orientation vers une sauvegarde | Faible |
| F-04 | Sauvegarde SQL exposée | Réponse 200 et contenu identique ; session absente selon le test du stagiaire | Divulgation de données personnelles et financières | Élevé |

Les niveaux sont qualitatifs. Ils évaluent l’impact démontré sur la confidentialité et les conditions d’accès disponibles dans les preuves. Aucun score CVSS ni privilège supplémentaire n’est inventé. L’absence de contrôle d’accès au fichier est distincte d’une simple exposition d’en-têtes, d’adresses publiques ou de ports attendus.

## 6.1 Contrôles et observations à interpréter avec prudence

La redirection vers HTTPS et le refus d’authentification FTP anonyme sont des contrôles observés. Ils ne compensent pas la divulgation de la sauvegarde ou la faiblesse des mots de passe des PDF. Une réponse 403 de répertoire, une absence de réponse DNSSEC ou une identification de technologie ne sont pas automatiquement des vulnérabilités exploitables.

# 7. Recommandations

| Priorité | Action | Validation attendue |
| --- | --- | --- |
| 1 | Retirer les sauvegardes des répertoires servis par le site et restreindre leur stockage | L’URL du fichier ne délivre plus le SQL sans autorisation |
| 1 | Paramétrer les requêtes d’authentification et contrôler l’accès à chaque rapport | La tentative d’injection est refusée et les documents d’autres comptes sont inaccessibles |
| 2 | Remplacer les secrets prévisibles par des secrets longs, aléatoires et propres à chaque PDF | Les anciens secrets ne fonctionnent plus sur les documents réémis |
| 2 | Supprimer les commentaires opérationnels et chemins internes des métadonnées distribuées | Les nouveaux originaux ne divulguent plus la piste de sauvegarde |
| 2 | Examiner les journaux et rechercher les autres sauvegardes déployées | L’étendue de l’exposition et les copies similaires sont vérifiées |
| 3 | Vérifier la provenance et la période de validité des données | Les dates, versions et responsabilités sont documentées |

# 8. Conclusion et bilan personnel

Le projet relie la reconnaissance à l’analyse d’impact : des documents récupérés peuvent révéler une piste dans leurs métadonnées, puis une sauvegarde accessible peut exposer des données structurées sans accès à la base du serveur. Les résultats M2 et M3 sont vérifiés ; la preuve HTTP de M1 reste à renforcer si une capture complète est disponible.

## 8.1 Compétences travaillées

J’ai travaillé sur la distinction entre la connexion à un service et une authentification réussie. Une réponse FTP 331 ne suffit pas à prouver qu’un compte est valide ou qu’une session est ouverte.

J’ai approfondi la récupération de mots de passe de PDF : l’extraction des données de vérification, le choix du dictionnaire et la vérification de l’ouverture réelle sont trois étapes distinctes.

J’ai appris à examiner les métadonnées des documents originaux avec leur mot de passe. Une copie réexportée peut conserver le contenu visible tout en perdant les commentaires internes utiles à l’analyse.

J’ai étudié la lecture d’une sauvegarde SQL en faisant correspondre les colonnes aux valeurs, puis en utilisant SELECT, COUNT, SUM et JOIN pour produire des tableaux et vérifier les résultats.

Ce projet m’a amené à distinguer une observation de reconnaissance d’une vulnérabilité démontrée, à conserver les preuves et à préparer une version de portfolio adaptée à une publication publique.

Le rapport suit la structure du modèle Pentesting-Report-Sample : cadre d’autorisation, introduction, périmètre, outils, activités, risques, recommandations, conclusion et preuves. Le résumé exécutif et les annexes de données répondent en complément aux exigences du sujet de la semaine 4.

# 9. Preuves collectées

Les captures originales et annexes confidentielles sont exclues de ce document. L’illustration suivante explique la chaîne de travail sans montrer de dossier patient, d’identité individuelle, de secret ou d’adresse réelle.

![Schéma pédagogique de la démarche ; aucune capture de la cible réelle.](<docs/illustrations/demarche.png>)

Schéma pédagogique de la démarche ; aucune capture de la cible réelle.

## 9.1 Reproduire l’analyse avec des données fictives

```text
python3 scripts/analyser_demo.py --source data/demo.sql --output outputs
python3 -m unittest discover -s tests -v
```

Le dépôt contient un export SQL entièrement fictif, le script d’analyse et des tests fonctionnels. Les résultats produits à partir de ce jeu sont des résultats de démonstration ; ils ne correspondent pas aux montants et identités du rapport confidentiel.

# Informations sur l’auteur et le projet

| Champ | Information |
| --- | --- |
| Auteur | Mardochée BONOU |
| Programme | Networkwalks Cybersecurity Internship — Semaine 4 — Batch B084 |
| Profil GitHub | https://github.com/Mardoch45 |
| Projet | Mediroza — analyse de preuves et rapport de pentest |
| Dépôt GitHub | https://github.com/Mardoch45/INTERSHIP-FINAL-REPORT |

## Utiliser le dépôt

Le rapport suit la structure du modèle personnel de la semaine 2, adaptée aux jalons M1–M4 de la semaine 4. Les documents publiables sont dans `docs/`.

```text
github_mediroza/
├── README.md
├── AUTEUR.md
├── PUBLICATION.md
├── docs/                  # Rapport public en PDF, DOCX et Markdown
├── data/demo.sql          # Export entièrement fictif
├── scripts/analyser_demo.py
└── tests/test_analyse.py
```

Depuis la racine du dépôt, avec Python 3 :

```bash
python3 scripts/analyser_demo.py --source data/demo.sql --output outputs
python3 -m unittest discover -s tests -v
```

Le script produit deux CSV et une synthèse JSON dans `outputs/`. Il utilise uniquement la bibliothèque standard Python et une base SQLite en mémoire. Les CSV utilisent UTF-8 et le séparateur point-virgule. Les valeurs du jeu de démonstration sont inventées et diffèrent des données confidentielles.

Les tests vérifient l'extraction complète, les totaux, la conservation du fichier source et l'interprétation des apostrophes SQL, y compris un point-virgule dans une chaîne.

Voir [PUBLICATION.md](PUBLICATION.md) pour envoyer cette copie locale vers le dépôt GitHub indiqué : [Mardoch45/INTERSHIP-FINAL-REPORT](https://github.com/Mardoch45/INTERSHIP-FINAL-REPORT).
