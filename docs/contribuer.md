# Comment contribuer

## Table des matières
- [Comment contribuer](#comment-contribuer)
  - [Créer une issue](#créer-une-issue)
  - [Contribuer](#contribuer)
  - [Les règles à respecter](#les-règles-à-respecter)

## Créer une issue

- Remonter un bug

Les bugs peuvent être remontés dans la section [issues](https://github.com/etalab-ia/chartsgouv/issues) du projet.  
Veillez à préciser le maximum d'éléments lors de la description de votre bug pour faciliter sa compréhension et votre contexte.

- Proposer une amélioration

Une issue peut être créée pour proposer une amélioration.  
Veillez à être le plus explicite possible sur un périmètre très limité pour faciliter l'implémentation de l'amélioration.

## Contribuer

Vous pouvez contribuer sur des besoins fonctionnels ou la documentation !

- Environnements

Les principaux outils sont: git, docker, docker-compose, python

- Implémentation

La première étape pour contribuer consiste à réaliser un [fork](https://docs.github.com/fr/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) du repo. Vous pouvez ensuite cloner votre fork avec la commande `git clone`.  
Depuis votre fork, nous vous recommandons de créer des branches pour implémenter vos fonctionnalités avec la commande `git branch -b branche_name main`.  
Si votre branche main venait à être désynchronisée avec la branche main du repo ChartsGouv, vous devez la resynchroniser avant de créer de nouvelle branche. Pour ce faire, les commandes suivantes vous seront utiles:
```bash
git add alias upstream https://github.com/etalab-ia/chartsgouv.git
# pour vérifier vos alias: git remote -v
# Pour récupérer les derniers changements
git fetch upstream
# Pour synchroniser votre branche locale main 
git checkout main
git merge upstream/main
# Pour synchroniser votre branche remote main 
git push origin main
```
A partir du merge, vous pouvez de nouveau créer une branche pour implémenter des modifications.  
Une fois l'implémentation réalisée et votre code push sur votre fork, vous pouvez réaliser une Pull Request.

- Réaliser une Pull Request

Depuis la page des [pull request](https://github.com/etalab-ia/chartsgouv/pulls), vous pouvez en créer une nouvelle qui prend comme origine la branche de votre fork.  
> **Important**  
Le titre de la PR doit suivre les [conventional commits](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13#types). Vos commits intermédiaires doivent être simples et explicites.  
La PR doit toujours se faire sur la branche `pre-release` du repo.

## Les règles à respecter

- Pour les maintainers

Les PR doivent être fusionnées uniquement sur la branche `pre-release` en utilisant **Squash and Merge**. _Le message du commit issu du squash **doit** respecter les conventionnels commits_.  
L'utilisation des [conventional commits](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13#types) permet la création de releases et la mise à jour du CHANGELOG.md automatiquement.  
Les maintainers doivent vérifier que le message de commit respecte les conventional commits avant de valider une PR.  
Dès qu'une version est prête à être release, une PR peut être réalisée de `pre-release` vers main en utilisant l'option **Create a merge commit**.