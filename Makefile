.PHONY: lint-all lint-helm lint-py lint-dockerfile lint-shell clean-docker-images clean-venv

# =================
# Variables
# =================
# Developpement
ENV_NAME = .env-dev

# Helm
TMP_DIR = /tmp/superset-chart
HELM_REPO_URL = http://apache.github.io/superset/
HELM_CHART    = superset/superset
VALUES_FILE   = docs/installation/helm/values.yaml

# Docker
SUPERSET_VERSION = 6.1.0
DSFR_VERSION = 1.15.0
DSFR_CHART_VERSION = 2.1.1

# =================
# Development
# =================
setup-py-env:
	@if [ -d $(ENV_NAME) ]; then rm -rf $(ENV_NAME); fi
	@echo "Creating virtual environment for translation checks..."
	python3 -m venv $(ENV_NAME)
	@echo "Installing packages..."
	./$(ENV_NAME)/bin/pip install -r requirements-dev.txt
	@echo "Installing pre-commit hooks..."
	./$(ENV_NAME)/bin/pre-commit install

# =================
# Linting
# =================

lint-py:
	./$(ENV_NAME)/bin/pre-commit run --all-files

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
# Checks
# =================

check-translation:
	@echo "Compiling translations..."
	./$(ENV_NAME)/bin/pybabel compile -d superset-dsfr/translations --statistics

# =================
# Docker builds
# =================

docker-build-dsfr:
	@echo "Building Superset with DSFR..."
	docker build \
		--build-arg SUPERSET_VERSION=$(SUPERSET_VERSION) \
		--build-arg DSFR_VERSION=$(DSFR_VERSION) \
		--build-arg DSFR_CHART_VERSION=$(DSFR_CHART_VERSION) \
		--build-arg USE_DSFR=true \
		--no-cache \
		-t chartsgouv:$(SUPERSET_VERSION)-dsfr-$(DSFR_VERSION)-chart-$(DSFR_CHART_VERSION) .

docker-build-without-dsfr:
	@echo "Building Superset without DSFR..."
	docker build \
		--build-arg SUPERSET_VERSION=$(SUPERSET_VERSION) \
		--build-arg DSFR_VERSION=$(DSFR_VERSION) \
		--build-arg DSFR_CHART_VERSION=$(DSFR_CHART_VERSION) \
		--build-arg USE_DSFR=false \
		--no-cache \
		-t chartsgouv:$(SUPERSET_VERSION)-no-dsfr .

# =================
# Cleanup
# =================

clean-docker-images:
	docker rmi chartsgouv:$(SUPERSET_VERSION)-dsfr-$(DSFR_VERSION)-chart-$(DSFR_CHART_VERSION) chartsgouv:$(SUPERSET_VERSION)-no-dsfr 2>/dev/null || true

clean-venv:
	rm -rf $(ENV_NAME)

clean-tmp: ## Nettoie les fichiers temporaires
	@echo "Nettoyage des fichiers temporaires"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✓ Nettoyage terminé"


clean-all: clean-docker-images clean-venv clean-tmp
