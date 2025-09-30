# 🚀 Déploiement de Chartsgouv avec Docker

> **Important :** ce mode de déploiement est à titre indicatif.

## Table des matières
- [🚀 Déploiement de Chartsgouv avec Docker](#-déploiement-de-chartsgouv-avec-docker)
  - [Table des matières](#table-des-matières)
  - [Pré-requis](#pré-requis)
  - [Construire son image Superset](#construire-son-image-superset)
  - [Lancement avec Docker Compose](#lancement-avec-docker-compose)

## Pré-requis

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Construire son image Superset

Vous pouvez personnaliser tous les éléments disponibles dans [superset-dsfr](../../../superset-dsfr/).

Une fois les personnalisations effectuées, il faudra build votre image:
```bash
# Lancez la commande depuis la racine du projet
docker build \
  --build-arg SUPERSET_VERSION=4.1.1 \
  --build-arg USE_DSFR=true \
  --build-arg TAG_DSFR=1.13.0 \
  --build-arg TAG_DSFR_CHART=2.0.3 \
  -t custom_superset:custom_tag .
```
`SUPERSET_VERSION`: la version officielle d'Apache Superset à utiliser.  
`USE_DSFR`: pour implémenter le dsfr. Télécharge le dsfr, dsfr-chart et applique la charte de l'Etat.  
`TAG_DSFR`: la version officielle du dsfr à utiliser.  
`TAG_DSFR_CHART`: la version officielle du dsfr-chart à utiliser.

## Lancement avec Docker Compose

1. Configurer le fichier Docker compose

Spécifiez l'image que vous souhaitez utiliser dans [superset-dsfr/docker-compose-image-tag.yml](../../../superset-dsfr/docker-compose-image-tag.yml#L24): :
```yaml
x-superset-image: &superset-image custom_superset:custom_tag
```

Vous pouvez utiliser les images officielles de Superset, l'image que vous venez de build ou celles mises à votre disposition.

Quelque soit l'image utilisée, vous avez la possibilité de personnaliser tous les éléments disponibles dans [superset-dsfr](../../../superset-dsfr/) et de les intégrer au déploiement Docker en utilisant les volumes.  

Si vous ne souhaitez pas associer de volumes, il faudra commenter les lignes suivantes du fichier [superset-dsfr/docker-compose-image-tag.yml](../../../superset-dsfr/docker-compose-image-tag.yml#L29).

```yaml
x-superset-volumes:
  &superset-volumes # /app/pythonpath_docker will be appended to the PYTHONPATH in the final container
  - ./docker:/app/docker
  - superset_home:/app/superset_home
  # Comment the following line if you are using your own custom image
#   - ./assets:/app/superset/static/assets/local
#   - ./templates_overrides:/app/superset/templates_overrides
#   - ./dsfr/dist:/app/superset/static/assets/dsfr
#   - ./dsfr-chart/dsfr-chart/dist/DSFRChart:/app/superset/static/assets/dsfr-chart
```

2. Configurer l'application  

Les variables d'environnements de votre application peuvent être configurées dans le fichier [.env](../../../superset-dsfr/docker/.env).  
```bash
# A secret key that will be used for securely signing the session cookie and can be used for any other security related needs by extensions or your application
SUPERSET_SECRET_KEY=TEST_NON_DEV_SECRET
# false pour enlever certains tags "development"
DEV_MODE=true
# Charger les données d'exemples
SUPERSET_LOAD_EXAMPLES=yes
# Connection à la base de données
POSTGRES_USER=superset
POSTGRES_PASSWORD=superset
# Superset
SUPERSET_PORT=8088
```
La valeur de `SUPERSET_SECRET_KEY` peut être générée avec la commande `openssl rand -base64 42`. Conserver bien cette clé.

3. Démarrer les services

Depuis la racine du projet:
```bash
# Lancez la commande depuis la racine du projetnew_admin
docker compose -f superset-dsfr/docker-compose-image-tag.yml up -d
```
Une fois les services lancés, se rendre sur http://localhost:8088 et rentrer les identifiants :  
nom d'utilisateur : `admin`  
mot de passe : `admin`  

Ces identifiants peuvent être modifiés via le fichier [superset-dsfr/docker/docker-init.sh](../../../superset-dsfr/docker/docker-init.sh#56).

```bash
# Remplacer username et password
superset fab create-admin \
    --username admin \
    --email admin@superset.com \
    --password "$ADMIN_PASSWORD" \
    --firstname Superset \
    --lastname Admin
```

Vous avez la possibilité de créer manuellement un utilisateur administratreur.
```bash
# Exécuter cette commande depuis le container.
docker exec -it superset_app sh -c "superset fab create-admin \
              --username new_admin \
              --firstname new \
              --lastname Admin \
              --email new_admin@domain.fr \
              --password new_admin"
```

4. Arrêter les services
```bash
# Lancez la commande depuis la racine du projet
docker compose -f superset-dsfr/docker-compose-image-tag.yml down
```
Des volumes seront créés sur votre machine locale. Pensez à les supprimer si vous ne les utilisez plus.
