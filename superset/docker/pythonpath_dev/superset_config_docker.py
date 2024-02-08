# /app/docker/pythonpath/superset_config_docker.py

BABEL_DEFAULT_LOCALE = "fr"

LANGUAGES = {
    "fr": {"flag": "fr", "name": "French"},
}

# MAPBOX_KEY=""

# A CHANGER
# Par exemple avec la commande :
# openssl rand -base64 42
# ou definir la variable d'environnement SUPERSET_SECRET_KEY
#SECRET_KEY = ""

FEATURE_FLAGS = {
    "TAGGING_SYSTEM": True,
    "ALLOW_FULL_CSV_EXPORT": True,
    "DRILL_BY": True,
    "DRILL_TO_DETAIL": True,
    "DYNAMIC_PLUGINS": True,
    "HORIZONTAL_FILTER_BARS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DISABLE_LEGACY_DATASOURCE_EDITOR": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "EMBEDDABLE_CHARTS": True,
    "EMBEDDED_SUPERSET": True,
    "WTF_CSRF_ENABLED": False,
}

PUBLIC_ROLE_LIKE = "Gamma"

# THEME_OVERRIDES is used for adding custom theme to superset
# see file superset-frontend/packages/superset-ui-core/src/style/index.tsx
THEME_OVERRIDES = {
    "borderRadius": 5,
    "colors": {
        "link": "#000091",
        "text": {
            "label": "#7b7b7b",
            "help": "#666666",
        },
        "primary": {
            "base": "#000091",
            "dark1": "#8585f6",
            "dark2": "#3313178",
            "light1": "#6a6af4",
            "light2": "#cacafb",
            "light3": "#e3e3fd",
            "light4": "#ececfe",
            "light5": "#f5f5fe",
        },
        "secondary": {
            "base": "#c9191e",
            "dark1": "#f95c5e",
            "dark2": "#5e2a2b",
            "dark3": "#3b2424",
            "light1": "#e1000f",
            "light2": "#fcbfbf",
            "light3": "#fddede",
            "light4": "#fee9e9",
            "light5": "#fef4f4",
        },
        "grayscale": {
            "base": "#7b7b7b",
            "dark1": "#3a3a3a",
            "dark2": "#353535",
            "light1": "#929292",
            "light2": "#cecece",
            "light3": "#dddddd",
            "light4": "#e5e5e5",
            "light5": "#ffffff",
        },
        "error": {
            "base": "#f60700",
            "dark1": "#642626",
            "dark2": "#412121",
            "light1": "#ffbdbd",
            "light2": "#ffdddd",
        },
        "warning": {
            "base": "#d64d00",
            "dark1": "#fc5d00",
            "dark2": "#5d2c20",
            "light1": "#ffbeb4",
            "light2": "#ffded9",
        },
        "alert": {
            "base": "#B7A73F",
            "dark1": "#3f3a20",
            "dark2": "#2d2a1d",
            "light1": "#e2cf58",
            "light2": "#fbe769",
        },
        "success": {
            "base": "#1f8d49",
            "dark1": "#18753c",
            "dark2": "#204129",
            "light1": "#3bea7e",
            "light2": "#88fdaa",
        },
        "info": {
            "base": "#0078f3",
            "dark1": "#273961",
            "dark2": "#222a3f",
            "light1": "#bccdff",
            "light2": "#dde5ff",
        },
    },
    "opacity": {
        "light": "10%",
        "mediumLight": "35%",
        "mediumHeavy": "60%",
        "heavy": "80%",
    },
    "typography": {
        "families": {
            "sansSerif": "Marianne",
            "serif": "Marianne",
            "monospace": "Marianne",
        },
        "weights": {
            "light": 200,
            "normal": 400,
            "medium": 500,
            "bold": 600,
        },
        "sizes": {
            "xxs": 9,
            "xs": 10,
            "s": 12,
            "m": 14,
            "l": 16,
            "xl": 21,
            "xxl": 28,
        },
    },
    "zIndex": {
        "aboveDashboardCharts": 10,
        "dropdown": 11,
        "max": 3000,
    },
    "transitionTiming": 0.3,
    "gridUnit": 4,
    "brandIconMaxWidth": 125,
}

SUPERSET_LOAD_EXAMPLES = False

FAVICONS = [{"href": "/static/assets/local/images/favicon.svg"}]
LOGO_TOOLTIP = "Superset"
APP_NAME = "Superset"

# Specify the App icon

APP_ICON = "/static/assets/local/images/app_icon.png"


# EXTRA_CATEGORICAL_COLOR_SCHEMES is used for adding custom categorical color schemes
# see DSFR colors "Couleurs illustratives"
# https://www.systeme-de-design.gouv.fr/elements-d-interface/fondamentaux-de-l-identite-de-l-etat/couleurs-palette
EXTRA_CATEGORICAL_COLOR_SCHEMES = [
    {
        "id": "dsfr_sun",
        "description": "Couleurs illustratives du DSFR (thème clair)",
        "label": "DSFR (thème clair)",
        "isDefault": True,
        "colors": [
            "#447049",
            "#2F4077",
            "#6E445A",
            "#8D533E",
            "#716043",
            "#755348",
            "#685C48",
            "#6A6156",
            "#297254",
            "#3558A2",
            "#a94645",
            "#695240",
            "#845d48",
            "#37635f",
            "#745B47",
            "#006A6F",
            "#66673D",
        ],
    },
    {
        "id": "dsfr_moon",
        "description": "Couleurs illustratives du DSFR (thème sombre)",
        "label": "DSFR (thème sombre)",
        "isDefault": True,
        "colors": [
            "#99C221",
            "#869ECE",
            "#CE70CC",
            "#FFB7AE",
            "#FFE552",
            "#FF732C",
            "#ECD7A2",
            "#D0C3B7",
            "#34CB6A",
            "#7AB1E8",
            "#FF9575",
            "#FFCA00",
            "#FBD8AB",
            "#21AB8E",
            "#E6BE92",
            "#34BAB5",
            "#D8C634",
        ],
    },
]

# EXTRA_SEQUENTIAL_COLOR_SCHEMES is used for adding custom sequential color schemes

#EXTRA_SEQUENTIAL_COLOR_SCHEMES = [
    #{
        #"id": "warmToHot",
        #"description": "",
        #"isDiverging": True,
        #"label": "My custom warm to hot",
        #"isDefault": True,
        #"colors": [
            #"#552288",
            #"#5AAA46",
            #"#CC7788",
            #"#EEDD55",
            #"#9977BB",
            #"#BBAA44",
            #"#DDCCDD",
            #"#006699",
            #"#009DD9",
            #"#5AAA46",
            #"#44AAAA",
            #"#DDAA77",
            #"#7799BB",
            #"#88AA77",
        #],
    #}
#]

# Do you want Talisman enabled?

TALISMAN_ENABLED = False

# If you want Talisman, how do you want it configured??

TALISMAN_CONFIG = {
    "content_security_policy": {
        "default-src": ["'self'"],
        "img-src": ["'self'", "data:"],
        "worker-src": ["'self'", "blob:"],
        "connect-src": [
            "'self'",
            "https://api.mapbox.com",
            "https://events.mapbox.com",
        ],
        "object-src": "'none'",
        "style-src": ["'self'", "'unsafe-inline'"],
        "script-src": ["'self'", "'strict-dynamic'"],
    },
    "content_security_policy_nonce_in": ["script-src"],
    "force_https": False,
}

# React requires `eval` to work correctly in dev mode

TALISMAN_DEV_CONFIG = {
    "content_security_policy": {
        "default-src": ["'self'"],
        "img-src": ["'self'", "data:"],
        "worker-src": ["'self'", "blob:"],
        "connect-src": [
            "'self'",
            "https://api.mapbox.com",
            "https://events.mapbox.com",
        ],
        "object-src": "'none'",
        "style-src": ["'self'", "'unsafe-inline'"],
        "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
    },
    "content_security_policy_nonce_in": ["script-src"],
    "force_https": False,
}

HTML_SANITIZATION = False
