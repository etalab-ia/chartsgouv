> AVERTISSEMENT : Ce système de conception est uniquement destiné à être utilisé pour les sites web officiels des services publics français.
> Son objectif principal est de faciliter l'identification des sites gouvernementaux par les citoyens. [Voir les conditions](https://www.systeme-de-design.gouv.fr/version-courante/fr/premiers-pas/perimetre-d-application).

## Cliquer pour voir le résultat en vidéo
<a href="https://www.youtube.com/watch?v=0o1JbSbwoM8" title="Regarder sur YouTube">
    <img src="/images/demo_graphes_echarts.png" width="750" alt="Regarder sur YouTube">
</a>


# Thème Superset DSFR

## Introduction
Ce guide présente l’intégration d’un thème **DSFR (Design Système de l’État)** dans **Apache Superset**. Il décrit les principaux éléments configurables afin d’adapter l’interface aux standards graphiques de l’administration. C'est un exemple de déploiement avec Docker fourni **à titre illustratif pour faciliter la prise en main**. Cet exemple n’a cependant **pas vocation à couvrir l’ensemble des bonnes pratiques de sécurité ou de configuration nécessaires pour une mise en production** : il doit être considéré comme une démonstration technique et non comme un modèle d’infrastructure prêt à l’emploi. D'autres exemples sont données dans [docs/installation/](https://github.com/etalab-ia/chartsgouv/blob/main/docs/installation) (🚧).

## Principales personnalisations disponibles
- :fr: police Marianne (voir [docker-compose-image-tag.yml](docker-compose-image-tag.yml#L27) et [tail_css_custom_extra.css](assets/css/tail_css_custom_extra.css) et les [templates overrides](templates_overrides/superset))
- :art: transposition des couleurs DSFR (voir `THEME_OVERRIDES` dans [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py#L92))
- :art: palettes de couleurs catégorielles et séquentielles pour les graphiques (voir `EXTRA_CATEGORICAL_COLOR_SCHEMES` et `EXTRA_SEQUENTIAL_COLOR_SCHEMES` dans [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py#L279))
- :x: pages d'erreurs [404.html](assets/404.html) et [500.html](assets/500.html) du [DSFR](https://www.systeme-de-design.gouv.fr/version-courante/fr/modeles/pages-types)
- :control_knobs: [composants DSFR](https://www.systeme-de-design.gouv.fr/version-courante/fr/composants) dans les zones de texte (optionnel, nécessite d'adapter `HTML_SANITIZATION_SCHEMA_EXTENSIONS`) => développement futur d'extensions spécifiques par la communauté pour fiabiliser la solution actuelle
- :chart_with_upwards_trend: [DSFR charts](https://gouvernementfr.github.io/dsfr-chart/) (optionnel, necéssite d'adapter `TALISMAN_CONFIG`) => développement futur d'extensions spécifiques par la communauté pour fiabiliser la solution actuelle.

## Adapter la configuration à vos besoins
Éditer [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py) pour l'adapter à vos besoins (e.g. rajouter des [feature flags](https://github.com/apache/superset/blob/master/RESOURCES/FEATURE_FLAGS.md)), ou remplacer des fichiers de ce dépôt montés dans le container, par exemple:
- [app_icon.png](assets/images/app_icon.png) pour modifier l'icone dans l'en-tête,
- [tail_css_custom_extra.css](assets/css/tail_css_custom_extra.css) pour rajouter des règles CSS globales,
- [tail_js_custom_extra.html](templates_overrides/tail_js_custom_extra.html) pour rajouter des scripts JS globaux,
- [head_custom_extra.html](templates_overrides/head_custom_extra.html),
- [public_welcome.html](templates_overrides/superset/public_welcome.html) pour personnaliser la page d'accueil,
- [404.html](assets/404.html) pour [ajouter un formulaire de contact](https://github.com/qleroy/chartsgouv/blob/refactor-300/superset/assets/404.html#L29),
- [500.html](assets/500.html) pour [ajouter un formulaire de contact](https://github.com/qleroy/chartsgouv/blob/refactor-300/superset/assets/500.html#L22).

## TL;DR

Ce dépôt fournit des éléments de configuration pour intégrer le **thème DSFR** dans **Apache Superset**.
👉 **Ce n’est pas un fork de Superset** et **il n’est pas lié à une version spécifique** de Superset.

### Intégrer le thème à une installation existante

Pour l'inclure à votre installation actuelle, regarder:
- `THEME_OVERRIDES` dans [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py#L192),
- `EXTRA_CATEGORICAL_COLOR_SCHEMES` dans [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py#L279),
- `EXTRA_SEQUENTIAL_COLOR_SCHEMES` dans [docker/pythonpath_dev/superset_config_docker.py](docker/pythonpath_dev/superset_config_docker.py#L411),
- les points de montage additionnels dans [docker-compose-image-tag.yml](docker-compose-image-tag.yml#L25) pour inclure le DSFR,
- et le script [docker/docker-dsfr.sh](docker/docker-dsfr.sh).

### Nouvelle installation (exemple rapide en local)

Pour une nouvelle installation suivre le snippet ci-dessous pour télécharger le DSFR, cloner ce dépôt et démarrer le déploiement Docker en local.

```bash
# Cloner le dépôt
git clone https://github.com/etalab-ia/chartsgouv
cd chartsgouv/superset/

# Définir une clé secrète Superset et l’enregistrer dans docker/.env-local
echo SUPERSET_SECRET_KEY="$(openssl rand -base64 42)" > docker/.env-local

# Télécharger et extraire le DSFR
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.14.0/dsfr-v1.14.0.zip
unzip dsfr-v1.14.0.zip -d dsfr

# Lancer Superset avec Docker (ici version 5.0.0)
TAG=5.0.0 docker compose -f docker-compose-image-tag.yml up -d

# Accéder à l’interface
# → http://localhost:8088
# Identifiants par défaut : admin / admin
```

## Pas à pas

Télécharger le [DSFR](https://github.com/GouvernementFR/dsfr) (fichiers compilés), ici la version v1.14.0 datée du 25/06/2025. Ces fichiers seront montés dans le container Superset sur le chemin `/app/superset/static/assets/dsfr`. Obligatoire pour inclure la police Marianne globalement. Ajoute aussi les icônes, pictogrammes:
```bash
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.14.0/dsfr-v1.14.0.zip
unzip dsfr-v1.14.0.zip -d dsfr
# Le dossier dsfr/dist peut être monté dans le container superset_app:/app/superset/static/assets/dsfr
```

Optionnel: Télécharger [DSFR-chart](https://github.com/GouvernementFR/dsfr-chart) (fichiers compilés), ici la version v2.0.4 datée du 19/05/2025. Ces fichiers seront montés dans le container Superset sur le chemin `/app/superset/static/assets/dsfr-chart`.
```bash
wget https://github.com/GouvernementFR/dsfr-chart/releases/download/v2.0.4/dsfr-chart-v2.0.4.zip
unzip dsfr-chart-v2.0.4.zip -d dsfr-chart
# Le dossier dsfr-chart/Charts peut être monté dans le container superset_app:/app/superset/static/assets/dsfr-chart
```

Cloner le dépôt ChartsGouv:

```bash
git clone https://github.com/etalab-ia/chartsgouv
cd chartsgouv/
```

Se déplacer dans le répertoire `superset/`:

```bash
cd superset/
```

Générer une [clé secrète](https://superset.apache.org/docs/installation/configuring-superset/#specifying-a-secret_key) et la sauvegarder dans `docker/.env-local`. Pour rappel, un déploiement en production nécessite des ajustements supplémentaires qui ne sont pas l'objet de ce guide.

```bash
echo SUPERSET_SECRET_KEY="$(openssl rand -base64 42)" > docker/.env-local
```

Tous les fichiers nécessaires sont présents dans ce répertoire, il n'y a pas besoin d'avoir le dépôt principal avec les sources complètes de Superset.

On utilise les images officielles d'Apache Superset (depuis le registre [apachesuperset.docker.scarf.sf](docker-compose-image-tag.yml#L24), voir [les précautions pour scarf](https://superset.apache.org/docs/frequently-asked-questions/#does-superset-collect-any-telemetry-data) ou utiliser un autre registre) avec un fichier modifié ([voir plus bas](#docker-compose-image-tag.yml)) du `docker-compose-image-tag.yml` pour ajouter des points de montage:

```bash
TAG=5.0.0 docker compose -f docker-compose-image-tag.yml up -d
```

Se rendre sur http://localhost:8088 et rentrer les identifiants :
- nom d'utilisateur : admin
- mot de passe : admin

## Détails

Ce guide fournit une configuration complète pour déployer Apache Superset avec une intégration poussée du Design Système de l'État (DSFR), à l’aide de Docker. Il comprend :

### 📦 Fichier docker-compose-image-tag.yml
Ce fichier permet de déployer Superset avec des volumes personnalisés pour intégrer des ressources spécifiques (icône, CSS, pages d’erreur) :

- 🖼️ `assets/images/app_icon.png` : icône de l'application, visible dans le coin supérieur gauche (modifiable),
- 🎨 `assets/css/tail_css_custom_extra.css` : correctifs CSS pour les liens et la police Marianne,
- ❌ `assets/404.html`, `assets/500.html` : pages d’erreur du DSFR,
- 🎛️ `dsfr/`: ressources DSFR (police Marianne, fichiers CSS/JS, icônes et pictogrammes),
- 📈 `dsfr-chart/`: extensions DSFR chart (fichiers CSS/JS).
- 🏠 `templates_overrides/superset/public_welcome.html` : page d’accueil (modifiable),
- 🧩 `templates_overrides/head_custom_extra.html`, `templates_overrides/tail_js_custom_extra.html` : pour charger globalement les ressources DSFR (CSS & JS).

### 🛠 Scripts Docker

- `docker/docker-dsfr.sh`: Remplacer certaines couleurs bleues par le bleu France, déplacer les fichiers personnalisés (templates, erreurs) dans les répertoires attendus par Superset (`/app/superset/templates/` et `/app/superset/static/assets/`).
- `docker/docker-bootstrap.sh` : Script de démarrage pour sourcer automatiquement docker-dsfr.sh.

### ⚙️ Configuration Superset `docker/pythonpath_dev/superset_config_docker.py`

Inclut:
- 🇫🇷 `THEME_OVERRIDES` : permet la transposition du thème Superset vers le DSFR (voir les correspondances de couleurs),
- 🎨 `EXTRA_CATEGORICAL_COLOR_SCHEMES` : définit une palette de couleurs illustratives DSFR pour les graphiques catégoriels,
- 🎨 `EXTRA_SEQUENTIAL_COLOR_SCHEMES` : définit des dégradés de couleurs pour les graphiques continus (ex : carte de pays).

Les extraits suivants présentent, sous forme de diffs, les modifications à appliquer dans les principaux fichiers du projet afin d’activer le thème et de charger les ressources associées.

### `docker-compose-image-tag.yml`

```diff
 -superset-volumes:
  &superset-volumes # /app/pythonpath_docker will be appended to the PYTHONPATH in the final container
  - ./docker:/app/docker
  - superset_home:/app/superset_home
+  - ./assets:/app/superset/static/assets/local
+  - ./templates_overrides:/app/superset/templates_overrides
+  - ./dsfr/dist:/app/superset/static/assets/dsfr
+  #- ./dsfr-chart/dsfr-chart/dist/DSFRChart:/app/superset/static/assets/dsfr-chart
```

### `head_custom_extra.html`

```diff
+ <link
+     rel="stylesheet"
+     type="text/css"
+     href="{{ assets_prefix }}/static/assets/dsfr/dsfr.min.css"
+ />
+ <link
+     rel="stylesheet"
+     type="text/css"
+     href="{{ assets_prefix }}/static/assets/dsfr/utility/utility.min.css"
+ />
+ <link
+     rel="stylesheet"
+     type="text/css"
+     href="{{ assets_prefix }}/static/assets/local/css/tail_css_custom_extra.css"
+ />
```

### `tail_js_custom_extra.html`

```diff
+ <script
+   type="module"
+   src="{{ assets_prefix }}/static/assets/dsfr/dsfr.module.min.js">
+ </script>
+ <script
+   type="text/javascript"
+   nomodule
+   src="{{ assets_prefix }}/static/assets/dsfr/dsfr.nomodule.min.js">
+ </script>
```

### Couleurs

| Couleur   | Teinte | Superset                                                         | hex       | DSFR                                                         | hex       |
| --------- | ------ | ---------------------------------------------------------------- | --------- | ------------------------------------------------------------ | --------- |
| text      | label  | ![superset](https://dummyimage.com/20/879399/000?text=+) | `#879399` | ![dsfr](https://dummyimage.com/20/666/000?text=+)    | `#666`    |
| text      | help   | ![superset](https://dummyimage.com/20/737373/000?text=+) | `#737373` | ![dsfr](https://dummyimage.com/20/666/000?text=+)    | `#666`    |
| primary   | base   | ![superset](https://dummyimage.com/20/20A7C9/000?text=+) | `#20A7C9` | ![dsfr](https://dummyimage.com/20/000091/000?text=+) | `#000091` |
| primary   | dark1  | ![superset](https://dummyimage.com/20/1A85A0/000?text=+) | `#1A85A0` | ![dsfr](https://dummyimage.com/20/000091/000?text=+) | `#000091` |
| primary   | dark2  | ![superset](https://dummyimage.com/20/156378/000?text=+) | `#156378` | ![dsfr](https://dummyimage.com/20/000091/000?text=+) | `#000091` |
| primary   | light1 | ![superset](https://dummyimage.com/20/79CADE/000?text=+) | `#79CADE` | ![dsfr](https://dummyimage.com/20/6a6af4/000?text=+) | `#6a6af4` |
| primary   | light2 | ![superset](https://dummyimage.com/20/A5DAE9/000?text=+) | `#A5DAE9` | ![dsfr](https://dummyimage.com/20/cacafb/000?text=+) | `#cacafb` |
| primary   | light3 | ![superset](https://dummyimage.com/20/D2EDF4/000?text=+) | `#D2EDF4` | ![dsfr](https://dummyimage.com/20/e3e3fd/000?text=+) | `#e3e3fd` |
| primary   | light4 | ![superset](https://dummyimage.com/20/E9F6F9/000?text=+) | `#E9F6F9` | ![dsfr](https://dummyimage.com/20/ececfe/000?text=+) | `#ececfe` |
| primary   | light5 | ![superset](https://dummyimage.com/20/F3F8FA/000?text=+) | `#F3F8FA` | ![dsfr](https://dummyimage.com/20/f5f5fe/000?text=+) | `#f5f5fe` |
| secondary | base   | ![superset](https://dummyimage.com/20/444E7C/000?text=+) | `#444E7C` | ![dsfr](https://dummyimage.com/20/000091/000?text=+)  | `#000091`  |
| secondary | dark1  | ![superset](https://dummyimage.com/20/363E63/000?text=+) | `#363E63` | ![dsfr](https://dummyimage.com/20/000/000?text=+)    | `#000`    |
| secondary | dark2  | ![superset](https://dummyimage.com/20/282E4A/000?text=+) | `#282E4A` | ![dsfr](https://dummyimage.com/20/000091/000?text=+) | `#000091` |
| secondary | dark3  | ![superset](https://dummyimage.com/20/1B1F31/000?text=+) | `#1B1F31` | ![dsfr](https://dummyimage.com/20/000091/000?text=+) | `#000091` |
| secondary | light1 | ![superset](https://dummyimage.com/20/8E94B0/000?text=+) | `#8E94B0` | ![dsfr](https://dummyimage.com/20/000091/000?text=+) | `#000091` |
| secondary | light2 | ![superset](https://dummyimage.com/20/B4B8CA/000?text=+) | `#B4B8CA` | ![dsfr](https://dummyimage.com/20/000091/000?text=+) | `#000091` |
| secondary | light3 | ![superset](https://dummyimage.com/20/D9DBE4/000?text=+) | `#D9DBE4` | ![dsfr](https://dummyimage.com/20/000091/000?text=+) | `#000091` |
| secondary | light4 | ![superset](https://dummyimage.com/20/ECEEF2/000?text=+) | `#ECEEF2` | ![dsfr](https://dummyimage.com/20/e3e3fd/000?text=+) | `#e3e3fd` |
| secondary | light5 | ![superset](https://dummyimage.com/20/F5F5F8/000?text=+) | `#F5F5F8` | ![dsfr](https://dummyimage.com/20/e3e3fd/000?text=+) | `#e3e3fd` |
| grayscale | base   | ![superset](https://dummyimage.com/20/666666/000?text=+) | `#666666` | ![dsfr](https://dummyimage.com/20/666/000?text=+)    | `#666`    |
| grayscale | dark1  | ![superset](https://dummyimage.com/20/323232/000?text=+) | `#323232` | ![dsfr](https://dummyimage.com/20/3a3a3a/000?text=+) | `#3a3a3a` |
| grayscale | dark2  | ![superset](https://dummyimage.com/20/000000/000?text=+) | `#000000` | ![dsfr](https://dummyimage.com/20/161616/000?text=+) | `#161616` |
| grayscale | light1 | ![superset](https://dummyimage.com/20/B2B2B2/000?text=+) | `#B2B2B2` | ![dsfr](https://dummyimage.com/20/929292/000?text=+) | `#929292` |
| grayscale | light2 | ![superset](https://dummyimage.com/20/E0E0E0/000?text=+) | `#E0E0E0` | ![dsfr](https://dummyimage.com/20/e5e5e5/000?text=+) | `#e5e5e5` |
| grayscale | light3 | ![superset](https://dummyimage.com/20/F0F0F0/000?text=+) | `#F0F0F0` | ![dsfr](https://dummyimage.com/20/eee/000?text=+)    | `#eee`    |
| grayscale | light4 | ![superset](https://dummyimage.com/20/F7F7F7/000?text=+) | `#F7F7F7` | ![dsfr](https://dummyimage.com/20/f6f6f6/000?text=+) | `#f6f6f6` |
| grayscale | light5 | ![superset](https://dummyimage.com/20/FFFFFF/000?text=+) | `#FFFFFF` | ![dsfr](https://dummyimage.com/20/fff/000?text=+)    | `#fff`    |
| error     | base   | ![superset](https://dummyimage.com/20/E04355/000?text=+) | `#E04355` | ![dsfr](https://dummyimage.com/20/ce0500/000?text=+) | `#ce0500` |
| error     | dark1  | ![superset](https://dummyimage.com/20/A7323F/000?text=+) | `#A7323F` | ![dsfr](https://dummyimage.com/20/ce0500/000?text=+) | `#ce0500` |
| error     | dark2  | ![superset](https://dummyimage.com/20/6F212A/000?text=+) | `#6F212A` | ![dsfr](https://dummyimage.com/20/000/000?text=+)    | `#000`    |
| error     | light1 | ![superset](https://dummyimage.com/20/EFA1AA/000?text=+) | `#EFA1AA` | ![dsfr](https://dummyimage.com/20/ce0500/000?text=+) | `#ce0500` |
| error     | light2 | ![superset](https://dummyimage.com/20/FAEDEE/000?text=+) | `#FAEDEE` | ![dsfr](https://dummyimage.com/20/ffe9e9/000?text=+) | `#ffe9e9` |
| warning   | base   | ![superset](https://dummyimage.com/20/FF7F44/000?text=+) | `#FF7F44` | ![dsfr](https://dummyimage.com/20/b34000/000?text=+) | `#b34000` |
| warning   | dark1  | ![superset](https://dummyimage.com/20/BF5E33/000?text=+) | `#BF5E33` | ![dsfr](https://dummyimage.com/20/b34000/000?text=+) | `#b34000` |
| warning   | dark2  | ![superset](https://dummyimage.com/20/7F3F21/000?text=+) | `#7F3F21` | ![dsfr](https://dummyimage.com/20/000/000?text=+)    | `#000`    |
| warning   | light1 | ![superset](https://dummyimage.com/20/FEC0A1/000?text=+) | `#FEC0A1` | ![dsfr](https://dummyimage.com/20/b34000/000?text=+) | `#b34000` |
| warning   | light2 | ![superset](https://dummyimage.com/20/FFF2EC/000?text=+) | `#FFF2EC` | ![dsfr](https://dummyimage.com/20/ffe9e6/000?text=+) | `#ffe9e6` |
| alert     | base   | ![superset](https://dummyimage.com/20/FCC700/000?text=+) | `#FCC700` | ![dsfr](https://dummyimage.com/20/fbe769/000?text=+) | `#fbe769` |
| alert     | dark1  | ![superset](https://dummyimage.com/20/BC9501/000?text=+) | `#BC9501` | ![dsfr](https://dummyimage.com/20/fbe769/000?text=+) | `#fbe769` |
| alert     | dark2  | ![superset](https://dummyimage.com/20/7D6300/000?text=+) | `#7D6300` | ![dsfr](https://dummyimage.com/20/000/000?text=+)    | `#000`    |
| alert     | light1 | ![superset](https://dummyimage.com/20/FDE380/000?text=+) | `#FDE380` | ![dsfr](https://dummyimage.com/20/fbe769/000?text=+) | `#fbe769` |
| alert     | light2 | ![superset](https://dummyimage.com/20/FEF9E6/000?text=+) | `#FEF9E6` | ![dsfr](https://dummyimage.com/20/fef7da/000?text=+) | `#fef7da` |
| success   | base   | ![superset](https://dummyimage.com/20/5AC189/000?text=+) | `#5AC189` | ![dsfr](https://dummyimage.com/20/18753c/000?text=+) | `#18753c` |
| success   | dark1  | ![superset](https://dummyimage.com/20/439066/000?text=+) | `#439066` | ![dsfr](https://dummyimage.com/20/18753c/000?text=+) | `#18753c` |
| success   | dark2  | ![superset](https://dummyimage.com/20/2B6144/000?text=+) | `#2B6144` | ![dsfr](https://dummyimage.com/20/000/000?text=+)    | `#000`    |
| success   | light1 | ![superset](https://dummyimage.com/20/ACE1C4/000?text=+) | `#ACE1C4` | ![dsfr](https://dummyimage.com/20/18753c/000?text=+) | `#18753c` |
| success   | light2 | ![superset](https://dummyimage.com/20/EEF8F3/000?text=+) | `#EEF8F3` | ![dsfr](https://dummyimage.com/20/b8fec9/000?text=+) | `#b8fec9` |
| info      | base   | ![superset](https://dummyimage.com/20/66BCFE/000?text=+) | `#66BCFE` | ![dsfr](https://dummyimage.com/20/0063cb/000?text=+) | `#0063cb` |
| info      | dark1  | ![superset](https://dummyimage.com/20/4D8CBE/000?text=+) | `#4D8CBE` | ![dsfr](https://dummyimage.com/20/0063cb/000?text=+) | `#0063cb` |
| info      | dark2  | ![superset](https://dummyimage.com/20/315E7E/000?text=+) | `#315E7E` | ![dsfr](https://dummyimage.com/20/000/000?text=+)    | `#000`    |
| info      | light1 | ![superset](https://dummyimage.com/20/B3DEFE/000?text=+) | `#B3DEFE` | ![dsfr](https://dummyimage.com/20/0063cb/000?text=+) | `#0063cb` |
| info      | light2 | ![superset](https://dummyimage.com/20/EFF8FE/000?text=+) | `#EFF8FE` | ![dsfr](https://dummyimage.com/20/e8edff/000?text=+) | `#e8edff` |

### Captures d'écran

| Description | Image |
| --- | --- |
|Police Marianne :fr:, Couleurs :art:|![demo_sill](/images/demo_sill.png)|
|Palettes de couleurs :art:|![demo_graphes_echarts](/images/demo_graphes_echarts.png)|
|Composants DSFR :control_knobs:|![demo_dsfr1](/images/demo_dsfr1.png)|
|DSFR Charts :chart_with_upwards_trend:|![demo_dsfr_chart1.png](/images/demo_dsfr_chart1.png)|
|DSFR Charts :chart_with_upwards_trend:|![demo_dsfr_chart2.png](/images/demo_dsfr_chart2.png)|
|Page d'erreur 404 :x:|![error404](/images/error404.png)|
