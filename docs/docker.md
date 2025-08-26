# 🚀 Déploiement de Chartsgouv avec Docker

> **Important :** Le lancement via **Docker** n’a pas vocation à être utilisé en production.  
> Pour un usage **production**, utilisez le déploiement via **Helm** (documentation à renseigner ici : `[lien_helm]`).

[[_TOC_]]

## [Lancement avec Docker](#lancement-avec-docker)

L'exécution directe de l'image via une commande Docker n'est pas possible compte tenu de la façon dont la configuration se charge dans Superset.

## [Lancement avec Docker Compose](#lancement-avec-docker-compose)

Spécifiez l'image que vous souhaitez utiliser dans `docker-compose-image-tag.yml` :
```yaml
x-superset-image: &superset-image nom_image:tag
```
Des images prêtent à l'emploi sont disponibles [sur ce repo](https://github.com/etalab-ia/chartsgouv/pkgs/container/chartsgouv).  
Démarrez les services avec :
```bash
# Lancez la commande depuis la racine du projet
docker compose -f superset/docker-compose-image-tag.yml up -d
```

Pour arrêter les services :
```bash
# Lancez la commande depuis la racine du projet
docker compose -f superset/docker-compose-image-tag.yml down
```
Des volumes seront créés sur votre machine locale. Pensez à les supprimer si vous ne les utilisez plus.

## [Personnalisation de la configuration](#personnalisation-de-la-configuration)

- Les variables d'environnement
- La configuration  
Vous pouvez modifier tous les éléments dans `docker/pythonpath_dev` pour modifier la configuration qui sera appliquée à votre instance de ChartsGouv.
Toutes les variables configurations peuvent être trouvée sur le repo officiel de superset: [configuration](https://github.com/apache/superset/blob/main/superset/config.py).  

Une fois vos modifications effectuées:
```env
# dans le fichier .env, inversé les chemins de dossiers
PYTHONPATH=/app/docker/pythonpath_dev:/app/pythonpath
```
Vous pouvez démarrer vos services.

## [Autres personnalisations (assets, templates, traductions ...)](#autres-personnalisations)

Pour des personnalisations avancées, modifiez les fichiers dans `superset/` puis reconstruisez l'image Docker à partir du `Dockerfile`. Utilisez ensuite cette image personnalisée avec les instructions précédentes.  
Pour construire une nouvelle image Docker :

```bash
# Lancez la commande depuis la racine du projet
docker build -t nom_image:tag .
```
Modifiez l'image utilisée dans `docker-compose-image-tag.yml` :
```yaml
x-superset-image: &superset-image nom_image:tag
```
Vous pouvez démarrer démarrer vos services.