.PHONY: lint-all lint-helm lint-py lint-dockerfile lint-shell

# =================
# Variables
# =================
# Helm
TMP_DIR = /tmp/superset-chart
HELM_REPO_URL = http://apache.github.io/superset/
HELM_CHART    = superset/superset
VALUES_FILE   = docs/installation/helm/values.yaml

# Docker
SUPERSET_VERSION = 6.1.0
DSFR_VERSION = 1.14.4
DSFR_CHART_VERSION = 2.0.3

# =================
# Linting
# =================

lint-py:
	ruff check superset-dsfr/docker/pythonpath_dev/

lint-dockerfile:
	docker run --rm -i ghcr.io/hadolint/hadolint < Dockerfile

lint-shell:
	shellcheck -x superset-dsfr/docker/docker-init.sh
	shellcheck -x superset-dsfr/docker/docker-bootstrap.sh
	shellcheck -x superset-dsfr/docker/docker-dsfr.sh

lint-helm:
	helm repo add superset $(HELM_REPO_URL)
	helm repo update
	rm -rf $(TMP_DIR)
	mkdir -p $(TMP_DIR)
	helm pull superset/superset --untar --untardir $(TMP_DIR)
	helm lint $(TMP_DIR)/superset -f $(VALUES_FILE)
	helm template test-release $(TMP_DIR)/superset -f $(VALUES_FILE) > /dev/null
	rm -rf $(TMP_DIR)

lint-all: lint-py lint-dockerfile lint-shell lint-helm check-translation

# =================
# Docker builds
# =================

docker-build-dsfr:
	@echo "Building Superset with DSFR..."
	docker build \
		--build-arg SUPERSET_VERSION=$(SUPERSET_VERSION) \
		--build-arg TAG_DSFR=$(DSFR_VERSION) \
		--build-arg TAG_DSFR_CHART=$(DSFR_CHART_VERSION) \
		--build-arg USE_DSFR=true \
		-t chartsgouv:$(SUPERSET_VERSION)-dsfr-$(DSFR_VERSION)-chart-$(DSFR_CHART_VERSION) .

docker-build-without-dsfr:
	@echo "Building Superset without DSFR..."
	docker build \
		--build-arg SUPERSET_VERSION=$(SUPERSET_VERSION) \
		--build-arg TAG_DSFR=$(DSFR_VERSION) \
		--build-arg TAG_DSFR_CHART=$(DSFR_CHART_VERSION) \
		--build-arg USE_DSFR=false \
		-t chartsgouv:$(SUPERSET_VERSION)-no-dsfr .

# =================
# Cleanup
# =================

clean-docker-images:
	docker rmi chartsgouv:$(SUPERSET_VERSION)-dsfr-$(DSFR_VERSION)-chart-$(DSFR_CHART_VERSION) chartsgouv:$(SUPERSET_VERSION)-no-dsfr 2>/dev/null || true
