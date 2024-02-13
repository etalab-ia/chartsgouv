# /app/docker/pythonpath/superset_config_docker.py
from typing import Any
from datetime import timedelta
from datetime import datetime

from superset.superset_typing import CacheConfig
from superset.key_value.types import JsonKeyValueCodec
from flask import g


BABEL_DEFAULT_LOCALE = "fr"

LANGUAGES = {
    "fr": {"flag": "fr", "name": "French"},
}

# Send user to a link where they can report bugs
BUG_REPORT_URL = "https://github.com/etalab-ia/chartsgouv/issues"
BUG_REPORT_TEXT = "Signaler un bug"
BUG_REPORT_ICON = "fr-icon-github-fill"  # Recommended size: 16x16

# Send user to a link where they can read more about Superset
DOCUMENTATION_URL = "https://etalab-ia.github.io/chartsgouv/blog/"
DOCUMENTATION_TEXT = "Documentation ChartsGouv"
DOCUMENTATION_ICON = "fr-icon-question-answer-fill"  # Recommended size: 16x16

FAVICONS = [{"href": "/static/assets/local/images/favicon.svg"}]
LOGO_TOOLTIP = "Superset"
APP_NAME = "Superset"

# Specify the App icon
APP_ICON = "/static/assets/local/images/app_icon.png"

# https://github.com/apache/superset/blob/master/RESOURCES/FEATURE_FLAGS.md
FEATURE_FLAGS = {
    "FEATURE_CHART_PLUGINS_EXPERIMENTAL": True,
    "TAGGING_SYSTEM": True,
    "DYNAMIC_PLUGINS": True,
    "DRILL_BY": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "EMBEDDED_SUPERSET": True,
    "DASHBOARD_RBAC": True,
    "ALERT_REPORTS": True,
}

# https://github.com/apache/superset/blob/master/RESOURCES/STANDARD_ROLES.md
PUBLIC_ROLE_LIKE = "Gamma"


# A dictionary of items that gets merged into the Jinja context for
# SQL Lab. The existing context gets updated with this dictionary,
# meaning values for existing keys get overwritten by the content of this
# dictionary. Exposing functionality through JINJA_CONTEXT_ADDONS has security
# implications as it opens a window for a user to execute untrusted code.
# It's important to make sure that the objects exposed (as well as objects attached
# to those objects) are harmless. We recommend only exposing simple/pure functions that
# return native types.
JINJA_CONTEXT_ADDONS = {
    'my_crazy_macro': lambda x: x*2,
    'foo': 1,
    'current_date': datetime.now().strftime("%d-%m-%Y"),
    'g': g,
}

DSFR_COLORS = {
  "sun": {
    "grey-1000-50": "#fff",
    "grey-1000-50-hover": "#f6f6f6",
    "grey-1000-50-active": "#ededed",
    "grey-950-100": "#eee",
    "grey-950-100-hover": "#d2d2d2",
    "grey-950-100-active": "#c1c1c1",
    "grey-200-850": "#3a3a3a",
    "grey-925-125": "#e5e5e5",
    "grey-1000-75": "#fff",
    "grey-1000-75-hover": "#f6f6f6",
    "grey-1000-75-active": "#ededed",
    "grey-1000-100": "#fff",
    "grey-1000-100-hover": "#f6f6f6",
    "grey-1000-100-active": "#ededed",
    "grey-975-100": "#f6f6f6",
    "grey-975-125": "#f6f6f6",
    "grey-975-125-hover": "#dfdfdf",
    "grey-975-125-active": "#cfcfcf",
    "grey-950-125": "#eee",
    "grey-950-125-hover": "#d2d2d2",
    "grey-950-125-active": "#c1c1c1",
    "grey-950-150": "#eee",
    "grey-950-150-hover": "#d2d2d2",
    "grey-950-150-active": "#c1c1c1",
    "grey-50-1000": "#161616",
    "grey-425-625": "#666",
    "grey-625-425": "#929292",
    "grey-0-1000": "#000",
    "grey-900-175": "#ddd",
    "blue-france-975-75": "#f5f5fe",
    "blue-france-975-75-hover": "#dcdcfc",
    "blue-france-975-75-active": "#cbcbfa",
    "blue-france-950-100": "#ececfe",
    "blue-france-950-100-hover": "#cecefc",
    "blue-france-950-100-active": "#bbbbfc",
    "blue-france-sun-113-625": "#000091",
    "blue-france-sun-113-625-hover": "#1212ff",
    "blue-france-sun-113-625-active": "#2323ff",
    "blue-france-925-125": "#e3e3fd",
    "blue-france-925-125-hover": "#c1c1fb",
    "blue-france-925-125-active": "#adadf9",
    "blue-france-975-sun-113": "#f5f5fe",
    "blue-france-main-525": "#6a6af4",
    "blue-france-850-200": "#cacafb",
    "red-marianne-975-75": "#fef4f4",
    "red-marianne-975-75-hover": "#fcd7d7",
    "red-marianne-975-75-active": "#fac4c4",
    "red-marianne-950-100": "#fee9e9",
    "red-marianne-950-100-hover": "#fdc5c5",
    "red-marianne-950-100-active": "#fcafaf",
    "red-marianne-425-625": "#c9191e",
    "red-marianne-425-625-hover": "#f93f42",
    "red-marianne-425-625-active": "#f95a5c",
    "red-marianne-925-125": "#fddede",
    "red-marianne-925-125-hover": "#fbb6b6",
    "red-marianne-925-125-active": "#fa9e9e",
    "red-marianne-main-472": "#e1000f",
    "red-marianne-850-200": "#fcbfbf",
    "info-950-100": "#e8edff",
    "info-950-100-hover": "#c2d1ff",
    "info-950-100-active": "#a9bfff",
    "info-425-625": "#0063cb",
    "info-425-625-hover": "#3b87ff",
    "info-425-625-active": "#6798ff",
    "info-975-75": "#f4f6ff",
    "success-950-100": "#b8fec9",
    "success-950-100-hover": "#46fd89",
    "success-950-100-active": "#34eb7b",
    "success-425-625": "#18753c",
    "success-425-625-hover": "#27a959",
    "success-425-625-active": "#2fc368",
    "success-975-75": "#dffee6",
    "warning-950-100": "#ffe9e6",
    "warning-950-100-hover": "#ffc6bd",
    "warning-950-100-active": "#ffb0a2",
    "warning-425-625": "#b34000",
    "warning-425-625-hover": "#ff6218",
    "warning-425-625-active": "#ff7a55",
    "warning-975-75": "#fff4f3",
    "error-950-100": "#ffe9e9",
    "error-950-100-hover": "#ffc5c5",
    "error-950-100-active": "#ffafaf",
    "error-425-625": "#ce0500",
    "error-425-625-hover": "#ff2725",
    "error-425-625-active": "#ff4140",
    "error-975-75": "#fff4f4",
    "green-tilleul-verveine-975-75": "#fef7da",
    "green-tilleul-verveine-975-75-hover": "#fce552",
    "green-tilleul-verveine-975-75-active": "#ebd54c",
    "green-tilleul-verveine-950-100": "#fceeac",
    "green-tilleul-verveine-950-100-hover": "#e8d45c",
    "green-tilleul-verveine-950-100-active": "#d4c254",
    "green-tilleul-verveine-sun-418-moon-817": "#66673d",
    "green-tilleul-verveine-sun-418-moon-817-hover": "#929359",
    "green-tilleul-verveine-sun-418-moon-817-active": "#a7a967",
    "green-tilleul-verveine-925-125": "#fbe769",
    "green-tilleul-verveine-925-125-hover": "#d7c655",
    "green-tilleul-verveine-925-125-active": "#c2b24c",
    "green-tilleul-verveine-main-707": "#b7a73f",
    "green-tilleul-verveine-850-200": "#e2cf58",
    "green-bourgeon-975-75": "#e6feda",
    "green-bourgeon-975-75-hover": "#a7fc62",
    "green-bourgeon-975-75-active": "#98ed4d",
    "green-bourgeon-950-100": "#c9fcac",
    "green-bourgeon-950-100-hover": "#9ae95d",
    "green-bourgeon-950-100-active": "#8dd555",
    "green-bourgeon-sun-425-moon-759": "#447049",
    "green-bourgeon-sun-425-moon-759-hover": "#639f6a",
    "green-bourgeon-sun-425-moon-759-active": "#72b77a",
    "green-bourgeon-925-125": "#a9fb68",
    "green-bourgeon-925-125-hover": "#8ed654",
    "green-bourgeon-925-125-active": "#7fc04b",
    "green-bourgeon-main-640": "#68a532",
    "green-bourgeon-850-200": "#95e257",
    "green-emeraude-975-75": "#e3fdeb",
    "green-emeraude-975-75-hover": "#94f9b9",
    "green-emeraude-975-75-active": "#6df1a3",
    "green-emeraude-950-100": "#c3fad5",
    "green-emeraude-950-100-hover": "#77eda5",
    "green-emeraude-950-100-active": "#6dd897",
    "green-emeraude-sun-425-moon-753": "#297254",
    "green-emeraude-sun-425-moon-753-hover": "#3ea47a",
    "green-emeraude-sun-425-moon-753-active": "#49bc8d",
    "green-emeraude-925-125": "#9ef9be",
    "green-emeraude-925-125-hover": "#69df97",
    "green-emeraude-925-125-active": "#5ec988",
    "green-emeraude-main-632": "#00a95f",
    "green-emeraude-850-200": "#6fe49d",
    "green-menthe-975-75": "#dffdf7",
    "green-menthe-975-75-hover": "#84f9e7",
    "green-menthe-975-75-active": "#70ebd8",
    "green-menthe-950-100": "#bafaee",
    "green-menthe-950-100-hover": "#79e7d5",
    "green-menthe-950-100-active": "#6fd3c3",
    "green-menthe-sun-373-moon-652": "#37635f",
    "green-menthe-sun-373-moon-652-hover": "#53918c",
    "green-menthe-sun-373-moon-652-active": "#62a9a2",
    "green-menthe-925-125": "#8bf8e7",
    "green-menthe-925-125-hover": "#6ed5c5",
    "green-menthe-925-125-active": "#62bfb1",
    "green-menthe-main-548": "#009081",
    "green-menthe-850-200": "#73e0cf",
    "green-archipel-975-75": "#e5fbfd",
    "green-archipel-975-75-hover": "#99f2f8",
    "green-archipel-975-75-active": "#73e9f0",
    "green-archipel-950-100": "#c7f6fc",
    "green-archipel-950-100-hover": "#64ecf8",
    "green-archipel-950-100-active": "#5bd8e3",
    "green-archipel-sun-391-moon-716": "#006a6f",
    "green-archipel-sun-391-moon-716-hover": "#009fa7",
    "green-archipel-sun-391-moon-716-active": "#00bbc3",
    "green-archipel-925-125": "#a6f2fa",
    "green-archipel-925-125-hover": "#62dbe5",
    "green-archipel-925-125-active": "#58c5cf",
    "green-archipel-main-557": "#009099",
    "green-archipel-850-200": "#60e0eb",
    "blue-ecume-975-75": "#f4f6fe",
    "blue-ecume-975-75-hover": "#d7dffb",
    "blue-ecume-975-75-active": "#c3cffa",
    "blue-ecume-950-100": "#e9edfe",
    "blue-ecume-950-100-hover": "#c5d0fc",
    "blue-ecume-950-100-active": "#adbffc",
    "blue-ecume-sun-247-moon-675": "#2f4077",
    "blue-ecume-sun-247-moon-675-hover": "#4e68bb",
    "blue-ecume-sun-247-moon-675-active": "#667dcf",
    "blue-ecume-925-125": "#dee5fd",
    "blue-ecume-925-125-hover": "#b4c5fb",
    "blue-ecume-925-125-active": "#99b3f9",
    "blue-ecume-main-400": "#465f9d",
    "blue-ecume-850-200": "#bfccfb",
    "blue-cumulus-975-75": "#f3f6fe",
    "blue-cumulus-975-75-hover": "#d3dffc",
    "blue-cumulus-975-75-active": "#bed0fa",
    "blue-cumulus-950-100": "#e6eefe",
    "blue-cumulus-950-100-hover": "#bcd3fc",
    "blue-cumulus-950-100-active": "#9fc3fc",
    "blue-cumulus-sun-368-moon-732": "#3558a2",
    "blue-cumulus-sun-368-moon-732-hover": "#5982e0",
    "blue-cumulus-sun-368-moon-732-active": "#7996e6",
    "blue-cumulus-925-125": "#dae6fd",
    "blue-cumulus-925-125-hover": "#a9c8fb",
    "blue-cumulus-925-125-active": "#8ab8f9",
    "blue-cumulus-main-526": "#417dc4",
    "blue-cumulus-850-200": "#b6cffb",
    "purple-glycine-975-75": "#fef3fd",
    "purple-glycine-975-75-hover": "#fcd4f8",
    "purple-glycine-975-75-active": "#fabff5",
    "purple-glycine-950-100": "#fee7fc",
    "purple-glycine-950-100-hover": "#fdc0f8",
    "purple-glycine-950-100-active": "#fca8f6",
    "purple-glycine-sun-319-moon-630": "#6e445a",
    "purple-glycine-sun-319-moon-630-hover": "#a66989",
    "purple-glycine-sun-319-moon-630-active": "#bb7f9e",
    "purple-glycine-925-125": "#fddbfa",
    "purple-glycine-925-125-hover": "#fbaff5",
    "purple-glycine-925-125-active": "#fa96f2",
    "purple-glycine-main-494": "#a558a0",
    "purple-glycine-850-200": "#fbb8f6",
    "pink-macaron-975-75": "#fef4f2",
    "pink-macaron-975-75-hover": "#fcd8d0",
    "pink-macaron-975-75-active": "#fac5b8",
    "pink-macaron-950-100": "#fee9e6",
    "pink-macaron-950-100-hover": "#fdc6bd",
    "pink-macaron-950-100-active": "#fcb0a2",
    "pink-macaron-sun-406-moon-833": "#8d533e",
    "pink-macaron-sun-406-moon-833-hover": "#ca795c",
    "pink-macaron-sun-406-moon-833-active": "#e08e73",
    "pink-macaron-925-125": "#fddfda",
    "pink-macaron-925-125-hover": "#fbb8ab",
    "pink-macaron-925-125-active": "#faa18d",
    "pink-macaron-main-689": "#e18b76",
    "pink-macaron-850-200": "#fcc0b4",
    "pink-tuile-975-75": "#fef4f3",
    "pink-tuile-975-75-hover": "#fcd7d3",
    "pink-tuile-975-75-active": "#fac4be",
    "pink-tuile-950-100": "#fee9e7",
    "pink-tuile-950-100-hover": "#fdc6c0",
    "pink-tuile-950-100-active": "#fcb0a7",
    "pink-tuile-sun-425-moon-750": "#a94645",
    "pink-tuile-sun-425-moon-750-hover": "#d5706f",
    "pink-tuile-sun-425-moon-750-active": "#da8a89",
    "pink-tuile-925-125": "#fddfdb",
    "pink-tuile-925-125-hover": "#fbb8ad",
    "pink-tuile-925-125-active": "#faa191",
    "pink-tuile-main-556": "#ce614a",
    "pink-tuile-850-200": "#fcbfb7",
    "yellow-tournesol-975-75": "#fef6e3",
    "yellow-tournesol-975-75-hover": "#fce086",
    "yellow-tournesol-975-75-active": "#f5d24b",
    "yellow-tournesol-950-100": "#feecc2",
    "yellow-tournesol-950-100-hover": "#fbd335",
    "yellow-tournesol-950-100-active": "#e6c130",
    "yellow-tournesol-sun-407-moon-922": "#716043",
    "yellow-tournesol-sun-407-moon-922-hover": "#a28a62",
    "yellow-tournesol-sun-407-moon-922-active": "#ba9f72",
    "yellow-tournesol-925-125": "#fde39c",
    "yellow-tournesol-925-125-hover": "#e9c53b",
    "yellow-tournesol-925-125-active": "#d3b235",
    "yellow-tournesol-main-731": "#c8aa39",
    "yellow-tournesol-850-200": "#efcb3a",
    "yellow-moutarde-975-75": "#fef5e8",
    "yellow-moutarde-975-75-hover": "#fcdca3",
    "yellow-moutarde-975-75-active": "#fbcd64",
    "yellow-moutarde-950-100": "#feebd0",
    "yellow-moutarde-950-100-hover": "#fdcd6d",
    "yellow-moutarde-950-100-active": "#f4be30",
    "yellow-moutarde-sun-348-moon-860": "#695240",
    "yellow-moutarde-sun-348-moon-860-hover": "#9b7b61",
    "yellow-moutarde-sun-348-moon-860-active": "#b58f72",
    "yellow-moutarde-925-125": "#fde2b5",
    "yellow-moutarde-925-125-hover": "#f6c43c",
    "yellow-moutarde-925-125-active": "#dfb135",
    "yellow-moutarde-main-679": "#c3992a",
    "yellow-moutarde-850-200": "#fcc63a",
    "orange-terre-battue-975-75": "#fef4f2",
    "orange-terre-battue-975-75-hover": "#fcd8d0",
    "orange-terre-battue-975-75-active": "#fac5b8",
    "orange-terre-battue-950-100": "#fee9e5",
    "orange-terre-battue-950-100-hover": "#fdc6ba",
    "orange-terre-battue-950-100-active": "#fcb09e",
    "orange-terre-battue-sun-370-moon-672": "#755348",
    "orange-terre-battue-sun-370-moon-672-hover": "#ab7b6b",
    "orange-terre-battue-sun-370-moon-672-active": "#c68f7d",
    "orange-terre-battue-925-125": "#fddfd8",
    "orange-terre-battue-925-125-hover": "#fbb8a5",
    "orange-terre-battue-925-125-active": "#faa184",
    "orange-terre-battue-main-645": "#e4794a",
    "orange-terre-battue-850-200": "#fcc0b0",
    "brown-cafe-creme-975-75": "#fbf6ed",
    "brown-cafe-creme-975-75-hover": "#f2deb6",
    "brown-cafe-creme-975-75-active": "#eacf91",
    "brown-cafe-creme-950-100": "#f7ecdb",
    "brown-cafe-creme-950-100-hover": "#edce94",
    "brown-cafe-creme-950-100-active": "#dabd84",
    "brown-cafe-creme-sun-383-moon-885": "#685c48",
    "brown-cafe-creme-sun-383-moon-885-hover": "#97866a",
    "brown-cafe-creme-sun-383-moon-885-active": "#ae9b7b",
    "brown-cafe-creme-925-125": "#f4e3c7",
    "brown-cafe-creme-925-125-hover": "#e1c386",
    "brown-cafe-creme-925-125-active": "#ccb078",
    "brown-cafe-creme-main-782": "#d1b781",
    "brown-cafe-creme-850-200": "#e7ca8e",
    "brown-caramel-975-75": "#fbf5f2",
    "brown-caramel-975-75-hover": "#f1dbcf",
    "brown-caramel-975-75-active": "#ecc9b5",
    "brown-caramel-950-100": "#f7ebe5",
    "brown-caramel-950-100-hover": "#eccbb9",
    "brown-caramel-950-100-active": "#e6b79a",
    "brown-caramel-sun-425-moon-901": "#845d48",
    "brown-caramel-sun-425-moon-901-hover": "#bb8568",
    "brown-caramel-sun-425-moon-901-active": "#d69978",
    "brown-caramel-925-125": "#f3e2d9",
    "brown-caramel-925-125-hover": "#e7bea6",
    "brown-caramel-925-125-active": "#e1a982",
    "brown-caramel-main-648": "#c08c65",
    "brown-caramel-850-200": "#eac7b2",
    "brown-opera-975-75": "#fbf5f2",
    "brown-opera-975-75-hover": "#f1dbcf",
    "brown-opera-975-75-active": "#ecc9b5",
    "brown-opera-950-100": "#f7ece4",
    "brown-opera-950-100-hover": "#eccdb3",
    "brown-opera-950-100-active": "#e6ba90",
    "brown-opera-sun-395-moon-820": "#745b47",
    "brown-opera-sun-395-moon-820-hover": "#a78468",
    "brown-opera-sun-395-moon-820-active": "#c09979",
    "brown-opera-925-125": "#f3e2d7",
    "brown-opera-925-125-hover": "#e7bfa0",
    "brown-opera-925-125-active": "#deaa7e",
    "brown-opera-main-680": "#bd987a",
    "brown-opera-850-200": "#eac7ad",
    "beige-gris-galet-975-75": "#f9f6f2",
    "beige-gris-galet-975-75-hover": "#eadecd",
    "beige-gris-galet-975-75-active": "#e1ceb1",
    "beige-gris-galet-950-100": "#f3ede5",
    "beige-gris-galet-950-100-hover": "#e1d0b5",
    "beige-gris-galet-950-100-active": "#d1bea2",
    "beige-gris-galet-sun-407-moon-821": "#6a6156",
    "beige-gris-galet-sun-407-moon-821-hover": "#988b7c",
    "beige-gris-galet-sun-407-moon-821-active": "#afa08f",
    "beige-gris-galet-925-125": "#eee4d9",
    "beige-gris-galet-925-125-hover": "#dbc3a4",
    "beige-gris-galet-925-125-active": "#c6b094",
    "beige-gris-galet-main-702": "#aea397",
    "beige-gris-galet-850-200": "#e0cab0",
  },
  "moon": {
    "grey-1000-50": "#161616",
    "grey-1000-50-hover": "#343434",
    "grey-1000-50-active": "#474747",
    "grey-975-75": "#1e1e1e",
    "grey-975-75-hover": "#3f3f3f",
    "grey-975-75-active": "#525252",
    "grey-950-100": "#242424",
    "grey-950-100-hover": "#474747",
    "grey-950-100-active": "#5b5b5b",
    "grey-200-850": "#cecece",
    "grey-925-125": "#2a2a2a",
    "grey-1000-75": "#1e1e1e",
    "grey-1000-75-hover": "#3f3f3f",
    "grey-1000-75-active": "#525252",
    "grey-1000-100": "#242424",
    "grey-1000-100-hover": "#474747",
    "grey-1000-100-active": "#5b5b5b",
    "grey-975-100": "#242424",
    "grey-975-100-hover": "#474747",
    "grey-975-100-active": "#5b5b5b",
    "grey-975-125": "#2a2a2a",
    "grey-975-125-hover": "#4e4e4e",
    "grey-975-125-active": "#636363",
    "grey-950-125": "#2a2a2a",
    "grey-950-125-hover": "#4e4e4e",
    "grey-950-125-active": "#636363",
    "grey-950-150": "#2f2f2f",
    "grey-950-150-hover": "#545454",
    "grey-950-150-active": "#696969",
    "grey-50-1000": "#fff",
    "grey-425-625": "#929292",
    "grey-625-425": "#666",
    "grey-0-1000": "#fff",
    "grey-900-175": "#353535",
    "blue-france-975-75": "#1b1b35",
    "blue-france-975-75-hover": "#3a3a68",
    "blue-france-975-75-active": "#4d4d83",
    "blue-france-950-100": "#21213f",
    "blue-france-950-100-hover": "#424275",
    "blue-france-950-100-active": "#56568c",
    "blue-france-sun-113-625": "#8585f6",
    "blue-france-sun-113-625-hover": "#b1b1f9",
    "blue-france-sun-113-625-active": "#c6c6fb",
    "blue-france-925-125": "#272747",
    "blue-france-925-125-hover": "#4a4a7d",
    "blue-france-925-125-active": "#5e5e90",
    "blue-france-975-sun-113": "#000091",
    "blue-france-main-525": "#6a6af4",
    "blue-france-850-200": "#313178",
    "red-marianne-975-75": "#2b1919",
    "red-marianne-975-75-hover": "#573737",
    "red-marianne-975-75-active": "#704848",
    "red-marianne-950-100": "#331f1f",
    "red-marianne-950-100-hover": "#613f3f",
    "red-marianne-950-100-active": "#7b5151",
    "red-marianne-425-625": "#f95c5e",
    "red-marianne-425-625-hover": "#fa9293",
    "red-marianne-425-625-active": "#fbabac",
    "red-marianne-925-125": "#3b2424",
    "red-marianne-925-125-hover": "#6b4545",
    "red-marianne-925-125-active": "#865757",
    "red-marianne-main-472": "#e1000f",
    "red-marianne-850-200": "#5e2a2b",
    "info-950-100": "#1d2437",
    "info-950-100-hover": "#3b4767",
    "info-950-100-active": "#4c5b83",
    "info-425-625": "#518fff",
    "info-425-625-hover": "#98b4ff",
    "info-425-625-active": "#b4c7ff",
    "info-975-75": "#171d2e",
    "success-950-100": "#19271d",
    "success-950-100-hover": "#344c3b",
    "success-950-100-active": "#44624d",
    "success-425-625": "#27a658",
    "success-425-625-hover": "#36d975",
    "success-425-625-active": "#3df183",
    "success-975-75": "#142117",
    "warning-950-100": "#361e19",
    "warning-950-100-hover": "#663d35",
    "warning-950-100-active": "#824f44",
    "warning-425-625": "#fc5d00",
    "warning-425-625-hover": "#ff8c73",
    "warning-425-625-active": "#ffa595",
    "warning-975-75": "#2d1814",
    "error-950-100": "#391c1c",
    "error-950-100-hover": "#6c3a3a",
    "error-950-100-active": "#894b4b",
    "error-425-625": "#ff5655",
    "error-425-625-hover": "#ff8c8c",
    "error-425-625-active": "#ffa6a6",
    "error-975-75": "#301717",
    "green-tilleul-verveine-975-75": "#201e14",
    "green-tilleul-verveine-975-75-hover": "#433f2e",
    "green-tilleul-verveine-975-75-active": "#57533d",
    "green-tilleul-verveine-950-100": "#272419",
    "green-tilleul-verveine-950-100-hover": "#4c4734",
    "green-tilleul-verveine-950-100-active": "#615b44",
    "green-tilleul-verveine-sun-418-moon-817": "#d8c634",
    "green-tilleul-verveine-sun-418-moon-817-hover": "#fee943",
    "green-tilleul-verveine-sun-418-moon-817-active": "#fef1ab",
    "green-tilleul-verveine-925-125": "#2d2a1d",
    "green-tilleul-verveine-925-125-hover": "#534f39",
    "green-tilleul-verveine-925-125-active": "#696349",
    "green-tilleul-verveine-main-707": "#b7a73f",
    "green-tilleul-verveine-850-200": "#3f3a20",
    "green-bourgeon-975-75": "#182014",
    "green-bourgeon-975-75-hover": "#35432e",
    "green-bourgeon-975-75-active": "#46573d",
    "green-bourgeon-950-100": "#1e2719",
    "green-bourgeon-950-100-hover": "#3d4c34",
    "green-bourgeon-950-100-active": "#4e6144",
    "green-bourgeon-sun-425-moon-759": "#99c221",
    "green-bourgeon-sun-425-moon-759-hover": "#baec2a",
    "green-bourgeon-sun-425-moon-759-active": "#c9fd2e",
    "green-bourgeon-925-125": "#232d1d",
    "green-bourgeon-925-125-hover": "#435339",
    "green-bourgeon-925-125-active": "#556949",
    "green-bourgeon-main-640": "#68a532",
    "green-bourgeon-850-200": "#2a401a",
    "green-emeraude-975-75": "#142018",
    "green-emeraude-975-75-hover": "#2e4335",
    "green-emeraude-975-75-active": "#3d5846",
    "green-emeraude-950-100": "#19271e",
    "green-emeraude-950-100-hover": "#344c3d",
    "green-emeraude-950-100-active": "#44624f",
    "green-emeraude-sun-425-moon-753": "#34cb6a",
    "green-emeraude-sun-425-moon-753-hover": "#42fb84",
    "green-emeraude-sun-425-moon-753-active": "#80fda3",
    "green-emeraude-925-125": "#1e2e23",
    "green-emeraude-925-125-hover": "#3b5543",
    "green-emeraude-925-125-active": "#4b6b55",
    "green-emeraude-main-632": "#00a95f",
    "green-emeraude-850-200": "#21402c",
    "green-menthe-975-75": "#15201e",
    "green-menthe-975-75-hover": "#30433f",
    "green-menthe-975-75-active": "#3f5753",
    "green-menthe-950-100": "#1a2624",
    "green-menthe-950-100-hover": "#364b47",
    "green-menthe-950-100-active": "#46605b",
    "green-menthe-sun-373-moon-652": "#21ab8e",
    "green-menthe-sun-373-moon-652-hover": "#2eddb8",
    "green-menthe-sun-373-moon-652-active": "#34f4cc",
    "green-menthe-925-125": "#1f2d2a",
    "green-menthe-925-125-hover": "#3c534e",
    "green-menthe-925-125-active": "#4d6963",
    "green-menthe-main-548": "#009081",
    "green-menthe-850-200": "#223f3a",
    "green-archipel-975-75": "#152021",
    "green-archipel-975-75-hover": "#2f4345",
    "green-archipel-975-75-active": "#3f5759",
    "green-archipel-950-100": "#1a2628",
    "green-archipel-950-100-hover": "#364a4e",
    "green-archipel-950-100-active": "#465f63",
    "green-archipel-sun-391-moon-716": "#34bab5",
    "green-archipel-sun-391-moon-716-hover": "#43e9e2",
    "green-archipel-sun-391-moon-716-active": "#4cfdf6",
    "green-archipel-925-125": "#1f2c2e",
    "green-archipel-925-125-hover": "#3c5255",
    "green-archipel-925-125-active": "#4d676b",
    "green-archipel-main-557": "#009099",
    "green-archipel-850-200": "#233e41",
    "blue-ecume-975-75": "#171d2f",
    "blue-ecume-975-75-hover": "#333e5e",
    "blue-ecume-975-75-active": "#445179",
    "blue-ecume-950-100": "#1d2437",
    "blue-ecume-950-100-hover": "#3b4767",
    "blue-ecume-950-100-active": "#4c5b83",
    "blue-ecume-sun-247-moon-675": "#869ece",
    "blue-ecume-sun-247-moon-675-hover": "#b8c5e2",
    "blue-ecume-sun-247-moon-675-active": "#ced6ea",
    "blue-ecume-925-125": "#222940",
    "blue-ecume-925-125-hover": "#424d73",
    "blue-ecume-925-125-active": "#536190",
    "blue-ecume-main-400": "#465f9d",
    "blue-ecume-850-200": "#273962",
    "blue-cumulus-975-75": "#171e2b",
    "blue-cumulus-975-75-hover": "#333f56",
    "blue-cumulus-975-75-active": "#43536f",
    "blue-cumulus-950-100": "#1c2433",
    "blue-cumulus-950-100-hover": "#3a4761",
    "blue-cumulus-950-100-active": "#4a5b7b",
    "blue-cumulus-sun-368-moon-732": "#7ab1e8",
    "blue-cumulus-sun-368-moon-732-hover": "#bad2f2",
    "blue-cumulus-sun-368-moon-732-active": "#d2e2f6",
    "blue-cumulus-925-125": "#212a3a",
    "blue-cumulus-925-125-hover": "#404f69",
    "blue-cumulus-925-125-active": "#516384",
    "blue-cumulus-main-526": "#417dc4",
    "blue-cumulus-850-200": "#263b58",
    "purple-glycine-975-75": "#251a24",
    "purple-glycine-975-75-hover": "#4c394a",
    "purple-glycine-975-75-active": "#634a60",
    "purple-glycine-950-100": "#2c202b",
    "purple-glycine-950-100-hover": "#554053",
    "purple-glycine-950-100-active": "#6c536a",
    "purple-glycine-sun-319-moon-630": "#ce70cc",
    "purple-glycine-sun-319-moon-630-hover": "#dfa4dd",
    "purple-glycine-sun-319-moon-630-active": "#e7bbe6",
    "purple-glycine-925-125": "#332632",
    "purple-glycine-925-125-hover": "#5d485c",
    "purple-glycine-925-125-active": "#755b73",
    "purple-glycine-main-494": "#a558a0",
    "purple-glycine-850-200": "#502e4d",
    "pink-macaron-975-75": "#261b19",
    "pink-macaron-975-75-hover": "#4e3a37",
    "pink-macaron-975-75-active": "#654c48",
    "pink-macaron-950-100": "#2e211f",
    "pink-macaron-950-100-hover": "#58423f",
    "pink-macaron-950-100-active": "#705551",
    "pink-macaron-sun-406-moon-833": "#ffb7ae",
    "pink-macaron-sun-406-moon-833-hover": "#ffe0dc",
    "pink-macaron-sun-406-moon-833-active": "#fff0ee",
    "pink-macaron-925-125": "#352724",
    "pink-macaron-925-125-hover": "#614a45",
    "pink-macaron-925-125-active": "#795d57",
    "pink-macaron-main-689": "#e18b76",
    "pink-macaron-850-200": "#52312a",
    "pink-tuile-975-75": "#281b19",
    "pink-tuile-975-75-hover": "#513a37",
    "pink-tuile-975-75-active": "#694c48",
    "pink-tuile-950-100": "#2f211f",
    "pink-tuile-950-100-hover": "#5a423e",
    "pink-tuile-950-100-active": "#725550",
    "pink-tuile-sun-425-moon-750": "#ff9575",
    "pink-tuile-sun-425-moon-750-hover": "#ffc4b7",
    "pink-tuile-sun-425-moon-750-active": "#ffd8d0",
    "pink-tuile-925-125": "#372624",
    "pink-tuile-925-125-hover": "#644845",
    "pink-tuile-925-125-active": "#7d5b57",
    "pink-tuile-main-556": "#ce614a",
    "pink-tuile-850-200": "#55302a",
    "yellow-tournesol-975-75": "#221d11",
    "yellow-tournesol-975-75-hover": "#473e29",
    "yellow-tournesol-975-75-active": "#5c5136",
    "yellow-tournesol-950-100": "#292416",
    "yellow-tournesol-950-100-hover": "#4f472f",
    "yellow-tournesol-950-100-active": "#655b3d",
    "yellow-tournesol-sun-407-moon-922": "#ffe552",
    "yellow-tournesol-sun-407-moon-922-hover": "#e1c700",
    "yellow-tournesol-sun-407-moon-922-active": "#cab300",
    "yellow-tournesol-925-125": "#302a1a",
    "yellow-tournesol-925-125-hover": "#584e34",
    "yellow-tournesol-925-125-active": "#6f6342",
    "yellow-tournesol-main-731": "#c8aa39",
    "yellow-tournesol-850-200": "#43391a",
    "yellow-moutarde-975-75": "#231d14",
    "yellow-moutarde-975-75-hover": "#483e2e",
    "yellow-moutarde-975-75-active": "#5e513d",
    "yellow-moutarde-950-100": "#2a2319",
    "yellow-moutarde-950-100-hover": "#514534",
    "yellow-moutarde-950-100-active": "#685944",
    "yellow-moutarde-sun-348-moon-860": "#ffca00",
    "yellow-moutarde-sun-348-moon-860-hover": "#cda200",
    "yellow-moutarde-sun-348-moon-860-active": "#b28c00",
    "yellow-moutarde-925-125": "#30291d",
    "yellow-moutarde-925-125-hover": "#584d39",
    "yellow-moutarde-925-125-active": "#6f6149",
    "yellow-moutarde-main-679": "#c3992a",
    "yellow-moutarde-850-200": "#453820",
    "orange-terre-battue-975-75": "#281a16",
    "orange-terre-battue-975-75-hover": "#513932",
    "orange-terre-battue-975-75-active": "#6a4b42",
    "orange-terre-battue-950-100": "#31201c",
    "orange-terre-battue-950-100-hover": "#5d403a",
    "orange-terre-battue-950-100-active": "#77534a",
    "orange-terre-battue-sun-370-moon-672": "#ff732c",
    "orange-terre-battue-sun-370-moon-672-hover": "#ffa48b",
    "orange-terre-battue-sun-370-moon-672-active": "#ffbbab",
    "orange-terre-battue-925-125": "#382621",
    "orange-terre-battue-925-125-hover": "#664840",
    "orange-terre-battue-925-125-active": "#7f5b51",
    "orange-terre-battue-main-645": "#e4794a",
    "orange-terre-battue-850-200": "#543125",
    "brown-cafe-creme-975-75": "#211d16",
    "brown-cafe-creme-975-75-hover": "#453e31",
    "brown-cafe-creme-975-75-active": "#5a5141",
    "brown-cafe-creme-950-100": "#28241c",
    "brown-cafe-creme-950-100-hover": "#4e4739",
    "brown-cafe-creme-950-100-active": "#635b4a",
    "brown-cafe-creme-sun-383-moon-885": "#ecd7a2",
    "brown-cafe-creme-sun-383-moon-885-hover": "#c5b386",
    "brown-cafe-creme-sun-383-moon-885-active": "#af9f77",
    "brown-cafe-creme-925-125": "#2e2a21",
    "brown-cafe-creme-925-125-hover": "#554e3f",
    "brown-cafe-creme-925-125-active": "#6b6351",
    "brown-cafe-creme-main-782": "#d1b781",
    "brown-cafe-creme-850-200": "#423925",
    "brown-caramel-975-75": "#251c16",
    "brown-caramel-975-75-hover": "#4c3c31",
    "brown-caramel-975-75-active": "#624e41",
    "brown-caramel-950-100": "#2c221c",
    "brown-caramel-950-100-hover": "#554439",
    "brown-caramel-950-100-active": "#6c574a",
    "brown-caramel-sun-425-moon-901": "#fbd8ab",
    "brown-caramel-sun-425-moon-901-hover": "#efb547",
    "brown-caramel-sun-425-moon-901-active": "#d6a23e",
    "brown-caramel-925-125": "#332821",
    "brown-caramel-925-125-hover": "#5d4b40",
    "brown-caramel-925-125-active": "#755f51",
    "brown-caramel-main-648": "#c08c65",
    "brown-caramel-850-200": "#4b3525",
    "brown-opera-975-75": "#241c17",
    "brown-opera-975-75-hover": "#4a3c33",
    "brown-opera-975-75-active": "#604f44",
    "brown-opera-950-100": "#2b221c",
    "brown-opera-950-100-hover": "#53443a",
    "brown-opera-950-100-active": "#6a574a",
    "brown-opera-sun-395-moon-820": "#e6be92",
    "brown-opera-sun-395-moon-820-hover": "#f2e2d3",
    "brown-opera-sun-395-moon-820-active": "#f8f0e9",
    "brown-opera-925-125": "#322821",
    "brown-opera-925-125-hover": "#5c4b40",
    "brown-opera-925-125-active": "#735f51",
    "brown-opera-main-680": "#bd987a",
    "brown-opera-850-200": "#493625",
    "beige-gris-galet-975-75": "#211d19",
    "beige-gris-galet-975-75-hover": "#453e37",
    "beige-gris-galet-975-75-active": "#595148",
    "beige-gris-galet-950-100": "#28231f",
    "beige-gris-galet-950-100-hover": "#4e453f",
    "beige-gris-galet-950-100-active": "#635950",
    "beige-gris-galet-sun-407-moon-821": "#d0c3b7",
    "beige-gris-galet-sun-407-moon-821-hover": "#eae5e1",
    "beige-gris-galet-sun-407-moon-821-active": "#f4f2f0",
    "beige-gris-galet-925-125": "#2e2924",
    "beige-gris-galet-925-125-hover": "#554d45",
    "beige-gris-galet-925-125-active": "#6b6157",
    "beige-gris-galet-main-702": "#aea397",
    "beige-gris-galet-850-200": "#433829",
  },
}

# THEME_OVERRIDES is used for adding custom theme to superset
# pour le theme par default voir superset-frontend/packages/superset-ui-core/src/style/index.tsx
# https://preset.io/blog/theming-superset-progress-update/
# [SIP-82] Improving Superset Theming https://github.com/apache/superset/issues/20159
# https://www.systeme-de-design.gouv.fr/elements-d-interface/fondamentaux-de-l-identite-de-l-etat/couleurs-palette
THEME_OVERRIDES = {
    "borderRadius": 5,
    "colors": {
        "text": {
            "label": DSFR_COLORS["sun"]["grey-425-625"],
            "help": DSFR_COLORS["sun"]["grey-425-625"],
        },
        "primary": {
            "base": DSFR_COLORS["sun"]["blue-france-sun-113-625"],
            "dark1": DSFR_COLORS["sun"]["blue-france-sun-113-625"],
            "dark2": DSFR_COLORS["sun"]["blue-france-sun-113-625"],
            "light1": DSFR_COLORS["sun"]["blue-france-main-525"],
            "light2": DSFR_COLORS["sun"]["blue-france-850-200"],
            "light3": DSFR_COLORS["sun"]["blue-france-925-125"],
            "light4": DSFR_COLORS["sun"]["blue-france-950-100"],
            "light5": DSFR_COLORS["sun"]["blue-france-975-75"],
        },
        "secondary": {
            "base": "FF1493", #Rose neon
            "dark1": DSFR_COLORS["sun"]["grey-0-1000"], #000000 dans les sub menu par exemple Requetes sauvegardes Historiques des requetes Consultes, il faut que cela ressorte mais cest du texte
            "dark2": DSFR_COLORS["sun"]["blue-france-sun-113-625"], # pas utilise pour l'instant, les boutons Actions Poubelle etc
            "dark3": DSFR_COLORS["sun"]["blue-france-sun-113-625"], # au hover de View Dataset uniquement dans le add dataset panel
            "light1": DSFR_COLORS["sun"]["blue-france-sun-113-625"], # pas utilise pour l'instant
            "light2": DSFR_COLORS["sun"]["blue-france-sun-113-625"], # par exemple le titre dans la modale Preview Saved Query
            "light3": DSFR_COLORS["sun"]["blue-france-sun-113-625"], # par exemple la bordure du TAPEZ "EFFACER" POUR CONFIRMER
            #"light4": DSFR_COLORS["sun"]["blue-france-850-200"], #cacafb le background dans les sub menu par exemple Requetes sauvegardes Historiques des requetes Consultes, il faut que cela ressorte mais cest du texte
            "light4": DSFR_COLORS["sun"]["blue-france-925-125"], #e3e3fd,
            #"light4": "grey-975-75",
            "light5": DSFR_COLORS["sun"]["blue-france-925-125"], # le background de TableCollection et le background des petites pills sur les SubMenu Requetes sauvegardees consultees etc
        },
        "grayscale": {
            "base": DSFR_COLORS["sun"]["grey-425-625"],# pas mal de sous-titres Recherche, Proprietaire, ..., les boutons '...' ou caret-down, les boutons Actions Poubelle etc
            "dark1": DSFR_COLORS["sun"]["grey-200-850"], # sous-menu SQL> Parametres>, les titres des graphs, le text hover des menus Dashboards Charts..., apparemment pas mal dans les plugins React
            "dark2": DSFR_COLORS["sun"]["grey-50-1000"], # utilise dans des plugins react, dans certains titres h4 comme DatabaseModal, le background des Tooltips (superset-ui-chart-controls/src/components/Tooltip.tsx
            "light1": DSFR_COLORS["sun"]["grey-625-425"],
            "light2": DSFR_COLORS["sun"]["grey-925-125"], #e5e5e5
            "light3": DSFR_COLORS["sun"]["grey-950-100"], #eeeeee
            "light4": DSFR_COLORS["sun"]["grey-975-75"], #f6f6f6
            "light5": DSFR_COLORS["sun"]["grey-1000-50"], #ffffff
        },
        "error": {
            "base": DSFR_COLORS["sun"]["error-425-625"], #ce0500
            "dark1": DSFR_COLORS["sun"]["error-425-625"],
            "dark2": DSFR_COLORS["sun"]["grey-0-1000"], #000000, 
            "light1": DSFR_COLORS["sun"]["error-425-625"], 
            "light2": DSFR_COLORS["sun"]["error-950-100"],
        },
        "warning": {
            "base": DSFR_COLORS["sun"]["warning-425-625"], #b34000
            "dark1": DSFR_COLORS["sun"]["warning-425-625"],
            "dark2": DSFR_COLORS["sun"]["grey-0-1000"], #000000, 
            "light1": DSFR_COLORS["sun"]["warning-425-625"],
            "light2": DSFR_COLORS["sun"]["warning-950-100"],
        },
        "alert": {
            "base": DSFR_COLORS["sun"]["green-tilleul-verveine-925-125"],
            "dark1": DSFR_COLORS["sun"]["green-tilleul-verveine-925-125"],
            "dark2": DSFR_COLORS["sun"]["grey-0-1000"], #000000, 
            "light1": DSFR_COLORS["sun"]["green-tilleul-verveine-925-125"],
            "light2": DSFR_COLORS["sun"]["green-tilleul-verveine-975-75"],
        },
        "success": {
            "base": DSFR_COLORS["sun"]["success-425-625"],
            "dark1": DSFR_COLORS["sun"]["success-425-625"],
            "dark2": DSFR_COLORS["sun"]["grey-0-1000"], #000000, 
            "light1": DSFR_COLORS["sun"]["success-425-625"],
            "light2": DSFR_COLORS["sun"]["success-950-100"],
        },
        "info": {
            "base": DSFR_COLORS["sun"]["info-425-625"],
            "dark1": DSFR_COLORS["sun"]["info-425-625"],
            "dark2": DSFR_COLORS["sun"]["grey-0-1000"], #000000, 
            "light1": DSFR_COLORS["sun"]["info-425-625"],
            "light2": DSFR_COLORS["sun"]["info-950-100"],
        },
    },
    "typography": {
        "families": {
            "sansSerif": "Marianne, Inter, Helvetice, Arial",
            "serif": "Marianne, Georgia, Times New Roman, Times, serif",
            "monospace": "Marianne, Fira Code, Courier New, monospace",
        },
    },
}


# EXTRA_CATEGORICAL_COLOR_SCHEMES is used for adding custom categorical color schemes
# see DSFR colors "Couleurs illustratives"
# https://preset.io/blog/customizing-chart-colors-with-superset-and-preset/#creating-custom-color-palettes
# https://gouvernementfr.github.io/dsfr-chart/#colors
EXTRA_CATEGORICAL_COLOR_SCHEMES = [
    {
        "id": "dsfr_sun",
        "description": "Couleurs illustratives du DSFR (thème clair)",
        "label": "DSFR (thème clair)",
        "isDefault": True,
        "colors": [
            DSFR_COLORS["sun"]["green-bourgeon-sun-425-moon-759"],
            DSFR_COLORS["sun"]["blue-ecume-sun-247-moon-675"],
            DSFR_COLORS["sun"]["purple-glycine-sun-319-moon-630"],
            DSFR_COLORS["sun"]["pink-macaron-sun-406-moon-833"],
            DSFR_COLORS["sun"]["yellow-tournesol-sun-407-moon-922"],
            DSFR_COLORS["sun"]["orange-terre-battue-sun-370-moon-672"],
            DSFR_COLORS["sun"]["brown-cafe-creme-sun-383-moon-885"],
            DSFR_COLORS["sun"]["beige-gris-galet-sun-407-moon-821"],
            DSFR_COLORS["sun"]["green-emeraude-sun-425-moon-753"],
            DSFR_COLORS["sun"]["blue-cumulus-sun-368-moon-732"],
            DSFR_COLORS["sun"]["pink-tuile-sun-425-moon-750"],
            DSFR_COLORS["sun"]["yellow-moutarde-sun-348-moon-860"],
            DSFR_COLORS["sun"]["brown-caramel-sun-425-moon-901"],
            DSFR_COLORS["sun"]["green-menthe-sun-373-moon-652"],
            DSFR_COLORS["sun"]["brown-opera-sun-395-moon-820"],
            DSFR_COLORS["sun"]["green-archipel-sun-391-moon-716"],
            DSFR_COLORS["sun"]["green-tilleul-verveine-sun-418-moon-817"],
        ],
    },
    {
        "id": "dsfr_moon",
        "description": "Couleurs illustratives du DSFR (thème sombre)",
        "label": "DSFR (thème sombre)",
        "isDefault": False,
        "colors": [
            DSFR_COLORS["moon"]["green-bourgeon-sun-425-moon-759"],
            DSFR_COLORS["moon"]["blue-ecume-sun-247-moon-675"],
            DSFR_COLORS["moon"]["purple-glycine-sun-319-moon-630"],
            DSFR_COLORS["moon"]["pink-macaron-sun-406-moon-833"],
            DSFR_COLORS["moon"]["yellow-tournesol-sun-407-moon-922"],
            DSFR_COLORS["moon"]["orange-terre-battue-sun-370-moon-672"],
            DSFR_COLORS["moon"]["brown-cafe-creme-sun-383-moon-885"],
            DSFR_COLORS["moon"]["beige-gris-galet-sun-407-moon-821"],
            DSFR_COLORS["moon"]["green-emeraude-sun-425-moon-753"],
            DSFR_COLORS["moon"]["blue-cumulus-sun-368-moon-732"],
            DSFR_COLORS["moon"]["pink-tuile-sun-425-moon-750"],
            DSFR_COLORS["moon"]["yellow-moutarde-sun-348-moon-860"],
            DSFR_COLORS["moon"]["brown-caramel-sun-425-moon-901"],
            DSFR_COLORS["moon"]["green-menthe-sun-373-moon-652"],
            DSFR_COLORS["moon"]["brown-opera-sun-395-moon-820"],
            DSFR_COLORS["moon"]["green-archipel-sun-391-moon-716"],
            DSFR_COLORS["moon"]["green-tilleul-verveine-sun-418-moon-817"],
        ],
    },
]

# EXTRA_SEQUENTIAL_COLOR_SCHEMES is used for adding custom sequential color schemes


def make_description(color_name):
    try:
        cut_index = color_name.index("sun")
        formatted_color_name = color_name[:cut_index].replace('-', ' ')
        return formatted_color_name.title()
    except ValueError:
        return color_name.title().replace('-', ' ')


EXTRA_SEQUENTIAL_COLOR_SCHEMES = [
    {
        "id": colorname,
        "description": make_description(colorname),
        "isDiverging": True,
        "label": make_description(colorname),
        "isDefault": False,
        "colors": [
            DSFR_COLORS["sun"][colorname],
            DSFR_COLORS["sun"]["grey-950-100"], 
        ],
    }
    for colorname in [
          "green-bourgeon-sun-425-moon-759",
          "blue-ecume-sun-247-moon-675",
          "purple-glycine-sun-319-moon-630",
          "pink-macaron-sun-406-moon-833",
          "yellow-tournesol-sun-407-moon-922",
          "orange-terre-battue-sun-370-moon-672",
          "brown-cafe-creme-sun-383-moon-885",
          "beige-gris-galet-sun-407-moon-821",
          "green-emeraude-sun-425-moon-753",
          "blue-cumulus-sun-368-moon-732",
          "pink-tuile-sun-425-moon-750",
          "yellow-moutarde-sun-348-moon-860",
          "brown-caramel-sun-425-moon-901",
          "green-menthe-sun-373-moon-652",
          "brown-opera-sun-395-moon-820",
          "green-archipel-sun-391-moon-716",
          "green-tilleul-verveine-sun-418-moon-817",
        ]
]
EXTRA_SEQUENTIAL_COLOR_SCHEMES[0]["isDefault"] = True

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

#HTML_SANITIZATION = False
# Sanitizes the HTML content used in markdowns to allow its rendering in a safe manner.
# Disabling this option is not recommended for security reasons. If you wish to allow
# valid safe elements that are not included in the default sanitization schema, use the
# HTML_SANITIZATION_SCHEMA_EXTENSIONS configuration.
HTML_SANITIZATION = True

# Use this configuration to extend the HTML sanitization schema.
# By default we use the GitHub schema defined in
# https://github.com/syntax-tree/hast-util-sanitize/blob/main/lib/schema.js
# For example, the following configuration would allow the rendering of the
# style attribute for div elements and the ftp protocol in hrefs:
HTML_SANITIZATION_SCHEMA_EXTENSIONS = {
  "attributes": {
    "div": ["style"],
  },
  "protocols": {
    "href": ["ftp"],
  }
}
# Be careful when extending the default schema to avoid XSS attacks.
HTML_SANITIZATION_SCHEMA_EXTENSIONS: dict[str, Any] = {}

# Default cache timeout, applies to all cache backends unless specifically overridden in
# each cache config.
CACHE_DEFAULT_TIMEOUT = int(timedelta(days=1).total_seconds())

# Default cache for Superset objects
CACHE_CONFIG: CacheConfig = {
    "CACHE_TYPE": "RedisCache",
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_cache',
    'CACHE_REDIS_URL': 'redis://redis:6379/1',
}

# Cache for datasource metadata and query results
DATA_CACHE_CONFIG: CacheConfig = {
    "CACHE_TYPE": "RedisCache",
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_data_cache',
    'CACHE_REDIS_URL': 'redis://redis:6379/1',
}

# Cache for dashboard filter state. `CACHE_TYPE` defaults to `SupersetMetastoreCache`
# that stores the values in the key-value table in the Superset metastore, as it's
# required for Superset to operate correctly, but can be replaced by any
# `Flask-Caching` backend.
FILTER_STATE_CACHE_CONFIG: CacheConfig = {
    "CACHE_TYPE": "RedisCache",
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_filter_cache',
    'CACHE_REDIS_URL': 'redis://redis:6379/1',
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=90).total_seconds()),
    # Should the timeout be reset when retrieving a cached value?
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    # The following parameter only applies to `MetastoreCache`:
    # How should entries be serialized/deserialized?
    "CODEC": JsonKeyValueCodec(),
}

# Cache for explore form data state. `CACHE_TYPE` defaults to `SupersetMetastoreCache`
# that stores the values in the key-value table in the Superset metastore, as it's
# required for Superset to operate correctly, but can be replaced by any
# `Flask-Caching` backend.
EXPLORE_FORM_DATA_CACHE_CONFIG: CacheConfig = {
    "CACHE_TYPE": "RedisCache",
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_explore_form_cache',
    'CACHE_REDIS_URL': 'redis://redis:6379/1',
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=7).total_seconds()),
    # Should the timeout be reset when retrieving a cached value?
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    # The following parameter only applies to `MetastoreCache`:
    # How should entries be serialized/deserialized?
    "CODEC": JsonKeyValueCodec(),
}

# Define a list of usernames to be excluded from all dropdown lists of users
# Owners, filters for created_by, etc.
# The users can also be excluded by overriding the get_exclude_users_from_lists method
# in security manager
EXCLUDE_USERS_FROM_LISTS: list[str] | None = None

# The link to a page containing common errors and their resolutions
# It will be appended at the bottom of sql_lab errors.
TROUBLESHOOTING_LINK = ""

# This link should lead to a page with instructions on how to gain access to a
# Datasource. It will be placed at the bottom of permissions errors.
PERMISSION_INSTRUCTIONS_LINK = ""

# If a callable is specified, it will be called at app startup while passing
# a reference to the Flask app. This can be used to alter the Flask app
# in whatever way.
# example: FLASK_APP_MUTATOR = lambda x: x.before_request = f
FLASK_APP_MUTATOR = None
