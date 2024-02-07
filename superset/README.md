```bash
wget https://github.com/GouvernementFR/dsfr/releases/download/v1.11.1/dsfr-v1.11.1.zip
unzip dsfr-v1.11.1.zip -d dsfr
git clone --single-branch https://github.com/etalab-ia/chartsgouv
cd superset/
TAG=3.0.0 docker compose -f docker-compose-non-dev.yml up -d
docker exec superset_app pybabel compile -d superset/translations
```
