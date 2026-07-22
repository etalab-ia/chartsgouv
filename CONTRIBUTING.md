# Contribuer à ChartsGouv

---

Merci de votre intérêt pour votre contribution à **ChartsGouv**.

Ce projet utilise le **GitHub Flow** : la branche `main` est la seule branche de production.

Chaque changement passe par une **Pull Request (PR)** et passe par les vérifications automatiques de la CI.

---

## Table des matières

- [Contribuer à ChartsGouv](#contribuer-à-chartsgouv)
  - [Table des matières](#table-des-matières)
  - [Installation de l'environnement](#installation-de-lenvironnement)
    - [Prérequis](#prérequis)
    - [Installer l'envrionnement python](#installer-lenvrionnement-python)
  - [Contribuer au code](#contribuer-au-code)
    - [Workflow de contribution (GitHub Flow)](#workflow-de-contribution-github-flow)
    - [Créer une Pull Request](#créer-une-pull-request)
    - [Convention de commits](#convention-de-commits)
  - [Linting et pre-commit](#linting-et-pre-commit)
    - [Installation des hooks](#installation-des-hooks)
    - [Linting manuel](#linting-manuel)
  - [Déployer ChartsGouv localement](#déployer-chartsgouv-localement)
    - [Docker](#docker)
  - [Travailler sur les traductions](#travailler-sur-les-traductions)
    - [Modifier les fichiers de traduction](#modifier-les-fichiers-de-traduction)
  - [Règles pour les maintainers](#règles-pour-les-maintainers)
  - [Structure du projet](#structure-du-projet)
  - [License](#license)

---

## Installation de l'environnement

### Prérequis

- **Docker** et **Docker Compose** (pour le développement local et le build)
- **Git** pour la gestion des versions
- **Python 3.10+** et **Node.js 24** (pour le linting et les traductions)
- **Helm** (pour le déploiement sur Kubernetes)

### Installer l'envrionnement python

```bash
# Créer et activer l'environnement de développement
make setup-py-env
```

---

## Contribuer au code

### Workflow de contribution (GitHub Flow)

Le projet suit le **GitHub Flow** :

1. **Forker** le dépôt [chartsgouv](https://github.com/etalab-ia/chartsgouv)
2. **Cloner** votre fork :
   ```bash
   git clone https://github.com/votre-nom/chartsgouv.git
   cd chartsgouv
   ```
3. **Ajouter le remote upstream** (le dépôt original) :
   ```bash
   git remote add upstream https://github.com/etalab-ia/chartsgouv.git
   ```
4. **Créer une branche** pour votre fonctionnalité :
   ```bash
   git fetch upstream
   git merge upstream/main
   git checkout -b nom-de-ma-fonctionnalite
   ```
5. **Implémenter** vos changements et **commit**
6. **Push** la branche sur votre fork :
   ```bash
   git push origin nom-de-ma-fonctionnalite
   ```
7. **Ouvrir une Pull Request** vers la branche `main` du dépôt principal

### Créer une Pull Request

Pour proposer vos modifications :

1. Depuis la page du dépôt, cliquez sur **Pull requests** > **New pull request**
2. Définissez comme **base** : `etalab-ia/chartsgouv/main`
3. Définissez comme **head** : votre fork et votre branche
4. Remplissez le **template de PR** avec :
   - Un titre clair et descriptif
   - Le type de changement (feat, fix, docs, etc.)
   - Les modifications réalisées
   - Les tests effectués
   - Les vérifications à faire manuellement

Le CI exécutera automatiquement les workflows de linting sur chaque PR.

### Convention de commits

Les commits doivent suivre les **[Conventional Commits](https://www.conventionalcommits.org/)** :

```
<type>(scope): description

[body optionnel]

[footer optionnel]
```

**Types de commits supportés :**

| Type | Description |
|---|---|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Modification de documentation |
| `style` | Modifications de formatage (pas de logique) |
| `perf` | Amélioration des performances |
| `test` | Ajout ou modification de tests |
| `chore` | Tâches de maintenance, deps |
| `refactor` | Breaking changes |

**Exemples :**

```
feat(superset-dsfr): ajouter le graphique en radar
fix(templates): corriger l'affichage du header DSFR
docs(contribuer): ajouter la section linting
```

Les PRs sont fusionnées avec **Squash and Merge**.

---

## Linting et pre-commit

Le projet utilise **pre-commit** avec les outils suivants :

- **ruff** pour le linting et le formatage Python
- **pre-commit-hooks** : trailing whitespace, fin de fichier, check YAML/TOML/JSON

### Installation des hooks

Les hooks sont installés automatiquement lors de l'[installation de l'environnement python.](#installer-lenvrionnement-python)

### Linting manuel

Il est possible de linter manuellement les fichiers avec les commandes suivantes

```bash
# Tous les linters
make lint-all

# Linter Python
make lint-py

# Linter Dockerfile
make lint-dockerfile

# Linter Shell
make lint-shell

# Linter Helm
make lint-helm
```

Les mêmes vérifications sont exécutées automatiquement par le CI via les workflows GitHub Actions :

| Workflow | Fichiers surveillés | Outil |
|---|---|---|
| **Lint Python** | `superset-dsfr/docker/pythonpath_dev/**` | ruff |
| **Lint Dockerfile** | `Dockerfile` | hadolint |
| **Lint Shell** | Scripts `docker/` | shellcheck |
| **Lint Helm** | `docs/installation/helm/**` | helm lint |
| **Translate Build** | `translations/**` | pybabel |


---

## Déployer ChartsGouv localement

### Docker

La méthode recommandée est de construire l'image Docker customisée de Superset avec le thème DSFR :

```bash
# Construire l'image avec DSFR
make docker-build-dsfr

# Ou sans DSFR
make docker-build-without-dsfr
```

Les paramètres sont configurables via les variables du `Makefile` ou via les variables du `Dockerfile` :

| Variable | Description | Défaut |
|---|---|---|
| `SUPERSET_VERSION` | Version d'Apache Superset | `4.1.1` |
| `TAG_DSFR` | Version du thème DSFR | `1.14.4` |
| `TAG_DSFR_CHART` | Version du chart DSFR | `2.0.3` |
| `USE_DSFR` | Activer le thème DSFR | `true` |

La configuration de Superset se trouve dans :
- `superset-dsfr/docker/pythonpath_dev/superset_config.py` — configuration d'intégration du DSFR
- `superset-dsfr/docker/pythonpath_dev/superset_config_docker.py` — configuration Docker

Vous pouvez vous référer au [guide de déploiement avec Docker](./docs/installation/docker/README.md) pour déployer ChartsGouv avec Docker.

---

## Travailler sur les traductions

Les traductions françaises se trouvent dans `superset-dsfr/translations/`.

### Modifier les fichiers de traduction

1. **Mettre à jour le fichier `.po`** avec vos nouvelles chaînes
2. **Compiler les translations** :
   ```bash
   make check-translation
   ```
3. **Vérifier le build de l'image** :
   ```bash
   # Construire l'image avec DSFR
   make docker-build-dsfr

   # Ou sans DSFR
   make docker-build-without-dsfr
   ```

> ⚠️ Les modifications dans `translations/` déclenchent automatiquement un workflow CI de vérification.

---

## Règles pour les maintainers

- Les PRs sont fusionnées avec **Squash and Merge** vers `main`
- Le message de squash **doit** respecter les **Conventional Commits**
- La release est publiée via un workflow manuel déclenché sur `main` (utilisation de [semantic-release](https://semantic-release.gitbook.io/semantic-release/))
- Le [CHANGELOG.md](CHANGELOG.md) est généré automatiquement par semantic-release

---

## Structure du projet

```
.
├── Dockerfile                  # Image Docker Superset with DSFR
├── Makefile                    # Commandes utilitaires (lint, build, clean)
├── package.json                # Dépendances npm (semantic-release)
├── requirements-dev.txt        # Dépendances Python pour le dev
├── .pre-commit-config.yaml     # Configuration pre-commit (ruff, hooks)
├── .releaserc                  # Configuration semantic-release
├── superset-dsfr/              # Personnalisation Superset DSFR
│   ├── assets/                 # CSS, images, favicon
│   ├── docker/                 # Scripts Docker et configs locales
│   ├── templates_overrides/    # Templates HTML DSFR
│   └── translations/           # Fichiers de traduction (.po)
├── docs/                       # Documentation
│   ├── installation/           # Guides Docker et Helm
│   ├── usage/                  # Guides d'usage (Grist, DeckGL, embedding)
│   ├── configuration_avancee.md
│   └── faq.md
└── .github/workflows/          # Workflows GitHub Actions (lint, release)
```

---

## License

Ce projet est distribué sous licence **EUPL v1.2** — voir le fichier [LICENCE](LICENCE) pour plus de détails.
