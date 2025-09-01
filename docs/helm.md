# 🚀 Déploiement de ChartsGouv avec Helm

Prérequis:
- Kubernetes
- Helm

## Installation

Par défaut, lors d'un déploiment d'Apache Superset via Helm, une nouvelle config par défaut est recréée et vient écraser celle de l'image. Il est nécessaire de monter la configuration à l'aide des configmap. 


- Créer le configmap avec la configuration
```bash
# Depuis la racine du projet
kubectl create configmap superset-dsfr-custom-config \
    --from-file=superset/docker/pythonpath_dev/config_options/cache_config.py \
    --from-file=superset/docker/pythonpath_dev/config_options/security_manager.py \
    --from-file=superset/docker/pythonpath_dev/config_options/user_model.py \
    --from-file=superset/docker/pythonpath_dev/config_options/feature_flags.py \
    --from-file=superset/docker/pythonpath_dev/config_options/html_sanitization.py \
    --from-file=superset/docker/pythonpath_dev/config_options/jinja_context_addons.py \
    --from-file=superset/docker/pythonpath_dev/config_options/talisman.py \
    --from-file=superset/docker/pythonpath_dev/config_options/theme.py
```

- Compléter le fichier `superset/values.yaml`  

Le fichier values.yaml mis à disposition est un exemple très minimal. Tous les éléments de configuration sont présents sur le repo officiel d'[Apache Superset](https://github.com/apache/superset/tree/master/helm/superset).

**ingress.hosts**: Renseigner le host depuis lequel votre instance sera accessible.  
**image.repository & image.tag**: préciser l'image à utiliser pour votre déploiement.  
**init.adminUser**: les informations de votre utilisateur administrateur. Il est possible de le créer manuellement en se connectant au pod directement.  
>Par défaut, le déploiement via Helm déploie également une instance de PostgreSQL. Nous recommandons de gérer votre instance PostgreSQL à part.  

Si vous utilisez votre propre instance PostgreSQL, compléter également la section suivante:
```yaml
connections:
    # You need to change below configuration incase bringing own PostgresSQL instance and also set postgresql.enabled:false
    db_host: "{{ .Release.Name }}-postgresql"
    db_port: "5432"
    db_user: superset
    db_pass: superset
    db_name: superset
## Set to false if bringing your own PostgreSQL.
postgresql:
  enabled: false
```

- Déployer l'application
```bash
# Depuis le dossier chartsgouv/superset
helm repo add superset http://apache.github.io/superset/
helm repo update superset
helm upgrade --install your_app_name superset/superset -f values.yaml \
    --set-file=configOverrides.config_override=docker/pythonpath_dev/superset_config_docker.py
```
