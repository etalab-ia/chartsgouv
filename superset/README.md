> AVERTISSEMENT : Ce système de conception est uniquement destiné à être utilisé pour les sites web officiels des services publics français.
> Son objectif principal est de faciliter l'identification des sites gouvernementaux par les citoyens. [Voir les conditions](https://www.systeme-de-design.gouv.fr/utilisation-et-organisation/perimetre-d-application).

## Cliquer pour voir le résultat en vidéo
<a href="https://www.youtube.com/watch?v=0o1JbSbwoM8" title="Regarder sur YouTube">
    <img src="/images/demo_graphes_echarts.png" width="750" alt="Regarder sur YouTube">
</a>

## Parcourir les dashboards d'exemple
- [Dashboard SILL](http://chartsgouv.lab.sspcloud.fr/superset/dashboard/sill/)
- [Graphes Apache Echarts avec couleurs DSFR](http://chartsgouv.lab.sspcloud.fr/superset/dashboard/demo-echarts/)
- [Composants DSFR et DSFR charts](http://chartsgouv.lab.sspcloud.fr/superset/dashboard/demo-dsfr/?standalone=2)

## Déploiement Docker d'Apache Superset
- police Marianne :fr: (voir [docker-compose-non-dev.yml](docker-compose-non-dev.yml#L27) et [tail_css_extra_custom.css](assets/css/tail_css_extra_custom.css) et les [templates overrides](templates_overrides/superset))
- version française :fr: (voir [docker/docker-dsfr.sh](docker/docker-dsfr.sh#L11))
- transposition des couleurs DSFR :art: (voir `THEME_OVERRIDES` dans [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py#L148))
- palettes de couleurs pour les graphiques :art:  (voir `EXTRA_CATEGORICAL_COLOR_SCHEMES` et `EXTRA_SEQUENTIAL_COLOR_SCHEMES` dans [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py#L235))
- pages d'erreurs :x: [404.html](assets/404.html) et [500.html](assets/500.html) du [DSFR](https://www.systeme-de-design.gouv.fr/elements-d-interface/modeles/page-d-erreurs)
- [composants DSFR](https://www.systeme-de-design.gouv.fr/elements-d-interface/composants) :control_knobs: dans les zones de texte (optionnel, nécessite d'adapter `HTML_SANITIZATION_SCHEMA_EXTENSIONS`) => développement futur de plugins spécifiques par la communauté pour fiabiliser la solution actuelle
- [DSFR charts](https://gouvernementfr.github.io/dsfr-chart/) :chart_with_upwards_trend: (optionnel, necéssite d'adapter `TALISMAN_CONFIG`) => développement futur de plugins spécifiques par la communauté pour fiabiliser la solution actuelle

Editer [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py) pour l'adapter à vos besoins (e.g. rajouter des [feature flags](https://github.com/apache/superset/blob/master/RESOURCES/FEATURE_FLAGS.md)), ou remplacer des fichiers de ce dépôt montés dans le container, par exemple:
- [app_icon.png](assets/images/app_icon.png) pour modifier l'icone dans l'en-tete,
- [tail_css_custom_extra.css](assets/css/tail_css_custom_extra.css) pour rajouter des règles CSS globales,
- [tail_js_custom_extra.html](templates_overrides/tail_js_custom_extra.html) pour rajouter des scripts JS globaux,
- [public_welcome.html](templates_overrides/superset/public_welcome.html) pour personnaliser la page d'accueil,
- [base.html](templates_overrides/superset/base.html#L49) pour ajouter ou non (commenter/décommenter) l'entièreté du DSFR/DSFR-Chart,
- [basic.html](templates_overrides/superset/basic.html#L86) pour ajouter ou non (commenter/décommenter) l'entièreté du DSFR/DSFR-Chart,
- [404.html](assets/404.html) pour [ajouter un formulaire de contact](https://github.com/qleroy/chartsgouv/blob/refactor-300/superset/assets/404.html#L29),
- [500.html](assets/500.html) pour [ajouter un formulaire de contact](https://github.com/qleroy/chartsgouv/blob/refactor-300/superset/assets/500.html#L22).

Voir [docker/pythonpath_dev/superset_config_docker.example.py](docker/pythonpath_dev/superset_config_docker.example.py) pour d'autres configurations optionnelles non liées directement au thème (macros Jinja, feature flags, cache, ...).

Voir [docker/pythonpath_dev/superset_config_docker.unsecure.py](docker/pythonpath_dev/superset_config_docker.unsecure.py#L330) pour une version provisoire (13/02/2024) d'une configuration non securisée mais fonctionnelle pour inclure les composants DSFR dans les zones de Texte et les DSFR-Chart avec le plugin [Handlebars](https://handlebarsjs.com).

## TL;DR

Ce dépôt contient des éléments de configuration pour Superset, ce n'est pas un fork de Superset et ce n'est pas lié à une version particulière de Superset.

Pour l'inclure à votre installation actuelle, regarder:
- `THEME_OVERRIDES` dans [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py#L148),
- les points de montage additionnels dans [docker-compose-non-dev.yml](docker-compose-non-dev.yml#L25),
- et le script [docker/docker-dsfr.sh](docker/docker-dsfr.sh).

Pour une nouvelle installation, ne pas oublier de générer une `SUPERSET_SECRET_KEY` et de la sauvegarder, et suivre le snippet ci-dessous pour télécharger le DSFR, cloner ce dépôt et démarrer le déploiement Docker en local.

```bash
# Definir une SUPERSET_SECRET_KEY et la sauvegarder !
export SUPERSET_SECRET_KEY="$(openssl rand -base64 42)"
echo "$SUPERSET_SECRET_KEY" > .secret_key
# Télécharger le DSFR
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.11.1/dsfr-v1.11.1.zip
unzip dsfr-v1.11.1.zip -d dsfr
# Optionnel: Télécharger DSFR-chart (en beta)
# wget https://github.com/GouvernementFR/dsfr-chart/releases/download/v1.0.0/dsfr-chart-1.0.0.zip
# unzip dsfr-chart-1.0.0.zip -d dsfr-chart
git clone --single-branch https://github.com/numerique-gouv/chartsgouv
cd superset/
TAG=3.1.0 docker compose -f docker-compose-non-dev.yml up -d
# Se rendre sur localhost:8088 avec identifiants admin/admin
```

## Pas à pas

Télécharger le [DSFR](https://github.com/GouvernementFR/dsfr) (fichiers compilés), ici la version v1.11.1 datée du 01/02/2024. Ces fichiers seront montés dans le container Superset sur le chemin `/app/superset/static/assets/dsfr`. Obligatoire pour inclure la police Marianne globalement. Ajoute aussi les icônes, pictogrammes:
```bash
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.11.1/dsfr-v1.11.1.zip
unzip dsfr-v1.11.1.zip -d dsfr
# Le dossier dsfr/dist est monté dans le container superset_app:/app/superset/static/assets/dsfr
# voir docker-compose-non-dev.yml
# x-superset-volumes:
#   &superset-volumes
#   - ./dsfr/dist:/app/superset/static/assets/dsfr
```

Optionnel: Télécharger [DSFR-chart](https://github.com/GouvernementFR/dsfr-chart) (fichiers compilés), ici la version v1.0.0 datée du 29/11/2023. Ces fichiers seront montés dans le container Superset sur le chemin `/app/superset/static/assets/dsfr-chart`.
```bash
wget https://github.com/GouvernementFR/dsfr-chart/releases/download/v1.0.0/dsfr-chart-1.0.0.zip
unzip dsfr-chart-1.0.0.zip -d dsfr-chart
# Le dossier dsfr-chart/Charts est monté dans le container superset_app:/app/superset/static/assets/dsfr-chart
# voir docker-compose-non-dev.yml
# x-superset-volumes:
#   &superset-volumes
#   - ./dsfr-chart/Charts:/app/superset/static/assets/dsfr-chart
```

Cloner le dépôt ChartsGouv, seule la branche principale est nécessaire.

```bash
git clone --single-branch https://github.com/numerique-gouv/chartsgouv
```

Se déplacer dans le répertoire `superset/`:

```bash
cd superset/
```

Générer une [clé secrète](https://superset.apache.org/docs/installation/configuring-superset/#specifying-a-secret_key) et la sauvegarder en sécurité:

```bash
export SUPERSET_SECRET_KEY="$(openssl rand -base64 42)"
echo "$SUPERSET_SECRET_KEY" > .secret_key
# Aussi possible de définir la variable SECRET_KEY dans docker/pythonpath_dev/superset_config_docker.py
# Attention, c'est bien SUPERSET_SECRET_KEY comme variable d'environnement,
# et SECRET_KEY comme variable python dans superset_config_docker.py
```

Tous les fichiers nécessaires sont présents dans ce répertoire, il n'y a pas besoin d'avoir le dépôt principal avec les sources complètes de Superset.

On utilise les images officielles d'Apache Superset (en l'occurence depuis le registre [apachesuperset.docker.scarf.sf](docker-compose-non-dev.yml#L17), voir [les précautions pour scarf](https://superset.apache.org/docs/frequently-asked-questions/#does-superset-collect-any-telemetry-data) ou utiliser un autre registre) avec un fichier modifié ([voir plus bas](#docker-compose-non-devyml)) du `docker-compose-non-dev.yml` adapté pour la production:

```bash
TAG=3.1.0 docker compose -f docker-compose-non-dev.yml up -d
```

Se rendre sur http://localhost:8088 et rentrer les identifiants :
- nom d'utilisateur : admin
- mot de passe : admin

Si le déploiement est sur un serveur distant, un exemple de fichier de configuration Nginx agissant en reverse-proxy est donné [plus bas](#nginx).

## Détails

Le dépôt contient:
- la spécification pour un déploiement Docker en production [docker-compose-non-dev.yml](docker-compose-non-dev.yml) avec des points de montage supplémentaires (assets supplémentaires, DSFR, templates overrides):
  - `./assets:/app/superset/static/assets/local` pour inclure [app_icon.png](assets/images/app_icon.png) et [tail_css_custom_extra.css](assets/css/tail_css_custom_extra.css), les pages d'erreur [404.html](assets/404.html) et [500.html](assets/500.html),
  - `./templates_overrides:/app/superset/templates_overrides` pour remplacer les templates [public_welcome.html](templates_overrides/superset/public_welcome.html), [base.html](templates_overrides/superset/base.html), [basic.html](templates_overrides/superset/basic.html) et [tail_js_custom_extra.html](templates_overrides/tail_js_custom_extra.html),
  - `./dsfr/dist:/app/superset/static/assets/dsfr` pour inclure [la police Marianne](https://www.systeme-de-design.gouv.fr/elements-d-interface/fondamentaux-de-l-identite-de-l-etat/typographie), [CSS et JS](https://www.systeme-de-design.gouv.fr/utilisation-et-organisation/developpeurs/prise-en-main), [icônes](https://www.systeme-de-design.gouv.fr/elements-d-interface/fondamentaux-techniques/icone) et [pictogrammes](https://www.systeme-de-design.gouv.fr/elements-d-interface/fondamentaux-techniques/pictogramme) du DSFR,
  - `./dsfr-chart/Charts:/app/superset/static/assets/dsfr-chart` pour inclure [CSS et JS supplémentaires](https://github.com/GouvernementFR/dsfr-chart?tab=readme-ov-file#configuration-de-votre-projet) pour les DSFR-Chart,
- le script [docker/docker-dsfr.sh](docker/docker-dsfr.sh) pour remplacer certaines teintes de bleu spécifiques aux pages génériques FAB par le bleu France, compiler les fichiers de traduction FAB, déplacer individuellement les templates et pages 404 et 500 à l'emplacement approprié pour que le remplacement soit effectif,
- le script [docker/docker-bootstrap.sh](docker/docker-bootstrap.sh#L38) modifié pour sourcer [docker/docker-dsfr.sh](docker/docker-dsfr.sh),
- le fichier de configuration [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py) qui inclut notamment: 
  - la [variable de configuration de thème](https://preset.io/blog/theming-superset-progress-update/) `THEME_OVERRIDES` pour faire la transposition design system de Superset => DSFR (voir le tableau de transposition des couleurs [plus bas](#couleurs)),
  - [les variables de configuration des couleurs des charts](https://preset.io/blog/customizing-chart-colors-with-superset-and-preset/) `EXTRA_CATEGORICAL_COLOR_SCHEMES` pour définir une nouvelle palette de couleurs avec [les couleurs illustratives du DSFR](https://gouvernementfr.github.io/dsfr-chart/#colors) pour les graphiques à variables catégorielles,
  - `EXTRA_SEQUENTIAL_COLOR_SCHEMES` pour définir des dégradés de couleur pour les graphiques à variables continues (e.g. plugin Carte de Pays),
- un fichier [superset/templates/tail_js_custom_extra.html](superset/templates/tail_js_custom_extra.html), pour inclure globalement les modules JS du DSFR,
- un fichier [assets/images/app_icon.png](assets/images/app_icon.png), à remplacer par l'image de votre choix pour l'icône de l'application dans l'en-tête,
- une version modifiée des templates `superset/templates/superset/{base,basic}.html` pour inclure le DSFR globalement (css et js),
- un fichier `assets/css/tail_css_custom_extra.css` pour corriger l'affichage de certains liens et corriger l'application de la police Marianne globalement,
- un fichier `superset/templates/superset/public_welcome.html`, optionnel pour démontrer la capacité de personnaliser la page d'accueil,
- un fichier `docker/requirements-local.txt`, optionnel où on peut ajouter des paquets Python supplémentaires, [par exemple nécessaires pour certains drivers](https://superset.apache.org/docs/databases/installing-database-drivers) comme `duckdb-engine`,
- les autres fichiers (`docker/docker-entrypoint-initdb.d/examples-init.sh`, `docker/pythonpath_dev/superset_config.py`, `docker/{.env-non-dev,docker-init.sh}`) sont les fichiers originaux du dépot principal non modifiés, ils viennent de la version 3.1.0 et sont stables dans le temps, sont nécessaires pour le déploiement avec Docker.

Ci-dessous les comparaisons des fichiers relatifs au déploiement Docker du dépôt principal (à gauche) avec les diff apportées par ce dépôt (à droite):

### `docker-compose-non-dev.yml`

![Capture d'écran lisible du diff entre le fichier du dépôt principal et sa version modifiée de ce dépôt](/images/screenshot_docker-compose-non-dev.yml.png)

```bash
$ curl -s https://raw.githubusercontent.com/apache/superset/master/docker-compose-non-dev.yml | diff - docker-compose-non-dev.yml
24a25,30
>   - ./assets:/app/superset/static/assets/local
>   - ./templates_overrides:/app/superset/templates_overrides
>   - ./dsfr/dist:/app/superset/static/assets/dsfr
>  #- ./dsfr-chart/Charts:/app/superset/static/assets/dsfr-chart
```

### `docker-bootstrap.sh`

![Capture d'écran lisible du diff entre le fichier du dépôt principal et sa version modifiée de ce dépôt](/images/screenshot_docker-bootstrap.sh.png)

```bash
$ curl -s https://raw.githubusercontent.com/apache/superset/master/docker/docker-bootstrap.sh | diff - docker/docker-bootstrap.sh
38c38,39
< #
---
> source docker/docker-dsfr.sh
>
```

### `public_welcome.html`

![Capture d'écran lisible du diff entre le fichier du dépôt principal et sa version modifiée de ce dépôt](/images/screenshot_public_welcome.html.png)

```bash
$ curl -s https://raw.githubusercontent.com/apache/superset/master/superset/templates/superset/public_welcome.html | diff - templates_overrides/superset/public_welcome.html
22c22
< <h2><center>Welcome to Apache Superset</center></h2>
---
> <h2><center>Bienvenue sur Apache Superset</center></h2>
```

### `base.html`
![Capture d'écran lisible du diff entre le fichier du dépôt principal et sa version modifiée de ce dépôt](/images/screenshot_base.html.png)

```bash
$ curl -s https://raw.githubusercontent.com/apache/superset/master/superset/templates/superset/base.html | diff - templates_overrides/superset/base.html
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
>     <!--
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/dsfr-chart/dsfr-chart.css"
>     />
>     -->
```

### `basic.html`

![Capture d'écran lisible du diff entre le fichier du dépôt principal et sa version modifiée de ce dépôt](/images/screenshot_basic.html.png)

```bash
$ curl -s https://raw.githubusercontent.com/apache/superset/master/superset/templates/superset/basic.html | diff - templates_overrides/superset/basic.html
70c70,91
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
>     <!--
>     <link
>       rel="stylesheet"
>       type="text/css"
>       href="{{ assets_prefix }}/static/assets/dsfr-chart/dsfr-chart.css"
>     />
>     -->
131c152,166
```

### `tail_js_custom_extra.html`

![Capture d'écran lisible du diff entre le fichier du dépôt principal et sa version modifiée de ce dépôt](/images/screenshot_tail_js_custom_extra.html.png)

```bash
$ curl -s https://raw.githubusercontent.com/apache/superset/master/superset/templates/tail_js_custom_extra.html | diff - templates_overrides/tail_js_custom_extra.html
25a26,41
>
> <script
>   type="module"
>   src="{{ assets_prefix }}/static/assets/dsfr/dsfr.module.min.js">
> </script>
> <script
>   type="text/javascript"
>   nomodule
>   src="{{ assets_prefix }}/static/assets/dsfr/dsfr.nomodule.min.js">
> </script>
> <!--
> <script
>   defer
>     src="{{ assets_prefix }}/static/assets/dsfr-chart/dsfr-chart.umd.js">
> </script>
> -->
```

Les fichiers supplémentaires:

### `docker-dsfr.sh`

```bash
for theme_filename in $(find /app/superset/static/assets -name "theme*.css"); do
    sed \
      -e "s/#20a7c9/#000091/g" \
      -e "s/#45bed6/#000091/g" \
      -e "s/#1985a0/#000091/g" \
      "$theme_filename" > temp.css && mv temp.css "$theme_filename"
done

pybabel compile -d superset/translations || true

cp /app/superset/templates_overrides/superset/{base,basic,public_welcome}.html /app/superset/templates/superset/
cp /app/superset/templates_overrides/tail_js_custom_extra.html /app/superset/templates/tail_js_custom_extra.html
cp /app/superset/static/assets/local/404.html /app/superset/static/assets/404.html
cp /app/superset/static/assets/local/500.html /app/superset/static/assets/500.html
```

### `tail_css_custom_extra.css`

```css
a {
  background-image: none !important;
}

[href] {
  background-image: none !important;
}

body {
  font-family: Marianne !important;
}

h1, h2, h3, h4, h5, h6,
.h1, .h2, .h3, .h4, .h5, .h6 {
  font-family: Marianne !important;
}
```

### Couleurs

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
| secondary | base   | ![superset](https://via.placeholder.com/20/444E7C/000000?text=+) | `#444E7C` | ![dsfr](https://via.placeholder.com/20/000091/000000?text=+)  | `#000091`  |
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

### Nginx

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

### Captures d'écran

| Description | Image |
| --- | --- |
|Police Marianne :fr:, Couleurs :art:|![demo_sill](/images/demo_sill.png)|
|Palettes de couleurs :art:|![demo_graphes_echarts](/images/demo_graphes_echarts.png)|
|Composants DSFR :control_knobs:|![demo_dsfr1](/images/demo_dsfr1.png)|
|DSFR Charts :chart_with_upwards_trend:|![demo_dsfr_chart1.png](/images/demo_dsfr_chart1.png)|
|DSFR Charts :chart_with_upwards_trend:|![demo_dsfr_chart2.png](/images/demo_dsfr_chart2.png)|
|Page d'erreur 404 :x:|![error404](/images/error404.png)|
