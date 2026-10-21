# Define ARGS (Defaults, overridden in GitLab CI)
ARG SUPERSET_REPO=apache/superset
ARG SUPERSET_VERSION=6.1.0
ARG REPO_OWNER=GouvernementFR
ARG REPO_NAME=dsfr
ARG TAG_DSFR=1.15.2
ARG TAG_DSFR_CHART=2.1.1
ARG USE_DSFR=true

# ------------------------------------------
# Stage 1: Build frontend translations
# ------------------------------------------
FROM node:24-bookworm-slim AS frontend_translations

ARG USE_DSFR
ARG DSFR_VERSION
ARG DSFR_CHART_VERSION
ARG SUPERSET_VERSION


ENV DSFR_ACCEPT_LICENSE=1
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /app

# Download DSFR only if USE_DSFR=true
RUN if [ "$USE_DSFR" = "true" ]; then \
    # Install dependencies
        echo "Installing DSFR dependencies"; \
        npm install @gouvfr/dsfr@${DSFR_VERSION} @gouvfr/dsfr-chart@${DSFR_CHART_VERSION}; \
    else \
        # Create dummy folders to avoid build errors
        echo "USE_DSFR=false, creating empty folders"; \
        mkdir -p /app/node_modules/@gouvfr/dsfr/ /app/node_modules/@gouvfr/dsfr-chart/; \
    fi

# Copy translation files
COPY superset-dsfr/translations /app/translations

# Install dependencies
RUN npm install -g po2json@0.4.5

# Convert the PO file matching the Superset version to JSON
RUN set -eux; \
    VER=$(echo "$SUPERSET_VERSION" | cut -d. -f1-3 | tr '.' '_'); \
    PO_FILE="/app/translations/messages_${VER}.po"; \
    if [ ! -f "$PO_FILE" ]; then \
        echo "ERROR: no translation file found for Superset version ${SUPERSET_VERSION}"; \
        ls -1 /app/translations/; \
        exit 1; \
    fi; \
    echo "Converting $PO_FILE -> /app/out/fr/LC_MESSAGES/messages.json"; \
    mkdir -p /app/out/fr/LC_MESSAGES; \
    po2json "$PO_FILE" "/app/out/fr/LC_MESSAGES/messages.json" --format=jed1.x --domain=superset;

# ------------------------------------------
# Stage 2: Build Superset Custom img
# ------------------------------------------
ARG SUPERSET_VERSION
ARG SUPERSET_REPO
FROM ${SUPERSET_REPO}:${SUPERSET_VERSION} AS superset_custom_img

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Must repeat ARG here to be able to use it in this stage
ARG SUPERSET_VERSION
ARG USE_DSFR

# Root user is 0
USER 0
WORKDIR /app

# Copy Superset custom folders
COPY superset-dsfr /tmp/superset-custom/
# Always copy (empty folders if USE_DSFR=false, real if USE_DSFR=true)
COPY --from=frontend_translations /app/node_modules/@gouvfr/dsfr/ /tmp/@gouvfr/dsfr/
COPY --from=frontend_translations /app/node_modules/@gouvfr/dsfr-chart/ /tmp/@gouvfr/dsfr-chart/

# ------------------------------------------
# Common Superset customization
# ------------------------------------------
RUN set -eux; \
    echo "Copying common Superset customizations"; \
    cp /tmp/superset-custom/assets/404.html  /app/superset/static/assets/404.html; \
    cp /tmp/superset-custom/assets/500.html  /app/superset/static/assets/500.html; \
    cp /tmp/superset-custom/templates_overrides/superset/public_welcome.html  /app/superset/templates/superset/; \
    cp /tmp/superset-custom/templates_overrides/head_custom_extra.html  /app/superset/templates/; \
    echo "Common customizations copied"

# ------------------------------------------
# French translation & DSFR integrations
# ------------------------------------------
RUN set -eux; \
    if [ "$USE_DSFR" = "true" ]; then \
        echo "Copying DSFR assets"; \
        cp -r /tmp/@gouvfr/dsfr/dist   /app/superset/static/assets/dsfr; \
        cp -r /tmp/@gouvfr/dsfr-chart       /app/superset/static/assets/dsfr-chart; \
        cp -r /tmp/superset-custom/assets       /app/superset/static/assets/local; \
    else \
        echo "Skipping DSFR integration"; \
    fi; \
    # Compile backend translations to MO files (version-specific .po)
    VER=$(echo "$SUPERSET_VERSION" | cut -d. -f1-3 | tr '.' '_'); \
    PO_FILE="/tmp/superset-custom/translations/messages_${VER}.po"; \
    if [ ! -f "$PO_FILE" ]; then \
        echo "ERROR: no translation file found for Superset version ${SUPERSET_VERSION}"; \
        ls -1 /tmp/superset-custom/translations/; \
        exit 1; \
    fi; \
    mkdir -p /app/translations_mo/fr/LC_MESSAGES; \
    cp "$PO_FILE" /app/translations_mo/fr/LC_MESSAGES/messages.po; \
    pybabel compile --statistics -d /app/translations_mo; \
    # Merge compiled backend MO files into Superset translations folder
    cp -r /app/translations_mo/* /app/superset/translations/;

# Copy frontend translations
COPY --from=frontend_translations /app/out /app/superset/translations

# Install additional dependencies
RUN set -eux; \
    echo "Installing extra packages"; \
    if command -v uv > /dev/null 2>&1; then \
        uv pip install --no-cache-dir -r /tmp/superset-custom/docker/requirements-local.txt; \
    else \
        pip install --no-cache-dir -r /tmp/superset-custom/docker/requirements-local.txt; \
    fi

# Superset user is 999
USER 999
