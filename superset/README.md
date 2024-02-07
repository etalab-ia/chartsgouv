> AVERTISSEMENT : Ce système de conception est uniquement destiné à être utilisé pour les sites web officiels des services publics français.
> Son objectif principal est de faciliter l'identification des sites gouvernementaux par les citoyens. [Voir les conditions](https://www.systeme-de-design.gouv.fr/utilisation-et-organisation/perimetre-d-application).

### tldr;

```bash
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.11.1/dsfr-v1.11.1.zip
unzip dsfr-v1.11.1.zip -d dsfr
git clone --single-branch https://github.com/etalab-ia/chartsgouv
cd superset/
TAG=3.0.0 docker compose -f docker-compose-non-dev.yml up -d
# Se rendre sur localhost:8088 avec identifiants admin/admin
```

### Pas à pas avec explications et possibilités d'adaptation

Télécharger le DSFR (fichiers compilés), ici la version v1.11.1 datée du 01/02/2024:
```bash
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.11.1/dsfr-v1.11.1.zip
unzip dsfr-v1.11.1.zip -d dsfr
```

Cloner le repo ChartsGouv, seule la branche principale est nécessaire.

```bash
git clone --single-branch https://github.com/etalab-ia/chartsgouv
```

Se déplacer dans le répertoire `superset/` qui contient le nécessaire pour déployer avec Docker Apache Superset configuré en français avec un thème DSFR appliqué globalement à toute l'interface, avec la police Marianne appliquée à toute l'interface, des palettes de couleurs respectueuses des couleurs illustratives du DSFR, les feuilles de style CSS et les fichiers Javascript du DSFR appliqués globalement pour pouvoir intégrer [des composants du DSFR](https://www.systeme-de-design.gouv.fr/elements-d-interface/composants) dans les Zones de texte:

```bash
cd superset/
```

Tous les fichiers nécessaires sont présents dans ce répertoire, il n'y a pas besoin d'avoir le dépôt principal avec les sources complètes de Superset.

On utilise les images officielles Apache Superset avec un fichier modifié (voir plus bas) du `docker-compose-non-dev.yml` adapté pour la production:

```bash
TAG=3.0.0 docker compose -f docker-compose-non-dev.yml up -d
```

Se rendre sur http://localhost:8088 et rentrer les identifiants :
- nom d'utilisateur : admin
- mot de passe : admin
Si le déploiement est sur un serveur distant, un exemple de fichier de configuration Nginx agissant en reverse-proxy est donné plus bas.

### Détails et possibilités d'adaptation

Le dépôt contient:
- une version modifiée de `docker-compose-non-dev.yml` avec des points de montage supplémentaire (assets supplémentaires, DSFR, templates,
- une version modifiée des templates `superset/templates/superset/{base,basic}.html` pour inclure le DSFR globalement (css et js),
- un fichier `assets/css/tail_css_custom_extra.css` pour corriger l'affichage de certains liens,
- un fichier `assets/images/app_icon.png`, à remplacer par l'image de votre choix pour l'icône de l'application dans le header,
- un fichier `superset/templates/superset/public_welcome.html`, optionnel pour démontrer la capacité de personnaliser la page d'accueil,
- un fichier `superset/templates/tail_js_custom_extra.html`, optionnel pour démontrer la capacité d'injecter un script globalement sur toutes les pages
- un fichier `docker/requirements-local.txt`, optionnel où on peut ajouter des paquets Python supplémentaires, [par exemple nécessaires pour certains drivers](https://superset.apache.org/docs/databases/installing-database-drivers) comme `duckdb-engine`,
- le fichier de configuration `docker/pythonpath_dev/superset_config_docker.py` qui inclut notamment: 
  - la [variable de configuration de thème](https://preset.io/blog/theming-superset-progress-update/) `THEME_OVERRIDES` pour faire la transposition DSFR => design system de Superset,
  - [les variables de configuration des couleurs des charts](https://preset.io/blog/customizing-chart-colors-with-superset-and-preset/) `EXTRA_CATEGORICAL_COLOR_SCHEMES` pour définir une nouvelle palette de couleurs avec [les couleurs illustratives du DSFR](https://gouvernementfr.github.io/dsfr-chart/#colors) pour les graphiques à variables catégorielles,
  - `EXTRA_SEQUENTIAL_COLOR_SCHEMES` pour définir des dégradés de couleur pour les graphiques à variables continues (e.g. plugin Carte de Pays).
- les autres fichiers (`docker/docker-entrypoint-initdb.d/examples-init.sh`, `docker/pythonpath_dev/superset_config.py`, `docker/{.env-non-dev,docker-bootstrap.sh,docker-init.sh}` sont les fichiers originaux du dépot principal non modifié, ils viennent de la version 3.0.0 et sont stables dans le temps.


Le CSS compilé, le JS compilé, la police Marianne, les icônes, les favicons et les pictogrammes sont montés comme volumes dans les containers dans le chemin `/app/superset/static/assets/dsfr`.

Voir cet extrait du fichier `docker-compose-non-dev.yml`.

```yaml
...
x-superset-volumes:
  &superset-volumes # /app/pythonpath_docker will be appended to the PYTHONPATH in the final container
  ...
  - ./dsfr/dist/fonts/:/app/superset/static/assets/dsfr/fonts
  - ./dsfr/dist/fonts/:/app/superset/static/assets/dsfr/fonts
  - ./dsfr/dist/favicon/:/app/superset/static/assets/dsfr/favicon/
  - ./dsfr/dist/dsfr.module.min.js:/app/superset/static/assets/dsfr/dsfr.module.min.js
  - ./dsfr/dist/dsfr.nomodule.min.js:/app/superset/static/assets/dsfr/dsfr.nomodule.min.js
  - ./dsfr/dist/dsfr.min.css:/app/superset/static/assets/dsfr/dsfr.min.css
  - ./dsfr/dist/utility/utility.min.css:/app/superset/static/assets/dsfr/utility/utility.min.css
  - ./dsfr/dist/icons/:/app/superset/static/assets/dsfr/icons
  - ./dsfr/dist/artwork/pictograms/:/app/superset/static/assets/dsfr/pictograms
  ...
```

Les templates Flask-App-Builder, sur quoi Superset est fondé, `superset/templates/superset/base.html` et `superset/templates/superset/basic.html` sont également montés individuellement commes volumes dans les containers pour **remplacer** les templates originaux. Toutes les pages et SPA (Single-Page-Application React) dérivent de ces templates de base et sont très stables dans le temps.
Voici le diff entre les templates `superset/templates/superset/base.html` de ce dépôt et [celui du dépôt officiel](https://github.com/apache/superset/blob/master/superset/templates/superset/base.html):

```bash
diff --git a/superset/templates/superset/base.html b/superset/templates/superset/base.html
index b226d3aed..02f5ec67a 100644
--- a/superset/templates/superset/base.html
+++ b/superset/templates/superset/base.html
@@ -30,6 +30,9 @@
       href="{{ "" if favicon.href.startswith("http") else assets_prefix }}{{favicon.href}}"
     >
   {% endfor %}
+  <link rel="stylesheet" href="/static/assets/dsfr/dsfr.min.css">
+  <link rel="stylesheet" href="/static/assets/dsfr/utility/utility.min.css">
+  <link rel="stylesheet" href="/static/assets/local/css/tail_css_custom_extra.css">
   {{ css_bundle("theme") }}
 {% endblock %}

@@ -43,4 +46,6 @@
   {{ js_bundle("preamble") }}
   {{ js_bundle('menu') }}
   {% include "tail_js_custom_extra.html" %}
+  <script type="module" src="/static/assets/dsfr.module.min.js"></script>
+  <script type="text/javascript" nomodule src="/static/assets/dsfr.nomodule.min.js"></script>
 {% endblock %}
```

Voici le diff entre les templates `superset/templates/superset/basic.html` de ce dépôt et [celui du dépôt officiel](https://github.com/apache/superset/blob/master/superset/templates/superset/basic.html):

```bash
```

Voici le diff entre les templates `superset/templates/superset/basic.html` de ce dépôt et [celui du dépôt officiel](https://github.com/apache/superset/blob/master/superset/templates/superset/public_welcome.html):

```bash
```


```bash
docker exec superset_app pybabel compile -d superset/translations
```

#### Nginx

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
sudo nginx -x reload
```
