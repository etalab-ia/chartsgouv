from config_options.feature_flags import FEATURE_FLAGS
from config_options.talisman import TALISMAN_ENABLED, TALISMAN_CONFIG
from config_options.html_sanitization import HTML_SANITIZATION, HTML_SANITIZATION_SCHEMA_EXTENSIONS
from config_options.theme import (
    THEME_OVERRIDES,
    EXTRA_CATEGORICAL_COLOR_SCHEMES,
    EXTRA_SEQUENTIAL_COLOR_SCHEMES
)
from config_options.cache_config import (
    CACHE_DEFAULT_TIMEOUT,
    CACHE_CONFIG,
    DATA_CACHE_CONFIG,
    FILTER_STATE_CACHE_CONFIG,
    EXPLORE_FORM_DATA_CACHE_CONFIG,
)

# Default values
FAVICONS = [{"href": "/static/assets/dsfr/favicon/favicon.svg"}]
LOGO_TOOLTIP = "ChartsGouv"
APP_NAME = "ChartsGouv"

# Specify the App icon
APP_ICON = "/static/assets/local/images/app_icon_avec_titre_horizontal.png"

# ---------------------------------------------------
# Babel config for translations
# ---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = "fr"
# The allowed translation for your app
LANGUAGES = {
    "fr": {"flag": "fr", "name": "Français"},
    "en": {"flag": "us", "name": "Anglais"},
}

# Number & Datetime format
D3_FORMAT = {
    "decimal": ",",           # - decimal place string (e.g., ".").
    "thousands": " ",         # - group separator string (e.g., " ").
    "grouping": [3],          # - array of group sizes (e.g., [3]), cycled as needed.
    "currency": ["", " €"]     # - currency prefix/suffix strings (e.g., ["$", ""])
}
D3_TIME_FORMAT = {
    "dateTime": "%A %e %B %Y à %X",
    "date": "%d/%m/%Y",
    "time": "%H:%M:%S",
    "periods": ["", ""],
    "days": [
        "Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"
    ],
    "shortDays": ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"],
    "months": [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août",
        "Septembre", "Octobre", "Novembre", "Décembre"
    ],
    "shortMonths": [
        "Jan", "Fév", "Mar", "Avr",
        "Mai", "Jun", "Jul", "Aoû",
        "Sep", "Oct", "Nov", "Déc"
    ]
}

# smtp server configuration
# SMTP_HOST = "host"
# SMTP_STARTTLS = True
# SMTP_SSL = False
# SMTP_USER = "username"
# SMTP_PORT = 25
# SMTP_PASSWORD = "password"  # noqa: S105
# SMTP_MAIL_FROM = "sender mail"
# If True creates a default SSL context with ssl.Purpose.CLIENT_AUTH using the
# default system root CA certificates.
# SMTP_SSL_SERVER_AUTH = False
# ENABLE_CHUNK_ENCODING = False

SUPERSET_DASHBOARD_POSITION_DATA_LIMIT = 6553500