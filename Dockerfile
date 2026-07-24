# Define ARGS (Defaults, overridden in GitLab CI)
ARG SUPERSET_REPO=apache/superset
ARG SUPERSET_VERSION=4.1.1
ARG DSFR_VERSION=1.13.0
ARG DSFR_CHART_VERSION=2.0.3
ARG USE_DSFR=true

# ------------------------------------------
# Stage 1: Build frontend translations
# ------------------------------------------
FROM node:24-bookworm-slim AS frontend_translations

ARG USE_DSFR
ARG DSFR_VERSION
ARG DSFR_CHART_VERSION


ENV DSFR_ACCEPT_LICENSE=1
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /app

# Download DSFR only if USE_DSFR=true
RUN if [ "$USE_DSFR" = "true" ]; then \
    # Install dependencies
        echo "Installing DSFR dependencies"; \
        npm install --save-exact @gouvfr/dsfr@${DSFR_VERSION} @gouvfr/dsfr-chart@${DSFR_CHART_VERSION}; \
    else \
        # Create dummy folders to avoid build errors
        echo "USE_DSFR=false, creating empty folders"; \
        mkdir -p /app/node_modules/@gouvfr/dsfr/ /app/node_modules/@gouvfr/dsfr-chart/; \
    fi

# Copy translation files
COPY superset-dsfr/translations /app/translations

# Install dependencies
RUN npm install -g po2json@0.4.5

# Convert PO to JSON for Superset and FAB
RUN set -eux; \
    # Superset translations
    find ./translations -name "*.po" | while read file -r; do \
        dirname=$(dirname "$file"); \
        basename=$(basename "$file" .po); \
        output_file="$dirname/$basename.json"; \
        echo "Converting $file -> $output_file"; \
        po2json "$file" "$output_file" --format=jed1.x --domain=superset || echo "Error converting $file"; \
    done;

# ------------------------------------------
# Stage 2: Build Superset Custom img
# ------------------------------------------
ARG SUPERSET_VERSION
ARG SUPERSET_REPO
FROM ${SUPERSET_REPO}:${SUPERSET_VERSION} AS superset_custom_img

# Must repeat ARG here to be able to use it in this stage
ARG SUPERSET_VERSION
ARG USE_DSFR

USER root
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
    # Compile backend translations to MO files
    cp -r /tmp/superset-custom/translations /app/translations_mo/; \
    pybabel compile --statistics -d /app/translations_mo; \
    # Merge compiled backend MO files into Superset translations folder
    cp -r /app/translations_mo/* /app/superset/translations/;

# Copy frontend translations
COPY --from=frontend_translations /app/translations /app/superset/translations

# Install additional dependencies
RUN set -eux; \
    echo "Installing extra packages"; \
    if command -v uv > /dev/null 2>&1; then \
        uv pip install --no-cache-dir -r /tmp/superset-custom/docker/requirements-local.txt; \
    else \
        pip install --no-cache-dir -r /tmp/superset-custom/docker/requirements-local.txt; \
    fi

USER superset
