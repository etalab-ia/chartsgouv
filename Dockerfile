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
FROM ubuntu:20.04 AS dsfr_image

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
RUN wget -O dsfr-chart.zip "https://github.com/${REPO_OWNER}/dsfr-chart/releases/download/v${TAG_DSFR_CHART}/dsfr-chart-v${TAG_DSFR_CHART}.zip"
RUN unzip dsfr-chart.zip -d dsfr-chart && rm dsfr-chart.zip

# Import custom Superset templates
COPY superset-dsfr ./superset-dsfr/

RUN ls -la /app

# ------------------------------------------
# Stage 2: Build chartsgouv Image
# ------------------------------------------
ARG SUPERSET_VERSION
ARG SUPERSET_REPO
FROM ${SUPERSET_REPO}:${SUPERSET_VERSION} AS chartsgouv_img

USER root
WORKDIR /app

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

# Override Superset french traduction
COPY --from=dsfr_image /app/superset-dsfr/translations/fr/LC_MESSAGES/messages.po    /app/superset/translations/fr/LC_MESSAGES/messages.po

# Update CSS Colors
RUN find /app/superset/static/assets -name "theme*.css" -exec sed -i \
        -e "s/#20a7c9/#000091/g" \
        -e "s/#45bed6/#000091/g" \
        -e "s/#1985a0/#000091/g" {} \;

# Install dependencies
COPY --from=dsfr_image /app/superset-dsfr/requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

USER superset
