![Static Badge](/static/badges/Build-with-Python.svg)   
![Static Badge](/static/badges/Build-with-Django.svg)   
![Static Badge](/static/badges/Build-with-Django-REST-framework.svg)   

![Static Badge](/static/badges/flake8-badge.svg)   

![Static Badge](/static/badges/Use-Postman.svg) ➔ [Documentation Postman du projet SoftDesk](https://documenter.getpostman.com/view/26427645/2s9Xy2Ps1k)

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/26427645-80fa9cda-470b-46d7-90ee-f3de31406629?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D26427645-80fa9cda-470b-46d7-90ee-f3de31406629%26entityType%3Dcollection%26workspaceId%3D848b9be2-0145-4866-b3c3-8e89c5cf329e)

<div id="top"></div>

# Menu   

1. **[Informations générales](#informations-générales)**   
2. **[Fonctionnalitées](#fonctionnalitées)**   
3. **[Interface d'administration Django](#interface-administration-django)**   
4. **[Liste pré-requis](#liste-pre-requis)**   
5. **[Création environnement](#creation-environnement)**   
6. **[Activation environnement](#activation-environnement)**   
7. **[Installation des librairies](#installation-librairies)**   
8. **[Exécution de l'application](#execution-application)**   
9. **[Liste end points](#liste-endpoints)**   
10. **[Liste end points administrateur](#liste-endpoints-admin)**   
11. **[Rapport avec flake8](#rapport-flake8)**   
12. **[Informations importantes sur les différents fichiers et dossiers](#informations-importantes)**   
13. **[Auteur et contact](#auteur-contact)**   

<div id="informations-générales"></div>

### Projet API RESTful   

- Création d'une **API RESTful** développé sur **Django REST framework** permettant d'échanger des informations en toute sécurité.   
- L'**API** permet de créer des utilisateurs, des projets, des contributions, des issues, des commentaires.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="fonctionnalitées"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Fonctionnalitées   

- Opérations **CRUD**.   
- ``Inscription`` et ``connexion``.   
- Navigation au travers des end points de l'**API**.   

Pour plus de détails sur le fonctionnement de cette API, se référer à sa ➔ [documentation](https://documenter.getpostman.com/view/26427645/2s9Xy2Ps1k) **Postman**.   

>_Note : Testé sous **Windows** 7 - **Python** 3.7.2 - **Django** 3.2.20 - **Django REST framework** 3.12.4_   

--------------------------------------------------------------------------------------------------------------------------------

<div id="interface-administration-django"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Interface d'administration Django    

- L'interface d'administration **Django** est disponible et fonctionnelle.   

- ``Créer`` et ``modifier`` des utilisateurs.   
- ``Créer`` et ``modifier`` des projets, des contributeurs, des issues et des commentaires.   

Identifiant : **Admin** | Mot de passe : **Hello123**
Page d'administration **Django** ➔ http://127.0.0.1:8000/admin/   

##### Utilisateurs de test enregistrés dans la basse de données    

| **Identifiant** | **Mot de passe** |
|-----------------|------------------|
|    Lisa         |    Hello123      |
|    Milhouse     |    Hello123      |
|    Marge        |    Hello123      |
|    Bart         |    Hello123      |

--------------------------------------------------------------------------------------------------------------------------------

<div id="liste-pre-requis"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Liste pré-requis   
Programme élaboré avec les les technologies suivantes :   
- **Python** v3.7.2 choisissez la version adaptée à votre ordinateur et système.   
- **Python** est disponible à l'adresse suivante ➔ https://www.python.org/downloads/    
- **Django** 3.2.19   
- **Django REST framework** 3.12.4   
- **Postman** ➔ https://www.postman.com/   
- **Windows** 7 professionnel SP1   
  &nbsp;   

- Les scripts **Python** s'exécutent depuis un terminal.   
  - Pour ouvrir un terminal sur **Windows**, pressez la touche ```windows + r``` et entrez ```cmd```.   
  - Sur **Mac**, pressez la touche ```command + espace``` et entrez ```terminal```.   
  - Sur **Linux**, vous pouvez ouviri un terminal en pressant les touches ```Ctrl + Alt + T```.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="creation-environnement"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Création de l'environnement virtuel   

- Installer une version de **Python** compatible pour votre ordinateur.   
- Une fois installer ouvrer **le cmd (terminal)** placer vous dans le dossier principal **(dossier racine)**.   

Taper dans votre terminal :   

```bash
python -m venv env
```
>_Note : Un répertoire appelé **env** doit être créé._   

--------------------------------------------------------------------------------------------------------------------------------

<div id="activation-environnement"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Activation de l'environnement virtuel   

- Placez-vous avec le terminal dans le dossier principale **(dossier racine)**.   

Pour activer l'environnement virtuel créé, il vous suffit de taper dans votre terminal :   

```bash
env\Scripts\activate.bat
```
- Ce qui ajoutera à chaque ligne de commande de votre terminal ``(env)``:   

Pour désactiver l'environnement virtuel, il suffit de taper dans votre terminal :   

```bash
deactivate
```

--------------------------------------------------------------------------------------------------------------------------------

<div id="installation-librairies"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Installation des librairies   

- Le programme utilise plusieurs librairies externes et modules de **Python**, qui sont répertoriés dans le fichier ```requirements.txt```.   
- Placez-vous dans le dossier où se trouve le fichier ``requirements.txt`` avec le terminal, l'environnement virtuel doit être activé.   
- Pour faire fonctionner le programme, il vous faudra installer les librairies requises.   
- À l'aide du fichiers ``requirements.txt`` mis à disposition.   

Taper dans votre terminal la commande :   

```bash
pip install -r requirements.txt
```

--------------------------------------------------------------------------------------------------------------------------------

<div id="execution-application"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Exécution de l'application

#### Utilisation

1. Lancement du serveur **Django**.   
- Placez-vous avec le terminal dans le dossier principal **LITReview**.   
- Activer l'environnement virtuel et ensuite lancer le serveur **Django**.   

Taper dans votre terminal la commande :   

```bash
python manage.py runserver
```

2. Lancement de l'application dans le navigateur de votre choix.   
- Se rendre à l'adresse ➔ http://127.0.0.1:8000/   

Il est possible de naviguer dans l'**API** avec différents outils :

- La plateforme ➔ [Postman](https://www.postman.com/) ;
- L'outil de commandes ➔ [cURL](https://curl.se) ;
- L'interface intégrée **Django REST framework** à l'adresse ➔ http://127.0.0.1:8000/ (adresse par défaut, cf. points de terminaison ci-dessous).

>_Note : **Créer** ou **utiliser** un utilisateur déja présent dans la base de données._   

- Si vous souhaitez créer un nouvel utilisateur dans l'environnement virtuel, utiliser le shell **Django**.   
- Si vous souhaitez que l'utilisateur est accés à l'interface d'administration de **Django** ➔ ```http://127.0.0.1:8000/admin/```   

Remplacer ```is_staff=False``` par ```is_staff=True```   

Tapez dans votre terminal les commandes :   

```bash
>>> python manage.py shell
>>> from user.models import User
>>> user = User.objects.create_user(username='nom_utilisateur', password='password_utilisateur', age=18, consent_choice=True, is_active=True, is_staff=False)
```
>Note : Remplacez **nom_utilisateur**, **password_utilisateur**, **age=18** par les valeurs que vous souhaitez.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="liste-endpoints"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

#### Liste des end points de l'API   

- Détails dans la ➔ [documentation](https://documenter.getpostman.com/view/26427645/2s9Xy2Ps1k) **Postman**.   
- Import et exécute la collection dans votre propre espace de travail **Postman** ➔ [<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="vertical-align: middle; width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/26427645-80fa9cda-470b-46d7-90ee-f3de31406629?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D26427645-80fa9cda-470b-46d7-90ee-f3de31406629%26entityType%3Dcollection%26workspaceId%3D848b9be2-0145-4866-b3c3-8e89c5cf329e)

| #   | End points d'API                                            | Méthode HTTP   | URL (base: http://127.0.0.1:8000)                                |
|-----|-------------------------------------------------------------|----------------|------------------------------------------------------------------|
|  1  | Permet de refresh le token                                  | POST           | /api/token/refresh/                                              | 
|  2  | Inscription de l'utilisateur                                | POST           | /api/signup/                                                     | 
|  3  | Connexion de l'utilisateur                                  | POST           | /api/login/                                                      |
|     |                                                             |                |                                                                  |  
|  4  | Récupérer la liste de tous les projets                      | GET            | /api/projects/                                                   |
|  5  | Récupérer les détails d'un projet via son id                | GET            | /api/projects/:project_id/                                       |
|  6  | Créer un projet                                             | POST           | /api/projects/                                                   |
|  7  | Mettre à jour un projet                                     | PUT            | /api/projects/:project_id/                                       |
|  8  | Supprimer un projet et ses problèmes                        | DELETE         | /api/projects/:project_id/                                       |
|     |                                                             |                |                                                                  |
|  9  | Récupérer la liste des contributeurs                        | GET            | /api/projects/:project_id/users/                                 |
| 10  | Ajouter ou modifier un contibuteur à un projet              | POST           | /api/projects/:project_id/users/                                 |
| 11  | Supprimer un contributeur d'un projet                       | DELETE         | /api/projects/:project_id/users/:contributor_id/                 |
|     |                                                             |                |                                                                  |
| 12  | Récupérer la liste des problèmes                            | GET            | /api/projects/:project_id/issues/                                |
| 13  | Créer un problème dans un projet                            | POST           | /api/projects/:project_id/issues/                                |
| 14  | Mettre à jour un problème dans un projet                    | PUT            | /api/projects/:project_id/issues/:issue_id/                      |
| 15  | Supprimer un problème d'un projet                           | DELETE         | /api/projects/:project_id/issues/:issue_id/                      |
|     |                                                             |                |                                                                  |
| 16  | Récupérer la liste des commentaires                         | GET            | /api/projects/:project_id/issues/:issue_id/comments/             |
| 17  | Ajouter ou modifier un commentaire                          | POST           | /api/projects/:project_id/issues/:issue_id/comments/             |
| 18  | Modifier un commentaire                                     | PUT            | /api/projects/:project_id/issues/:issue_id/comments/:comment_id/ |
| 19  | Supprimer un commentaire                                    | DELETE         | /api/projects/:project_id/issues/:issue_id/comments/:comment_id/ |

--------------------------------------------------------------------------------------------------------------------------------

<div id="liste-endpoints-admin"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

#### Liste des end points de l'API en administrateur   

| **Note : Les end points suivants sont disponibles en administrateur pour pouvoir visualiser les données.** |
|------------------------------------------------------------------------------------------------------------|
|&rarr; http://127.0.0.1:8000/api/admin/users/                                                               |
|&rarr; http://127.0.0.1:8000/api/admin/users/{id}/                                                          |
|                                                                                                            |
|&rarr; http://127.0.0.1:8000/api/admin/projects/                                                            |
|&rarr; http://127.0.0.1:8000/api/admin/projects/{id}/                                                       |
|                                                                                                            |
|&rarr; http://127.0.0.1:8000/api/admin/contributors/                                                        |
|&rarr; http://127.0.0.1:8000/api/admin/contributors/{id}/                                                   |
|                                                                                                            |
|&rarr; http://127.0.0.1:8000/api/admin/issues/                                                              |
|&rarr; http://127.0.0.1:8000/api/admin/issues/{id}/                                                         |
|                                                                                                            |
|&rarr; http://127.0.0.1:8000/api/admin/comments/                                                            |
|&rarr; http://127.0.0.1:8000/api/admin/comments/{id}/                                                       |


**Navigateur.**   
>*Note : Les tests ont était fait sur **Firefox** et **Google Chrome**.*   

--------------------------------------------------------------------------------------------------------------------------------

<div id="rapport-flake8"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Rapport avec flake8   

- Le repository contient un rapport **flake8**, qui renvoi ```All good! No flake8 errors found in 20 files scanned.``` ➔ ([.flake8](.flake8))   
- Il est possible d'en générer un nouveau en installant le module ```flake8``` s'il n'est pas installé.   

Installation de flake8 en entrant dans votre terminal la commande :   

```bash
pip install flake8-html
```
- Créer un fichier ```.flake8``` si il n'existe pas.   
- Ecrire le texte suivant dedans :   

```bash
[flake8]
exclude = .git, env, .gitignore, static, static, *tests.py, **/templates/, **/migrations/
max-line-length = 119
ignore = F401, W504, F811, F821
```

Tapez dans votre terminal la commande :   

```bash
flake8 --format=html --htmldir=flake-report
```
- Un rapport sera généré dans le dossier ``flake-report``.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="informations-importantes"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Informations importantes sur les différents fichiers et dossiers   

**Le dossier api**   

  - Le dossier est une apps **Django** qui contient :   
  - Un dossier ```migrations``` contenant les fichiers de configuration pour la base de données. ➔ ([migrations](api/migrations))   
  - Á la racine du dossier ```api``` les fichiers tels que views.py, models.py, serializers.py, permissions.py. ➔ ([api](api))   

**Le dossier user**   

  - Le dossier est une apps **Django** qui contient :   
  - Un dossier ```migrations``` contenant les fichiers de configuration pour la base de données. ➔ ([migrations](user/migrations))   
  - Á la racine du dossier ```user``` les fichiers tels que views.py, models.py, serializers.py. ➔ ([user](user))   

**Le dossier SoftDesk**   

  - Le dossier est une apps **Django** qui contient :   
  - Les fichiers de configuration du projet.   
  - Á la racine du dossier ```SoftDesk``` les fichiers tels que settings.py, urls.py. ➔ ([SoftDesk](SoftDesk))   

**Le dossier static**   

  - Dossier qui contient qui contient les images svg des badges.   

--------------------------------------------------------------------------------------------------------------------------------

<div id="auteur-contact"></div>
<a href="#top" style="float: right;">Retour en haut 🡅</a>

### Auteur et contact   

Pour toute information supplémentaire, vous pouvez me contacter.   
**Bubhux:** bubhuxpaindepice@gmail.com   
