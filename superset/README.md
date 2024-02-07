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

Télécharger le DSFR (fichiers compilés).
```bash
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.11.1/dsfr-v1.11.1.zip
unzip dsfr-v1.11.1.zip -d dsfr
```

Cloner le repo ChartsGouv, seule la branche principale est nécessaire.
Le dépôt contient:
- une version modifiée de `docker-compose-non-dev.yml` avec des points de montage supplémentaire (assets supplémentaires, DSFR, templates,
- une version modifiée des templates `superset/templates/superset/{base,basic}.html` pour inclure le DSFR globalement (css et js),
- un fichier `assets/css/tail_css_custom_extra.css` pour corriger l'affichage de certains liens,
- un fichier `assets/images/app_icon.png`, à remplacer par l'image de votre choix pour l'icône de l'application dans le header,
- un fichier `superset/templates/superset/public_welcome.html`, optionnel pour démontrer la capacité de personnaliser la page d'accueil
- un fichier `superset/templates/tail_js_custom_extra.html`, optionnel pour démontrer la capacité d'injecter un script globalement sur toutes les pages
- un fichier `docker/requirements-local.txt`, où on peut ajouter des paquets Python supplémentaires, ![par exemple nécessaires pour certains drivers](https://superset.apache.org/docs/databases/installing-database-drivers) comme `duckdb-engine`,
- le fichier de configuration `docker/pythonpath_dev/superset_config_docker.py` qui inclut notamment: 
  - la ![variable de configuration de thème](https://preset.io/blog/theming-superset-progress-update/) `THEME_OVERRIDES` pour faire la transposition DSFR => design system de Superset,
  - ![les variables de configuration des couleurs des charts](https://preset.io/blog/customizing-chart-colors-with-superset-and-preset/) `EXTRA_CATEGORICAL_COLOR_SCHEMES` pour définir une nouvelle palette de couleurs avec ![les couleurs illustratives du DSFR](https://gouvernementfr.github.io/dsfr-chart/#colors) pour les graphiques à variables catégorielles,
  - `EXTRA_SEQUENTIAL_COLOR_SCHEMES` pour définir des dégradés de couleur pour les graphiques à variables continues (e.g. plugin Carte de Pays).
- les autres fichiers (`docker/docker-entrypoint-initdb.d/examples-init.sh`, `docker/pythonpath_dev/superset_config.py`, `docker/{.env-non-dev,docker-bootstrap.sh,docker-init.sh}` sont les fichiers originaux du dépot principal non modifié, ils viennent de la version 3.0.0 et sont stables dans le temps.

```bash
git clone --single-branch https://github.com/etalab-ia/chartsgouv
cd superset/
TAG=3.0.0 docker compose -f docker-compose-non-dev.yml up -d
```

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
Voici le diff entre les templates `superset/templates/superset/base.html` de ce dépôt et ![celui du dépôt officiel](https://github.com/apache/superset/blob/master/superset/templates/superset/base.html):

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

Voici le diff entre les templates `superset/templates/superset/basic.html` de ce dépôt et ![celui du dépôt officiel](https://github.com/apache/superset/blob/master/superset/templates/superset/basic.html):

```bash
```

Voici le diff entre les templates `superset/templates/superset/basic.html` de ce dépôt et ![celui du dépôt officiel](https://github.com/apache/superset/blob/master/superset/templates/superset/public_welcome.html):

```bash
```


```bash
docker exec superset_app pybabel compile -d superset/translations
```
