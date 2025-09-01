## Personnaliser Apache Superset
> Ce dépôt contient des éléments de configuration pour Superset, ce n'est pas un fork de Superset et ce n'est pas lié à une version particulière de Superset.

Cette documentation présente tous les éléments personnalisables d'Apache Superset, intégrés par défaut dans ChartsGouv.

# Table des matières

- [La configuration](#la-configuration)
  - [via fichiers python](#configuration-via-fichiers-python)
  - [via variables d'environnement](#configuration-via-variables-d'environnement)
- [Le thème](#le-thème)
  - Les templates
  - Les schémas de couleurs et les couleurs 
- [OIDC](#oidc)
- [La traduction](#la-traduction)
- [Les plugins](#les-plugins)

## La configuration
Il  est possible de configurer une instance Superset via les fichiers python de configuration disponibles dans `docker/pythonpath_dev` ou via le fichier `.env` pour les déploiements Docker.
Certains éléments sont configurables exclusivement par les fichiers python et d'autres par les variables d'environnement.  
> Pour les configurations non-sensibles, nous recommandons d'utiliser les fichiers python.

#### Configuration via fichiers python

Le backend d'Apache Superset se base sur le framework Flask. Il existe donc un certains nombre de paramètres de configuration qui peuvent être customisés.  
Une configuration par défaut est disponible dans `docker/pythonpath_dev`.  
Ci-dessous le descriptif de chacun des fichiers. L'organisation de ces fichiers est arbitraire.

- `superset_config.py`  

Ce fichier est le seul à laisser tel qu'il est. Il permet l'importation de tous les autres éléments de configuration.

- `superset_config_docker.py`

Vous pouvez configurer certains éléments globaux de votre application comme son `APP_NAME`, `APP_ICON`, les langues utilisés, les formats des nombres ...   
Il sert également de fichier d'agrégation des autres éléments de configuration.

- `config_options/cache_config.py`  

Les paramètres globlaux de gestion du cache.

- `config_options/feature_flags.py`  

Les feature flags sont des fonctionnalités globales qui peuvent être activées ou désactivées.

- `config_options/html_sanitization.py`

Cette partie de la configuration d'autoriser/refuser l'ajout de HTML/CSS depuis les graphiques qui le permettent.  
Si des balises HTML ne sont pas autorisées, elles sont automatiquement retirées du rendu.

- `config_options/jinja_context_addons.py`  

A compléter

- `config_options/talisman.py`  

A compléter

- `config_options/theme.py`

Ce fichier de configuration inclut notamment: 
  - la [variable de configuration de thème](https://preset.io/blog/theming-superset-progress-update/) `THEME_OVERRIDES` pour faire la transposition design system de Superset vers le DSFR (voir le tableau de transposition des couleurs [plus bas](#couleurs)),
  - [les variables de configuration des couleurs des charts](https://preset.io/blog/customizing-chart-colors-with-superset-and-preset/) `EXTRA_CATEGORICAL_COLOR_SCHEMES` pour définir une nouvelle palette de couleurs avec [les couleurs illustratives du DSFR](https://gouvernementfr.github.io/dsfr-chart/#colors) pour les graphiques à variables catégorielles,
  - `EXTRA_SEQUENTIAL_COLOR_SCHEMES` pour définir des dégradés de couleur pour les graphiques à variables continues (e.g. plugin Carte de Pays)

D'autres schémas peuvent être ajoutés.
- `config_options/user_model.py` & `config_options/security_manager.py`  

Ces deux fichiers de configuration permettent gérer le modèle des utilisateurs pour leur ajouter des propriétés qui peuvent par la suite être exploitées.

Pour plus d'éléments de configuration, vous pouvez consulter le [fichier de config](https://github.com/apache/superset/blob/master/superset/config.py) du repo officiel de Superset.

#### Configuration via variables d'environnement

Le fichier `docker/.env` contient certaines variables d'environnement. Ce fichier est exclusivement utilisé pour les déploiements Docker.  
Les informations de l'utilisateur admin peuvent être modifiées dans le fichier `docker/docker-init.sh`.


## Le thème

Tous les éléments visuels du frontend peuvent être customisés tels que les templates, les assets et/ou la couleur (via la configuration).  
A compléter

1. Les templates  

Les templates suivants sont présents et éditables:
- [app_icon.png](assets/images/app_icon.png) pour modifier l'icone dans l'en-tete,
- [tail_css_custom_extra.css](assets/css/tail_css_custom_extra.css) pour rajouter des règles CSS globales,
- [tail_js_custom_extra.html](templates_overrides/tail_js_custom_extra.html) pour rajouter des scripts JS globaux,
- [public_welcome.html](templates_overrides/superset/public_welcome.html) pour personnaliser la page d'accueil,
- [base.html](templates_overrides/superset/base.html#L49) pour ajouter ou non (commenter/décommenter) l'entièreté du DSFR/DSFR-Chart,
- [basic.html](templates_overrides/superset/basic.html#L86) pour ajouter ou non (commenter/décommenter) l'entièreté du DSFR/DSFR-Chart,
- [404.html](assets/404.html) pour [ajouter un formulaire de contact](https://github.com/qleroy/chartsgouv/blob/refactor-300/superset/assets/404.html#L29),
- [500.html](assets/500.html) pour [ajouter un formulaire de contact](https://github.com/qleroy/chartsgouv/blob/refactor-300/superset/assets/500.html#L22).


Ci-dessous les différences entre les templates officiels de Superset (à gauche) et ceux de ChartsGouv (à droite) par défaut.

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

2. Les couleurs

Les couleurs et les schéma de couleurs peuvent être personnalisés.  
Voir la section concernant le fichier de configuration `config_options/theme.py`.

Par défaut, les couleurs embarquées sont les suivantes:

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


## [OIDC](#oidc)
Documentation à venir.

## [La traduction](#traduction)
Le fichier qui contient toutes les traductions est disponible dans `translations/`.  
Les traductions sont compilées en .mo et .json lors du build de l'image.  
Toutes les suggestions d'améliorations de la traduction sont les bienvenues.

## [Les plugins](#plugins)

Documentation a venir. En attente de l'implémenter de la nouvelle architecture des plugins.
