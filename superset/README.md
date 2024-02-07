> AVERTISSEMENT : Ce système de conception est uniquement destiné à être utilisé pour les sites web officiels des services publics français.
> Son objectif principal est de faciliter l'identification des sites gouvernementaux par les citoyens. [Voir les conditions](https://www.systeme-de-design.gouv.fr/utilisation-et-organisation/perimetre-d-application).

Télécharger le DSFR (fichiers compilés).
```bash
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.11.1/dsfr-v1.11.1.zip
unzip dsfr-v1.11.1.zip -d dsfr
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
```

Voici le diff entre les templates `superset/templates/superset/basic.html` de ce dépôt et ![celui du dépôt officiel](https://github.com/apache/superset/blob/master/superset/templates/superset/basic.html):

```bash
```

Voici le diff entre les templates `superset/templates/superset/basic.html` de ce dépôt et ![celui du dépôt officiel](https://github.com/apache/superset/blob/master/superset/templates/superset/public_welcome.html):

```bash
```

Cloner le repo ChartsGouv, seule la branche principale est nécessaire.
```bash
git clone --single-branch https://github.com/etalab-ia/chartsgouv
cd superset/
TAG=3.0.0 docker compose -f docker-compose-non-dev.yml up -d
```

```bash
docker exec superset_app pybabel compile -d superset/translations
```
