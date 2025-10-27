# Define ARGS (Defaults, overridden in GitLab CI)
ARG SUPERSET_REPO=apache/superset
ARG SUPERSET_VERSION=4.1.1
ARG REPO_OWNER=GouvernementFR
ARG REPO_NAME=dsfr
ARG TAG_DSFR=1.13.0
ARG TAG_DSFR_CHART=2.0.3
ARG USE_DSFR=true


# ------------------------------------------
# Stage 1: Download DSFR
# ------------------------------------------
FROM ubuntu:24.04 AS custom_image

# Must repeat ARG here to be able to use it in this stage
ARG REPO_OWNER
ARG REPO_NAME
ARG TAG_DSFR
ARG TAG_DSFR_CHART
ARG USE_DSFR

USER root

# Set the working directory
WORKDIR /app

# Import Superset custom folder
COPY superset-dsfr ./superset-custom/

# Download DSFR only if USE_DSFR=true
RUN if [ "$USE_DSFR" = "true" ]; then \
    # Install dependencies
        apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*; \
        # Debugging: Check if wget/unzip are installed
        command -v unzip && command -v wget; \
        # Download DSFR assets
        wget -O dsfr-base.zip "https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/download/v${TAG_DSFR}/${REPO_NAME}-v${TAG_DSFR}.zip" && \
        unzip dsfr-base.zip -d dsfr-base && rm dsfr-base.zip && \
        wget -O dsfr-chart.zip "https://github.com/${REPO_OWNER}/dsfr-chart/archive/refs/tags/v${TAG_DSFR_CHART}.zip" && \
        unzip dsfr-chart.zip -d dsfr-chart && rm dsfr-chart.zip && \
        echo "DSFR downloaded"; \
    else \
        # Create dummy folders to avoid build errors
        mkdir -p dsfr-base/dist dsfr-chart; \
      echo "Skipping DSFR download. Dummy folders dsfr-base/dist dsfr-chart created."; \
    fi

# ------------------------------------------
# Stage 2: Build frontend translations
# ------------------------------------------
FROM node:24-bookworm-slim AS frontend_translations

WORKDIR /app

# Copy translation files
COPY superset-dsfr/translations /app/translations

# Install dependencies
RUN npm install -g po2json

# Convert PO to JSON for Superset and FAB
RUN set -eux; \
    # Superset translations
    find ./translations -name "*.po" | while read file; do \
        dirname=$(dirname "$file"); \
        basename=$(basename "$file" .po); \
        output_file="$dirname/$basename.json"; \
        echo "Converting $file -> $output_file"; \
        po2json "$file" "$output_file" --format=jed1.x --domain=superset || echo "Error converting $file"; \
    done;

# ------------------------------------------
# Stage 3: Build Superset Custom img
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
COPY --from=custom_image /app/superset-custom/ /tmp/superset-custom/
# Always copy (empty folders if USE_DSFR=false, real if USE_DSFR=true)
COPY --from=custom_image /app/dsfr-base/ /tmp/dsfr-base/
COPY --from=custom_image /app/dsfr-chart/ /tmp/dsfr-chart/

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
# Version-specific overrides
# ------------------------------------------
RUN set -eux; \
    major_superset_version="$(echo "$SUPERSET_VERSION" | cut -d. -f1)"; \
    if [ "$major_superset_version" -lt 6 ]; then \
        echo "Applying overrides for Superset v<6"; \
        cp /tmp/superset-custom/templates_overrides/superset/base.html  /app/superset/templates/superset/; \
        cp /tmp/superset-custom/templates_overrides/superset/basic.html /app/superset/templates/superset/; \
        cp /tmp/superset-custom/templates_overrides/tail_js_custom_extra.html \
           /app/superset/templates/tail_js_custom_extra.html; \
    else \
        echo "Skipping old overrides (Superset > 6)"; \
    fi

# ------------------------------------------
# Optional DSFR integration
# ------------------------------------------
RUN set -eux; \
    if [ "$USE_DSFR" = "true" ]; then \
        echo "Copying DSFR assets"; \
        cp -r /tmp/dsfr-base/dist   /app/superset/static/assets/dsfr; \
        cp -r /tmp/dsfr-chart       /app/superset/static/assets/dsfr-chart; \
        cp -r /tmp/superset-custom/assets       /app/superset/static/assets/local; \
        echo "Updating DSFR CSS colors"; \
        find /app/superset/static/assets -name "theme*.css" -exec sed -i \
          -e "s/#20a7c9/#000091/g" \
          -e "s/#45bed6/#000091/g" \
          -e "s/#1985a0/#000091/g" {} \; ; \
        echo "DSFR integration done"; \
    else \
        echo "Skipping DSFR integration"; \
    fi

# Override Superset french traduction
# Copy backend translations (PO files)
COPY --from=custom_image /app/superset-custom/translations /app/translations_mo

# Compile backend translations to MO files
RUN pybabel compile --statistics -d /app/translations_mo

# Merge compiled backend MO files into Superset translations folder
RUN cp -r /app/translations_mo/* /app/superset/translations/

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
