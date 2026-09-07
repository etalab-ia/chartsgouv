# 🚀 Déploiement de ChartsGouv avec Helm

> **Important :** ce mode de déploiement est à titre indicatif.

## Table des matières
- [🚀 Déploiement de ChartsGouv avec Helm](#-déploiement-de-chartsgouv-avec-helm)
  - [Table des matières](#table-des-matières)
  - [Pré-requis](#pré-requis)
  - [Installation simple](#installation-simple)
  - [Installation simple avec surcharge de la configuration](#installation-simple-avec-surcharge-de-la-configuration)
  - [Installation complexe](#installation-complexe)

## Pré-requis

- [kubernetes](https://kubernetes.io/)
- [Helm](https://helm.sh/docs/)

## Installation simple

L'installation simple se basera sur l'utilisation d'une image Docker prête à l'emploi. L'image utilisée peut être celles de [Superset](https://hub.docker.com/r/apache/superset/tags?name=5.0), celles mises à votre disposition sur le repo [ChartsGouv](https://github.com/etalab-ia/chartsgouv/pkgs/container/chartsgouv) ou les vôtres si vous les avez build.  
L'exemple ci-dessous utilisera les images ChartsGouv mises à disposition et se basera sur la plateforme kubernetes [SSPCloud](https://datalab.sspcloud.fr/) pour la gestion des urls.

1. Configurer le fichier `values.yaml`

Le fichier [values.yaml](values.yaml) est une version allégée et minimale pour réaliser un déploiement Helm.  
Tous les éléments pouvant être configurés sont disponibles dans le fichier [values.yaml officiel de Superset](https://github.com/apache/superset/blob/master/helm/superset/values.yaml).  
<br>
Ci-dessous les sections minimales à configurer:

- La section **ingress** permet de définir l'url à partir de laquelle votre instance sera accessible.  
- La section **image** permet de définir l'image à utiliser pour votre instance.  
- La section **bootstrapScript** permet d'exécuter des commandes à l'initialisation des containers. Elle est notamment utile pour l'installation de packages complémentaires.
> **Important**: Depuis la version 4.1, les images de Superset n'embarquent plus les drivers pour se connecter aux bases de données. Il faut donc les installer lors de la construction de l'image ou via la section bootstrapScript
- La section **init** permet de charger les données d'exemple (‼️récupérées et chargées depuis internet) et de créer votre utilisateur admin.  
- La section **supersetNode** permet de connecter votre instance à une base de données pour stocker la configuration de votre instance. Cette base n'est pas nécessairement celle qui doit être utilisée pour stocker vos données. Par défaut,
le chart Helm déploie un service PostgreSQL et s'y connecte automatiquement.  


2. Installer le chart

Pour installer le chart, exécutez les commandes suivantes

``` bash
helm repo add superset http://apache.github.io/superset/
helm repo update superset
helm upgrade --install custom-app-name superset/superset -f values.yaml
```

La 1ère installation peut durer quelque minutes. Superset doit lancer les services Redis et PostgreSQL et initialiser la base de données.  
Une fois l'installation terminée, le message suivant sera affiché:
```
NAME: custom-app-name
LAST DEPLOYED: Mon Oct 20 15:03:49 2025
NAMESPACE: projet-dsci
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
1. Get the application URL by running these commands:
  http://my-own-superset.lab.sspcloud.fr/
```

3. Désinstaller le chart

Pour désinstaller votre chart, exécutez les commandes suivantes

``` bash
helm delete custom-app-name
```

🚩Si vous avez utilisé le service PostgreSQL par défaut, un PVC a également été créé. N'oubliez pas de le supprimer également.
``` bash
kubectl get pvc
kubectl delete pvc data-custom-app-name-postgresql-0
```

## Installation simple avec surcharge de la configuration

Par défaut, toutes les images que vous utilisez (qu'elles proviennent de Superset ou d'autres sources) embarquent un fichier de configuration.  
Il est possible de surcharger cette configuration en suivant les étapes suivantes.
> **note :** Toutes les étapes de la section précédente restent valides. Les étapes suivantes sont complémentaires.

L'exemple ci-dessous utilisera le fichier de configuration [superset_config_docker.py](../../../superset-dsfr/docker/pythonpath_dev/superset_config_docker.py). Vous pouvez créer votre propre fichier de configuration et modifier le chemin d'accès dans les commandes suivantes.

1. Configurer le fichier `values.yaml`

Aucune étape complémentaire à la section précédente n'est nécessaire.

2. Installer le chart

Pour installer le chart, exécutez les commandes suivantes

``` bash
helm repo add superset http://apache.github.io/superset/
helm repo update superset
helm upgrade --install custom-app-name superset/superset \
    -f values.yaml \
    --set-file=configOverrides.config_override="../../../superset-dsfr/docker/pythonpath_dev/superset_config_docker.py"
```

## Installation complexe

Ce mode de déploiement est mis à titre informatif pour les environnements restreints/cloisonnés (sans accès internet).  
**Pré-requis**: 
- Avoir téléchargé en amont tous les éléments de configuration et de personnalisations (assets, templates html, fichier de configuration ...)
- Un hub qui contient les images de Superset que vous pouvez pull

🚧En cours de rédaction🚧
