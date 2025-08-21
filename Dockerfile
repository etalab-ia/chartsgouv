# Define ARGS (Defaults, overridden in GitLab CI)
ARG SUPERSET_REPO=apache/superset
ARG SUPERSET_VERSION=4.1.1
ARG REPO_OWNER=GouvernementFR
ARG REPO_NAME=dsfr
ARG TAG_DSFR=1.13.0
ARG TAG_DSFR_CHART=2.0.3


# ------------------------------------------
# Stage 1: Download DSFR
# ------------------------------------------
FROM ubuntu:24.04 AS dsfr_image

# Getting back ARG values
ARG REPO_OWNER
ARG REPO_NAME
ARG TAG_DSFR
ARG TAG_DSFR_CHART

USER root

# Install dependencies
RUN apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*

# Debugging: Check if wget/unzip are installed
RUN command -v unzip && command -v wget

# Set the working directory
WORKDIR /app

# Define DSFR Download URL
# Download DSFR
RUN wget -O dsfr-base.zip "https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/download/v${TAG_DSFR}/${REPO_NAME}-v${TAG_DSFR}.zip"
RUN unzip dsfr-base.zip -d dsfr-base && rm dsfr-base.zip

# Download DSFR Chart dynamically
RUN wget -O dsfr-chart.zip "https://github.com/${REPO_OWNER}/dsfr-chart/archive/refs/tags/v${TAG_DSFR_CHART}.zip"
RUN unzip dsfr-chart.zip -d dsfr-chart && rm dsfr-chart.zip

# Import custom Superset templates
COPY superset ./superset-dsfr/
COPY translations ./translations/

RUN ls -la /app

# ------------------------------------------
# Stage 2: Build frontend translations
# ------------------------------------------
FROM node:24-bookworm-slim AS frontend_translations

WORKDIR /app

# Copy translation files
COPY translations /app/translations

# Install dependencies
RUN npm install -g po2json

# Convert PO to JSON for Superset and FAB
RUN set -eux; \
    # Superset translations
    find ./translations/superset/translations -name "*.po" | while read file; do \
        dirname=$(dirname "$file"); \
        basename=$(basename "$file" .po); \
        output_file="$dirname/$basename.json"; \
        echo "Converting $file -> $output_file"; \
        po2json "$file" "$output_file" --format=jed1.x --domain=superset || echo "Error converting $file"; \
    done;

# ------------------------------------------
# Stage 3: Build chartsgouv Image
# ------------------------------------------
ARG SUPERSET_VERSION
ARG SUPERSET_REPO
FROM ${SUPERSET_REPO}:${SUPERSET_VERSION} AS chartsgouv_img

USER root
WORKDIR /app

# Copy base + dsfr config
ENV SUPERSET_CONFIG_PATH=/app/pythonpath/superset_config_base_dsfr.py
COPY --from=dsfr_image /app/superset-dsfr/docker/pythonpath_dev/superset_config_docker.py /app/pythonpath/superset_config_base_dsfr.py

# Copy DSFR assets from dsfr_image stage
COPY --from=dsfr_image /app/dsfr-base/dist /app/superset/static/assets/dsfr
COPY --from=dsfr_image /app/dsfr-chart/ /app/superset/static/assets/dsfr-chart
COPY --from=dsfr_image /app/superset-dsfr/assets  /app/superset/static/assets/local

# Override Superset templates
COPY --from=dsfr_image /app/superset-dsfr/templates_overrides/superset/base.html      /app/superset/templates/superset/
COPY --from=dsfr_image /app/superset-dsfr/templates_overrides/superset/basic.html     /app/superset/templates/superset/
COPY --from=dsfr_image /app/superset-dsfr/templates_overrides/superset/public_welcome.html    /app/superset/templates/superset/
COPY --from=dsfr_image /app/superset-dsfr/templates_overrides/tail_js_custom_extra.html   /app/superset/templates/tail_js_custom_extra.html
COPY --from=dsfr_image /app/superset-dsfr/assets/404.html     /app/superset/static/assets/404.html
COPY --from=dsfr_image /app/superset-dsfr/assets/500.html     /app/superset/static/assets/500.html


# Update CSS Colors
RUN find /app/superset/static/assets -name "theme*.css" -exec sed -i \
        -e "s/#20a7c9/#000091/g" \
        -e "s/#45bed6/#000091/g" \
        -e "s/#1985a0/#000091/g" {} \;


# Override Superset french traduction
# 1️⃣ Copy backend translations (PO files)
COPY translations/superset/translations /app/translations_mo

# 2️⃣ Compile backend translations to MO files
RUN pybabel compile --statistics -d /app/translations_mo

# 3️⃣ Merge compiled backend MO files into Superset translations folder
RUN cp -r /app/translations_mo/* /app/superset/translations/

# 4️⃣ Copy frontend translations
COPY --from=frontend_translations /app/translations/superset/translations /app/superset/translations

# Install additional dependencies
COPY --from=dsfr_image /app/superset-dsfr/requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

USER superset
