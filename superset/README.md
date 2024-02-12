> AVERTISSEMENT : Ce système de conception est uniquement destiné à être utilisé pour les sites web officiels des services publics français.
> Son objectif principal est de faciliter l'identification des sites gouvernementaux par les citoyens. [Voir les conditions](https://www.systeme-de-design.gouv.fr/utilisation-et-organisation/perimetre-d-application).

Déploiement Docker d'Apache Superset.

Editer `docker/pythonpath_dev/superset_config_docker.py` pour l'adapter à vos besoins (e.g. changer l'icône principale).

Voir `docker/pythonpath_dev/superset_config_docker.example.py` pour d'autres configurations optionnelles non liées directement au thème (macros Jinja, feature flags, cache, ...).

### tldr;

```bash
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.11.1/dsfr-v1.11.1.zip
unzip dsfr-v1.11.1.zip -d dsfr
# DSFR chart optionnel
# wget https://github.com/GouvernementFR/dsfr-chart/releases/download/v1.0.0/dsfr-chart-1.0.0.zip
# unzip dsfr-chart-1.0.0.zip dsfr-chart
git clone --single-branch https://github.com/numerique-gouv/chartsgouv
cd superset/
TAG=3.1.0 docker compose -f docker-compose-non-dev.yml up -d
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

Se déplacer dans le répertoire `superset/` qui contient le nécessaire pour déployer avec Docker Apache Superset configuré en français avec un thème DSFR appliqué globalement à toute l'interface, avec la police Marianne appliquée à toute l'interface, des palettes de couleurs respectueuses des couleurs illustratives du DSFR, les feuilles de style CSS et les fichiers Javascript du DSFR appliqués globalement pour pouvoir intégrer [des composants du DSFR](https://www.systeme-de-design.gouv.fr/elements-d-interface/composants) dans les Zones de texte (optionnel et nécessite d'adapter `TALISMAN_CONFIG` et `HTML_SANITIZATION_SCHEME_EXTENSIONS`):

```bash
cd superset/
```

Tous les fichiers nécessaires sont présents dans ce répertoire, il n'y a pas besoin d'avoir le dépôt principal avec les sources complètes de Superset.

On utilise les images officielles Apache Superset avec un fichier modifié (voir plus bas) du `docker-compose-non-dev.yml` adapté pour la production:

```bash
TAG=3.1.0 docker compose -f docker-compose-non-dev.yml up -d
```

Se rendre sur http://localhost:8088 et rentrer les identifiants :
- nom d'utilisateur : admin
- mot de passe : admin

Si le déploiement est sur un serveur distant, un exemple de fichier de configuration Nginx agissant en reverse-proxy est donné plus bas.

### Détails et possibilités d'adaptation

Le dépôt contient:
- une version modifiée de `docker-compose-non-dev.yml` avec des points de montage supplémentaire (assets supplémentaires, DSFR, templates),
- le fichier de configuration `docker/pythonpath_dev/superset_config_docker.py` qui inclut notamment: 
  - la [variable de configuration de thème](https://preset.io/blog/theming-superset-progress-update/) `THEME_OVERRIDES` pour faire la transposition DSFR => design system de Superset (voir le tableau de transposition des couleurs plus bas),
  - [les variables de configuration des couleurs des charts](https://preset.io/blog/customizing-chart-colors-with-superset-and-preset/) `EXTRA_CATEGORICAL_COLOR_SCHEMES` pour définir une nouvelle palette de couleurs avec [les couleurs illustratives du DSFR](https://gouvernementfr.github.io/dsfr-chart/#colors) pour les graphiques à variables catégorielles,
  - `EXTRA_SEQUENTIAL_COLOR_SCHEMES` pour définir des dégradés de couleur pour les graphiques à variables continues (e.g. plugin Carte de Pays),
- un fichier `assets/images/app_icon.png`, à remplacer par l'image de votre choix pour l'icône de l'application dans le header,
- une version modifiée des templates `superset/templates/superset/{base,basic,spa}.html` pour inclure le DSFR globalement (css et js),
- un fichier `assets/css/tail_css_custom_extra.css` pour corriger l'affichage de certains liens et appliquer la police Marianne globalement,
- un fichier `superset/templates/superset/public_welcome.html`, optionnel pour démontrer la capacité de personnaliser la page d'accueil,
- un fichier `superset/templates/tail_js_custom_extra.html`, optionnel pour démontrer la capacité d'injecter un script globalement sur toutes les pages,
- un fichier `docker/requirements-local.txt`, optionnel où on peut ajouter des paquets Python supplémentaires, [par exemple nécessaires pour certains drivers](https://superset.apache.org/docs/databases/installing-database-drivers) comme `duckdb-engine`,
- les autres fichiers (`docker/docker-entrypoint-initdb.d/examples-init.sh`, `docker/pythonpath_dev/superset_config.py`, `docker/{.env-non-dev,docker-bootstrap.sh,docker-init.sh}` sont les fichiers originaux du dépot principal non modifié, ils viennent de la version 3.1.0 et sont stables dans le temps, sont nécessaires pour le déploiement avec Docker.


Le CSS compilé, le JS compilé, la police Marianne, les icônes, les favicons et les pictogrammes sont montés comme volumes dans les containers dans le chemin `/app/superset/static/assets/dsfr`.

### `docker-compose-non-dev.yml`

```bash
curl -s https://raw.githubusercontent.com/apache/superset/master/docker-compose-non-dev.yml | diff - docker-compose-non-dev.yml
24a25,30
>   - ./assets:/app/superset/static/assets/local
>   - ./templates_overrides:/app/superset/templates_overrides/
>   - ./dsfr/dist/:/app/superset/static/assets/dsfr/
>   - ./dsfr-chart/Charts/:/app/superset/static/assets/dsfr-chart/
>   - ./dsfr/tool/example/img/:/app/superset/static/assets/dsfr/img/
>
```

Les templates Flask-App-Builder, sur quoi Superset est fondé, `superset/templates/superset/base.html` et `superset/templates/superset/basic.html` sont également montés individuellement commes volumes dans les containers pour **remplacer** les templates originaux. Toutes les pages et SPA (Single-Page-Application React) dérivent de ces templates de base et sont très stables dans le temps.

### `public_welcome.html`

```bash
curl -s https://raw.githubusercontent.com/apache/superset/master/superset/templates/superset/public_welcome.html | diff - templates_overrides/superset/public_welcome.html
22c22
< <h2><center>Welcome to Apache Superset</center></h2>
---
> <h2><center>Bienvenue sur Apache Superset</center></h2>
```

### `tail_js_custom_extra.html`

```bash
curl -s https://raw.githubusercontent.com/apache/superset/master/superset/templates/tail_js_custom_extra.html | diff - templates_overrides/tail_js_custom_extra.html
25a26,30
> <script>
> window.addEventListener('DOMContentLoaded', function() {
> });
> </script>
> </script>
> <script
>   type="module"
>   src="{{ assets_prefix }}/static/assets/dsfr/dsfr.module.min.js">
> </script>
> <script
>   type="text/javascript"
>   nomodule
>   src="{{ assets_prefix }}/static/assets/dsfr/dsfr.nomodule.min.js">
> </script>
> <script
>   defer
>     src="{{ assets_prefix }}/static/assets/dsfr-chart/dsfr-chart.umd.js">
> </script>
```

### `base.html`

```bash
curl -s https://raw.githubusercontent.com/apache/superset/master/superset/templates/superset/base.html | diff - templates_overrides/superset/base.html
33a34,53
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/dsfr/dsfr.min.css"
>     />
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/dsfr/utility/utility.min.css"
>     />
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/local/css/tail_css_custom_extra.css"
>     />
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/dsfr-chart/dsfr-chart.css"
>     />
```

### `basic.html`

```bash
curl -s https://raw.githubusercontent.com/apache/superset/master/superset/templates/superset/basic.html | diff - templates_overrides/superset/basic.html
70c70,91
<     {{ css_bundle("theme") }} {% if entry %} {{ css_bundle(entry) }} {% endif %}
---
>     {{ css_bundle("theme") }}
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/dsfr/dsfr.min.css"
>     />
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/dsfr/utility/utility.min.css"
>     />
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/local/css/tail_css_custom_extra.css"
>     />
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/dsfr-chart/dsfr-chart.css"
>     />
>     {% if entry %} {{ css_bundle(entry) }} {% endif %}
131c152,166
```

### `docker/docker-bootstrap.sh`

```bash
curl -s https://raw.githubusercontent.com/apache/superset/master/docker/docker-bootstrap.sh | diff - docker/docker-bootstrap.sh
38c38,53
< #
---
> for theme_filename in $(find /app/superset/static/assets -name "theme*.css"); do
>     sed \
>       -e "s/#20a7c9/#000091/g" \
>       -e "s/#45bed6/#000091/g" \
>       -e "s/#1985a0/#000091/g" \
>       "$theme_filename" > temp.css && mv temp.css "$theme_filename"
> done
> pybabel compile -d superset/translations || true
> cp /app/superset/templates_overrides/superset/base.html /app/superset/templates/superset/base.html
> cp /app/superset/templates_overrides/superset/basic.html /app/superset/templates/superset/basic.html
> cp /app/superset/templates_overrides/superset/spa.html /app/superset/templates/superset/spa.html
> cp /app/superset/templates_overrides/superset/public_welcome.html /app/superset/templates/superset/public_welcome.html
> cp /app/superset/templates_overrides/tail_js_custom_extra.html /app/superset/templates/tail_js_custom_extra.html
> cp /app/superset/static/assets/local/404.html /app/superset/static/assets/404.html
> cp /app/superset/static/assets/local/500.html /app/superset/static/assets/500.html
```

#### Couleurs

| Couleur   | Teinte | Superset                                                         | hex       | DSFR                                                         | hex       |
| --------- | ------ | ---------------------------------------------------------------- | --------- | ------------------------------------------------------------ | --------- |
| text      | label  | ![superset](https://via.placeholder.com/20/879399/000000?text=+) | `#879399` | ![dsfr](https://via.placeholder.com/20/666/000000?text=+)    | `#666`    |
| text      | help   | ![superset](https://via.placeholder.com/20/737373/000000?text=+) | `#737373` | ![dsfr](https://via.placeholder.com/20/666/000000?text=+)    | `#666`    |
| primary   | base   | ![superset](https://via.placeholder.com/20/20A7C9/000000?text=+) | `#20A7C9` | ![dsfr](https://via.placeholder.com/20/000091/000000?text=+) | `#000091` |
| primary   | dark1  | ![superset](https://via.placeholder.com/20/1A85A0/000000?text=+) | `#1A85A0` | ![dsfr](https://via.placeholder.com/20/000091/000000?text=+) | `#000091` |
| primary   | dark2  | ![superset](https://via.placeholder.com/20/156378/000000?text=+) | `#156378` | ![dsfr](https://via.placeholder.com/20/000091/000000?text=+) | `#000091` |
| primary   | light1 | ![superset](https://via.placeholder.com/20/79CADE/000000?text=+) | `#79CADE` | ![dsfr](https://via.placeholder.com/20/6a6af4/000000?text=+) | `#6a6af4` |
| primary   | light2 | ![superset](https://via.placeholder.com/20/A5DAE9/000000?text=+) | `#A5DAE9` | ![dsfr](https://via.placeholder.com/20/cacafb/000000?text=+) | `#cacafb` |
| primary   | light3 | ![superset](https://via.placeholder.com/20/D2EDF4/000000?text=+) | `#D2EDF4` | ![dsfr](https://via.placeholder.com/20/e3e3fd/000000?text=+) | `#e3e3fd` |
| primary   | light4 | ![superset](https://via.placeholder.com/20/E9F6F9/000000?text=+) | `#E9F6F9` | ![dsfr](https://via.placeholder.com/20/ececfe/000000?text=+) | `#ececfe` |
| primary   | light5 | ![superset](https://via.placeholder.com/20/F3F8FA/000000?text=+) | `#F3F8FA` | ![dsfr](https://via.placeholder.com/20/f5f5fe/000000?text=+) | `#f5f5fe` |
| secondary | base   | ![superset](https://via.placeholder.com/20/444E7C/000000?text=+) | `#444E7C` | ![dsfr](https://via.placeholder.com/20/F1493/000000?text=+)  | `FF1493`  |
| secondary | dark1  | ![superset](https://via.placeholder.com/20/363E63/000000?text=+) | `#363E63` | ![dsfr](https://via.placeholder.com/20/000/000000?text=+)    | `#000`    |
| secondary | dark2  | ![superset](https://via.placeholder.com/20/282E4A/000000?text=+) | `#282E4A` | ![dsfr](https://via.placeholder.com/20/000091/000000?text=+) | `#000091` |
| secondary | dark3  | ![superset](https://via.placeholder.com/20/1B1F31/000000?text=+) | `#1B1F31` | ![dsfr](https://via.placeholder.com/20/000091/000000?text=+) | `#000091` |
| secondary | light1 | ![superset](https://via.placeholder.com/20/8E94B0/000000?text=+) | `#8E94B0` | ![dsfr](https://via.placeholder.com/20/000091/000000?text=+) | `#000091` |
| secondary | light2 | ![superset](https://via.placeholder.com/20/B4B8CA/000000?text=+) | `#B4B8CA` | ![dsfr](https://via.placeholder.com/20/000091/000000?text=+) | `#000091` |
| secondary | light3 | ![superset](https://via.placeholder.com/20/D9DBE4/000000?text=+) | `#D9DBE4` | ![dsfr](https://via.placeholder.com/20/000091/000000?text=+) | `#000091` |
| secondary | light4 | ![superset](https://via.placeholder.com/20/ECEEF2/000000?text=+) | `#ECEEF2` | ![dsfr](https://via.placeholder.com/20/e3e3fd/000000?text=+) | `#e3e3fd` |
| secondary | light5 | ![superset](https://via.placeholder.com/20/F5F5F8/000000?text=+) | `#F5F5F8` | ![dsfr](https://via.placeholder.com/20/e3e3fd/000000?text=+) | `#e3e3fd` |
| grayscale | base   | ![superset](https://via.placeholder.com/20/666666/000000?text=+) | `#666666` | ![dsfr](https://via.placeholder.com/20/666/000000?text=+)    | `#666`    |
| grayscale | dark1  | ![superset](https://via.placeholder.com/20/323232/000000?text=+) | `#323232` | ![dsfr](https://via.placeholder.com/20/3a3a3a/000000?text=+) | `#3a3a3a` |
| grayscale | dark2  | ![superset](https://via.placeholder.com/20/000000/000000?text=+) | `#000000` | ![dsfr](https://via.placeholder.com/20/161616/000000?text=+) | `#161616` |
| grayscale | light1 | ![superset](https://via.placeholder.com/20/B2B2B2/000000?text=+) | `#B2B2B2` | ![dsfr](https://via.placeholder.com/20/929292/000000?text=+) | `#929292` |
| grayscale | light2 | ![superset](https://via.placeholder.com/20/E0E0E0/000000?text=+) | `#E0E0E0` | ![dsfr](https://via.placeholder.com/20/e5e5e5/000000?text=+) | `#e5e5e5` |
| grayscale | light3 | ![superset](https://via.placeholder.com/20/F0F0F0/000000?text=+) | `#F0F0F0` | ![dsfr](https://via.placeholder.com/20/eee/000000?text=+)    | `#eee`    |
| grayscale | light4 | ![superset](https://via.placeholder.com/20/F7F7F7/000000?text=+) | `#F7F7F7` | ![dsfr](https://via.placeholder.com/20/f6f6f6/000000?text=+) | `#f6f6f6` |
| grayscale | light5 | ![superset](https://via.placeholder.com/20/FFFFFF/000000?text=+) | `#FFFFFF` | ![dsfr](https://via.placeholder.com/20/fff/000000?text=+)    | `#fff`    |
| error     | base   | ![superset](https://via.placeholder.com/20/E04355/000000?text=+) | `#E04355` | ![dsfr](https://via.placeholder.com/20/ce0500/000000?text=+) | `#ce0500` |
| error     | dark1  | ![superset](https://via.placeholder.com/20/A7323F/000000?text=+) | `#A7323F` | ![dsfr](https://via.placeholder.com/20/ce0500/000000?text=+) | `#ce0500` |
| error     | dark2  | ![superset](https://via.placeholder.com/20/6F212A/000000?text=+) | `#6F212A` | ![dsfr](https://via.placeholder.com/20/000/000000?text=+)    | `#000`    |
| error     | light1 | ![superset](https://via.placeholder.com/20/EFA1AA/000000?text=+) | `#EFA1AA` | ![dsfr](https://via.placeholder.com/20/ce0500/000000?text=+) | `#ce0500` |
| error     | light2 | ![superset](https://via.placeholder.com/20/FAEDEE/000000?text=+) | `#FAEDEE` | ![dsfr](https://via.placeholder.com/20/ffe9e9/000000?text=+) | `#ffe9e9` |
| warning   | base   | ![superset](https://via.placeholder.com/20/FF7F44/000000?text=+) | `#FF7F44` | ![dsfr](https://via.placeholder.com/20/b34000/000000?text=+) | `#b34000` |
| warning   | dark1  | ![superset](https://via.placeholder.com/20/BF5E33/000000?text=+) | `#BF5E33` | ![dsfr](https://via.placeholder.com/20/b34000/000000?text=+) | `#b34000` |
| warning   | dark2  | ![superset](https://via.placeholder.com/20/7F3F21/000000?text=+) | `#7F3F21` | ![dsfr](https://via.placeholder.com/20/000/000000?text=+)    | `#000`    |
| warning   | light1 | ![superset](https://via.placeholder.com/20/FEC0A1/000000?text=+) | `#FEC0A1` | ![dsfr](https://via.placeholder.com/20/b34000/000000?text=+) | `#b34000` |
| warning   | light2 | ![superset](https://via.placeholder.com/20/FFF2EC/000000?text=+) | `#FFF2EC` | ![dsfr](https://via.placeholder.com/20/ffe9e6/000000?text=+) | `#ffe9e6` |
| alert     | base   | ![superset](https://via.placeholder.com/20/FCC700/000000?text=+) | `#FCC700` | ![dsfr](https://via.placeholder.com/20/fbe769/000000?text=+) | `#fbe769` |
| alert     | dark1  | ![superset](https://via.placeholder.com/20/BC9501/000000?text=+) | `#BC9501` | ![dsfr](https://via.placeholder.com/20/fbe769/000000?text=+) | `#fbe769` |
| alert     | dark2  | ![superset](https://via.placeholder.com/20/7D6300/000000?text=+) | `#7D6300` | ![dsfr](https://via.placeholder.com/20/000/000000?text=+)    | `#000`    |
| alert     | light1 | ![superset](https://via.placeholder.com/20/FDE380/000000?text=+) | `#FDE380` | ![dsfr](https://via.placeholder.com/20/fbe769/000000?text=+) | `#fbe769` |
| alert     | light2 | ![superset](https://via.placeholder.com/20/FEF9E6/000000?text=+) | `#FEF9E6` | ![dsfr](https://via.placeholder.com/20/fef7da/000000?text=+) | `#fef7da` |
| success   | base   | ![superset](https://via.placeholder.com/20/5AC189/000000?text=+) | `#5AC189` | ![dsfr](https://via.placeholder.com/20/18753c/000000?text=+) | `#18753c` |
| success   | dark1  | ![superset](https://via.placeholder.com/20/439066/000000?text=+) | `#439066` | ![dsfr](https://via.placeholder.com/20/18753c/000000?text=+) | `#18753c` |
| success   | dark2  | ![superset](https://via.placeholder.com/20/2B6144/000000?text=+) | `#2B6144` | ![dsfr](https://via.placeholder.com/20/000/000000?text=+)    | `#000`    |
| success   | light1 | ![superset](https://via.placeholder.com/20/ACE1C4/000000?text=+) | `#ACE1C4` | ![dsfr](https://via.placeholder.com/20/18753c/000000?text=+) | `#18753c` |
| success   | light2 | ![superset](https://via.placeholder.com/20/EEF8F3/000000?text=+) | `#EEF8F3` | ![dsfr](https://via.placeholder.com/20/b8fec9/000000?text=+) | `#b8fec9` |
| info      | base   | ![superset](https://via.placeholder.com/20/66BCFE/000000?text=+) | `#66BCFE` | ![dsfr](https://via.placeholder.com/20/0063cb/000000?text=+) | `#0063cb` |
| info      | dark1  | ![superset](https://via.placeholder.com/20/4D8CBE/000000?text=+) | `#4D8CBE` | ![dsfr](https://via.placeholder.com/20/0063cb/000000?text=+) | `#0063cb` |
| info      | dark2  | ![superset](https://via.placeholder.com/20/315E7E/000000?text=+) | `#315E7E` | ![dsfr](https://via.placeholder.com/20/000/000000?text=+)    | `#000`    |
| info      | light1 | ![superset](https://via.placeholder.com/20/B3DEFE/000000?text=+) | `#B3DEFE` | ![dsfr](https://via.placeholder.com/20/0063cb/000000?text=+) | `#0063cb` |
| info      | light2 | ![superset](https://via.placeholder.com/20/EFF8FE/000000?text=+) | `#EFF8FE` | ![dsfr](https://via.placeholder.com/20/e8edff/000000?text=+) | `#e8edff` |

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
sudo nginx -s reload
```
