SHELL := /usr/bin/env bash
.PHONY: helmlint

TMP_DIR = /tmp/superset-chart
HELM_REPO_URL = http://apache.github.io/superset/
HELM_CHART    = superset/superset
VALUES_FILE   = docs/installation/helm/values.yaml

.PHONY: helmlint

helmlint:
	helm repo add superset $(HELM_REPO_URL)
	helm repo update
	rm -rf $(TMP_DIR)
	mkdir -p $(TMP_DIR)
	helm pull superset/superset --untar --untardir $(TMP_DIR)
	helm lint $(TMP_DIR)/superset -f $(VALUES_FILE)
	helm template test-release $(TMP_DIR)/superset -f $(VALUES_FILE) > /dev/null
	rm -rf $(TMP_DIR)
