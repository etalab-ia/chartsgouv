# 🚀 Déploiement de Chartsgouv avec Docker

> **Important :** Le lancement via **Docker** n’a pas vocation à être utilisé en production.  
> Pour un usage **production**, utilisez le déploiement via **Helm** (documentation à renseigner ici : `[lien_helm]`).

[[_TOC_]]

> Tous les éléments de personnalisations se situent dans le dossier `chartsgouv/superset`. Il n'y a pas besoin du repo officiel de apache Superset.

## L'image de ChartsGouv
1. Les images mises à disposition  

Plusieurs images prêtent à l'emploi se situent [ici](https://github.com/etalab-ia/chartsgouv/pkgs/container/chartsgouv).  
Le tag des images se lit de la façon suivante: `chartsgouv:version_superset-version_dsfr-version_dsfr_chart`

2. Personnaliser une image  

Tous les éléments de personnalisations se situent dans le dossier [`chartsgouv/superset`](https://github.com/etalab-ia/chartsgouv/tree/main/superset). Vous pouvez vous référer à la documentation pour customiser tous les éléments.

Une fois les modifications effectuées, il faudra build votre image:
```bash
# Lancez la commande depuis la racine du projet
docker build -t nom_image:votre_tag .
```
Vous pouvez ensuite l'utiliser dans un déploiement avec Docker compose.

## [Lancement avec Docker](#lancement-avec-docker)

L'exécution directe de l'image via une commande Docker n'est pas possible compte tenu de la façon dont la configuration se charge dans Superset.

## [Lancement avec Docker Compose](#lancement-avec-docker-compose)

Spécifiez l'image que vous souhaitez utiliser dans `superset/docker-compose-image-tag.yml` :
```yaml
x-superset-image: &superset-image nom_image:tag
```
Vous pouvez utiliser l'image que vous venez de build ou celles mises à votre disposition.  

- Configurer l'application  

Les variables d'environnements de votre application peuvent être configurées dans le fichier [.env](https://github.com/etalab-ia/chartsgouv/blob/main/superset/docker/.env).  
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
```
La valeur de `SUPERSET_SECRET_KEY` peut être générée avec la commande `openssl rand -base64 42`

Depuis la racine du projet:
- Démarrer les services
```bash
# Lancez la commande depuis la racine du projet
docker compose -f superset/docker-compose-image-tag.yml up -d
```
Une fois les services lancés, se rendre sur http://localhost:8088 et rentrer les identifiants :  
nom d'utilisateur : `admin`  
mot de passe : `admin`  
Ces identifiants peuvent être modifiés via le fichier `superset/docker/docker-init.sh`.
```bash
# Remplacer username et password
superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password $ADMIN_PASSWORD
```
> les fichiers de scripts sont montés dans l'image. Vous avez la possibilité de créer manuellement un utilisateur administratreur.
```bash
# Exécuter cette commande depuis le container. Remplacer username et password
docker exec -it superset_app sh -c "superset fab create-admin \
              --username user \
              --firstname Superset \
              --lastname Admin \
              --email user@superset.com \
              --password user"
```

- Pour arrêter les services
```bash
# Lancez la commande depuis la racine du projet
docker compose -f superset/docker-compose-image-tag.yml down
```
Des volumes seront créés sur votre machine locale. Pensez à les supprimer si vous ne les utilisez plus.


### Nginx / A COMPLETER
Si le déploiement est sur un serveur distant, un exemple de fichier de configuration Nginx agissant en reverse-proxy est donné [plus bas](#nginx).

Fichier `/etc/nginx/sites-available/superset`:
```
server {
  index index.html index.htm;
  access_log /var/log/nginx/mondomaine.fr_access.log;
  error_log /var/log/nginx/mondomaine.fr_error.log;
  server_name mondomaine.fr www.mondomaine.fr;
  location / {
    proxy_pass http://localhost:8088;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    # WebSocket support
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    #proxy_set_header Connection "upgrade";
    proxy_set_header Connection $http_connection;
  }

  listen 443 ssl;
  ssl_certificate /etc/letsencrypt/live/mondomaine.fr/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/mondomaine.fr/privkey.pem;
  include /etc/letsencrypt/options-ssl-nginx.conf;
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
  if ($host = mondomaine.fr) {
    return 301 https://$host$request_uri;
  }

  listen 80;
  listen [::]:80;
  server_name mondomaine.fr;
  return 404;
}
```

```bash
sudo ln -s /etc/nginx-sites-available/superset /etc/nginx/sites-enabled/superset 
sudo nginx -s reload
```
