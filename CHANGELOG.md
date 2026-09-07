## [2.0.0](https://github.com/etalab-ia/chartsgouv/compare/v1.4.0...v2.0.0) (2026-09-07)

### ⚠ BREAKING CHANGES

* simplify repo and release strategy (#99)

### Features

* **dsfr/config:** update override config to match v6.1 ([0ddf08b](https://github.com/etalab-ia/chartsgouv/commit/0ddf08b482d4be29f139cd70519a7e2de74c2193))
* **installation/helm:** update values to match latest superset helm chart ([87cd3e0](https://github.com/etalab-ia/chartsgouv/commit/87cd3e03e7a44ed7fe48be47bd1027d905445afe))
* simplify repo and release strategy ([#99](https://github.com/etalab-ia/chartsgouv/issues/99)) ([2725792](https://github.com/etalab-ia/chartsgouv/commit/272579275f04e91579f74e80cde5bc88b52394b8))

### Bug Fixes

* **ci:** mise à jour de l'intégration du DSFR ([#105](https://github.com/etalab-ia/chartsgouv/issues/105)) ([e03910e](https://github.com/etalab-ia/chartsgouv/commit/e03910ef42a52567462c904958e064804aef642e))
* **ci:** update build img workflow ([#103](https://github.com/etalab-ia/chartsgouv/issues/103)) ([c4871ef](https://github.com/etalab-ia/chartsgouv/commit/c4871ef2468dcde1f0266944020fe6127cfb88ff))
* **lint:** update dockerfile ([#102](https://github.com/etalab-ia/chartsgouv/issues/102)) ([9f50ac9](https://github.com/etalab-ia/chartsgouv/commit/9f50ac9ebf808fe6ae887d574af120c5eb9e9a90))
* **lint:** update lint helm workflow to fetch Superset chart before linting ([#101](https://github.com/etalab-ia/chartsgouv/issues/101)) ([f618332](https://github.com/etalab-ia/chartsgouv/commit/f618332a3a6425c2e1dda03e9cd1a8e2ad22faec))
* **lint:** update shell scripts to pass shell check ([#100](https://github.com/etalab-ia/chartsgouv/issues/100)) ([38b64f7](https://github.com/etalab-ia/chartsgouv/commit/38b64f7cc3263553674d7d1ffc78a8ab196e7038))

### Autres

* **ci:** add Dependabot config for daily updates ([b5e1757](https://github.com/etalab-ia/chartsgouv/commit/b5e1757c87f5cfc21c4bdf7aecde9552e8081918))
* **ci:** Fix package-ecosystem name for GitHub Actions ([c590bef](https://github.com/etalab-ia/chartsgouv/commit/c590bef4f1a37dd79acf84caf6ee56408bf81e75))
* **deps:** remove uv package eco-system in dependabot ([02b7c32](https://github.com/etalab-ia/chartsgouv/commit/02b7c325056e733af694413d55385ff09c7cc319))
* **docs:** apply linting ([9a58883](https://github.com/etalab-ia/chartsgouv/commit/9a5888337c0f5fed7e9eb9ec3385b325ac823828))

## [1.4.0](https://github.com/etalab-ia/chartsgouv/compare/v1.3.0...v1.4.0) (2025-10-27)

### Features

* **superset-dsfr:** update config py file to include more base default options ([#93](https://github.com/etalab-ia/chartsgouv/issues/93)) ([4dc4af4](https://github.com/etalab-ia/chartsgouv/commit/4dc4af41cc9fe351993aca47bdddcdd6761ad7c1))

### Bug Fixes

* **build:** update Dockerfile ([#90](https://github.com/etalab-ia/chartsgouv/issues/90)) ([2667766](https://github.com/etalab-ia/chartsgouv/commit/26677661d7278ba8aa8609c94295c7dcc8dba804))

### Documentation

* add doc to contribute ([#94](https://github.com/etalab-ia/chartsgouv/issues/94)) ([73ce1e3](https://github.com/etalab-ia/chartsgouv/commit/73ce1e3fb07f689b0eb10783de08c383d885ab1c))
* add docker deployment doc ([#91](https://github.com/etalab-ia/chartsgouv/issues/91)) ([b2814a9](https://github.com/etalab-ia/chartsgouv/commit/b2814a9e4375bd2418e7310da5d20cf91259035b))
* **installation:** add Helm deployment ([#92](https://github.com/etalab-ia/chartsgouv/issues/92)) ([a446fa1](https://github.com/etalab-ia/chartsgouv/commit/a446fa1d2b38d152ed39547752c9f4368c33d739))

## [1.3.0](https://github.com/etalab-ia/chartsgouv/compare/v1.2.0...v1.3.0) (2025-08-20)

### Bug Fixes

* **img:** update Dockerfile ([4ba1c16](https://github.com/etalab-ia/chartsgouv/commit/4ba1c166b52f3cf0e57b31cc19cc1efa2d7a9887))
* **traduction:** merging backend and frontend traduction into a single file ([0977321](https://github.com/etalab-ia/chartsgouv/commit/09773214ae6a87cabfa72d0641e5b0b59c45f2ff))
* **traduction:** mise à jour du fichier po et du dockerfile ([b5a7a46](https://github.com/etalab-ia/chartsgouv/commit/b5a7a46f87b616e08a08b5a730ca56bf304aa35d))
* **traduction:** update Dockerfile ([87299c0](https://github.com/etalab-ia/chartsgouv/commit/87299c0a0c9261e8a744e5fc15176f8a50a094af))

### Improvements

* **docker:** update default app name to ChartsGouv ([796b02c](https://github.com/etalab-ia/chartsgouv/commit/796b02c3916c5c2df018003b3d58c888a4c5d339))

## [1.2.0](https://github.com/etalab-ia/chartsgouv/compare/v1.1.0...v1.2.0) (2025-06-27)

### Improvements

* **ci:** using archive refs from dsfr-chart repo ([3cfe021](https://github.com/etalab-ia/chartsgouv/commit/3cfe021820f1dbdf8634f03bb9a5dea576668f56))

## [1.1.0](https://github.com/etalab-ia/chartsgouv/compare/v1.0.0...v1.1.0) (2025-06-27)

### Bug Fixes

* **ci:** building using the right translation file ([7a158bd](https://github.com/etalab-ia/chartsgouv/commit/7a158bdb4ed8ed203f0eb7f8bbbd0a90853d7bd8))
* **ci:** downgrade ubuntu image version to resolve cert issue ([25c81ba](https://github.com/etalab-ia/chartsgouv/commit/25c81baef513301f6d6c62e6b63fab723c495edc))
* **ci:** update env var name ([e1ba65b](https://github.com/etalab-ia/chartsgouv/commit/e1ba65bb4651dbc368a362740e36b00d4ea8d66f))

### Improvements

* **ci:** using github vars instead of hardcoded values in build img workflow ([76b4756](https://github.com/etalab-ia/chartsgouv/commit/76b4756f96564ea8503adf739494227e0a383916))

## 1.0.0 (2025-06-21)

### Features

* add french traduction file ([2165668](https://github.com/etalab-ia/chartsgouv/commit/2165668599fcb93faed502b3a2223fe2f732d75a))
* add french traduction file ([fe9f858](https://github.com/etalab-ia/chartsgouv/commit/fe9f85862fe8e27cd2e730497c99632df2c34147))
* add missing superset_config file ([3212a60](https://github.com/etalab-ia/chartsgouv/commit/3212a605f8b21a8efab055fe9cd726349c49862c))
* add superset-custom folder ([2d7fcda](https://github.com/etalab-ia/chartsgouv/commit/2d7fcda559324a6d9c659bdace72881709d1cb0e))
* delete duplicate folder ([76a9410](https://github.com/etalab-ia/chartsgouv/commit/76a94100bff3bf3225d6d7c3bac6a8db65a1542f))
* removing docker folder ([001ed2c](https://github.com/etalab-ia/chartsgouv/commit/001ed2c7e75183fb246d098722f5431120d93bfd))
* rename folder name ([11cb853](https://github.com/etalab-ia/chartsgouv/commit/11cb85323e753c66a3b2fafae8c76863ae525b82))
* update readme ([61c7b24](https://github.com/etalab-ia/chartsgouv/commit/61c7b24a35309fcf7a65c2c08cfe4729db431bd8))

### Bug Fixes

* mise à jour de la construction de l'image ([38360fc](https://github.com/etalab-ia/chartsgouv/commit/38360fc95956e0fe239ea229a0a06fd04350c1a2))
* restore logo ([646c357](https://github.com/etalab-ia/chartsgouv/commit/646c3572e55117ccf40c233da499047d3881086c))

### Documentation

* update readme ([ff6a505](https://github.com/etalab-ia/chartsgouv/commit/ff6a505324ef3cff670ae87e21069426bda14094))
* update readme ([18e68fe](https://github.com/etalab-ia/chartsgouv/commit/18e68fea6686ae387766373051e678ff929488e3))
