TMP_DIR = /tmp/superset-chart
HELM_REPO_URL = http://apache.github.io/superset/
HELM_CHART    = superset/superset
VALUES_FILE   = docs/installation/helm/values.yaml

.PHONY: lint-all lint-helm lint-py lint-dockerfile lint-shell

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

