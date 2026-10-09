# PythonServer — API REST avec FastAPI et MySQL

**PythonServer** est un serveur backend développé en Python avec FastAPI. Il expose des endpoints REST permettant de gérer les utilisateurs et les avis, tout en stockant les données dans une base de données MySQL.

Le projet met en pratique plusieurs bonnes pratiques de développement backend : séparation des responsabilités, architecture modulaire, gestion des dépendances, ORM SQLAlchemy et utilisation du design pattern Singleton pour centraliser le moteur de connexion à la base de données.

---

## Sommaire

* [1. Présentation du projet](#1-présentation-du-projet)
* [2. Technologies utilisées](#2-technologies-utilisées)
* [3. Architecture du projet](#3-architecture-du-projet)
* [4. Prérequis](#4-prérequis)
* [5. Installation](#5-installation)
* [6. Configuration des variables d'environnement](#6-configuration-des-variables-denvironnement)
* [7. Démarrage de MySQL avec Docker](#7-démarrage-de-mysql-avec-docker)
* [8. Lancement du serveur](#8-lancement-du-serveur)
* [9. Documentation de l'API](#9-documentation-de-lapi)
* [10. Fonctionnement de la base de données](#10-fonctionnement-de-la-base-de-données)
* [11. Design pattern Singleton](#11-design-pattern-singleton)
* [12. Gestion des erreurs HTTP](#12-gestion-des-erreurs-http)
* [13. Bonnes pratiques de sécurité](#13-bonnes-pratiques-de-sécurité)
* [14. Résolution des problèmes](#14-résolution-des-problèmes)
* [15. Améliorations futures](#15-améliorations-futures)

---

## 1. Présentation du projet

PythonServer est une API backend conçue pour apprendre et appliquer les concepts fondamentaux du développement d'applications web avec Python.

Le serveur permet notamment de travailler sur :

* La création et la récupération des utilisateurs.
* La recherche d'un utilisateur par son identifiant.
* La création et la gestion des avis associés aux utilisateurs.
* La communication entre FastAPI et MySQL.
* La manipulation des données avec SQLAlchemy.
* L'organisation du code en modèles, contrôleurs et routes.
* La gestion des connexions à la base de données avec le pattern Singleton.

### Objectifs pédagogiques

1. Comprendre le fonctionnement d'une API REST.
2. Maîtriser les méthodes HTTP : `GET`, `POST`, `PUT`, `PATCH` et `DELETE`.
3. Comprendre le rôle des routes, des contrôleurs et des modèles.
4. Apprendre à utiliser SQLAlchemy comme ORM.
5. Appliquer le design pattern Singleton.
6. Déployer les services de développement avec Docker Compose.
7. Tester les endpoints avec Swagger UI.

---

## 2. Technologies utilisées

| Technologie       | Rôle                                         |
| ----------------- | -------------------------------------------- |
| Python            | Langage de programmation                     |
| FastAPI           | Framework de développement d'API             |
| Uvicorn           | Serveur ASGI                                 |
| SQLAlchemy        | ORM pour la base de données                  |
| PyMySQL           | Pilote de connexion à MySQL                  |
| MySQL 8.4         | Système de gestion de base de données        |
| Docker            | Conteneurisation des services                |
| Docker Compose    | Orchestration de MySQL et phpMyAdmin         |
| phpMyAdmin        | Interface web d'administration MySQL         |
| Pydantic Settings | Chargement et validation de la configuration |
| Git               | Gestion de versions                          |

---

## 3. Architecture du projet

Le projet suit une organisation modulaire qui sépare les différentes responsabilités.

```text
Python_Server/
│
├── Config/
│   └── db.py
│
├── controllers/
│   ├── user_controller.py
│   ├── test_controller.py
│   └── avis_controller.py
│
├── models/
│   ├── User_model.py
│   └── avis.py
│
├── route/
│   ├── home_routes.py
│   ├── user_routes.py
│   └── test.py
│
├── .env
├── .gitignore
├── docker-compose.yml
├── main.py
├── requirements.txt
├── README.md
└── .venv/
```

Cette arborescence est indicative : adapte les noms aux fichiers réellement présents dans ton dépôt.

### Rôle des principaux composants

**`main.py`**

Point d'entrée de l'application. Il initialise FastAPI, configure le démarrage du serveur et enregistre les routeurs.

**`route/`**

Définit les endpoints HTTP et transmet les requêtes aux contrôleurs. Les dépendances FastAPI, notamment les sessions de base de données, sont injectées à ce niveau.

**`controllers/`**

Contient la logique de traitement des requêtes : création d'utilisateurs, récupération des données et création d'avis.

**`models/`**

Contient les modèles représentant les entités stockées en base de données, par exemple les utilisateurs et les avis.

**`Config/db.py`**

Centralise la gestion du moteur SQLAlchemy et fournit des sessions aux requêtes de l'application.

**`.env`**

Contient les paramètres de configuration et les informations de connexion. Ce fichier ne doit pas être publié dans un dépôt public.

---

## 4. Prérequis

Avant de démarrer le projet, vérifie que les outils suivants sont installés :

* Python 3.10 ou version compatible avec les dépendances du projet.
* pip.
* Docker Desktop.
* Docker Compose.
* Git, si le projet est cloné depuis un dépôt distant.

Vérifie les installations :

```powershell
python --version
python -m pip --version
docker --version
docker compose version
```

---

## 5. Installation

### 5.1. Accéder au projet

```powershell
cd D:\Python\python_server\Python_Server
```

### 5.2. Créer l'environnement virtuel

```powershell
python -m venv .venv
```

Activer l'environnement virtuel sous Windows :

```powershell
.\.venv\Scripts\Activate.ps1
```

L'environnement virtuel permet d'isoler les dépendances du projet de celles des autres applications Python.

### 5.3. Installer les dépendances

Si le fichier `requirements.txt` est déjà renseigné :

```powershell
python -m pip install -r requirements.txt
```

Sinon, installe les dépendances nécessaires :

```powershell
python -m pip install fastapi "uvicorn[standard]" sqlalchemy pymysql pydantic-settings python-multipart "pwdlib[argon2]"
```

Les dernières dépendances sont utiles respectivement pour le serveur, la configuration, les formulaires et le hachage des mots de passe si ces fonctionnalités sont utilisées dans le code.

### 5.4. Mettre à jour `requirements.txt`

Après l'installation des bibliothèques :

```powershell
python -m pip freeze > requirements.txt
```

Ce fichier permettra de reproduire l'environnement Python sur une autre machine.

---

## 6. Configuration des variables d'environnement

À la racine du projet, crée un fichier `.env` :

```dotenv
APP_NAME=PythonServer
APP_ENV=development
HOST=127.0.0.1
PORT=8081

# Configuration MySQL
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=UserDB
DB_USERNAME=Marcel
DB_PASSWORD=marcel123
```

### Explication des paramètres

| Variable      | Description                 |
| ------------- | --------------------------- |
| `APP_NAME`    | Nom de l'application        |
| `APP_ENV`     | Environnement d'exécution   |
| `HOST`        | Adresse d'écoute du serveur |
| `PORT`        | Port HTTP de l'API          |
| `DB_HOST`     | Adresse du serveur MySQL    |
| `DB_PORT`     | Port MySQL                  |
| `DB_NAME`     | Nom de la base de données   |
| `DB_USERNAME` | Utilisateur MySQL           |
| `DB_PASSWORD` | Mot de passe MySQL          |

**Important :** ces identifiants sont des exemples de développement. Utilise des mots de passe robustes et ne publie jamais tes véritables secrets.

Si FastAPI est exécuté directement sur Windows, `127.0.0.1:3306` convient lorsque le port MySQL est publié par Docker. Si FastAPI est lui-même placé dans un conteneur du même réseau Docker, l'hôte doit généralement être le nom du service, par exemple `mysql`.

---

## 7. Démarrage de MySQL avec Docker

Le projet utilise Docker Compose pour démarrer MySQL et phpMyAdmin.

### 7.1. Lancer les conteneurs

Depuis le répertoire contenant `docker-compose.yml` :

```powershell
docker compose up -d
```

### 7.2. Vérifier l'état des services

```powershell
docker compose ps
```

Afficher les journaux de MySQL :

```powershell
docker compose logs --tail=100 mysql
```

Le conteneur MySQL doit être opérationnel avant que l'API tente d'accéder à la base de données.

### 7.3. Accéder à phpMyAdmin

Ouvre l'adresse suivante dans ton navigateur :

http://localhost:8080

Utilise les identifiants définis dans le fichier Compose pour te connecter.

phpMyAdmin permet notamment de :

* Visualiser la base `UserDB`.
* Consulter les tables.
* Insérer ou modifier des données.
* Exécuter des requêtes SQL.
* Vérifier les utilisateurs et les avis enregistrés.

### 7.4. Persistance des données

Le volume Docker `mysql_data` conserve les données de MySQL après l'arrêt ou la recréation des conteneurs.

Pour arrêter les services sans supprimer les données :

```powershell
docker compose down
```

Évite `docker compose down -v` si tu souhaites conserver les données du volume.

---

## 8. Lancement du serveur

Une fois les dépendances installées et MySQL opérationnel, démarre l'application :

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8081
```

Le serveur est alors accessible à l'adresse :

http://127.0.0.1:8081

L'option `--reload` redémarre automatiquement le serveur pendant le développement lorsque le code change. Elle est réservée au développement, pas à la production.

Il est également possible de lancer le programme avec :

```powershell
python main.py
```

si le bloc de lancement Uvicorn est correctement défini dans `main.py`.

---

## 9. Documentation de l'API

FastAPI génère automatiquement une documentation interactive à partir des routes déclarées.

### Swagger UI

http://127.0.0.1:8081/docs

Cette interface permet de consulter les endpoints, leurs paramètres, les formats de requêtes et les réponses, puis de les tester directement depuis le navigateur.

### ReDoc

http://127.0.0.1:8081/redoc

ReDoc propose une autre présentation de la documentation OpenAPI.

### Endpoints principaux

Les chemins ci-dessous correspondent à l'organisation prévue dans le projet. Les chemins définitifs dépendent des décorateurs et des préfixes configurés dans les routeurs.

| Méthode | Endpoint indicatif | Fonction                                      |
| ------- | ------------------ | --------------------------------------------- |
| `GET`   | `/home/`           | Vérifier le fonctionnement du serveur         |
| `POST`  | `/users/`          | Créer un utilisateur                          |
| `GET`   | `/users/`          | Récupérer les utilisateurs                    |
| `GET`   | `/users/user?id=1` | Rechercher un utilisateur par identifiant     |
| `GET`   | `/database/`       | Tester la connexion à MySQL                   |
| `POST`  | `/avis/`           | Créer un avis, si cette route est enregistrée |

Consulte `/docs` pour confirmer les chemins effectivement exposés.

### Exemple : créer un utilisateur

Si la route attend des données de formulaire, utilise les champs suivants :

```text
username: Marcel
email: marcel@example.com
password: mot_de_passe_de_test
```

Une création réussie doit renvoyer le statut HTTP `201 Created`.

Le mot de passe ne doit jamais être retourné dans la réponse. Il doit être haché avant d'être enregistré dans la base de données.

### Exemple : vérifier la connexion MySQL

Requête :

```http
GET /database/
```

Réponse indicative :

```json
{
  "message": "Connexion MySQL réussie",
  "database": "UserDB"
}
```

Cette réponse dépend du format réellement implémenté dans le contrôleur de test.

---

## 10. Fonctionnement de la base de données

Le projet utilise SQLAlchemy pour interagir avec MySQL sans écrire systématiquement les requêtes SQL à la main.

### 10.1. Les modèles

Les modèles définissent la structure des entités persistées, comme `UserSchema` ou `Avis`.

Ils permettent de représenter les tables MySQL sous forme de classes Python.

### 10.2. Les sessions

Une session SQLAlchemy sert à effectuer les opérations de lecture et d'écriture.

Exemple :

```python
db.add(user)
db.commit()
db.refresh(user)
```

* `add()` prépare l'insertion de l'objet.
* `commit()` valide la transaction.
* `refresh()` recharge les données de l'objet depuis la base de données.

Pour une lecture :

```python
users = db.query(UserSchema).all()
```

La session doit être fermée après son utilisation. La dépendance `get_db()` est chargée de fournir et de fermer la session pour chaque requête.

### 10.3. Transactions et erreurs

Si une opération SQL échoue pendant une transaction, il faut appeler :

```python
db.rollback()
```

Cela annule la transaction en cours et permet de remettre la session dans un état utilisable avant de poursuivre.

---

## 11. Design pattern Singleton

Le projet applique le design pattern Singleton à la gestion du moteur de connexion à MySQL.

### 11.1. Définition

Le Singleton est un patron de conception qui vise à garantir qu'une classe possède une seule instance partagée, accessible depuis plusieurs parties de l'application.

### 11.2. Application dans PythonServer

Le composant `Database` centralise la création du moteur SQLAlchemy.

Son fonctionnement repose sur les éléments suivants :

* Une référence à l'instance partagée.
* Une méthode de création contrôlée de cette instance.
* Un moteur SQLAlchemy partagé.
* Une fabrique de sessions permettant d'ouvrir des sessions indépendantes.

### 11.3. Pourquoi ce choix ?

Ce mécanisme évite de créer inutilement un nouveau moteur SQLAlchemy à chaque requête. Le moteur gère un pool de connexions réutilisables.

Il est important de distinguer :

| Élément              | Rôle                                                  |
| -------------------- | ----------------------------------------------------- |
| Singleton `Database` | Centralise la gestion du moteur                       |
| `Engine` SQLAlchemy  | Gère le pool de connexions                            |
| `Session` SQLAlchemy | Représente une unité de travail avec la base          |
| `get_db()`           | Fournit une session à une requête et la ferme ensuite |

Le Singleton ne signifie donc pas que toutes les requêtes doivent partager une unique session SQLAlchemy. Chaque requête doit utiliser sa propre session.

---

## 12. Gestion des erreurs HTTP

L'API utilise des codes de statut HTTP pour indiquer le résultat d'une opération.

| Code                        | Signification         | Exemple                       |
| --------------------------- | --------------------- | ----------------------------- |
| `200 OK`                    | Requête réussie       | Liste des utilisateurs        |
| `201 Created`               | Ressource créée       | Nouvel utilisateur            |
| `400 Bad Request`           | Requête invalide      | Champ obligatoire manquant    |
| `404 Not Found`             | Ressource inexistante | Utilisateur introuvable       |
| `409 Conflict`              | Conflit de données    | Email déjà utilisé            |
| `500 Internal Server Error` | Erreur interne        | Échec inattendu du traitement |
| `503 Service Unavailable`   | Service indisponible  | Connexion à MySQL impossible  |

Les erreurs doivent être traitées de manière cohérente. En production, les détails internes des exceptions ne doivent pas être exposés aux clients.

---

## 13. Bonnes pratiques de sécurité

Pour améliorer la sécurité de PythonServer :

* Ne jamais versionner le fichier `.env`.
* Ajouter `.env` et `.venv/` au fichier `.gitignore`.
* Utiliser des mots de passe robustes pour MySQL.
* Ne jamais stocker les mots de passe des utilisateurs en clair.
* Utiliser un algorithme de hachage adapté aux mots de passe, par exemple Argon2.
* Ne jamais retourner les mots de passe dans les réponses API.
* Valider les données reçues par les endpoints.
* Gérer les transactions avec `commit()` et `rollback()`.
* Limiter les détails d'erreur renvoyés en production.
* Désactiver le rechargement automatique du serveur en production.
* Utiliser HTTPS et une configuration adaptée avant toute mise en production.

Exemple de `.gitignore` :

```gitignore
# Environnement Python
.venv/
__pycache__/
*.py[cod]

# Secrets et configuration locale
.env
.env.*

# Exceptions éventuelles pour des modèles de configuration
!.env.example

# Outils et fichiers temporaires
.vscode/
.pytest_cache/
.coverage
```

Un fichier `.env.example` sans secrets peut être versionné pour documenter les variables requises.

---

## 14. Résolution des problèmes

### MySQL est `unhealthy`

Consulte les journaux :

```powershell
docker compose logs --tail=100 mysql
```

Vérifie le mot de passe root, les variables d'initialisation et l'état du volume persistant.

### Impossible de se connecter à MySQL

Vérifie que :

* Le conteneur MySQL fonctionne.
* Le port `3306` est publié.
* Le nom de la base de données est correct.
* Les identifiants correspondent à ceux initialisés dans MySQL.
* L'hôte est adapté à l'environnement d'exécution de FastAPI.

### `ModuleNotFoundError`

Vérifie que l'environnement virtuel est activé et que les dépendances sont installées :

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Vérifie aussi les chemins d'import des modules Python.

Attention à la casse : `Config` et `config` peuvent être traités différemment selon le système d'exploitation. Il est préférable de choisir une convention et de l'utiliser partout.

### `Object of type ... is not JSON serializable`

Ne retourne pas directement un objet SQLAlchemy dans `JSONResponse`. Convertis-le en dictionnaire contenant uniquement les attributs nécessaires, ou utilise un schéma Pydantic de réponse.

### `Depends` ne fournit pas une session

`Depends(get_db)` est résolu automatiquement par FastAPI lorsqu'il appelle une route ou une dépendance déclarée. Si un contrôleur est appelé directement comme une fonction Python, il faut lui transmettre explicitement la session reçue par la route.

---

## 15. Améliorations futures

Les évolutions suivantes pourront être ajoutées progressivement :

* [ ] Ajouter des schémas Pydantic pour valider les entrées et structurer les réponses.
* [ ] Implémenter les opérations CRUD complètes pour les utilisateurs.
* [ ] Ajouter les endpoints de consultation, modification et suppression des avis.
* [ ] Mettre en place un système d'authentification et d'autorisation.
* [ ] Ajouter des migrations de base de données avec Alembic.
* [ ] Écrire des tests automatisés avec Pytest et FastAPI TestClient.
* [ ] Ajouter des tests d'intégration avec MySQL.
* [ ] Ajouter une journalisation structurée.
* [ ] Mettre en place un pipeline CI/CD.
* [ ] Préparer une configuration de déploiement adaptée à la production.

---

## Auteur et contribution

Ce projet est développé dans un objectif d'apprentissage et de mise en pratique du développement backend avec Python.

Les contributions et propositions d'amélioration peuvent être organisées autour de branches Git, de commits explicites et de tests avant intégration.

---

## Licence

Aucune licence spécifique n'est définie dans ce document. Ajoute un fichier `LICENSE` si tu souhaites distribuer le projet sous une licence open source.

```
```
