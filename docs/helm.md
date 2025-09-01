# 🚀 Déploiement de ChartsGouv avec Helm

Prérequis:
- Kubernetes
- Helm

## Image par défaut

En cours de rédaction

Pour monter la configuration dans votre environnement k8s,


Pour déployer l'application:
```bash
# Lancez la commande depuis le dossier chartsgouv/superset
helm repo add superset http://apache.github.io/superset/
helm repo update superset
helm upgrade --install app_name superset/superset -f values.yaml
```


## Image avec une configuration customisée

En cours de rédaction





Tous les éléments de configuration sont présents sur le repo officiel d'[Apache Superset](https://github.com/apache/superset/tree/master/helm/superset)